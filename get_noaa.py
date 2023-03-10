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
        self.G_forecast = (raw_data['1']['G']['Scale'], raw_data['2']['G']['Scale'])
        self.S_forecast = (raw_data['1']['S']['Prob'], raw_data['2']['S']['Prob'])

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
        self.G_forecast = (raw_data['1']['G']['Scale'], raw_data['2']['G']['Scale'])
        self.S_forecast = (raw_data['1']['S']['Prob'], raw_data['2']['S']['Prob'])

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
    R = {0: 0, 1: 0, 2: 0}
    G = {0: 0, 1: 0, 2: 0}
    S = {0: 0, 1: 0, 2: 0}
    P = {0: 0, 1: 0, 2: 0}
    R[0] = noaa_scales.R
    G[0] = noaa_scales.G
    S[0] = noaa_scales.S
    for i in (0, 1):
        R[i] = int((2 * 1.5 * noaa_scales.R_forecast[i]['Minor_p'] + 3 * 4 * noaa_scales.R_forecast[i]['Major_p'])
                   /
                   600)
        G[i] = int(noaa_scales.G_forecast[i])
        S[i] = int(int(noaa_scales.S_forecast[i])*5*3/100)
    for i in range(3):
        P[i] = int(((G[i]/5)**2 + (S[i]/5)**2)*6/2)
    return {'R': R, 'P': P}


if __name__ == '__main__':
    directory = "/products/noaa-scales.json"
    curr_noaa_scales = NoaaScales()
    print(curr_noaa_scales)
    print("--- NEW INDICES ---\n")
    print(calculate_indices(curr_noaa_scales))

