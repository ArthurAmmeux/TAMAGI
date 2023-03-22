### Python code for download the requested data from the eSWua web-service

#-------Import of the requested libraries.
import json
import urllib.request
from datetime import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np


def low_pass(lis):
    rtn = np.zeros(len(lis))
    rtn[0] = lis[0] * 0.7 + lis[1] * 0.2 + lis[2]*0.1
    rtn[1] = lis[0] * 0.2 + lis[1] * 0.4 + lis[2] * 0.2 + lis[3] * 0.1
    rtn[-1] = lis[-1] * 0.7 + lis[-2] * 0.2 + lis[-3] * 0.1
    rtn[-2] = lis[-1] * 0.2 + lis[-2] * 0.4 + lis[-3] * 0.2 + lis[-4] * 0.1
    for i in range(2, len(lis) - 2):
        rtn[i] = lis[i - 2] * 0.1 + lis[i - 1] * 0.2 + lis[i] * 0.4 + lis[i + 1] * 0.2 + lis[i + 2] * 0.1
    return rtn


def avg(lis):
    res = 0
    length = len(lis)
    for num in lis:
        if num is not None:
            res += num
        else:
            length -= 1
    return res/length


def get_st_en_time():
    time = datetime.now()
    ysd = time - timedelta(days=1)
    return f"{ysd.year}-{ysd.month}-{ysd.day}%20{ysd.hour}:{ysd.minute}:{ysd.second}", \
           f"{time.year}-{time.month}-{time.day}%20{time.hour}:{time.minute}:{time.second}"


def get_st_en_ysd():
    time = datetime.now()
    ysd = time - timedelta(days=1)
    dm2 = time - timedelta(days=2)
    return f"{dm2.year}-{dm2.month}-{dm2.day}%20{dm2.hour}:{dm2.minute}:{dm2.second}", \
           f"{ysd.year}-{ysd.month}-{ysd.day}%20{ysd.hour}:{ysd.minute}:{ysd.second}"


def get_s4_data(st_time, en_time):

    # -------Retrieve the data from the web-service and create the list of dictionary containing the data.

    url='http://ws-eswua.rm.ingv.it/scintillation.php/records/wsnic0p?filter=dt,bt,{},{}&filter0=PRN,' \
        'sw,G&filter1=PRN,sw,N&filter2=PRN,sw,N&filter3=PRN,sw,N&filter4=PRN,sw,N&filter5=PRN,sw,N&filter6=PRN,' \
        'sw,N&include=dt,PRN,s4_l1_vert,&order=dt'.format(st_time, en_time)
    webURL = urllib.request.urlopen(url)
    param = json.loads(webURL.read().decode())
    parameters = param["records"]
    return parameters


def s4_avg_to_s4_index(s4_avg):
    thresholds = [0.15, 0.3, 0.45, 0.6, 0.75]
    s4_index = 0
    k = 0
    while s4_avg > thresholds[k] and k < 4:
        s4_index += 1
        k += 1
    return s4_index


def get_s4_index():
    st_time, en_time = get_st_en_time()
    data = get_s4_data(st_time, en_time)
    data_ = [d["s4_l1_vert"] for d in data]
    s4_avg = avg(data_)
    s4_index = s4_avg_to_s4_index(s4_avg)
    return s4_index, data


def get_s4m1_index():
    # Get s4 index from yesterday
    st_time, en_time = get_st_en_ysd()
    data = get_s4_data(st_time, en_time)
    data_ = [d["s4_l1_vert"] for d in data]
    s4_avg = avg(data_)
    s4_index = s4_avg_to_s4_index(s4_avg)
    return s4_index


def plot_s4(data):
    timestamps = set(d["dt"] for d in data)
    s4_vert = []
    for timestamp in timestamps:
        cur_s4 = 0
        n = 0
        for d in data:
            if d['dt'] == timestamp and d['s4_l1_vert'] is not None:
                cur_s4 += d['s4_l1_vert']
                n += 1
        cur_s4 = cur_s4 / n
        s4_vert.append({'time': timestamp, 's4': cur_s4})
    x_data = np.array([s4['time'] for s4 in s4_vert], dtype='datetime64')
    x_data = np.sort(x_data)
    y_data = low_pass([s4['s4'] for s4 in s4_vert])
    plt.figure(figsize=(10, 6))
    plt.plot(x_data, y_data, color='red', lw=0.7)
    plt.plot(x_data, [0.25]*len(x_data), '--', color='black', lw=1.5)
    locator = mdates.AutoDateLocator(minticks=6, maxticks=10)
    formatter = mdates.ConciseDateFormatter(locator)
    ax = plt.gca()
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)
    plt.grid(True)
    plt.xlabel('Time')
    plt.ylabel('S4')
    plt.legend(['Past day world averaged scintillation', 'SC1 alert level'])
    plt.show()


def main():
    st_time = "2023-01-25%2008:10:00"
    en_time = "2023-01-25%2011:10:00"

    parameters = get_s4_data(st_time, en_time)

    print(parameters[0].keys())

    print(parameters)

    timestamps = set(param["dt"] for param in parameters)
    s4_vert = []

    print(s4_vert)


if __name__ == "__main__":
    #main()
    #print(s4_avg_to_s4_index(0.5))
    s4_index, data = get_s4_index()
    print(s4_index)
    plot_s4(data)

