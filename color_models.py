"""We default that each component of RGB is a float between 0.0 and 255.0.
Therefore, each component of the RGB input should be multiplied by 255 when
using hundred-mark system. """
PI = 3.14159265358979


def hex_rgb(_hex_):
    _hex_ = int(_hex_[1:], 16)
    return _hex_ >> 16, _hex_ >> 8 & 255, _hex_ & 255


def rgb_rgb(rgb, form='dft', dpv=('.4f', '.4f', '.4f')):
    r_, g_, b_ = rgb
    if form == 'hs':
        return f'({format(r_ / 255, dpv[0])}, {format(g_ / 255, dpv[1])}, {format(b_ / 255, dpv[2])})'
    if form == 'int':
        return f"({format(r_, '.0f')}, {format(g_, '.0f')}, {format(b_, '.0f')})"
    return int(format(r_, '.0f')), int(format(g_, '.0f')), int(format(b_, '.0f'))


def rgb_hex(rgb, a_form='upper'):
    _hex_ = '#'
    for cv in rgb:
        cv = '{:02X}'.format(cv)
        _hex_ += cv
    return _hex_ if a_form == 'upper' else _hex_.lower()


def hsl_rgb(hsl, h_form='dft'):
    h_, s_, l_ = hsl
    if h_form == 'rs':  # radian system
        h_ *= 180 / PI
    elif h_form == 'hs':  # hundred-mark system
        h_ *= 360
    t = s_ * (1 - abs(2 * l_ - 1))
    c = 255 * (t / 2 + l_)
    x = 255 * (t * (0.5 - abs((h_ / 60) % 2 - 1)) + l_)
    m = 255 * (l_ - t / 2)
    if h_ < 60:
        r_, g_, b_ = c, x, m
    elif h_ < 120:
        r_, g_, b_ = x, c, m
    elif h_ < 180:
        r_, g_, b_ = m, c, x
    elif h_ < 240:
        r_, g_, b_ = m, x, c
    elif h_ < 300:
        r_, g_, b_ = x, m, c
    else:
        r_, g_, b_ = c, m, x
    return r_, g_, b_


def rgb_hsl(rgb, h_form='dft', dpv=('.4f', '.4f', '.4f')):
    r_, g_, b_ = rgb
    c_max = max(r_, g_, b_)
    c_min = min(r_, g_, b_)
    delta = c_max - c_min
    # calculate hue
    if delta == 0:
        h_ = 0
    elif c_max == g_:
        h_ = (b_ - r_) / delta * 60 + 120
    elif c_max == b_:
        h_ = (r_ - g_) / delta * 60 + 240
    elif g_ < b_:
        h_ = (g_ - b_) / delta * 60 + 360
    else:
        h_ = (g_ - b_) / delta * 60
    if h_form == 'rs':  # radian system
        h_ *= PI / 180
    elif h_form == 'hs':  # hundred-mark system
        h_ /= 360
    # calculate lightness
    l_ = (c_max + c_min) / 510
    # calculate saturation
    if delta == 0:
        s_ = 0
    elif l_ <= 0.5:
        s_ = delta / (c_max + c_min)
    else:
        s_ = delta / (510 - c_max - c_min)

    return f'({format(h_, dpv[0])}, {format(s_, dpv[1])}, {format(l_, dpv[2])})'


def hsv_rgb(hsv, h_form='dft'):
    h_, s_, v_ = hsv
    if h_form == 'rs':  # radian system
        h_ *= 180 / PI
    elif h_form == 'hs':  # hundred-mark system
        h_ *= 360
    c = 255 * v_
    x = 255 * v_ * (1 - s_ * abs((h_ / 60) % 2 - 1))
    m = 255 * v_ * (1 - s_)
    if h_ < 60:
        r_, g_, b_ = c, x, m
    elif h_ < 120:
        r_, g_, b_ = x, c, m
    elif h_ < 180:
        r_, g_, b_ = m, c, x
    elif h_ < 240:
        r_, g_, b_ = m, x, c
    elif h_ < 300:
        r_, g_, b_ = x, m, c
    else:
        r_, g_, b_ = c, m, x
    return r_, g_, b_


def rgb_hsv(rgb, h_form='dft', dpv=('.4f', '.4f', '.4f')):
    r_, g_, b_ = rgb
    c_max = max(r_, g_, b_)
    c_min = min(r_, g_, b_)
    delta = c_max - c_min
    # calculate hue
    if delta == 0:
        h_ = 0
    elif c_max == g_:
        h_ = (b_ - r_) / delta * 60 + 120
    elif c_max == b_:
        h_ = (r_ - g_) / delta * 60 + 240
    elif g_ < b_:
        h_ = (g_ - b_) / delta * 60 + 360
    else:
        h_ = (g_ - b_) / delta * 60
    if h_form == 'rs':  # radian system
        h_ *= PI / 180
    elif h_form == 'hs':  # hundred-mark system
        h_ /= 360
    # calculate saturation
    s_ = 0 if c_max == 0.0 else delta / c_max
    return f'({format(h_, dpv[0])}, {format(s_, dpv[1])}, {format(c_max / 255, dpv[2])})'


def cmyk_rgb(cmyk):
    r_ = (1 - cmyk[0]) * (1 - cmyk[3]) * 255
    g_ = (1 - cmyk[1]) * (1 - cmyk[3]) * 255
    b_ = (1 - cmyk[2]) * (1 - cmyk[3]) * 255
    return r_, g_, b_


def rgb_cmyk(rgb, dpv=('.4f', '.4f', '.4f', '.4f')):
    r_, g_, b_ = rgb[0] / 255, rgb[1] / 255, rgb[2] / 255
    k_ = 1 - max(r_, g_, b_)
    if k_ == 1:
        return f'({format(1.0, dpv[0])}, {format(1.0, dpv[1])}, {format(1.0, dpv[2])}, {format(1.0, dpv[3])})'
    c_ = (1 - r_ - k_) / (1 - k_)
    m_ = (1 - g_ - k_) / (1 - k_)
    y_ = (1 - b_ - k_) / (1 - k_)
    return f'({format(c_, dpv[0])}, {format(m_, dpv[1])}, {format(y_, dpv[2])}, {format(k_, dpv[3])})'


if __name__ == '__main__':
    pass
