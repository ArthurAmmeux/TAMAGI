import requests
import shutil  # save img locally

base_url = "https://sdo.gsfc.nasa.gov"
sun_file_name = "sun_last_img.jpg"


def get_img(directory):
    r = requests.get(base_url + directory, stream=True)

    status = r.status_code

    if status == 200:
        with open(sun_file_name, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
        print('Image successfully Downloaded: ', sun_file_name)
    else:
        print('Image Couldn\'t be retrieved')


def get_sun_img():
    directory = '/assets/img/latest/latest_1024_0171.jpg'
    get_img(directory)


def main():
    get_sun_img()


if __name__ == '__main__':
    main()
