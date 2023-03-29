import tkinter as tk

from pyautogui import position

THEME = '#154260'
BACK = '#FAFAFA'
FORE = '#000000'
SET_FORE = '#154260'
SHADE = '#C8C8C8'
SLC_SHADE = '#95AAB7'
BAR_SHADE = '#738EA0'
FONT = '黑体'
FONT_SIZE = 12


class TopBarTraction(object):
    def __init__(self, bar, ban_xs=(0, 0), ban_ys=(0, 0)):
        self.__ban_xs, self.__ban_ys = ban_xs, ban_ys
        self.__bar = bar
        self.__click_x = 0
        self.__click_y = 0
        self.__bar.bind('<Button-1>', self.__get_click_pos)
        self.__bar.bind('<B1-Motion>', self.__move)

    # noinspection PyUnusedLocal event
    def __get_click_pos(self, event):
        clc_x, clc_y = position()
        self.__click_x, self.__click_y = clc_x - self.__bar.master.winfo_x(), clc_y - self.__bar.master.winfo_y()
        '''
        Principle: self.__click_x, self.__click_y = event.x, event.y.  
        Attention: The event works for all widgets in self.__win.
        '''

    # noinspection PyUnusedLocal event
    def __move(self, event):
        if not (self.__ban_xs[0] < self.__click_x < self.__ban_xs[1]
                and self.__ban_ys[0] < self.__click_y < self.__ban_ys[1]):
            ex, ey = position()
            x, y = ex - self.__click_x, ey - self.__click_y
            self.__bar.master.geometry(f'+{x}+{y}')
        '''
        Principle: 
            x = event.x - self.__click_x + self.__win.winfo_x()
            y = event.y - self.__click_y + self.__win.winfo_y()
            self.__win.geometry(f'+{x}+{y}')
        '''


class Button(tk.Button):
    def __init__(self, mst, tex, cmd=lambda: print('None')):
        super().__init__(master=mst, bg=BACK, fg=FORE, font=(FONT, FONT_SIZE),
                         activebackground=THEME, activeforeground=BACK,
                         bd=0, relief='flat', command=cmd, text=tex
                         )
        self.bind('<Motion>', lambda e: self.configure(bg=SLC_SHADE, fg=THEME))
        self.bind('<Leave>', lambda e: self.configure(bg=BACK, fg=FORE))


class FButton(tk.Frame):
    def __init__(self, mst, tex, cmd=lambda: print('None')):
        super().__init__(master=mst, highlightthickness=2, highlightbackground=SHADE,
                         highlightcolor=SHADE, bd=0)
        self.button = tk.Button(self, bg=BACK, fg=FORE, font=(FONT, FONT_SIZE),
                                activebackground=THEME, activeforeground=BACK,
                                bd=0, relief='flat', command=cmd, text=tex)
        self.button.pack()
        self.button.bind('<Motion>', lambda e: self.__move())
        self.button.bind('<Leave>', lambda e: self.__leave())

    def __move(self):
        self.configure(highlightcolor=THEME, highlightbackground=THEME)
        self.button.configure(bg=SLC_SHADE, fg=THEME)

    def __leave(self):
        self.configure(highlightcolor=SHADE, highlightbackground=SHADE)
        self.button.configure(bg=BACK, fg=FORE)


class NavigationButt(tk.Button):
    def __init__(self, mst, tex):
        super().__init__(master=mst, highlightthickness=0, bd=0, bg=THEME, fg=BACK,
                         text=tex, activeforeground=THEME, disabledforeground=THEME,
                         activebackground=BACK, font=(FONT, FONT_SIZE))
        self.bind('<Motion>', lambda e: self.configure(bg=BAR_SHADE, fg=THEME))
        self.bind('<Leave>', lambda e: self.configure(bg=THEME, fg=BACK))

    def disable(self):
        self.configure(state='disabled', bg=BACK)
        self.unbind('<Motion>')
        self.unbind('<Leave>')

    def able(self):
        self.configure(state='normal', bg=THEME, fg=BACK)
        self.bind('<Motion>', lambda e: self.configure(bg=BAR_SHADE, fg=THEME))
        self.bind('<Leave>', lambda e: self.configure(bg=THEME, fg=BACK))


class CMenu(tk.Menu):
    def __init__(self, mst):
        super().__init__(master=mst, tearoff=False, font=(FONT, FONT_SIZE), bg=BACK, fg=FORE,
                         bd=0)
        self.add_command(label='复制', command=self.__coppy, accelerator='Ctrl+C')

    def __coppy(self):
        self.master.event_generate('<<Copy>>')
        # wcl.OpenClipboard()
        # wcl.SetClipboardData(1, wcl.GetClipboardData())
        # wcl.CloseClipboard()

    def popup(self, event):
        self.post(event.x_root, event.y_root)


class CXPMenu(CMenu):
    def __init__(self, mst):
        super().__init__(mst)
        self.add_command(label='剪切', command=self.__cut, accelerator='Ctrl+X')
        self.add_command(label='粘贴', command=self.__paste, accelerator='Ctrl+P')
        self.add_separator()
        self.add_command(label='全选', command=self.__slc_al, accelerator='Ctrl+A')
        self.add_command(label='清空', command=self.__delete)

    def __cut(self):
        self.master.event_generate('<<Cut>>')
        # wcl.OpenClipboard()
        # wcl.SetClipboardData(1, wcl.GetClipboardData())
        # wcl.CloseClipboard()

    def __paste(self):
        self.master.event_generate('<<Paste>>')

    def __slc_al(self):
        self.master.select_range(0, 'end')

    def __delete(self):
        self.master.delete(0, 'end')


class FEntry(tk.Frame):
    def __init__(self, mst, _width_):
        super().__init__(master=mst, highlightthickness=2, highlightbackground=SHADE,
                         highlightcolor=SHADE, bd=0, bg=BACK)
        self.entry = tk.Entry(self, bd=0, highlightthickness=0, width=_width_,
                              fg=FORE, bg=BACK, justify='center', font=(FONT, FONT_SIZE)
                              )
        self.entry.pack(padx=10, pady=10)
        self.entry.bind('<Motion>', lambda e: self.__move())
        self.entry.bind('<Leave>', lambda e: self.__leave())
        self.menu = CXPMenu(self.entry)
        self.entry.bind("<Button-3>", lambda e: self.menu.popup(e))

    def __move(self):
        self.configure(highlightbackground=THEME, highlightcolor=THEME)
        self.entry.configure(selectbackground=THEME, insertbackground=FORE, selectforeground=BACK)

    def __leave(self):
        self.configure(highlightbackground=SHADE, highlightcolor=SHADE)
        self.entry.configure(selectbackground=SHADE, insertbackground=BACK, selectforeground=FORE)


class Text(tk.Frame):
    def __init__(self, mst, _width_):
        super().__init__(master=mst, highlightthickness=2, highlightbackground=THEME,
                         highlightcolor=THEME, bd=0, bg=BACK)
        self.text = tk.Text(self, bd=0, highlightthickness=0, width=_width_, height=1,
                            fg=FORE, bg=BACK, font=(FONT, FONT_SIZE), state='disabled'
                            )
        self.text.pack(padx=10, pady=10)
        self.menu = CMenu(self.text)
        self.text.bind("<Button-3>", lambda e: self.menu.popup(e))

    def put_text(self, text):
        self.text.config(state='normal')
        self.text.delete('1.0', 'end')
        self.text.tag_configure('center', justify='center')
        self.text.insert('end', text, 'center')
        self.text.config(state='disabled')


class ParameterSettingPage(tk.Frame):
    def __init__(self, mst, title, types_or_forms, vars_to_change_their_decimal_places, scale_length):
        super().__init__(mst, highlightthickness=0, bd=0, bg=BACK)
        self.__colum = len(types_or_forms)
        if self.__colum != 0:
            self.type_tile = tk.Label(self, highlightthickness=0, bd=0, bg=BACK, fg=SET_FORE, text=title,
                                      font=(FONT, FONT_SIZE))
            self.type_tile.grid(row=0, column=0, columnspan=self.__colum, pady=10)
            self.radios = []
            self.radio_int_var = tk.IntVar()
            for ti in range(self.__colum):
                self.radios.append(tk.Radiobutton(self, text=types_or_forms[ti], value=ti, variable=self.radio_int_var,
                                                  relief='flat', fg=SET_FORE, bg=BACK, font=(FONT, FONT_SIZE)))
                self.radios[ti].grid(row=1, column=ti)
        else:
            self.__colum = 1
        #
        self.__scale_num = len(vars_to_change_their_decimal_places)
        if self.__scale_num != 0:
            self.dp_tile = tk.Label(self, highlightthickness=0, bd=0, bg=BACK, fg=SET_FORE, text='小数位数',
                                    font=(FONT, FONT_SIZE))
            self.dp_tile.grid(row=2, column=0, columnspan=self.__colum, pady=10)
            self.scales = []
            self.__names = []
            self.__fra = tk.Frame(self, highlightthickness=0, bd=0, bg=BACK)
            self.__fra.grid(row=3, columnspan=self.__colum, column=0)
            for ti in range(self.__scale_num):
                self.__names.append(tk.Label(self.__fra, highlightthickness=0, bd=0, bg=BACK, fg=SET_FORE,
                                             text=vars_to_change_their_decimal_places[ti], width=2, height=1,
                                             font=(FONT, FONT_SIZE)))
                self.__names[ti].grid(row=ti, column=0, pady=10)
                self.scales.append(tk.Scale(self.__fra, orient='horizontal', from_=1, to=9,
                                            resolution=1, length=scale_length, sliderlength=20, bd=0,
                                            bg=BACK, fg=SET_FORE, sliderrelief='flat', font=(FONT, FONT_SIZE),
                                            takefocus=True, tickinterval=1,
                                            activebackground=SLC_SHADE, troughcolor=SET_FORE, highlightthickness=0))
                self.scales[ti].grid(row=ti, column=1)


class ParameterSettingTop(tk.Toplevel):
    def __init__(self, butt_to_be_bend):
        self.butt_bend = butt_to_be_bend
        super().__init__()
        self.exit_butt = None
        self.bar = None
        self.attributes('-topmost', True)
        self.overrideredirect(True)
        self.configure(bg=BACK)
        x, y = position()
        self.geometry(f'+{x}+{y}')
        self.confirm_butt = FButton(self, tex='确认')
        self.confirm_butt.button.configure(bg=BACK, fg=SET_FORE)
        self.confirm_butt.pack(side='bottom')

    def __exit(self):
        self.butt_bend.configure(state='normal')
        self.destroy()

    def _pack_(self):
        self.update()
        self.bar = tk.Canvas(self, highlightthickness=0, bd=0, bg=SET_FORE, width=self.winfo_width(), height=40)
        self.bar.pack_propagate(False)
        self.bar.pack(side='top')
        TopBarTraction(self.bar, (self.winfo_width() - 40, self.winfo_width()), (0, 40))
        self.exit_butt = Button(self.bar, tex='×', cmd=lambda: self.__exit())
        self.exit_butt.configure(bg=SET_FORE, fg=BACK, activeforeground=SET_FORE, activebackground=BACK)
        self.exit_butt.unbind('<Leave>')
        self.exit_butt.bind('<Leave>', lambda e: self.exit_butt.configure(fg=BACK, bg=SET_FORE))
        self.exit_butt.pack(side='right')


class TypeParameterSetting(ParameterSettingTop):
    def __init__(self, pra_mng, button_whose_tex_to_be_changed):
        super().__init__(button_whose_tex_to_be_changed)
        self.__bwt = button_whose_tex_to_be_changed
        self.__mng = pra_mng
        self.tps = ('HEX', 'RGB', 'HSL', 'HSV', 'CMYK')
        self.psp = ParameterSettingPage(self, '输入类型', self.tps, (), 0)
        self.psp.radio_int_var.set(self.tps.index(pra_mng.input_type))
        self.psp.pack(side='bottom')
        self.confirm_butt.button.configure(command=self.__confirm)
        self._pack_()

    def __confirm(self):
        self.__mng.input_type = self.tps[self.psp.radio_int_var.get()]
        self.__bwt.configure(text=self.__mng.input_type)


class HexParameterSetting(ParameterSettingTop):
    def __init__(self, pra_mng, butt_ben):
        super().__init__(butt_ben)
        self.__mng = pra_mng
        self.tps = ('大写', '小写')
        self.tps_i = ('upper', 'lower')
        self.psp = ParameterSettingPage(self, '字母形式', self.tps, (), 0)
        self.psp.radio_int_var.set(self.tps_i.index(pra_mng.hex_form))
        self.psp.pack(side='bottom')
        self.confirm_butt.button.configure(command=self.__confirm)
        self._pack_()

    def __confirm(self):
        self.__mng.hex_form = self.tps_i[self.psp.radio_int_var.get()]


class RgbParameterSetting(ParameterSettingTop):
    def __init__(self, pra_mng, scale_width, butt_ben):
        super().__init__(butt_ben)
        self.__mng = pra_mng
        self.tps = ('普通', '百分制')
        self.tps_i = ('int', 'hs')
        self.rgb = ('R', 'G', 'B')
        self.psp = ParameterSettingPage(self, 'RGB形式', self.tps, self.rgb, scale_width)
        self.psp.radio_int_var.set(self.tps_i.index(pra_mng.rgb_form))
        self.psp.scales[0].set(int(self.__mng.r_dp[1:2]))
        self.psp.scales[1].set(int(self.__mng.g_dp[1:2]))
        self.psp.scales[2].set(int(self.__mng.b_dp[1:2]))
        self.psp.pack(side='bottom')
        self.confirm_butt.button.configure(command=self.__confirm)
        self._pack_()

    def __confirm(self):
        self.__mng.rgb_form = self.tps_i[self.psp.radio_int_var.get()]
        self.__mng.r_dp = f'.{self.psp.scales[0].get()}f'
        self.__mng.g_dp = f'.{self.psp.scales[1].get()}f'
        self.__mng.b_dp = f'.{self.psp.scales[2].get()}f'


class HslParameterSetting(ParameterSettingTop):
    def __init__(self, pra_mng, scale_width, butt_ben):
        super().__init__(butt_ben)
        self.__mng = pra_mng
        self.tps = ('普通', 'H百分制', 'H弧度制')
        self.tps_i = ('dft', 'hs', 'rs')
        self.hsl = ('H', 'S', 'L')
        self.psp = ParameterSettingPage(self, 'H形式', self.tps, self.hsl, scale_width)
        self.psp.radio_int_var.set(self.tps_i.index(pra_mng.hsl_form))
        self.psp.scales[0].set(int(self.__mng.hl_dp[1:2]))
        self.psp.scales[1].set(int(self.__mng.sl_dp[1:2]))
        self.psp.scales[2].set(int(self.__mng.l_dp[1:2]))
        self.psp.pack(side='bottom')
        self.confirm_butt.button.configure(command=self.__confirm)
        self._pack_()

    def __confirm(self):
        self.__mng.hsl_form = self.tps_i[self.psp.radio_int_var.get()]
        self.__mng.hl_dp = f'.{self.psp.scales[0].get()}f'
        self.__mng.sl_dp = f'.{self.psp.scales[1].get()}f'
        self.__mng.l_dp = f'.{self.psp.scales[2].get()}f'


class HsvParameterSetting(ParameterSettingTop):
    def __init__(self, pra_mng, scale_width, butt_ben):
        super().__init__(butt_ben)
        self.__mng = pra_mng
        self.tps = ('普通', 'H百分制', 'H弧度制')
        self.tps_i = ('dft', 'hs', 'rs')
        self.hsv = ('H', 'S', 'V')
        self.psp = ParameterSettingPage(self, 'H形式', self.tps, self.hsv, scale_width)
        self.psp.radio_int_var.set(self.tps_i.index(pra_mng.hsv_form))
        self.psp.scales[0].set(int(self.__mng.hv_dp[1:2]))
        self.psp.scales[1].set(int(self.__mng.sv_dp[1:2]))
        self.psp.scales[2].set(int(self.__mng.v_dp[1:2]))
        self.psp.pack(side='bottom')
        self.confirm_butt.button.configure(command=self.__confirm)
        self._pack_()

    def __confirm(self):
        self.__mng.hsv_form = self.tps_i[self.psp.radio_int_var.get()]
        self.__mng.hv_dp = f'.{self.psp.scales[0].get()}f'
        self.__mng.sv_dp = f'.{self.psp.scales[1].get()}f'
        self.__mng.v_dp = f'.{self.psp.scales[2].get()}f'


class CmyParameterSetting(ParameterSettingTop):
    def __init__(self, pra_mng, scale_width, butt_ben):
        super().__init__(butt_ben)
        self.__mng = pra_mng
        self.hsl = ('C', 'M', 'K', 'Y')
        self.psp = ParameterSettingPage(self, 'H形式', (), self.hsl, scale_width)
        self.psp.scales[0].set(int(self.__mng.c_dp[1:2]))
        self.psp.scales[1].set(int(self.__mng.m_dp[1:2]))
        self.psp.scales[2].set(int(self.__mng.k_dp[1:2]))
        self.psp.scales[3].set(int(self.__mng.y_dp[1:2]))
        self.psp.pack(side='bottom')
        self.confirm_butt.button.configure(command=self.__confirm)
        self._pack_()

    def __confirm(self):
        self.__mng.c_dp = f'.{self.psp.scales[0].get()}f'
        self.__mng.m_dp = f'.{self.psp.scales[1].get()}f'
        self.__mng.k_dp = f'.{self.psp.scales[2].get()}f'
        self.__mng.y_dp = f'.{self.psp.scales[3].get()}f'


class ValueConvertorPage(tk.Frame):
    def __init__(self, mst, cvs_w, cvs_h, pra_mng):
        self.pra_mng = pra_mng
        self.__scl_w = cvs_w
        super().__init__(mst, highlightthickness=0, bd=0, bg=BACK)
        width = 54
        pdx = 2
        pdy = 3
        self.cvs = tk.Canvas(self, highlightthickness=2, bd=0, highlightcolor=SHADE, highlightbackground=SHADE,
                             bg=BACK, height=cvs_h, width=cvs_w)
        self.cvs.grid(column=0, row=0, columnspan=3, pady=10)
        self.input_b = Button(self, ' RGB ')
        self.input_b.grid(column=0, row=1)
        self.input_b.configure(command=lambda: self.__input_func())
        self.hex_b = Button(self, ' HEX ')
        self.hex_b.grid(column=0, row=2)
        self.hex_b.configure(command=lambda: self.__hex_func())
        self.rgb_b = Button(self, ' RGB ')
        self.rgb_b.grid(column=0, row=3)
        self.rgb_b.configure(command=lambda: self.__rgb_func())
        self.hsl_b = Button(self, ' HSL ')
        self.hsl_b.grid(column=0, row=4)
        self.hsl_b.configure(command=lambda: self.__hsl_func())
        self.hsv_b = Button(self, ' HSV ')
        self.hsv_b.grid(column=0, row=5)
        self.hsv_b.configure(command=lambda: self.__hsv_func())
        self.cmyk_b = Button(self, 'CMYK ')
        self.cmyk_b.grid(column=0, row=6)
        self.cmyk_b.configure(command=lambda: self.__cmy_func())
        #
        self.input = FEntry(self, width)
        self.input.grid(column=1, row=1, pady=pdy, padx=pdx)
        self.hex = Text(self, width)
        self.hex.grid(column=1, row=2, pady=pdy, padx=pdx)
        self.rgb = Text(self, width)
        self.rgb.grid(column=1, row=3, pady=pdy, padx=pdx)
        self.hsl = Text(self, width)
        self.hsl.grid(column=1, row=4, pady=pdy, padx=pdx)
        self.hsv = Text(self, width)
        self.hsv.grid(column=1, row=5, pady=pdy, padx=pdx)
        self.cmyk = Text(self, width)
        self.cmyk.grid(column=1, row=6, pady=pdy, padx=pdx)

        self.ok = FButton(self, '确认')
        self.ok.grid(column=2, row=1)

    def __input_func(self):
        self.input_b.configure(state='disabled')
        TypeParameterSetting(self.pra_mng, self.input_b)

    def __hex_func(self):
        self.hex_b.configure(state='disabled')
        HexParameterSetting(self.pra_mng, self.hex_b)

    def __rgb_func(self):
        self.rgb_b.configure(state='disabled')
        RgbParameterSetting(self.pra_mng, self.__scl_w, self.rgb_b)

    def __hsl_func(self):
        self.hsl_b.configure(state='disabled')
        HslParameterSetting(self.pra_mng, self.__scl_w, self.hsl_b)

    def __hsv_func(self):
        self.hsv_b.configure(state='disabled')
        HsvParameterSetting(self.pra_mng, self.__scl_w, self.hsv_b)

    def __cmy_func(self):
        self.cmyk_b.configure(state='disabled')
        CmyParameterSetting(self.pra_mng, self.__scl_w, self.cmyk_b)


class HelperPage(tk.Label):
    def __init__(self, mst):
        str1 = '1. 单击“取色工具”， 开始取色。\n\n'
        str2 = '2. 将鼠标指针对准目标像素，按下“Ctrl”，完成取色。\n\n'
        str3 = '3. 点击方向键可对鼠标指针位置进行微调。\n\n'
        str4 = '4. 在色彩模型中，点击文本框左侧文字可进行相关参数设置。'
        super().__init__(mst, highlightthickness=0, bd=0, bg=BACK, font=(FONT, FONT_SIZE + 2), fg=THEME,
                         anchor="center", justify="left", text=str1 + str2 + str3 + str4)


class CurrentColorContainerPage(tk.Frame):
    def __init__(self, mst, canvas_w, canvas_h, mng):
        super().__init__(master=mst, highlightthickness=0, bd=0)
        self.__frm = []
        self.__cvs = []
        self.__tex = []
        self.__men = []
        self.__cs = 4
        self.__rs = 3
        self.__num = self.__cs * self.__rs
        self.__cols = ['N'] * self.__num
        for r in range(self.__rs):
            for c in range(self.__cs):
                self.__frm.append(tk.Frame(self, highlightthickness=2, highlightbackground=SHADE,
                                           highlightcolor=SHADE, bd=0, bg=BACK))
                self.__frm[-1].grid(column=c, row=r)
                self.__cvs.append(tk.Canvas(self.__frm[-1], highlightthickness=0, bd=0,
                                            bg=BACK, width=canvas_w, height=canvas_h))
                self.__cvs[-1].pack(side='top', padx=5, pady=5)
                self.__tex.append(tk.Text(self.__frm[-1], highlightthickness=0, height=1, width=7,
                                          selectbackground=THEME, selectforeground=BACK,
                                          bg=BACK, bd=0, fg=FORE, font=(FONT, FONT_SIZE))
                                  )
                # self.__tex[-1].tag_configure('center', justify='center')
                # self.__tex[-1].insert('1.0', 'NONE', 'center')
                self.__tex[-1].configure(state='disabled')
                self.__tex[-1].pack(side='bottom', padx=2, pady=1)
                self.__men.append(CMenu(self.__tex[-1]))
                # bind
                self.__cvs[-1].bind(
                    '<Button-1>', lambda e, i=self.__cvs.index(self.__cvs[-1]), m=mng: self.__clic(i, m))
                self.__cvs[-1].bind('<Motion>', lambda e, f=self.__frm[-1], t=self.__tex[-1]: self.__move(f, t))
                self.__cvs[-1].bind('<Leave>', lambda e, f=self.__frm[-1], t=self.__tex[-1]: self.__leave(f, t))
                self.__tex[-1].bind('<Motion>', lambda e, f=self.__frm[-1], t=self.__tex[-1]: self.__move(f, t))
                self.__tex[-1].bind('<Leave>', lambda e, f=self.__frm[-1], t=self.__tex[-1]: self.__leave(f, t))
                self.__tex[-1].bind('<Button-3>', lambda e, m=self.__men[-1]: m.popup(e))

    @staticmethod
    def __move(frm, tex):
        frm.configure(highlightbackground=THEME, highlightcolor=THEME)
        tex.configure(fg=THEME)

    @staticmethod
    def __leave(frm, tex):
        frm.configure(highlightbackground=SHADE, highlightcolor=SHADE)
        tex.configure(fg=FORE)

    def tmp_save(self, color_hex):
        if color_hex in self.__cols:
            del self.__cols[self.__cols.index(color_hex)]
            self.__cols.insert(0, color_hex)
        else:
            del self.__cols[-1]
            self.__cols.insert(0, color_hex)
        for idx in range(self.__num):
            if self.__cols[idx] == 'N':
                return
            self.__cvs[idx].configure(bg=self.__cols[idx])
            self.__tex[idx].configure(state='normal')
            self.__tex[idx].delete('1.0', 'end')
            self.__tex[idx].insert('1.0', self.__cols[idx])
            self.__tex[idx].configure(state='disabled')

    def __clic(self, idx, mng):
        if self.__cols[idx] == 'N':
            return
        _hex_ = int(self.__cols[idx][1:], 16)
        mng.r, mng.g, mng.b = _hex_ >> 16, _hex_ >> 8 & 255, _hex_ & 255
        mng.output()
        self.tmp_save(self.__cols[idx])


class NavigationBar(tk.Canvas):
    def __init__(self, mst, bar_w, bar_h):
        super().__init__(mst, highlightthickness=0, bd=0, bg=THEME, width=bar_w, height=bar_h)
        self.pack_propagate(False)
        self.__fra = tk.Frame(self, highlightthickness=0, bd=0, bg=THEME)
        self.__fra.pack(side='right')
        self.but = []
        self.__tx = ('取色工具', '色彩模型', '最近记录', '帮助')
        for tx in self.__tx:
            self.but.append(NavigationButt(self.__fra, tx))
            self.but[-1].configure(width=bar_w, height=4)
            self.but[-1].pack(side='top')


class Tk(tk.Tk):
    def __init__(self, _mng_):
        super().__init__()
        self.win_w = self.winfo_screenwidth() >> 1
        self.win_h = self.winfo_screenheight() >> 1
        self.win_ept_w = self.win_w - (self.win_w >> 3)
        self.configure(bg=BACK)
        self.geometry(f'{self.win_w}x{self.win_h}+{self.win_w >> 1}+{self.win_h >> 1}')
        self.maxsize(self.win_w, self.win_h)
        self.bar = NavigationBar(self, self.win_w >> 3, self.win_h)
        self.bar.pack(side='left')
        self.__fill = tk.Canvas(self, highlightthickness=0, bd=0, bg=BACK, width=self.win_w >> 4, height=self.win_h)
        self.__fill.pack_propagate(False)
        self.__fill.pack(side='right')
        self.main = tk.Frame(self, highlightthickness=0, bd=0, bg=BACK)
        self.main.pack(side='right')
        # Pages
        self.convertor = ValueConvertorPage(self.main, cvs_w=(self.win_ept_w << 1) / 3, cvs_h=50, pra_mng=_mng_)
        self.col_container = CurrentColorContainerPage(self.main, self.win_ept_w // 5, self.win_h // 10, _mng_)
        self.helper = HelperPage(self.main)
        self.helper.pack(side='right')
        self.bar.but[3].disable()
        self.__crt_page = self.helper
        self.__crt_pg_id = 3
        self.bar.but[1].configure(command=lambda: self.__exchange_page(self.convertor, 1))
        self.bar.but[2].configure(command=lambda: self.__exchange_page(self.col_container, 2))
        self.bar.but[3].configure(command=lambda: self.__exchange_page(self.helper, 3))

    def __exchange_page(self, obj, _id_):
        self.__crt_page.pack_forget()
        self.__crt_page = obj
        self.bar.but[self.__crt_pg_id].able()
        self.__crt_pg_id = _id_
        obj.pack(side='right')
        self.bar.but[_id_].disable()
