import requests

base_url = "https://services.swpc.noaa.gov"


def get_json(directory):

    r = requests.get(base_url + directory)

    status = r.status_code

    if status == 200:
        return r.json()


def main():
    get_json("directory")


if __name__ == "__main__":
    main()
    