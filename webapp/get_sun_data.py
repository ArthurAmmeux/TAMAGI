import requests
import shutil  # save img locally


base_url = "https://sdo.gsfc.nasa.gov"
sun_file_prefix = "./images/sun_last_img_"


def get_img(directory, index):
    r = requests.get(base_url + directory, stream=True)
    status = r.status_code

    if status == 200:
        with open(sun_file_prefix + str(index) + ".jpg", 'wb') as f:
            shutil.copyfileobj(r.raw, f)


def get_sun_img(index):
    # get last image of the sun at 171 Angstrom
    directory = '/assets/img/latest/latest_1024_0171.jpg'
    get_img(directory, index)


def main():
    get_sun_img(0)


if __name__ == '__main__':
    main()
