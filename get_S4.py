### Python code for download the requested data from the eSWua web-service

#-------Import of the requested libraries.
import json
import urllib.request
import time


def avg(lis):
    res = 0
    length = len(lis)
    for num in lis:
        if num is not None:
            res += num
        else:
            length -= 1
    return res/length


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
        print(k)
    return s4_index


def main():
    st_time = "2023-01-25%2008:10:00"
    en_time = "2023-01-25%2011:10:00"

    parameters = get_s4_data(st_time, en_time)

    # print(parameters[0][0].keys())

    timestamps = set(param["dt"] for param in parameters)

    print(timestamps)

    s4_vert = [param["s4_l1_vert"] for param in parameters]

    s4_avg = avg(s4_vert)

    print(s4_vert)

    print(s4_avg)

    s4_index = s4_avg_to_s4_index(s4_avg)

    print(s4_index)


if __name__ == "__main__":
    #main()
    print(s4_avg_to_s4_index(0.5))


