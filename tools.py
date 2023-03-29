import base64 as b64
import os
import re
from ctypes import *

from pyautogui import position

PI = 3.14159265358979


def analyse_user_input(input_string, v_type='RGB'):
    if v_type == 'HEX':
        data_list = re.findall(r'[0-9a-fA-F]+', input_string)
        if len(data_list) == 0:
            return None
        _hex_ = ''.join(data_list)[:6].lower()
        return '#' + (6 - len(_hex_)) * '0' + _hex_
    data_list = re.findall(r'\d*\.\d+|\d+', input_string)
    if v_type != 'CMYK':
        if len(data_list) < 3:
            return None
        return float(data_list[0]), float(data_list[1]), float(data_list[2])
    else:
        if len(data_list) < 4:
            return None
        return float(data_list[0]), float(data_list[1]), float(data_list[2]), float(data_list[3])


def is_interval_legal(tri, v_type, form):
    if v_type == 'HSL' or v_type == 'HSV':
        if form == 'hs':
            if not (0 <= tri[0] < 1 and 0 <= tri[1] <= 1 and 0 <= tri[2] <= 1):
                return False
        elif form == 'rs':
            if not (0 <= tri[0] < 2 * PI and 0 <= tri[1] <= 1 and 0 <= tri[2] <= 1):
                return False
        else:
            if not (0 <= tri[0] < 360 and 0 <= tri[1] <= 1 and 0 <= tri[2] <= 1):
                return False
    elif v_type == 'CMYK':
        if not (0 <= tri[0] <= 1 and 0 <= tri[1] <= 1 and 0 <= tri[2] <= 1 and 0 <= tri[3] <= 1):
            return False
    else:
        if not (0 <= tri[0] <= 255 and 0 <= tri[1] <= 255 and 0 <= tri[2] <= 255):
            return False
    return True


def load_ico(string):
    img_path = f'temporary_files__the_icon_for_WinHUE.ico'
    if os.path.isfile(img_path):
        os.remove(img_path)
    img_file = open(img_path, 'wb')
    img_file.write(b64.b64decode(string))
    img_file.close()
    return img_path


class EyeDropper(object):
    def __init__(self):
        self.__cv = None

    def get_color_value(self):
        p_x, p_y = position()
        self.__cv = windll.gdi32.GetPixel(windll.user32.GetDC(None), p_x, p_y)

    def return_hex(self):
        if self.__cv is not None:
            hex_cv = "{:06X}".format(self.__cv)
            return '#' + hex_cv[4:6] + hex_cv[2:4] + hex_cv[0:2]

    def return_rgb(self):
        if self.__cv is not None:
            return self.__cv & 255, self.__cv >> 8 & 255, self.__cv >> 16


if __name__ == '__main__':
    pass
