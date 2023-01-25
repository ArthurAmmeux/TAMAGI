import requests

base_url = "https://services.swpc.noaa.gov"


def get_json(directory):

    r = requests.get(base_url + directory)

    status = r.status_code

    if status == 200:
        return r.json()


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
        raw_data = get_json(directory)
        R = int(raw_data['0']['R']['Scale'])
        G = int(raw_data['0']['G']['Scale'])
        S = int(raw_data['0']['S']['Scale'])
        R_forecast = ({'Minor_p': raw_data['1']['R']['MinorProb'], 'Major_p': raw_data['1']['R']['MajorProb']},
                      {'Minor_p': raw_data['2']['R']['MinorProb'], 'Major_p': raw_data['2']['R']['MajorProb']})
        G_forecast = (raw_data['1']['G']['Scale'], raw_data['2']['G']['Scale'])
        S_forecast = (raw_data['1']['S']['Prob'], raw_data['2']['S']['Prob'])

    def update(self):
        raw_data = get_json(directory)
        R = int(raw_data['0']['R']['Scale'])
        G = int(raw_data['0']['G']['Scale'])
        S = int(raw_data['0']['S']['Scale'])
        R_forecast = ({'Minor_p': raw_data['1']['R']['MinorProb'], 'Major_p': raw_data['1']['R']['MajorProb']},
                      {'Minor_p': raw_data['2']['R']['MinorProb'], 'Major_p': raw_data['2']['R']['MajorProb']})
        G_forecast = (raw_data['1']['G']['Scale'], raw_data['2']['G']['Scale'])
        S_forecast = (raw_data['1']['S']['Prob'], raw_data['2']['S']['Prob'])


def calculate_indices(noaa_scales):
    R = {0: 0, 1: 0, 2: 0}
    G = {0: 0, 1: 0, 2: 0}
    S = {0: 0, 1: 0, 2: 0}
    SO = {0: 0, 1: 0, 2: 0}
    R[0] = int(noaa_scales['0']['R']['Scale'])
    G[0] = int(noaa_scales['0']['G']['Scale'])
    S[0] = int(noaa_scales['0']['S']['Scale'])
    for i in (1, 2):
        R[i] = int((2*1.5*int(noaa_scales[str(i)]['R']['MinorProb']) + 3*4*int(noaa_scales[str(i)]['R']['MajorProb']))/600)
        G[i] = int(noaa_scales[str(i)]['G']['Scale'])
        S[i] = int(int(noaa_scales[str(i)]['S']['Prob'])*5*3/100)
    for i in range(3):
        SO[i] = int(((G[i]/5)**2 + (S[i]/5)**2)*6/2)
    return {'R': R, 'SO': SO}


if __name__ == '__main__':
    directory = "/products/noaa-scales.json"
    curr_noaa_scales = get_json(directory)
    print_raw_indices(curr_noaa_scales)
    print(calculate_indices(curr_noaa_scales))

