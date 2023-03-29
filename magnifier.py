import tkinter as tk
from ctypes import *
from multiprocessing import Process, Queue, freeze_support

import win32con
import win32gui
import win32ui
from PIL import ImageTk, Image
from keyboard import on_release
from pyautogui import position, moveTo


class MagnifierWin(tk.Tk):
    def __init__(self, side_length=250, text_height=50):
        """
        Recommendation: The value of side_length is an odd number multiplied by 10.
        """
        self.__width = side_length
        self.__height = side_length + text_height
        # Parameters related to the screenshot area
        self.__img = None
        self.__grab_len = self.__width // 10
        self.__half_grab_len = self.__grab_len >> 1
        self.__center = self.__width >> 1
        # Parameters related to coordinates of the window
        self.__dist = self.__grab_len + 10
        self.__dpw = self.__dist + self.__width
        self.__dph = self.__dist + self.__height
        self.not_in_loop = True
        super().__init__()
        self.__wwb_dpw = self.winfo_screenwidth() - self.__dpw
        self.__whb_dph = self.winfo_screenheight() - self.__dph
        # Root settings
        self.overrideredirect(True)
        self.attributes('-topmost', 'true')
        self.geometry(f'{self.__width}x{self.__height}')
        self.resizable(False, False)
        # Widgets for showing image and text
        self.__magnifier = tk.Canvas(self, width=self.__width, height=self.__width, highlightthickness=1)
        self.__magnifier.pack(side='top')
        self.__cv_text = tk.Label(self, width=self.__width, height=text_height, font=('Times New Roman', 16))
        self.__cv_text.pack(side='bottom')
        # self.__bri = 0.5**2.2*(1+1.5**2.2+0.6**2.2)
        # Axis settings
        ax_l = (self.__width << 1) // 5
        ax_ld2 = ax_l >> 1
        self.__x_axis = tk.Canvas(self.__magnifier, width=ax_l, height=1, bd=0, highlightthickness=0)
        self.__x_axis.place(x=self.__center - ax_ld2, y=self.__center)
        self.__y_axis = tk.Canvas(self.__magnifier, width=1, height=ax_l, bd=0, highlightthickness=0)
        self.__y_axis.place(x=self.__center, y=self.__center - ax_ld2)
        # Running
        on_release(self.__key_control)
        self.__run()
        # self.mainloop()

    def __run(self):
        x, y = position()
        # Color information
        pcv = windll.gdi32.GetPixel(windll.user32.GetDC(None), x, y)
        r, g, b = pcv & 255, (pcv >> 8) & 255, pcv >> 16
        # (r/255)**2.2+(1.5*g/255)**2.2+(0.6*b/255)**2 > self.__bri
        axi_tex_col = 'black' if r + g + b > 381 else 'white'
        text = '#' + '{:02X}'.format(r) + '{:02X}'.format(g) + '{:02X}'.format(b)
        # Screenshot
        self.__img = self.__screenshot(
            x - self.__half_grab_len, y - self.__half_grab_len, self.__grab_len, self.__grab_len,
            self.__width, self.__width
        )
        # Modify content of widgets.
        # noinspection PyBroadException
        try:
            self.__x_axis.configure(bg=axi_tex_col)
            self.__y_axis.configure(bg=axi_tex_col)
            self.__cv_text.configure(bg=text, text=text, fg=axi_tex_col)
            self.__magnifier.create_image(self.__center, self.__center, image=self.__img)
        except BaseException:
            return
        # Motion
        x = x - self.__dpw if self.__wwb_dpw < x else x + self.__dist
        y = y - self.__dph if self.__whb_dph < y else y + self.__dist
        self.geometry(f'+{x}+{y}')
        self.after(1, self.__run)

    @staticmethod
    def __screenshot(x, y, w, h, nw, nh):
        hwn = 0
        hwn_dc = win32gui.GetWindowDC(hwn)
        mfc_dc = win32ui.CreateDCFromHandle(hwn_dc)
        save_dc = mfc_dc.CreateCompatibleDC()
        bitmap = win32ui.CreateBitmap()
        bitmap.CreateCompatibleBitmap(mfc_dc, w, h)
        # Save the image to the bitmap.
        save_dc.SelectObject(bitmap)
        # get source: (x, y)rct(x+w, y+h); get object: (0, 0)rct(w, h)
        save_dc.BitBlt((0, 0), (w, h), mfc_dc, (x, y), win32con.SRCCOPY)
        info = bitmap.GetInfo()
        bits = bitmap.GetBitmapBits(True)
        # Release memory space.
        win32gui.DeleteObject(bitmap.GetHandle())
        save_dc.DeleteDC()
        mfc_dc.DeleteDC()
        win32gui.ReleaseDC(hwn, hwn_dc)
        # Return the image.
        return ImageTk.PhotoImage(
            Image.frombuffer(
                'RGB', (info['bmWidth'], info['bmHeight']), bits, 'raw', 'BGRX', 0, 1
            ).resize((nw, nh))
        )

    # noinspection PyBroadException
    def __key_control(self, event):
        if self.not_in_loop:
            return
        if event.event_type == 'up' and (event.name == 'ctrl' or event.name == 'right ctrl'):
            self.destroy()
        elif event.event_type == 'up' and event.name == 'up':
            mx, my = position()
            try:
                moveTo(mx, my - 1, duration=0)
            except BaseException:
                return
        elif event.event_type == 'up' and event.name == 'down':
            mx, my = position()
            try:
                moveTo(mx, my + 1, duration=0)
            except BaseException:
                return
        elif event.event_type == 'up' and event.name == 'left':
            mx, my = position()
            try:
                moveTo(mx - 1, my, duration=0)
            except BaseException:
                return
        elif event.event_type == 'up' and event.name == 'right':
            mx, my = position()
            try:
                moveTo(mx + 1, my, duration=0)
            except BaseException:
                return


class MagnifierWinController(object):
    def __init__(self):
        freeze_support()
        self.queue = Queue()
        self.__mag_process = Process(target=self.mag_targ, args=(self.queue,))
        self.__mag_process.start()

    @staticmethod
    def mag_targ(queue):
        mag = MagnifierWin()
        queue.get(True)
        mag.not_in_loop = False
        mag.mainloop()

    def create_magnifier(self):
        self.queue.put(True)

    def delete_magnifier(self):
        self.exit()
        self.__init__()

    def exit(self):
        try:
            self.__mag_process.terminate()
        except AttributeError:
            pass


if __name__ == '__main__':
    pass
