import win32clipboard as wcl
from keyboard import on_release

import color_models as cm
import icon
import widgets as wdt
from magnifier import MagnifierWinController
from tools import *


class ParameterManager(object):
    def __init__(self):
        self.eye_dp = False
        self.input_type = 'RGB'
        self.rgb_form = 'int'
        self.hex_form = 'upper'
        self.hsl_form = 'dft'
        self.hsv_form = 'dft'
        self.r_dp = '.4f'
        self.g_dp = '.4f'
        self.b_dp = '.4f'
        self.hl_dp = '.4f'
        self.sl_dp = '.4f'
        self.l_dp = '.4f'
        self.hv_dp = '.4f'
        self.sv_dp = '.4f'
        self.v_dp = '.4f'
        self.c_dp = '.4f'
        self.m_dp = '.4f'
        self.y_dp = '.4f'
        self.k_dp = '.4f'
        self.r = 250
        self.g = 250
        self.b = 250
        self.current_hex = None

    def output(self):
        self.current_hex = cm.rgb_hex(cm.rgb_rgb((self.r, self.g, self.b)), self.hex_form)
        rt.convertor.cvs.configure(bg=self.current_hex)
        rt.convertor.rgb.put_text(
            cm.rgb_rgb((self.r, self.g, self.b), self.rgb_form, (self.r_dp, self.g_dp, self.b_dp)))
        rt.convertor.hex.put_text(self.current_hex)
        rt.convertor.hsl.put_text(
            cm.rgb_hsl((self.r, self.g, self.b), self.hsl_form, (self.hl_dp, self.sl_dp, self.l_dp)))
        rt.convertor.hsv.put_text(
            cm.rgb_hsv((self.r, self.g, self.b), self.hsv_form, (self.hv_dp, self.sv_dp, self.v_dp)))
        rt.convertor.cmyk.put_text(
            cm.rgb_cmyk((self.r, self.g, self.b), (self.c_dp, self.m_dp, self.y_dp, self.k_dp)))


def eyedrop():
    rt.bar.but[0].disable()
    pra_manager.eye_dp = True
    _mag_.create_magnifier()


def release_eyedrop(event):
    if not pra_manager.eye_dp:
        return
    if event.event_type == 'up' and (event.name == 'ctrl' or event.name == 'right ctrl'):
        rt.bar.but[0].able()
        pra_manager.eye_dp = False
        dropper.get_color_value()
        rt.col_container.tmp_save(dropper.return_hex())
        pra_manager.r, pra_manager.g, pra_manager.b = dropper.return_rgb()
        pra_manager.output()
        _mag_.delete_magnifier()


def get_input():
    in_val = rt.convertor.input.entry.get()
    rt.convertor.input.entry.delete(0, 'end')
    if in_val is None:
        return
    in_val = analyse_user_input(in_val, pra_manager.input_type)
    if in_val is None:
        return
    #
    form = 'None'
    if pra_manager.input_type == 'RGB' and pra_manager.rgb_form == 'hs':
        in_val = (in_val[0] * 255, in_val[1] * 255, in_val[2] * 255)
    elif pra_manager.input_type == 'HSL':
        form = pra_manager.hsl_form
    elif pra_manager.input_type == 'HSV':
        form = pra_manager.hsv_form
    if pra_manager.input_type != 'HEX':
        if not is_interval_legal(in_val, pra_manager.input_type, form):
            return
    if pra_manager.input_type == 'HEX':
        pra_manager.r, pra_manager.g, pra_manager.b = cm.hex_rgb(in_val)
    elif pra_manager.input_type == 'HSV':
        pra_manager.r, pra_manager.g, pra_manager.b = cm.hsv_rgb(in_val, pra_manager.hsv_form)
    elif pra_manager.input_type == 'HSL':
        pra_manager.r, pra_manager.g, pra_manager.b = cm.hsl_rgb(in_val, pra_manager.hsl_form)
    elif pra_manager.input_type == 'CMYK':
        pra_manager.r, pra_manager.g, pra_manager.b = cm.cmyk_rgb(in_val)
    else:
        pra_manager.r, pra_manager.g, pra_manager.b = in_val[0], in_val[1], in_val[2]
    pra_manager.output()
    rt.col_container.tmp_save(pra_manager.current_hex)


if __name__ == "__main__":
    _mag_ = MagnifierWinController()
    dropper = EyeDropper()
    pra_manager = ParameterManager()
    on_release(release_eyedrop)
    rt = wdt.Tk(_mng_=pra_manager)
    ico_pt = load_ico(icon.icon_img)
    rt.iconbitmap(ico_pt)
    os.remove(ico_pt)
    rt.title('WinHUE')
    rt.bar.but[0].configure(command=eyedrop)
    rt.convertor.input.entry.bind('<Return>', lambda event: get_input())
    rt.convertor.ok.button.configure(command=lambda: get_input())
    rt.mainloop()
    # noinspection PyBroadException
    try:
        wcl.OpenClipboard()
        wcl.SetClipboardData(1, wcl.GetClipboardData())
        wcl.CloseClipboard()
    except BaseException:
        pass
    _mag_.exit()
