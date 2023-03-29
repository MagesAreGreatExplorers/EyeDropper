from legacy_scheme.magnifier import MagnifierController
from keyboard import on_release
from tools import EyeDropper
import widgets as wdt
import win32clipboard as wcl
eye_dp = False


def eyedrop():
    r.bar.but[0].disable()
    global eye_dp
    eye_dp = True
    mag.startup_magnifier()


def release_eyedrop(event):
    global eye_dp
    if not eye_dp:
        return
    if event.event_type == 'up' and (event.name == 'ctrl' or event.name == 'right ctrl'):
        r.bar.but[0].able()
        eye_dp = False
        dp.get_color_value()
        col_container.tmp_save(dp.return_hex())


if __name__ == "__main__":
    mag = MagnifierController()
    mag.start()
    dp = EyeDropper()
    on_release(release_eyedrop)
    r = wdt.Tk()

    r.bar.but[0].configure(command=eyedrop)
    col_container = wdt.CurrentColorContainerPage(r.main, r.win_ept_w // 4, r.win_h // 4)
    col_container.pack(side='right')

    r.mainloop()
    mag.terminate()
    # noinspection PyBroadException
    try:
        wcl.OpenClipboard()
        wcl.SetClipboardData(1, wcl.GetClipboardData())
        wcl.CloseClipboard()
    except BaseException:
        pass
