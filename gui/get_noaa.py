import requests
import shutil
import urllib.request
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from datetime import datetime
from datetime import timedelta

base_url = "https://services.swpc.noaa.gov"


def get_json(directory):

    r = requests.get(base_url + directory)

    status = r.status_code

    if status == 200:
        return r.json()


def get_img(directory, file_name):
    r = requests.get(base_url + directory, stream=True)

    status = r.status_code

    if status == 200:
        with open(file_name, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
    else:
        print('Image Couldn\'t be retrieved')


def print_raw_indices(noaa_scales):

    print('-------------\nToday\n')
    print('R = ', noaa_scales['0']['R']['Scale'])
    print('G = ', noaa_scales['0']['G']['Scale'])
    print('S = ', noaa_scales['0']['S']['Scale'])

    print('-------------\nJ + 1\n')
    print('R1 - R2 probability = ', noaa_scales['1']['R']['MinorProb'])
    print('R3 - R5 probability = ', noaa_scales['1']['R']['MajorProb'])
    print('G = ', noaa_scales['1']['G']['Scale'])
    print('S1-S5 probability = ', noaa_scales['1']['S']['Prob'])

    print('-------------\nJ + 2\n')
    print('R1 - R2 probability = ', noaa_scales['2']['R']['MinorProb'])
    print('R3 - R5 probability = ', noaa_scales['2']['R']['MajorProb'])
    print('G = ', noaa_scales['2']['G']['Scale'])
    print('S1-S5 probability = ', noaa_scales['2']['S']['Prob'])


class NoaaScales:

    directory = '/products/noaa-scales.json'

    def __init__(self):
        raw_data = get_json(self.directory)
        self.R = int(raw_data['0']['R']['Scale'])
        self.G = int(raw_data['0']['G']['Scale'])
        self.S = int(raw_data['0']['S']['Scale'])
        self.R_forecast = ({'Minor_p': int(raw_data['1']['R']['MinorProb']),
                            'Major_p': int(raw_data['1']['R']['MajorProb'])
                            },
                           {'Minor_p': int(raw_data['2']['R']['MinorProb']),
                            'Major_p': int(raw_data['2']['R']['MajorProb'])
                            }
                           )
        self.G_forecast = (int(raw_data['1']['G']['Scale']), int(raw_data['2']['G']['Scale']))
        self.S_forecast = (int(raw_data['1']['S']['Prob']), int(raw_data['2']['S']['Prob']))

    def update(self):
        raw_data = get_json(self.directory)
        self.R = int(raw_data['0']['R']['Scale'])
        self.G = int(raw_data['0']['G']['Scale'])
        self.S = int(raw_data['0']['S']['Scale'])
        self.R_forecast = ({'Minor_p': int(raw_data['1']['R']['MinorProb']),
                            'Major_p': int(raw_data['1']['R']['MajorProb'])
                            },
                           {'Minor_p': int(raw_data['2']['R']['MinorProb']),
                            'Major_p': int(raw_data['2']['R']['MajorProb'])
                            }
                           )
        self.G_forecast = (int(raw_data['1']['G']['Scale']), int(raw_data['2']['G']['Scale']))
        self.S_forecast = (int(raw_data['1']['S']['Prob']), int(raw_data['2']['S']['Prob']))

    def __str__(self):
        rtn = "-------------\nToday\n"
        rtn += f"R = {self.R}\n"
        rtn += f"R = {self.G}\n"
        rtn += f"S = {self.S}\n"
        rtn += "-------------\nJ + 1\n"
        rtn += f"R1 - R2 probability = {self.R_forecast[0]['Minor_p']}\n"
        rtn += f"R1 - R2 probability = {self.R_forecast[0]['Major_p']}\n"
        rtn += f"G = {self.G_forecast[0]}\n"
        rtn += f"S1-S5 probability = {self.S_forecast[0]}\n"
        rtn += "-------------\nJ + 2\n"
        rtn += f"R1 - R2 probability = {self.R_forecast[1]['Minor_p']}\n"
        rtn += f"R1 - R2 probability = {self.R_forecast[1]['Major_p']}\n"
        rtn += f"G = {self.G_forecast[1]}\n"
        rtn += f"S1-S5 probability = {self.S_forecast[1]}\n"
        return rtn


def calculate_indices(noaa_scales):
    R = {-1: -1, 0: 0, 1: 0, 2: 0}
    G = {-1: -1, 0: 0, 1: 0, 2: 0}
    S = {-1: -1, 0: 0, 1: 0, 2: 0}
    P = {-1: -1, 0: 0, 1: 0, 2: 0}
    R[0] = noaa_scales.R
    G[0] = noaa_scales.G
    S[0] = noaa_scales.S
    for i in (0, 1):
        R[i+1] = round((2 * noaa_scales.R_forecast[i]['Minor_p'] + 5 * noaa_scales.R_forecast[i]['Major_p'])
                       /
                       100)
        G[i+1] = noaa_scales.G_forecast[i]
        S[i+1] = round(noaa_scales.S_forecast[i]*5/100)
    for i in range(3):
        P[i] = round(((G[i]/5)**2 + (S[i]/5)**2)*5/2)
    return {'R': R, 'P': P}


def get_g_dm1():
    directory = "/products/noaa-planetary-k-index.json"
    kp_json = get_json(directory)
    date = datetime.now().date()
    yesterday = date - timedelta(days=1)
    avg_kp = 0
    n_kp = 0
    for elt in kp_json:
        if elt[0][:10] == str(yesterday):
            avg_kp += float(elt[1])
            n_kp += 1
    avg_kp = avg_kp/n_kp
    g = 0
    if avg_kp >= 5:
        g = 1
    if avg_kp >= 6:
        g = 2
    if avg_kp >= 7:
        g = 3
    if avg_kp >= 8:
        g = 4
    if avg_kp > 9:
        g = 5
    return g


def get_s_dm1():
    directory = "/json/goes/primary/integral-protons-3-day.json"
    goes_proton = get_json(directory)
    date = datetime.now().date()
    yesterday = date - timedelta(days=1)
    gp10mev = [gp["flux"] for gp in goes_proton if gp["energy"] == ">=10 MeV" and gp["time_tag"][:10] == str(yesterday)]
    avg_flux = sum(gp10mev)/len(gp10mev)
    s = 0
    if avg_flux > 10:
        s = 1
    if avg_flux > 100:
        s = 2
    if avg_flux > 1000:
        s = 3
    if avg_flux > 10_000:
        s = 4
    if avg_flux > 100_000:
        s = 5
    return s


def get_p_dm1():
    g = get_g_dm1()
    s = get_s_dm1()
    p = round(((g / 5) ** 2 + (s / 5) ** 2) * 5 / 2)
    return p


def get_bulletin(r, p, sc, n):
    # Handle no data cases
    r_, p_, sc_, n_ = r.copy(), p.copy(), sc.copy(), n.copy()
    for i, x in enumerate(r_):
        if x == -1:
            r_[i - 1] = "-"
    for i, x in enumerate(p_):
        if x == -1:
            p_[i - 1] = "-"
    for i, x in enumerate(sc_):
        if x == -1:
            sc_[i - 1] = "-"
    for i, x in enumerate(n_):
        if x == -1:
            n_[i - 1] = "-"

    # Get NOAA bulletin
    f = urllib.request.urlopen("https://services.swpc.noaa.gov/text/3-day-forecast.txt") #Read the NOOA official bulletin
    lines = [f.readline().decode('utf-8'), f.readline().decode('utf-8')]
    month = lines[1][14:18]
    day = int(lines[1][18:20])

    content = lines+["<br>TAMAGI Index Forecast :"]  # will be the content of the forecast file
    content.append("<br>&emsp;&emsp;&ensp; "+month+str(day)+"&emsp; "+month+str(day+1)+"&emsp; "+month+str(day+2))
    content.append("<br>R index"+"&emsp; "+str(r_[0])+"&emsp;&emsp;&emsp; "+str(r_[1])+"&emsp;&emsp;&emsp; "+str(r_[2]))
    content.append("<br>P index"+"&emsp; "+str(p_[0])+"&emsp;&emsp;&emsp; "+str(p_[1])+"&emsp;&emsp;&emsp; "+str(p_[2]))
    content.append("<br>SC index"+"&ensp; "+str(sc_[0])+"&emsp;&emsp;&emsp; "+str(sc_[1])+"&emsp;&emsp;&emsp; "+str(sc_[2]))
    content.append("<br>N index"+"&emsp; "+str(n_[0])+"&emsp;&emsp;&emsp; "+str(n_[1])+"&emsp;&emsp;&emsp; "+str(n_[2]))
    content.append("<br>NOOA Bulletin :\n")
    for i, line in enumerate(f):
        content.append("<br>"+line.decode('utf-8'))
    
    return ''.join(content)


def get_muf(index):
    directory_north = "/images/animations/d-rap/north-pole/d-rap/latest.png"
    directory_south = "/images/animations/d-rap/south-pole/d-rap/latest.png"
    get_img(directory_north, f"images/muf_north_pole_{index}.png")
    get_img(directory_south, f"images/muf_south_pole_{index}.png")


def get_sunspot():
    directory = "/json/solar-cycle/sunspots.json"
    ssn = get_json(directory)
    last_ssn = ssn[-120:]
    tendency_ssn = [0]*120
    tendency_ssn[0] = (last_ssn[0]['ssn'] + last_ssn[1]['ssn'] + last_ssn[2]['ssn']) / 3
    tendency_ssn[1] = (last_ssn[0]['ssn'] + last_ssn[1]['ssn'] + last_ssn[2]['ssn'] +
                       last_ssn[3]['ssn']) / 4
    tendency_ssn[-2] = (last_ssn[-4]['ssn'] + last_ssn[-3]['ssn'] + last_ssn[-2]['ssn'] +
                        last_ssn[-1]['ssn']) / 4
    tendency_ssn[-1] = (last_ssn[-3]['ssn'] + last_ssn[-2]['ssn'] + last_ssn[-1]['ssn']) / 3
    for i in range(2, len(last_ssn) - 2):
        tendency_ssn[i] = (last_ssn[i - 2]['ssn'] + last_ssn[i - 1]['ssn'] + last_ssn[i]['ssn'] +
                           last_ssn[i + 1]['ssn'] + last_ssn[i + 2]['ssn']) / 5
    ssn_data = pd.DataFrame(last_ssn)
    ssn_data['tendency'] = tendency_ssn
    ssn_data = ssn_data.melt('time-tag', var_name='plots', value_name='vals')
    return ssn_data, ssn[-1]['ssn']


def get_goes_proton():
    directory = "/json/goes/primary/integral-protons-3-day.json"
    goes_proton = get_json(directory)
    gp10mev = [{"time": gp["time_tag"], "> 10 MeV particle flux": gp["flux"]} for gp in goes_proton
               if gp["energy"] == ">=10 MeV"]
    gp10mev_data = pd.DataFrame(gp10mev)
    x_data = np.array(gp10mev_data['time'], dtype='datetime64')
    y_data = gp10mev_data["> 10 MeV particle flux"]
    plt.figure(figsize=(10, 6))
    plt.semilogy(x_data, y_data)
    plt.xlabel('Time')
    plt.ylabel('Flux ($part.cm^{-1}.s^{-1}.str^{-1}$)')
    plt.legend(['> 10 MeV particle flux'])
    locator = mdates.AutoDateLocator(minticks=6, maxticks=10)
    formatter = mdates.ConciseDateFormatter(locator)
    ax = plt.gca()
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)
    plt.show()


if __name__ == '__main__':
    """
    directory = "/products/noaa-scales.json"
    curr_noaa_scales = NoaaScales()
    print(curr_noaa_scales)
    print("--- NEW INDICES ---\n")
    print(calculate_indices(curr_noaa_scales))
    get_goes_proton()
    """
    print(get_g_dm1())
    print(get_s_dm1())