import requests
import shutil  # save img locally
import cairosvg
import os


base_url = "https://prop.kc2g.com/renders/current/mufd-normal-now.svg"
muf_file_prefix = "muf_world"


def get_muf(index):
    r = requests.get(base_url, stream=True, timeout=5)

    status = r.status_code

    if status == 200:
        with open(muf_file_prefix + ".svg", 'wb') as f:
            shutil.copyfileobj(r.raw, f)
        print('Image successfully Downloaded: ', muf_file_prefix + '.svg')
        # read svg file -> write png file
        input_svg_path = muf_file_prefix + '.svg'
        output_png_path = muf_file_prefix + '_' + '.png'
        # input size: 1092.8 x 546.4
        width = 1093
        height = 547
        cairosvg.svg2png(url=input_svg_path, write_to=output_png_path, output_width=width, output_height=height)
        os.remove("./" + muf_file_prefix + ".svg")
    else:
        print('Image Couldn\'t be retrieved')


if __name__ == '__main__':
    get_muf(0)
