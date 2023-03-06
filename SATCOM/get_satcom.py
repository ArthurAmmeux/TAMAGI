import json
import math

import numpy as np
import matplotlib.pyplot as plt
import requests
from datetime import datetime, timedelta, timezone
import geopandas as gpd
import pandas as pd
import re
from io import StringIO
import shapely

DELTA_MINUTES = 1440
ELEVATION_MIN = 20
INGV_BASE_URL = "http://ws-eswua.rm.ingv.it/scintillation.php/records/ws"
IMPC_BASE_URL = "https://impc.dlr.de/SWE/Ionospheric_Perturbations/Local_Scintillation_Measurements/"
END_DT = datetime.now(timezone.utc).isoformat(sep=' ', timespec='seconds')
START_DT = (datetime.now(timezone.utc) - timedelta(minutes=DELTA_MINUTES)).isoformat(sep=' ', timespec='seconds')
LEAP_SECONDS = 18


def gps_to_utc(gpsweek, gpsseconds, leapseconds):
    datetimeformat = "%Y-%m-%d %H:%M:%S"
    epoch = datetime.strptime("1980-01-06 00:00:00", datetimeformat)
    elapsed = timedelta(days=(gpsweek * 7), seconds=(gpsseconds - leapseconds))
    return (epoch + elapsed).replace(tzinfo=timezone.utc)


# GeoPandas initialization
# From GeoPandas, our world map data
worldmap = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))


# INGV Stations lists with related metadata
def init_stations_INGV():
    ingv_stations = json.loads(requests.get(
        "http://ws-eswua.rm.ingv.it/scintillation.php/records/wsstation?order=code&include=code,lat,lon,name,status").content)[
        "records"]
    ingv_active_stations = list()
    not_wanted_stations = []  # ["dmc0p", "dmc1p", "dmc2p","lyb0p", "mal0p","mzs0p"]

    for station in ingv_stations:
        if station["status"] == "Active" and station["code"] not in not_wanted_stations:
            ingv_active_stations.append(station)
    return pd.DataFrame(ingv_active_stations).drop(columns=["status"])


def init_stations_IMPC():
    df = pd.DataFrame()
    df["code"] = pd.Series(["mski01", "msnz02", "msto01", "mste01"])
    df["lat"] = [67.8, 53.3, 43.6, 28.5]
    df["lon"] = [20.4, 13.1, 1.5, -16.3]
    df["name"] = ["Kiruna", "Neustrelitz", "Toulouse", "Tenerife"]
    return df


stations_INGV = init_stations_INGV()
stations_IMPC = init_stations_IMPC()
stations = pd.concat([stations_IMPC, stations_INGV], ignore_index=True)


def get_s4_ingv_lasts(id_station, ):
    request_url = INGV_BASE_URL + id_station + "?filter=dt,bt," + START_DT + "," + END_DT + "&filter=elevation,gt," + str(
        ELEVATION_MIN) + "&order=dt,desc&include=dt,elevation,ipp_lat,ipp_lon,totals4l1,sigmaccdl1"
    response = requests.get(request_url)

    if response.status_code != 200:
        print("ERROR - " + id_station + "HTTP Response Code :" + str(response.status_code))

        return -1
    elif response.content == b'{"records":[]}':
        print("ERROR - " + id_station + " - Void Content")
        return pd.DataFrame()
    else:
        station_data_records = pd.json_normalize(json.loads(response.content)["records"])
        print("OK - " + id_station + " Fetched")
        formatted_data = pd.DataFrame()
        formatted_data["datetime"] = station_data_records["dt"]
        formatted_data["code"] = id_station
        formatted_data["name"] = stations.loc[stations["code"] == id_station]["name"].values[0]
        formatted_data["lat"] = station_data_records["ipp_lat"]
        formatted_data["lon"] = station_data_records["ipp_lon"]
        formatted_data["s4"] = station_data_records["totals4l1"]
        formatted_data["sigmaphi"] = station_data_records["sigmaccdl1"]
        return formatted_data


def get_s4_ingv_all():
    s4_data = pd.DataFrame()
    for station_code in stations_INGV["code"]:
        s4_data = pd.concat([s4_data, get_s4_ingv_lasts(station_code)], ignore_index=True)
    s4_data.drop(s4_data[s4_data["s4"] < 0].index, inplace=True)
    return pd.DataFrame(s4_data)


# http s://impc.dlr.de/SWE/Ionospheric_Perturbations/Local_Scintillation_Measurements/msto01/2023/001/ for free
# access archives (no login required)
def get_s4_impc_lasts(id_station):
    request_url = IMPC_BASE_URL + id_station + "/latest/" + id_station + "scintillation.dat"
    response = requests.get(request_url)

    if response.status_code != 200:
        print("ERROR - " + id_station + "HTTP Response Code :" + str(response.status_code))
        return -1
    else:
        # Replace spaces by a comma and deleting first column of commas
        data = re.sub(r" +", ",", response.content.decode(), 0, re.MULTILINE)
        data = re.sub(r"^,", "", data, 0, re.MULTILINE)

        columns = ["GPS_Week", "GPS_TOW", "PRN", "S4", "Sigma"]

        # String to an IO data to be read with pandas
        dataIO = StringIO(data)
        station_data_records = pd.read_csv(dataIO, header=0, names=columns, index_col=False)
        print("OK - " + id_station + " Fetched")

        formatted_data = pd.DataFrame()
        formatted_data["datetime"] = station_data_records.apply(
            lambda x: gps_to_utc(x.GPS_Week, x.GPS_TOW, LEAP_SECONDS), axis=1)
        formatted_data["code"] = id_station
        formatted_data["name"] = stations.loc[stations["code"] == id_station]["name"].values[0]
        formatted_data["lat"] = stations.loc[stations["code"] == id_station]["lat"].values[0]
        formatted_data["lon"] = stations.loc[stations["code"] == id_station]["lon"].values[0]
        formatted_data["s4"] = station_data_records["S4"]
        formatted_data["sigmaphi"] = station_data_records["Sigma"]
        return formatted_data


def get_s4_impc_all():
    s4_data = pd.DataFrame()
    for station_code in stations_IMPC["code"]:
        s4_data = pd.concat([s4_data, get_s4_impc_lasts(station_code)], ignore_index=True)
    s4_data["timestamp"] = s4_data["datetime"].apply(datetime.timestamp)
    s4_data["timestamp"] = s4_data["timestamp"].apply(str)
    s4_data.drop(s4_data[s4_data["timestamp"] < str(datetime.fromisoformat(START_DT).timestamp())].index, inplace=True)
    s4_data.drop(s4_data[s4_data["s4"] < 0].index, inplace=True)
    return s4_data


def get_s4_from_stations():
    return pd.concat([get_s4_impc_all(), get_s4_ingv_all()])


def get_sc_indice(data):
    s4_max = data['s4'].quantile(q=0.9)
    print("S4_max : " + str(s4_max))
    indice = max(0, min(math.floor(s4_max * 4), 5))
    return {0: indice, 1: indice, 2: indice}


# GeoPandas grid creation
# square_size in degrees of length (10 -> 10° longitude and 10° latitude)
def get_grid(s4_data, square_size=10):
    # Parameters of the net
    xmin, ymin = (-180, -90)
    xmax, ymax = (180, 90)
    grid_cells = []

    # For loop to create the grid
    for x0 in np.arange(xmin, xmax + square_size, square_size):
        for y0 in np.arange(ymin, ymax + square_size, square_size):
            # bounds
            x1 = x0 - square_size
            y1 = y0 + square_size
            grid_cells.append(shapely.geometry.box(x0, y0, x1, y1))

    # Data formatting
    s4_data.drop(columns=["timestamp"])
    cell = gpd.GeoDataFrame(grid_cells, columns=['geometry'], crs="EPSG:4326")
    gdf_data = gpd.GeoDataFrame(s4_data,
                                geometry=gpd.points_from_xy(s4_data.lon, s4_data.lat),
                                crs="EPSG:4326")

    merged = gpd.sjoin(gdf_data, cell, how='left', predicate='within')
    # Compute stats per grid cell | aggregate to grid cells with dissolve
    dissolve = merged.dissolve(by="index_right", aggfunc={"s4": lambda x: np.percentile(x, 90)})

    # Conversion to indice scale (by severity from 0 calm to 5 extreme)
    dissolve.loc[dissolve['s4'] > 1.25, 's4'] = 5
    dissolve.loc[(1 < dissolve['s4']) & (dissolve['s4'] <= 1.25), 's4'] = 4
    dissolve.loc[(0.75 < dissolve['s4']) & (dissolve['s4'] <= 1), 's4'] = 3
    dissolve.loc[(0.5 < dissolve['s4']) & (dissolve['s4'] <= 0.75), 's4'] = 2
    dissolve.loc[(0.25 < dissolve['s4']) & (dissolve['s4'] <= 0.5), 's4'] = 1
    dissolve.loc[dissolve['s4'] <= 0.25, 's4'] = 0

    # put this into cell
    cell.loc[dissolve.index, 's4'] = dissolve.s4.values

    return cell


def display_map(cell):
    # Plotting the map
    ax = cell.plot(column='s4', figsize=(12, 8), vmin=0.0, vmax=5., cmap='plasma', legend=True, alpha=0.5)
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres')).to_crs(cell.crs)
    world.plot(ax=ax, color='lightgrey', zorder=0)  # , cax=cax)
    plt.title("S4 Index Map")

# %%
data = get_s4_from_stations()
# %%
print(get_sc_indice(data))
display_map(get_grid(data))

