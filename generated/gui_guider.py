# Copyright 2021 NXP
# SPDX-License-Identifier: MIT

import SDL
import utime as time
import usys as sys
import lvgl as lv
import lodepng as png
import ustruct

lv.init()
SDL.init(w=240,h=320)

# Register SDL display driver.
disp_buf1 = lv.disp_draw_buf_t()
buf1_1 = bytearray(240*10)
disp_buf1.init(buf1_1, None, len(buf1_1)//4)
disp_drv = lv.disp_drv_t()
disp_drv.init()
disp_drv.draw_buf = disp_buf1
disp_drv.flush_cb = SDL.monitor_flush
disp_drv.hor_res = 240
disp_drv.ver_res = 320
disp_drv.register()

# Regsiter SDL mouse driver
indev_drv = lv.indev_drv_t()
indev_drv.init() 
indev_drv.type = lv.INDEV_TYPE.POINTER
indev_drv.read_cb = SDL.mouse_read
indev_drv.register()

# Below: Taken from https://github.com/lvgl/lv_binding_micropython/blob/master/driver/js/imagetools.py#L22-L94

COLOR_SIZE = lv.color_t.__SIZE__
COLOR_IS_SWAPPED = hasattr(lv.color_t().ch,'green_h')

class lodepng_error(RuntimeError):
    def __init__(self, err):
        if type(err) is int:
            super().__init__(png.error_text(err))
        else:
            super().__init__(err)

# Parse PNG file header
# Taken from https://github.com/shibukawa/imagesize_py/blob/ffef30c1a4715c5acf90e8945ceb77f4a2ed2d45/imagesize.py#L63-L85

def get_png_info(decoder, src, header):
    # Only handle variable image types

    if lv.img.src_get_type(src) != lv.img.SRC.VARIABLE:
        return lv.RES.INV

    data = lv.img_dsc_t.__cast__(src).data
    if data == None:
        return lv.RES.INV

    png_header = bytes(data.__dereference__(24))

    if png_header.startswith(b'\211PNG\r\n\032\n'):
        if png_header[12:16] == b'IHDR':
            start = 16
        # Maybe this is for an older PNG version.
        else:
            start = 8
        try:
            width, height = ustruct.unpack(">LL", png_header[start:start+8])
        except ustruct.error:
            return lv.RES.INV
    else:
        return lv.RES.INV

    header.always_zero = 0
    header.w = width
    header.h = height
    header.cf = lv.img.CF.TRUE_COLOR_ALPHA

    return lv.RES.OK

def convert_rgba8888_to_bgra8888(img_view):
    for i in range(0, len(img_view), lv.color_t.__SIZE__):
        ch = lv.color_t.__cast__(img_view[i:i]).ch
        ch.red, ch.blue = ch.blue, ch.red

# Read and parse PNG file

def open_png(decoder, dsc):
    img_dsc = lv.img_dsc_t.__cast__(dsc.src)
    png_data = img_dsc.data
    png_size = img_dsc.data_size
    png_decoded = png.C_Pointer()
    png_width = png.C_Pointer()
    png_height = png.C_Pointer()
    error = png.decode32(png_decoded, png_width, png_height, png_data, png_size)
    if error:
        raise lodepng_error(error)
    img_size = png_width.int_val * png_height.int_val * 4
    img_data = png_decoded.ptr_val
    img_view = img_data.__dereference__(img_size)

    if COLOR_SIZE == 4:
        convert_rgba8888_to_bgra8888(img_view)
    else:
        raise lodepng_error("Error: Color mode not supported yet!")

    dsc.img_data = img_data
    return lv.RES.OK

# Above: Taken from https://github.com/lvgl/lv_binding_micropython/blob/master/driver/js/imagetools.py#L22-L94

decoder = lv.img.decoder_create()
decoder.info_cb = get_png_info
decoder.open_cb = open_png

def anim_x_cb(obj, v):
    obj.set_x(v)

def anim_y_cb(obj, v):
    obj.set_y(v)

def ta_event_cb(e,kb):
    code = e.get_code()
    ta = e.get_target()
    if code == lv.EVENT.FOCUSED:
        kb.set_textarea(ta)
        kb.clear_flag(lv.obj.FLAG.HIDDEN)

    if code == lv.EVENT.DEFOCUSED:
        kb.set_textarea(None)
        kb.add_flag(lv.obj.FLAG.HIDDEN)


scrWelcome = lv.obj()
# create style style_scrwelcome_main_main_default
style_scrwelcome_main_main_default = lv.style_t()
style_scrwelcome_main_main_default.init()
style_scrwelcome_main_main_default.set_bg_color(lv.color_make(0x00,0x00,0x00))
style_scrwelcome_main_main_default.set_bg_opa(255)

# add style for scrWelcome
scrWelcome.add_style(style_scrwelcome_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

scrWelcome_imgLogo = lv.img(scrWelcome)
scrWelcome_imgLogo.set_pos(0,60)
scrWelcome_imgLogo.set_size(240,112)
scrWelcome_imgLogo.add_flag(lv.obj.FLAG.CLICKABLE)
try:
    with open('D:\\SRC\\gui-guider\\lvgl_ui\\generated\\mp461442711.png','rb') as f:
        scrWelcome_imgLogo_img_data = f.read()
except:
    print('Could not open D:\\SRC\\gui-guider\\lvgl_ui\\generated\\mp461442711.png')
    sys.exit()

scrWelcome_imgLogo_img = lv.img_dsc_t({
  'data_size': len(scrWelcome_imgLogo_img_data),
  'header': {'always_zero': 0, 'w': 240, 'h': 112, 'cf': lv.img.CF.TRUE_COLOR_ALPHA},
  'data': scrWelcome_imgLogo_img_data
})

scrWelcome_imgLogo.set_src(scrWelcome_imgLogo_img)
scrWelcome_imgLogo.set_pivot(0,0)
scrWelcome_imgLogo.set_angle(0)
# create style style_scrwelcome_imglogo_main_main_default
style_scrwelcome_imglogo_main_main_default = lv.style_t()
style_scrwelcome_imglogo_main_main_default.init()
style_scrwelcome_imglogo_main_main_default.set_img_recolor(lv.color_make(0xff,0xff,0xff))
style_scrwelcome_imglogo_main_main_default.set_img_recolor_opa(0)
style_scrwelcome_imglogo_main_main_default.set_img_opa(255)

# add style for scrWelcome_imgLogo
scrWelcome_imgLogo.add_style(style_scrwelcome_imglogo_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

scrWelcome_labelTitle = lv.label(scrWelcome)
scrWelcome_labelTitle.set_pos(0,200)
scrWelcome_labelTitle.set_size(240,14)
scrWelcome_labelTitle.set_text("Designd by Hang MENG")
scrWelcome_labelTitle.set_long_mode(lv.label.LONG.CLIP)
scrWelcome_labelTitle.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
# create style style_scrwelcome_labeltitle_main_main_default
style_scrwelcome_labeltitle_main_main_default = lv.style_t()
style_scrwelcome_labeltitle_main_main_default.init()
style_scrwelcome_labeltitle_main_main_default.set_radius(0)
style_scrwelcome_labeltitle_main_main_default.set_bg_color(lv.color_make(0x21,0x95,0xf6))
style_scrwelcome_labeltitle_main_main_default.set_bg_grad_color(lv.color_make(0x21,0x95,0xf6))
style_scrwelcome_labeltitle_main_main_default.set_bg_grad_dir(lv.GRAD_DIR.VER)
style_scrwelcome_labeltitle_main_main_default.set_bg_opa(0)
style_scrwelcome_labeltitle_main_main_default.set_text_color(lv.color_make(0xff,0xff,0xff))
try:
    style_scrwelcome_labeltitle_main_main_default.set_text_font(lv.font_FiraCode_Retina_14)
except AttributeError:
    try:
        style_scrwelcome_labeltitle_main_main_default.set_text_font(lv.font_montserrat_14)
    except AttributeError:
        style_scrwelcome_labeltitle_main_main_default.set_text_font(lv.font_montserrat_16)
style_scrwelcome_labeltitle_main_main_default.set_text_letter_space(0)
style_scrwelcome_labeltitle_main_main_default.set_pad_left(0)
style_scrwelcome_labeltitle_main_main_default.set_pad_right(0)
style_scrwelcome_labeltitle_main_main_default.set_pad_top(0)
style_scrwelcome_labeltitle_main_main_default.set_pad_bottom(0)

# add style for scrWelcome_labelTitle
scrWelcome_labelTitle.add_style(style_scrwelcome_labeltitle_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

scrModeSelect = lv.obj()
# create style style_scrmodeselect_main_main_default
style_scrmodeselect_main_main_default = lv.style_t()
style_scrmodeselect_main_main_default.init()
style_scrmodeselect_main_main_default.set_bg_color(lv.color_make(0x80,0x80,0x80))
style_scrmodeselect_main_main_default.set_bg_opa(255)

# add style for scrModeSelect
scrModeSelect.add_style(style_scrmodeselect_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

scrModeSelect_listMode = lv.list(scrModeSelect)
scrModeSelect_listMode.set_pos(0,0)
scrModeSelect_listMode.set_size(240,320)
# create style style_scrmodeselect_listmode_extra_btns_main_default
style_scrmodeselect_listmode_extra_btns_main_default = lv.style_t()
style_scrmodeselect_listmode_extra_btns_main_default.init()
style_scrmodeselect_listmode_extra_btns_main_default.set_radius(5)
style_scrmodeselect_listmode_extra_btns_main_default.set_bg_color(lv.color_make(0xff,0xff,0xff))
style_scrmodeselect_listmode_extra_btns_main_default.set_bg_grad_color(lv.color_make(0xff,0xff,0xff))
style_scrmodeselect_listmode_extra_btns_main_default.set_bg_grad_dir(lv.GRAD_DIR.VER)
style_scrmodeselect_listmode_extra_btns_main_default.set_bg_opa(255)
style_scrmodeselect_listmode_extra_btns_main_default.set_text_color(lv.color_make(0x00,0x00,0x00))
try:
    style_scrmodeselect_listmode_extra_btns_main_default.set_text_font(lv.font_FiraCode_Retina_18)
except AttributeError:
    try:
        style_scrmodeselect_listmode_extra_btns_main_default.set_text_font(lv.font_montserrat_18)
    except AttributeError:
        style_scrmodeselect_listmode_extra_btns_main_default.set_text_font(lv.font_montserrat_16)


# create style style_scrmodeselect_listmode_extra_btns_main_pressed
style_scrmodeselect_listmode_extra_btns_main_pressed = lv.style_t()
style_scrmodeselect_listmode_extra_btns_main_pressed.init()
style_scrmodeselect_listmode_extra_btns_main_pressed.set_radius(5)
style_scrmodeselect_listmode_extra_btns_main_pressed.set_bg_color(lv.color_make(0xff,0xff,0xff))
style_scrmodeselect_listmode_extra_btns_main_pressed.set_bg_grad_color(lv.color_make(0xff,0xff,0xff))
style_scrmodeselect_listmode_extra_btns_main_pressed.set_bg_grad_dir(lv.GRAD_DIR.VER)
style_scrmodeselect_listmode_extra_btns_main_pressed.set_bg_opa(255)
style_scrmodeselect_listmode_extra_btns_main_pressed.set_text_color(lv.color_make(0x00,0x00,0x00))
try:
    style_scrmodeselect_listmode_extra_btns_main_pressed.set_text_font(lv.font_FiraCode_Retina_18)
except AttributeError:
    try:
        style_scrmodeselect_listmode_extra_btns_main_pressed.set_text_font(lv.font_montserrat_18)
    except AttributeError:
        style_scrmodeselect_listmode_extra_btns_main_pressed.set_text_font(lv.font_montserrat_16)


# create style style_scrmodeselect_listmode_extra_btns_main_focused
style_scrmodeselect_listmode_extra_btns_main_focused = lv.style_t()
style_scrmodeselect_listmode_extra_btns_main_focused.init()
style_scrmodeselect_listmode_extra_btns_main_focused.set_radius(5)
style_scrmodeselect_listmode_extra_btns_main_focused.set_bg_color(lv.color_make(0xff,0xff,0xff))
style_scrmodeselect_listmode_extra_btns_main_focused.set_bg_grad_color(lv.color_make(0xff,0xff,0xff))
style_scrmodeselect_listmode_extra_btns_main_focused.set_bg_grad_dir(lv.GRAD_DIR.VER)
style_scrmodeselect_listmode_extra_btns_main_focused.set_bg_opa(255)
style_scrmodeselect_listmode_extra_btns_main_focused.set_text_color(lv.color_make(0x00,0x00,0x00))
try:
    style_scrmodeselect_listmode_extra_btns_main_focused.set_text_font(lv.font_FiraCode_Retina_18)
except AttributeError:
    try:
        style_scrmodeselect_listmode_extra_btns_main_focused.set_text_font(lv.font_montserrat_18)
    except AttributeError:
        style_scrmodeselect_listmode_extra_btns_main_focused.set_text_font(lv.font_montserrat_16)


scrModeSelect_listMode_btn_0 = scrModeSelect_listMode.add_btn(lv.SYMBOL.SETTINGS, "WIFI")

# add style for scrModeSelect_listMode_btn_0
scrModeSelect_listMode_btn_0.add_style(style_scrmodeselect_listmode_extra_btns_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)


# add style for scrModeSelect_listMode_btn_0
scrModeSelect_listMode_btn_0.add_style(style_scrmodeselect_listmode_extra_btns_main_pressed, lv.PART.MAIN|lv.STATE.PRESSED)


# add style for scrModeSelect_listMode_btn_0
scrModeSelect_listMode_btn_0.add_style(style_scrmodeselect_listmode_extra_btns_main_focused, lv.PART.MAIN|lv.STATE.FOCUSED)

scrModeSelect_listMode_btn_1 = scrModeSelect_listMode.add_btn(lv.SYMBOL.DOWNLOAD, "PROGRAMMER")

# add style for scrModeSelect_listMode_btn_1
scrModeSelect_listMode_btn_1.add_style(style_scrmodeselect_listmode_extra_btns_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)


# add style for scrModeSelect_listMode_btn_1
scrModeSelect_listMode_btn_1.add_style(style_scrmodeselect_listmode_extra_btns_main_pressed, lv.PART.MAIN|lv.STATE.PRESSED)


# add style for scrModeSelect_listMode_btn_1
scrModeSelect_listMode_btn_1.add_style(style_scrmodeselect_listmode_extra_btns_main_focused, lv.PART.MAIN|lv.STATE.FOCUSED)

scrModeSelect_listMode_btn_2 = scrModeSelect_listMode.add_btn(lv.SYMBOL.CHARGE, "POWER METER")

# add style for scrModeSelect_listMode_btn_2
scrModeSelect_listMode_btn_2.add_style(style_scrmodeselect_listmode_extra_btns_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)


# add style for scrModeSelect_listMode_btn_2
scrModeSelect_listMode_btn_2.add_style(style_scrmodeselect_listmode_extra_btns_main_pressed, lv.PART.MAIN|lv.STATE.PRESSED)


# add style for scrModeSelect_listMode_btn_2
scrModeSelect_listMode_btn_2.add_style(style_scrmodeselect_listmode_extra_btns_main_focused, lv.PART.MAIN|lv.STATE.FOCUSED)

# create style style_scrmodeselect_listmode_main_main_default
style_scrmodeselect_listmode_main_main_default = lv.style_t()
style_scrmodeselect_listmode_main_main_default.init()
style_scrmodeselect_listmode_main_main_default.set_radius(5)
style_scrmodeselect_listmode_main_main_default.set_bg_color(lv.color_make(0xff,0xff,0xff))
style_scrmodeselect_listmode_main_main_default.set_bg_grad_color(lv.color_make(0xff,0xff,0xff))
style_scrmodeselect_listmode_main_main_default.set_bg_grad_dir(lv.GRAD_DIR.VER)
style_scrmodeselect_listmode_main_main_default.set_bg_opa(255)
style_scrmodeselect_listmode_main_main_default.set_border_color(lv.color_make(0xe1,0xe6,0xee))
style_scrmodeselect_listmode_main_main_default.set_border_width(1)
style_scrmodeselect_listmode_main_main_default.set_pad_left(5)
style_scrmodeselect_listmode_main_main_default.set_pad_right(5)
style_scrmodeselect_listmode_main_main_default.set_pad_top(5)

# add style for scrModeSelect_listMode
scrModeSelect_listMode.add_style(style_scrmodeselect_listmode_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

# create style style_scrmodeselect_listmode_main_scrollbar_default
style_scrmodeselect_listmode_main_scrollbar_default = lv.style_t()
style_scrmodeselect_listmode_main_scrollbar_default.init()
style_scrmodeselect_listmode_main_scrollbar_default.set_radius(5)
style_scrmodeselect_listmode_main_scrollbar_default.set_bg_color(lv.color_make(0xff,0xff,0xff))
style_scrmodeselect_listmode_main_scrollbar_default.set_bg_grad_color(lv.color_make(0xff,0xff,0xff))
style_scrmodeselect_listmode_main_scrollbar_default.set_bg_grad_dir(lv.GRAD_DIR.VER)
style_scrmodeselect_listmode_main_scrollbar_default.set_bg_opa(255)

# add style for scrModeSelect_listMode
scrModeSelect_listMode.add_style(style_scrmodeselect_listmode_main_scrollbar_default, lv.PART.SCROLLBAR|lv.STATE.DEFAULT)

scrWifi = lv.obj()
# create style style_scrwifi_main_main_default
style_scrwifi_main_main_default = lv.style_t()
style_scrwifi_main_main_default.init()
style_scrwifi_main_main_default.set_bg_color(lv.color_make(0x00,0x00,0x00))
style_scrwifi_main_main_default.set_bg_opa(255)

# add style for scrWifi
scrWifi.add_style(style_scrwifi_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

scrWifi_spangroupLog = lv.spangroup(scrWifi)
scrWifi_spangroupLog.set_pos(10,120)
scrWifi_spangroupLog.set_size(220,190)
scrWifi_spangroupLog.set_align(lv.TEXT_ALIGN.LEFT)
scrWifi_spangroupLog.set_overflow(lv.SPAN_OVERFLOW.CLIP)
scrWifi_spangroupLog.set_mode(lv.SPAN_MODE.BREAK)
scrWifi_spangroupLog_span = scrWifi_spangroupLog.new_span()
scrWifi_spangroupLog_span.set_text("LOG")
scrWifi_spangroupLog_span.style.set_text_color(lv.color_make(0xff,0xff,0xff))
scrWifi_spangroupLog_span.style.set_text_decor(lv.TEXT_DECOR.NONE)
try:
    scrWifi_spangroupLog_span.style.set_text_font(lv.font_FiraCode_Retina_14)
except AttributeError:
    try:
        scrWifi_spangroupLog_span.style.set_text_font(lv.font_montserrat_14)
    except AttributeError:
        scrWifi_spangroupLog_span.style.set_text_font(lv.font_montserrat_16)
scrWifi_spangroupLog.refr_mode()
# create style style_scrwifi_spangrouplog_main_main_default
style_scrwifi_spangrouplog_main_main_default = lv.style_t()
style_scrwifi_spangrouplog_main_main_default.init()
style_scrwifi_spangrouplog_main_main_default.set_bg_color(lv.color_make(0x21,0x95,0xf6))
style_scrwifi_spangrouplog_main_main_default.set_bg_grad_color(lv.color_make(0x21,0x95,0xf6))
style_scrwifi_spangrouplog_main_main_default.set_bg_grad_dir(lv.GRAD_DIR.VER)
style_scrwifi_spangrouplog_main_main_default.set_bg_opa(0)
style_scrwifi_spangrouplog_main_main_default.set_border_color(lv.color_make(0xff,0xff,0xff))
style_scrwifi_spangrouplog_main_main_default.set_border_width(1)
style_scrwifi_spangrouplog_main_main_default.set_pad_left(2)
style_scrwifi_spangrouplog_main_main_default.set_pad_right(2)
style_scrwifi_spangrouplog_main_main_default.set_pad_top(2)
style_scrwifi_spangrouplog_main_main_default.set_pad_bottom(2)

# add style for scrWifi_spangroupLog
scrWifi_spangroupLog.add_style(style_scrwifi_spangrouplog_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

scrWifi_labelIp = lv.label(scrWifi)
scrWifi_labelIp.set_pos(10,45)
scrWifi_labelIp.set_size(35,14)
scrWifi_labelIp.set_text("IP:")
scrWifi_labelIp.set_long_mode(lv.label.LONG.CLIP)
scrWifi_labelIp.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
# create style style_scrwifi_labelip_main_main_default
style_scrwifi_labelip_main_main_default = lv.style_t()
style_scrwifi_labelip_main_main_default.init()
style_scrwifi_labelip_main_main_default.set_radius(0)
style_scrwifi_labelip_main_main_default.set_bg_color(lv.color_make(0x21,0x95,0xf6))
style_scrwifi_labelip_main_main_default.set_bg_grad_color(lv.color_make(0x21,0x95,0xf6))
style_scrwifi_labelip_main_main_default.set_bg_grad_dir(lv.GRAD_DIR.VER)
style_scrwifi_labelip_main_main_default.set_bg_opa(0)
style_scrwifi_labelip_main_main_default.set_text_color(lv.color_make(0xff,0xff,0xff))
try:
    style_scrwifi_labelip_main_main_default.set_text_font(lv.font_FiraCode_Retina_14)
except AttributeError:
    try:
        style_scrwifi_labelip_main_main_default.set_text_font(lv.font_montserrat_14)
    except AttributeError:
        style_scrwifi_labelip_main_main_default.set_text_font(lv.font_montserrat_16)
style_scrwifi_labelip_main_main_default.set_text_letter_space(2)
style_scrwifi_labelip_main_main_default.set_pad_left(0)
style_scrwifi_labelip_main_main_default.set_pad_right(0)
style_scrwifi_labelip_main_main_default.set_pad_top(0)
style_scrwifi_labelip_main_main_default.set_pad_bottom(0)

# add style for scrWifi_labelIp
scrWifi_labelIp.add_style(style_scrwifi_labelip_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

scrWifi_labelIpValue = lv.label(scrWifi)
scrWifi_labelIpValue.set_pos(45,45)
scrWifi_labelIpValue.set_size(185,14)
scrWifi_labelIpValue.set_text("NULL")
scrWifi_labelIpValue.set_long_mode(lv.label.LONG.CLIP)
scrWifi_labelIpValue.set_style_text_align(lv.TEXT_ALIGN.LEFT, 0)
# create style style_scrwifi_labelipvalue_main_main_default
style_scrwifi_labelipvalue_main_main_default = lv.style_t()
style_scrwifi_labelipvalue_main_main_default.init()
style_scrwifi_labelipvalue_main_main_default.set_radius(0)
style_scrwifi_labelipvalue_main_main_default.set_bg_color(lv.color_make(0x21,0x95,0xf6))
style_scrwifi_labelipvalue_main_main_default.set_bg_grad_color(lv.color_make(0x21,0x95,0xf6))
style_scrwifi_labelipvalue_main_main_default.set_bg_grad_dir(lv.GRAD_DIR.VER)
style_scrwifi_labelipvalue_main_main_default.set_bg_opa(0)
style_scrwifi_labelipvalue_main_main_default.set_text_color(lv.color_make(0xff,0xff,0xff))
try:
    style_scrwifi_labelipvalue_main_main_default.set_text_font(lv.font_FiraCode_Retina_14)
except AttributeError:
    try:
        style_scrwifi_labelipvalue_main_main_default.set_text_font(lv.font_montserrat_14)
    except AttributeError:
        style_scrwifi_labelipvalue_main_main_default.set_text_font(lv.font_montserrat_16)
style_scrwifi_labelipvalue_main_main_default.set_text_letter_space(2)
style_scrwifi_labelipvalue_main_main_default.set_pad_left(0)
style_scrwifi_labelipvalue_main_main_default.set_pad_right(0)
style_scrwifi_labelipvalue_main_main_default.set_pad_top(0)
style_scrwifi_labelipvalue_main_main_default.set_pad_bottom(0)

# add style for scrWifi_labelIpValue
scrWifi_labelIpValue.add_style(style_scrwifi_labelipvalue_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

scrWifi_btnScanAp = lv.btn(scrWifi)
scrWifi_btnScanAp.set_pos(10,75)
scrWifi_btnScanAp.set_size(220,30)
scrWifi_btnScanAp_label = lv.label(scrWifi_btnScanAp)
scrWifi_btnScanAp_label.set_text("SCAN WIFI")
scrWifi_btnScanAp.set_style_pad_all(0, lv.STATE.DEFAULT)
scrWifi_btnScanAp_label.align(lv.ALIGN.CENTER,0,0)
scrWifi_btnScanAp_label.set_style_text_color(lv.color_make(0xff,0xff,0xff), lv.STATE.DEFAULT)
try:
    scrWifi_btnScanAp_label.set_style_text_font(lv.font_FiraCode_Retina_14, lv.STATE.DEFAULT)
except AttributeError:
    try:
        scrWifi_btnScanAp_label.set_style_text_font(lv.font_montserrat_14, lv.STATE.DEFAULT)
    except AttributeError:
        scrWifi_btnScanAp_label.set_style_text_font(lv.font_montserrat_16, lv.STATE.DEFAULT)
# create style style_scrwifi_btnscanap_main_main_default
style_scrwifi_btnscanap_main_main_default = lv.style_t()
style_scrwifi_btnscanap_main_main_default.init()
style_scrwifi_btnscanap_main_main_default.set_radius(15)
style_scrwifi_btnscanap_main_main_default.set_bg_color(lv.color_make(0x00,0x00,0x00))
style_scrwifi_btnscanap_main_main_default.set_bg_grad_color(lv.color_make(0x00,0x00,0x00))
style_scrwifi_btnscanap_main_main_default.set_bg_grad_dir(lv.GRAD_DIR.VER)
style_scrwifi_btnscanap_main_main_default.set_bg_opa(255)
style_scrwifi_btnscanap_main_main_default.set_shadow_color(lv.color_make(0x21,0x95,0xf6))
style_scrwifi_btnscanap_main_main_default.set_shadow_opa(0)
style_scrwifi_btnscanap_main_main_default.set_border_color(lv.color_make(0xff,0xff,0xff))
style_scrwifi_btnscanap_main_main_default.set_border_width(1)
style_scrwifi_btnscanap_main_main_default.set_border_opa(255)

# add style for scrWifi_btnScanAp
scrWifi_btnScanAp.add_style(style_scrwifi_btnscanap_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

scrWifi_ddlistApList = lv.dropdown(scrWifi)
scrWifi_ddlistApList.set_pos(10,10)
scrWifi_ddlistApList.set_width(220)
# create style style_scrwifi_ddlistaplist_extra_list_selected_default
style_scrwifi_ddlistaplist_extra_list_selected_default = lv.style_t()
style_scrwifi_ddlistaplist_extra_list_selected_default.init()
style_scrwifi_ddlistaplist_extra_list_selected_default.set_radius(3)
style_scrwifi_ddlistaplist_extra_list_selected_default.set_bg_color(lv.color_make(0x00,0xa1,0xb5))
style_scrwifi_ddlistaplist_extra_list_selected_default.set_bg_grad_color(lv.color_make(0x00,0xa1,0xb5))
style_scrwifi_ddlistaplist_extra_list_selected_default.set_bg_grad_dir(lv.GRAD_DIR.VER)
style_scrwifi_ddlistaplist_extra_list_selected_default.set_bg_opa(255)
style_scrwifi_ddlistaplist_extra_list_selected_default.set_border_color(lv.color_make(0xe1,0xe6,0xee))
style_scrwifi_ddlistaplist_extra_list_selected_default.set_border_width(1)
style_scrwifi_ddlistaplist_extra_list_selected_default.set_text_color(lv.color_make(0xff,0xff,0xff))
try:
    style_scrwifi_ddlistaplist_extra_list_selected_default.set_text_font(lv.font_simsun_12)
except AttributeError:
    try:
        style_scrwifi_ddlistaplist_extra_list_selected_default.set_text_font(lv.font_montserrat_12)
    except AttributeError:
        style_scrwifi_ddlistaplist_extra_list_selected_default.set_text_font(lv.font_montserrat_16)

def scrWifi_ddlistApList_event_cb(e):
    scrWifi_ddlistApList.get_list().add_style(style_scrwifi_ddlistaplist_extra_list_selected_default, lv.PART.SELECTED|lv.STATE.DEFAULT)

scrWifi_ddlistApList.add_event_cb(scrWifi_ddlistApList_event_cb, lv.EVENT.READY, None)

# create style style_scrwifi_ddlistaplist_extra_list_main_default
style_scrwifi_ddlistaplist_extra_list_main_default = lv.style_t()
style_scrwifi_ddlistaplist_extra_list_main_default.init()
style_scrwifi_ddlistaplist_extra_list_main_default.set_radius(3)
style_scrwifi_ddlistaplist_extra_list_main_default.set_bg_color(lv.color_make(0xff,0xff,0xff))
style_scrwifi_ddlistaplist_extra_list_main_default.set_bg_grad_color(lv.color_make(0xff,0xff,0xff))
style_scrwifi_ddlistaplist_extra_list_main_default.set_bg_grad_dir(lv.GRAD_DIR.VER)
style_scrwifi_ddlistaplist_extra_list_main_default.set_bg_opa(255)
style_scrwifi_ddlistaplist_extra_list_main_default.set_border_color(lv.color_make(0xe1,0xe6,0xee))
style_scrwifi_ddlistaplist_extra_list_main_default.set_border_width(1)
style_scrwifi_ddlistaplist_extra_list_main_default.set_text_color(lv.color_make(0x0D,0x30,0x55))
try:
    style_scrwifi_ddlistaplist_extra_list_main_default.set_text_font(lv.font_simsun_12)
except AttributeError:
    try:
        style_scrwifi_ddlistaplist_extra_list_main_default.set_text_font(lv.font_montserrat_12)
    except AttributeError:
        style_scrwifi_ddlistaplist_extra_list_main_default.set_text_font(lv.font_montserrat_16)
style_scrwifi_ddlistaplist_extra_list_main_default.set_max_height(90)

def scrWifi_ddlistApList_event_cb(e):
    scrWifi_ddlistApList.get_list().add_style(style_scrwifi_ddlistaplist_extra_list_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

scrWifi_ddlistApList.add_event_cb(scrWifi_ddlistApList_event_cb, lv.EVENT.READY, None)

# create style style_scrwifi_ddlistaplist_extra_list_scrollbar_default
style_scrwifi_ddlistaplist_extra_list_scrollbar_default = lv.style_t()
style_scrwifi_ddlistaplist_extra_list_scrollbar_default.init()
style_scrwifi_ddlistaplist_extra_list_scrollbar_default.set_radius(3)
style_scrwifi_ddlistaplist_extra_list_scrollbar_default.set_bg_color(lv.color_make(0x00,0xff,0x00))
style_scrwifi_ddlistaplist_extra_list_scrollbar_default.set_bg_grad_color(lv.color_make(0xff,0xff,0xff))
style_scrwifi_ddlistaplist_extra_list_scrollbar_default.set_bg_grad_dir(lv.GRAD_DIR.VER)
style_scrwifi_ddlistaplist_extra_list_scrollbar_default.set_bg_opa(255)

def scrWifi_ddlistApList_event_cb(e):
    scrWifi_ddlistApList.get_list().add_style(style_scrwifi_ddlistaplist_extra_list_scrollbar_default, lv.PART.SCROLLBAR|lv.STATE.DEFAULT)

scrWifi_ddlistApList.add_event_cb(scrWifi_ddlistApList_event_cb, lv.EVENT.READY, None)

# create style style_scrwifi_ddlistaplist_main_main_default
style_scrwifi_ddlistaplist_main_main_default = lv.style_t()
style_scrwifi_ddlistaplist_main_main_default.init()
style_scrwifi_ddlistaplist_main_main_default.set_radius(3)
style_scrwifi_ddlistaplist_main_main_default.set_bg_color(lv.color_make(0xff,0xff,0xff))
style_scrwifi_ddlistaplist_main_main_default.set_bg_grad_color(lv.color_make(0xff,0xff,0xff))
style_scrwifi_ddlistaplist_main_main_default.set_bg_grad_dir(lv.GRAD_DIR.VER)
style_scrwifi_ddlistaplist_main_main_default.set_bg_opa(255)
style_scrwifi_ddlistaplist_main_main_default.set_border_color(lv.color_make(0xe1,0xe6,0xee))
style_scrwifi_ddlistaplist_main_main_default.set_border_width(1)
style_scrwifi_ddlistaplist_main_main_default.set_text_color(lv.color_make(0x00,0x00,0x00))
try:
    style_scrwifi_ddlistaplist_main_main_default.set_text_font(lv.font_FiraCode_Retina_14)
except AttributeError:
    try:
        style_scrwifi_ddlistaplist_main_main_default.set_text_font(lv.font_montserrat_14)
    except AttributeError:
        style_scrwifi_ddlistaplist_main_main_default.set_text_font(lv.font_montserrat_16)
style_scrwifi_ddlistaplist_main_main_default.set_text_line_space(20)

# add style for scrWifi_ddlistApList
scrWifi_ddlistApList.add_style(style_scrwifi_ddlistaplist_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

scrProg = lv.obj()
# create style style_scrprog_main_main_default
style_scrprog_main_main_default = lv.style_t()
style_scrprog_main_main_default.init()
style_scrprog_main_main_default.set_bg_color(lv.color_make(0x00,0x00,0x00))
style_scrprog_main_main_default.set_bg_opa(255)

# add style for scrProg
scrProg.add_style(style_scrprog_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

scrProg_labelMtp = lv.label(scrProg)
scrProg_labelMtp.set_pos(10,18)
scrProg_labelMtp.set_size(45,14)
scrProg_labelMtp.set_text("MTP:")
scrProg_labelMtp.set_long_mode(lv.label.LONG.WRAP)
scrProg_labelMtp.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
# create style style_scrprog_labelmtp_main_main_default
style_scrprog_labelmtp_main_main_default = lv.style_t()
style_scrprog_labelmtp_main_main_default.init()
style_scrprog_labelmtp_main_main_default.set_radius(0)
style_scrprog_labelmtp_main_main_default.set_bg_color(lv.color_make(0x21,0x95,0xf6))
style_scrprog_labelmtp_main_main_default.set_bg_grad_color(lv.color_make(0x21,0x95,0xf6))
style_scrprog_labelmtp_main_main_default.set_bg_grad_dir(lv.GRAD_DIR.VER)
style_scrprog_labelmtp_main_main_default.set_bg_opa(0)
style_scrprog_labelmtp_main_main_default.set_text_color(lv.color_make(0xff,0xff,0xff))
try:
    style_scrprog_labelmtp_main_main_default.set_text_font(lv.font_FiraCode_Retina_14)
except AttributeError:
    try:
        style_scrprog_labelmtp_main_main_default.set_text_font(lv.font_montserrat_14)
    except AttributeError:
        style_scrprog_labelmtp_main_main_default.set_text_font(lv.font_montserrat_16)
style_scrprog_labelmtp_main_main_default.set_text_letter_space(2)
style_scrprog_labelmtp_main_main_default.set_pad_left(0)
style_scrprog_labelmtp_main_main_default.set_pad_right(0)
style_scrprog_labelmtp_main_main_default.set_pad_top(0)
style_scrprog_labelmtp_main_main_default.set_pad_bottom(0)

# add style for scrProg_labelMtp
scrProg_labelMtp.add_style(style_scrprog_labelmtp_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

scrProg_labelCfg = lv.label(scrProg)
scrProg_labelCfg.set_pos(10,58)
scrProg_labelCfg.set_size(45,14)
scrProg_labelCfg.set_text("CFG:")
scrProg_labelCfg.set_long_mode(lv.label.LONG.WRAP)
scrProg_labelCfg.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
# create style style_scrprog_labelcfg_main_main_default
style_scrprog_labelcfg_main_main_default = lv.style_t()
style_scrprog_labelcfg_main_main_default.init()
style_scrprog_labelcfg_main_main_default.set_radius(0)
style_scrprog_labelcfg_main_main_default.set_bg_color(lv.color_make(0x21,0x95,0xf6))
style_scrprog_labelcfg_main_main_default.set_bg_grad_color(lv.color_make(0x21,0x95,0xf6))
style_scrprog_labelcfg_main_main_default.set_bg_grad_dir(lv.GRAD_DIR.VER)
style_scrprog_labelcfg_main_main_default.set_bg_opa(0)
style_scrprog_labelcfg_main_main_default.set_text_color(lv.color_make(0xff,0xff,0xff))
try:
    style_scrprog_labelcfg_main_main_default.set_text_font(lv.font_FiraCode_Retina_14)
except AttributeError:
    try:
        style_scrprog_labelcfg_main_main_default.set_text_font(lv.font_montserrat_14)
    except AttributeError:
        style_scrprog_labelcfg_main_main_default.set_text_font(lv.font_montserrat_16)
style_scrprog_labelcfg_main_main_default.set_text_letter_space(2)
style_scrprog_labelcfg_main_main_default.set_pad_left(0)
style_scrprog_labelcfg_main_main_default.set_pad_right(0)
style_scrprog_labelcfg_main_main_default.set_pad_top(0)
style_scrprog_labelcfg_main_main_default.set_pad_bottom(0)

# add style for scrProg_labelCfg
scrProg_labelCfg.add_style(style_scrprog_labelcfg_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

scrProg_btnStart = lv.btn(scrProg)
scrProg_btnStart.set_pos(10,90)
scrProg_btnStart.set_size(220,30)
scrProg_btnStart_label = lv.label(scrProg_btnStart)
scrProg_btnStart_label.set_text("START")
scrProg_btnStart.set_style_pad_all(0, lv.STATE.DEFAULT)
scrProg_btnStart_label.align(lv.ALIGN.CENTER,0,0)
scrProg_btnStart_label.set_style_text_color(lv.color_make(0xff,0xff,0xff), lv.STATE.DEFAULT)
try:
    scrProg_btnStart_label.set_style_text_font(lv.font_FiraCode_Retina_14, lv.STATE.DEFAULT)
except AttributeError:
    try:
        scrProg_btnStart_label.set_style_text_font(lv.font_montserrat_14, lv.STATE.DEFAULT)
    except AttributeError:
        scrProg_btnStart_label.set_style_text_font(lv.font_montserrat_16, lv.STATE.DEFAULT)
# create style style_scrprog_btnstart_main_main_default
style_scrprog_btnstart_main_main_default = lv.style_t()
style_scrprog_btnstart_main_main_default.init()
style_scrprog_btnstart_main_main_default.set_radius(15)
style_scrprog_btnstart_main_main_default.set_bg_color(lv.color_make(0x00,0x00,0x00))
style_scrprog_btnstart_main_main_default.set_bg_grad_color(lv.color_make(0x00,0x00,0x00))
style_scrprog_btnstart_main_main_default.set_bg_grad_dir(lv.GRAD_DIR.VER)
style_scrprog_btnstart_main_main_default.set_bg_opa(255)
style_scrprog_btnstart_main_main_default.set_shadow_color(lv.color_make(0x21,0x95,0xf6))
style_scrprog_btnstart_main_main_default.set_shadow_opa(0)
style_scrprog_btnstart_main_main_default.set_border_color(lv.color_make(0xff,0xff,0xff))
style_scrprog_btnstart_main_main_default.set_border_width(1)
style_scrprog_btnstart_main_main_default.set_border_opa(255)

# add style for scrProg_btnStart
scrProg_btnStart.add_style(style_scrprog_btnstart_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

scrProg_spangroupLog = lv.spangroup(scrProg)
scrProg_spangroupLog.set_pos(10,135)
scrProg_spangroupLog.set_size(220,135)
scrProg_spangroupLog.set_align(lv.TEXT_ALIGN.LEFT)
scrProg_spangroupLog.set_overflow(lv.SPAN_OVERFLOW.CLIP)
scrProg_spangroupLog.set_mode(lv.SPAN_MODE.FIXED)
scrProg_spangroupLog_span = scrProg_spangroupLog.new_span()
scrProg_spangroupLog_span.set_text("LOG")
scrProg_spangroupLog_span.style.set_text_color(lv.color_make(0xff,0xff,0xff))
scrProg_spangroupLog_span.style.set_text_decor(lv.TEXT_DECOR.NONE)
try:
    scrProg_spangroupLog_span.style.set_text_font(lv.font_FiraCode_Retina_14)
except AttributeError:
    try:
        scrProg_spangroupLog_span.style.set_text_font(lv.font_montserrat_14)
    except AttributeError:
        scrProg_spangroupLog_span.style.set_text_font(lv.font_montserrat_16)
# create style style_scrprog_spangrouplog_main_main_default
style_scrprog_spangrouplog_main_main_default = lv.style_t()
style_scrprog_spangrouplog_main_main_default.init()
style_scrprog_spangrouplog_main_main_default.set_bg_color(lv.color_make(0x21,0x95,0xf6))
style_scrprog_spangrouplog_main_main_default.set_bg_grad_color(lv.color_make(0x21,0x95,0xf6))
style_scrprog_spangrouplog_main_main_default.set_bg_grad_dir(lv.GRAD_DIR.VER)
style_scrprog_spangrouplog_main_main_default.set_bg_opa(0)
style_scrprog_spangrouplog_main_main_default.set_border_color(lv.color_make(0xff,0xff,0xff))
style_scrprog_spangrouplog_main_main_default.set_border_width(1)
style_scrprog_spangrouplog_main_main_default.set_pad_left(2)
style_scrprog_spangrouplog_main_main_default.set_pad_right(2)
style_scrprog_spangrouplog_main_main_default.set_pad_top(2)
style_scrprog_spangrouplog_main_main_default.set_pad_bottom(2)

# add style for scrProg_spangroupLog
scrProg_spangroupLog.add_style(style_scrprog_spangrouplog_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

scrProg_barProgress = lv.bar(scrProg)
scrProg_barProgress.set_pos(10,280)
scrProg_barProgress.set_size(220,30)
scrProg_barProgress.set_style_anim_time(1000, lv.PART.INDICATOR|lv.STATE.DEFAULT)
scrProg_barProgress.set_mode(lv.bar.MODE.NORMAL)
scrProg_barProgress.set_value(50, lv.ANIM.OFF)
# create style style_scrprog_barprogress_main_main_default
style_scrprog_barprogress_main_main_default = lv.style_t()
style_scrprog_barprogress_main_main_default.init()
style_scrprog_barprogress_main_main_default.set_radius(15)
style_scrprog_barprogress_main_main_default.set_bg_color(lv.color_make(0xff,0xff,0xff))
style_scrprog_barprogress_main_main_default.set_bg_grad_color(lv.color_make(0xff,0xff,0xff))
style_scrprog_barprogress_main_main_default.set_bg_grad_dir(lv.GRAD_DIR.VER)
style_scrprog_barprogress_main_main_default.set_bg_opa(82)
style_scrprog_barprogress_main_main_default.set_pad_left(0)
style_scrprog_barprogress_main_main_default.set_pad_right(0)
style_scrprog_barprogress_main_main_default.set_pad_top(0)
style_scrprog_barprogress_main_main_default.set_pad_bottom(0)

# add style for scrProg_barProgress
scrProg_barProgress.add_style(style_scrprog_barprogress_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

# create style style_scrprog_barprogress_main_indicator_default
style_scrprog_barprogress_main_indicator_default = lv.style_t()
style_scrprog_barprogress_main_indicator_default.init()
style_scrprog_barprogress_main_indicator_default.set_radius(10)
style_scrprog_barprogress_main_indicator_default.set_bg_color(lv.color_make(0x21,0x95,0xf6))
style_scrprog_barprogress_main_indicator_default.set_bg_grad_color(lv.color_make(0x21,0x95,0xf6))
style_scrprog_barprogress_main_indicator_default.set_bg_grad_dir(lv.GRAD_DIR.VER)
style_scrprog_barprogress_main_indicator_default.set_bg_opa(255)

# add style for scrProg_barProgress
scrProg_barProgress.add_style(style_scrprog_barprogress_main_indicator_default, lv.PART.INDICATOR|lv.STATE.DEFAULT)

scrProg_ddlistCfgFile = lv.dropdown(scrProg)
scrProg_ddlistCfgFile.set_pos(55,50)
scrProg_ddlistCfgFile.set_width(175)
scrProg_ddlistCfgFile.set_options("NULL")
# create style style_scrprog_ddlistcfgfile_extra_list_selected_default
style_scrprog_ddlistcfgfile_extra_list_selected_default = lv.style_t()
style_scrprog_ddlistcfgfile_extra_list_selected_default.init()
style_scrprog_ddlistcfgfile_extra_list_selected_default.set_radius(3)
style_scrprog_ddlistcfgfile_extra_list_selected_default.set_bg_color(lv.color_make(0x00,0xa1,0xb5))
style_scrprog_ddlistcfgfile_extra_list_selected_default.set_bg_grad_color(lv.color_make(0x00,0xa1,0xb5))
style_scrprog_ddlistcfgfile_extra_list_selected_default.set_bg_grad_dir(lv.GRAD_DIR.VER)
style_scrprog_ddlistcfgfile_extra_list_selected_default.set_bg_opa(255)
style_scrprog_ddlistcfgfile_extra_list_selected_default.set_border_color(lv.color_make(0xe1,0xe6,0xee))
style_scrprog_ddlistcfgfile_extra_list_selected_default.set_border_width(1)
style_scrprog_ddlistcfgfile_extra_list_selected_default.set_text_color(lv.color_make(0xff,0xff,0xff))
try:
    style_scrprog_ddlistcfgfile_extra_list_selected_default.set_text_font(lv.font_simsun_12)
except AttributeError:
    try:
        style_scrprog_ddlistcfgfile_extra_list_selected_default.set_text_font(lv.font_montserrat_12)
    except AttributeError:
        style_scrprog_ddlistcfgfile_extra_list_selected_default.set_text_font(lv.font_montserrat_16)

def scrProg_ddlistCfgFile_event_cb(e):
    scrProg_ddlistCfgFile.get_list().add_style(style_scrprog_ddlistcfgfile_extra_list_selected_default, lv.PART.SELECTED|lv.STATE.DEFAULT)

scrProg_ddlistCfgFile.add_event_cb(scrProg_ddlistCfgFile_event_cb, lv.EVENT.READY, None)

# create style style_scrprog_ddlistcfgfile_extra_list_main_default
style_scrprog_ddlistcfgfile_extra_list_main_default = lv.style_t()
style_scrprog_ddlistcfgfile_extra_list_main_default.init()
style_scrprog_ddlistcfgfile_extra_list_main_default.set_radius(3)
style_scrprog_ddlistcfgfile_extra_list_main_default.set_bg_color(lv.color_make(0xff,0xff,0xff))
style_scrprog_ddlistcfgfile_extra_list_main_default.set_bg_grad_color(lv.color_make(0xff,0xff,0xff))
style_scrprog_ddlistcfgfile_extra_list_main_default.set_bg_grad_dir(lv.GRAD_DIR.VER)
style_scrprog_ddlistcfgfile_extra_list_main_default.set_bg_opa(255)
style_scrprog_ddlistcfgfile_extra_list_main_default.set_border_color(lv.color_make(0xe1,0xe6,0xee))
style_scrprog_ddlistcfgfile_extra_list_main_default.set_border_width(1)
style_scrprog_ddlistcfgfile_extra_list_main_default.set_text_color(lv.color_make(0x0D,0x30,0x55))
try:
    style_scrprog_ddlistcfgfile_extra_list_main_default.set_text_font(lv.font_simsun_12)
except AttributeError:
    try:
        style_scrprog_ddlistcfgfile_extra_list_main_default.set_text_font(lv.font_montserrat_12)
    except AttributeError:
        style_scrprog_ddlistcfgfile_extra_list_main_default.set_text_font(lv.font_montserrat_16)
style_scrprog_ddlistcfgfile_extra_list_main_default.set_max_height(90)

def scrProg_ddlistCfgFile_event_cb(e):
    scrProg_ddlistCfgFile.get_list().add_style(style_scrprog_ddlistcfgfile_extra_list_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

scrProg_ddlistCfgFile.add_event_cb(scrProg_ddlistCfgFile_event_cb, lv.EVENT.READY, None)

# create style style_scrprog_ddlistcfgfile_extra_list_scrollbar_default
style_scrprog_ddlistcfgfile_extra_list_scrollbar_default = lv.style_t()
style_scrprog_ddlistcfgfile_extra_list_scrollbar_default.init()
style_scrprog_ddlistcfgfile_extra_list_scrollbar_default.set_radius(3)
style_scrprog_ddlistcfgfile_extra_list_scrollbar_default.set_bg_color(lv.color_make(0x00,0xff,0x00))
style_scrprog_ddlistcfgfile_extra_list_scrollbar_default.set_bg_grad_color(lv.color_make(0xff,0xff,0xff))
style_scrprog_ddlistcfgfile_extra_list_scrollbar_default.set_bg_grad_dir(lv.GRAD_DIR.VER)
style_scrprog_ddlistcfgfile_extra_list_scrollbar_default.set_bg_opa(255)

def scrProg_ddlistCfgFile_event_cb(e):
    scrProg_ddlistCfgFile.get_list().add_style(style_scrprog_ddlistcfgfile_extra_list_scrollbar_default, lv.PART.SCROLLBAR|lv.STATE.DEFAULT)

scrProg_ddlistCfgFile.add_event_cb(scrProg_ddlistCfgFile_event_cb, lv.EVENT.READY, None)

# create style style_scrprog_ddlistcfgfile_main_main_default
style_scrprog_ddlistcfgfile_main_main_default = lv.style_t()
style_scrprog_ddlistcfgfile_main_main_default.init()
style_scrprog_ddlistcfgfile_main_main_default.set_radius(3)
style_scrprog_ddlistcfgfile_main_main_default.set_bg_color(lv.color_make(0xff,0xff,0xff))
style_scrprog_ddlistcfgfile_main_main_default.set_bg_grad_color(lv.color_make(0xff,0xff,0xff))
style_scrprog_ddlistcfgfile_main_main_default.set_bg_grad_dir(lv.GRAD_DIR.VER)
style_scrprog_ddlistcfgfile_main_main_default.set_bg_opa(255)
style_scrprog_ddlistcfgfile_main_main_default.set_border_color(lv.color_make(0xff,0xff,0xff))
style_scrprog_ddlistcfgfile_main_main_default.set_border_width(2)
style_scrprog_ddlistcfgfile_main_main_default.set_text_color(lv.color_make(0x00,0x00,0x00))
try:
    style_scrprog_ddlistcfgfile_main_main_default.set_text_font(lv.font_FiraCode_Retina_14)
except AttributeError:
    try:
        style_scrprog_ddlistcfgfile_main_main_default.set_text_font(lv.font_montserrat_14)
    except AttributeError:
        style_scrprog_ddlistcfgfile_main_main_default.set_text_font(lv.font_montserrat_16)
style_scrprog_ddlistcfgfile_main_main_default.set_text_line_space(20)

# add style for scrProg_ddlistCfgFile
scrProg_ddlistCfgFile.add_style(style_scrprog_ddlistcfgfile_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

scrProg_ddlistMtpFile = lv.dropdown(scrProg)
scrProg_ddlistMtpFile.set_pos(55,10)
scrProg_ddlistMtpFile.set_width(175)
scrProg_ddlistMtpFile.set_options("NULL")
# create style style_scrprog_ddlistmtpfile_extra_list_selected_default
style_scrprog_ddlistmtpfile_extra_list_selected_default = lv.style_t()
style_scrprog_ddlistmtpfile_extra_list_selected_default.init()
style_scrprog_ddlistmtpfile_extra_list_selected_default.set_radius(3)
style_scrprog_ddlistmtpfile_extra_list_selected_default.set_bg_color(lv.color_make(0x00,0xa1,0xb5))
style_scrprog_ddlistmtpfile_extra_list_selected_default.set_bg_grad_color(lv.color_make(0x00,0xa1,0xb5))
style_scrprog_ddlistmtpfile_extra_list_selected_default.set_bg_grad_dir(lv.GRAD_DIR.VER)
style_scrprog_ddlistmtpfile_extra_list_selected_default.set_bg_opa(255)
style_scrprog_ddlistmtpfile_extra_list_selected_default.set_border_color(lv.color_make(0xe1,0xe6,0xee))
style_scrprog_ddlistmtpfile_extra_list_selected_default.set_border_width(1)
style_scrprog_ddlistmtpfile_extra_list_selected_default.set_text_color(lv.color_make(0xff,0xff,0xff))
try:
    style_scrprog_ddlistmtpfile_extra_list_selected_default.set_text_font(lv.font_simsun_12)
except AttributeError:
    try:
        style_scrprog_ddlistmtpfile_extra_list_selected_default.set_text_font(lv.font_montserrat_12)
    except AttributeError:
        style_scrprog_ddlistmtpfile_extra_list_selected_default.set_text_font(lv.font_montserrat_16)

def scrProg_ddlistMtpFile_event_cb(e):
    scrProg_ddlistMtpFile.get_list().add_style(style_scrprog_ddlistmtpfile_extra_list_selected_default, lv.PART.SELECTED|lv.STATE.DEFAULT)

scrProg_ddlistMtpFile.add_event_cb(scrProg_ddlistMtpFile_event_cb, lv.EVENT.READY, None)

# create style style_scrprog_ddlistmtpfile_extra_list_main_default
style_scrprog_ddlistmtpfile_extra_list_main_default = lv.style_t()
style_scrprog_ddlistmtpfile_extra_list_main_default.init()
style_scrprog_ddlistmtpfile_extra_list_main_default.set_radius(3)
style_scrprog_ddlistmtpfile_extra_list_main_default.set_bg_color(lv.color_make(0xff,0xff,0xff))
style_scrprog_ddlistmtpfile_extra_list_main_default.set_bg_grad_color(lv.color_make(0xff,0xff,0xff))
style_scrprog_ddlistmtpfile_extra_list_main_default.set_bg_grad_dir(lv.GRAD_DIR.VER)
style_scrprog_ddlistmtpfile_extra_list_main_default.set_bg_opa(255)
style_scrprog_ddlistmtpfile_extra_list_main_default.set_border_color(lv.color_make(0xe1,0xe6,0xee))
style_scrprog_ddlistmtpfile_extra_list_main_default.set_border_width(1)
style_scrprog_ddlistmtpfile_extra_list_main_default.set_text_color(lv.color_make(0x0D,0x30,0x55))
try:
    style_scrprog_ddlistmtpfile_extra_list_main_default.set_text_font(lv.font_simsun_12)
except AttributeError:
    try:
        style_scrprog_ddlistmtpfile_extra_list_main_default.set_text_font(lv.font_montserrat_12)
    except AttributeError:
        style_scrprog_ddlistmtpfile_extra_list_main_default.set_text_font(lv.font_montserrat_16)
style_scrprog_ddlistmtpfile_extra_list_main_default.set_max_height(90)

def scrProg_ddlistMtpFile_event_cb(e):
    scrProg_ddlistMtpFile.get_list().add_style(style_scrprog_ddlistmtpfile_extra_list_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

scrProg_ddlistMtpFile.add_event_cb(scrProg_ddlistMtpFile_event_cb, lv.EVENT.READY, None)

# create style style_scrprog_ddlistmtpfile_extra_list_scrollbar_default
style_scrprog_ddlistmtpfile_extra_list_scrollbar_default = lv.style_t()
style_scrprog_ddlistmtpfile_extra_list_scrollbar_default.init()
style_scrprog_ddlistmtpfile_extra_list_scrollbar_default.set_radius(3)
style_scrprog_ddlistmtpfile_extra_list_scrollbar_default.set_bg_color(lv.color_make(0x00,0xff,0x00))
style_scrprog_ddlistmtpfile_extra_list_scrollbar_default.set_bg_grad_color(lv.color_make(0xff,0xff,0xff))
style_scrprog_ddlistmtpfile_extra_list_scrollbar_default.set_bg_grad_dir(lv.GRAD_DIR.VER)
style_scrprog_ddlistmtpfile_extra_list_scrollbar_default.set_bg_opa(255)

def scrProg_ddlistMtpFile_event_cb(e):
    scrProg_ddlistMtpFile.get_list().add_style(style_scrprog_ddlistmtpfile_extra_list_scrollbar_default, lv.PART.SCROLLBAR|lv.STATE.DEFAULT)

scrProg_ddlistMtpFile.add_event_cb(scrProg_ddlistMtpFile_event_cb, lv.EVENT.READY, None)

# create style style_scrprog_ddlistmtpfile_main_main_default
style_scrprog_ddlistmtpfile_main_main_default = lv.style_t()
style_scrprog_ddlistmtpfile_main_main_default.init()
style_scrprog_ddlistmtpfile_main_main_default.set_radius(3)
style_scrprog_ddlistmtpfile_main_main_default.set_bg_color(lv.color_make(0xff,0xff,0xff))
style_scrprog_ddlistmtpfile_main_main_default.set_bg_grad_color(lv.color_make(0xff,0xff,0xff))
style_scrprog_ddlistmtpfile_main_main_default.set_bg_grad_dir(lv.GRAD_DIR.VER)
style_scrprog_ddlistmtpfile_main_main_default.set_bg_opa(255)
style_scrprog_ddlistmtpfile_main_main_default.set_border_color(lv.color_make(0xff,0xff,0xff))
style_scrprog_ddlistmtpfile_main_main_default.set_border_width(2)
style_scrprog_ddlistmtpfile_main_main_default.set_text_color(lv.color_make(0x00,0x00,0x00))
try:
    style_scrprog_ddlistmtpfile_main_main_default.set_text_font(lv.font_FiraCode_Retina_14)
except AttributeError:
    try:
        style_scrprog_ddlistmtpfile_main_main_default.set_text_font(lv.font_montserrat_14)
    except AttributeError:
        style_scrprog_ddlistmtpfile_main_main_default.set_text_font(lv.font_montserrat_16)
style_scrprog_ddlistmtpfile_main_main_default.set_text_line_space(20)

# add style for scrProg_ddlistMtpFile
scrProg_ddlistMtpFile.add_style(style_scrprog_ddlistmtpfile_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

scrPowerMeter = lv.obj()
# create style style_scrpowermeter_main_main_default
style_scrpowermeter_main_main_default = lv.style_t()
style_scrpowermeter_main_main_default.init()
style_scrpowermeter_main_main_default.set_bg_color(lv.color_make(0x00,0x00,0x00))
style_scrpowermeter_main_main_default.set_bg_opa(255)

# add style for scrPowerMeter
scrPowerMeter.add_style(style_scrpowermeter_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

scrPowerMeter_labelVolVal = lv.label(scrPowerMeter)
scrPowerMeter_labelVolVal.set_pos(70,165)
scrPowerMeter_labelVolVal.set_size(120,32)
scrPowerMeter_labelVolVal.set_text("0.0000")
scrPowerMeter_labelVolVal.set_long_mode(lv.label.LONG.CLIP)
scrPowerMeter_labelVolVal.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
# create style style_scrpowermeter_labelvolval_main_main_default
style_scrpowermeter_labelvolval_main_main_default = lv.style_t()
style_scrpowermeter_labelvolval_main_main_default.init()
style_scrpowermeter_labelvolval_main_main_default.set_radius(0)
style_scrpowermeter_labelvolval_main_main_default.set_bg_color(lv.color_make(0x21,0x95,0xf6))
style_scrpowermeter_labelvolval_main_main_default.set_bg_grad_color(lv.color_make(0x21,0x95,0xf6))
style_scrpowermeter_labelvolval_main_main_default.set_bg_grad_dir(lv.GRAD_DIR.VER)
style_scrpowermeter_labelvolval_main_main_default.set_bg_opa(0)
style_scrpowermeter_labelvolval_main_main_default.set_text_color(lv.color_make(0x00,0x7f,0xff))
try:
    style_scrpowermeter_labelvolval_main_main_default.set_text_font(lv.font_FiraCode_Retina_32)
except AttributeError:
    try:
        style_scrpowermeter_labelvolval_main_main_default.set_text_font(lv.font_montserrat_32)
    except AttributeError:
        style_scrpowermeter_labelvolval_main_main_default.set_text_font(lv.font_montserrat_16)
style_scrpowermeter_labelvolval_main_main_default.set_text_letter_space(0)
style_scrpowermeter_labelvolval_main_main_default.set_pad_left(0)
style_scrpowermeter_labelvolval_main_main_default.set_pad_right(0)
style_scrpowermeter_labelvolval_main_main_default.set_pad_top(0)
style_scrpowermeter_labelvolval_main_main_default.set_pad_bottom(0)

# add style for scrPowerMeter_labelVolVal
scrPowerMeter_labelVolVal.add_style(style_scrpowermeter_labelvolval_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

scrPowerMeter_labelCurVal = lv.label(scrPowerMeter)
scrPowerMeter_labelCurVal.set_pos(70,210)
scrPowerMeter_labelCurVal.set_size(120,32)
scrPowerMeter_labelCurVal.set_text("0.0000")
scrPowerMeter_labelCurVal.set_long_mode(lv.label.LONG.CLIP)
scrPowerMeter_labelCurVal.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
# create style style_scrpowermeter_labelcurval_main_main_default
style_scrpowermeter_labelcurval_main_main_default = lv.style_t()
style_scrpowermeter_labelcurval_main_main_default.init()
style_scrpowermeter_labelcurval_main_main_default.set_radius(0)
style_scrpowermeter_labelcurval_main_main_default.set_bg_color(lv.color_make(0x21,0x95,0xf6))
style_scrpowermeter_labelcurval_main_main_default.set_bg_grad_color(lv.color_make(0x21,0x95,0xf6))
style_scrpowermeter_labelcurval_main_main_default.set_bg_grad_dir(lv.GRAD_DIR.VER)
style_scrpowermeter_labelcurval_main_main_default.set_bg_opa(0)
style_scrpowermeter_labelcurval_main_main_default.set_text_color(lv.color_make(0xff,0x00,0x00))
try:
    style_scrpowermeter_labelcurval_main_main_default.set_text_font(lv.font_FiraCode_Retina_32)
except AttributeError:
    try:
        style_scrpowermeter_labelcurval_main_main_default.set_text_font(lv.font_montserrat_32)
    except AttributeError:
        style_scrpowermeter_labelcurval_main_main_default.set_text_font(lv.font_montserrat_16)
style_scrpowermeter_labelcurval_main_main_default.set_text_letter_space(0)
style_scrpowermeter_labelcurval_main_main_default.set_pad_left(0)
style_scrpowermeter_labelcurval_main_main_default.set_pad_right(0)
style_scrpowermeter_labelcurval_main_main_default.set_pad_top(0)
style_scrpowermeter_labelcurval_main_main_default.set_pad_bottom(0)

# add style for scrPowerMeter_labelCurVal
scrPowerMeter_labelCurVal.add_style(style_scrpowermeter_labelcurval_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

scrPowerMeter_labelPwrVal = lv.label(scrPowerMeter)
scrPowerMeter_labelPwrVal.set_pos(70,255)
scrPowerMeter_labelPwrVal.set_size(120,32)
scrPowerMeter_labelPwrVal.set_text("0.0000")
scrPowerMeter_labelPwrVal.set_long_mode(lv.label.LONG.CLIP)
scrPowerMeter_labelPwrVal.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
# create style style_scrpowermeter_labelpwrval_main_main_default
style_scrpowermeter_labelpwrval_main_main_default = lv.style_t()
style_scrpowermeter_labelpwrval_main_main_default.init()
style_scrpowermeter_labelpwrval_main_main_default.set_radius(0)
style_scrpowermeter_labelpwrval_main_main_default.set_bg_color(lv.color_make(0x21,0x95,0xf6))
style_scrpowermeter_labelpwrval_main_main_default.set_bg_grad_color(lv.color_make(0x21,0x95,0xf6))
style_scrpowermeter_labelpwrval_main_main_default.set_bg_grad_dir(lv.GRAD_DIR.VER)
style_scrpowermeter_labelpwrval_main_main_default.set_bg_opa(0)
style_scrpowermeter_labelpwrval_main_main_default.set_text_color(lv.color_make(0xff,0x7f,0x00))
try:
    style_scrpowermeter_labelpwrval_main_main_default.set_text_font(lv.font_FiraCode_Retina_32)
except AttributeError:
    try:
        style_scrpowermeter_labelpwrval_main_main_default.set_text_font(lv.font_montserrat_32)
    except AttributeError:
        style_scrpowermeter_labelpwrval_main_main_default.set_text_font(lv.font_montserrat_16)
style_scrpowermeter_labelpwrval_main_main_default.set_text_letter_space(0)
style_scrpowermeter_labelpwrval_main_main_default.set_pad_left(0)
style_scrpowermeter_labelpwrval_main_main_default.set_pad_right(0)
style_scrpowermeter_labelpwrval_main_main_default.set_pad_top(0)
style_scrpowermeter_labelpwrval_main_main_default.set_pad_bottom(0)

# add style for scrPowerMeter_labelPwrVal
scrPowerMeter_labelPwrVal.add_style(style_scrpowermeter_labelpwrval_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

scrPowerMeter_labelVol = lv.label(scrPowerMeter)
scrPowerMeter_labelVol.set_pos(30,165)
scrPowerMeter_labelVol.set_size(40,32)
scrPowerMeter_labelVol.set_text("U:")
scrPowerMeter_labelVol.set_long_mode(lv.label.LONG.CLIP)
scrPowerMeter_labelVol.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
# create style style_scrpowermeter_labelvol_main_main_default
style_scrpowermeter_labelvol_main_main_default = lv.style_t()
style_scrpowermeter_labelvol_main_main_default.init()
style_scrpowermeter_labelvol_main_main_default.set_radius(0)
style_scrpowermeter_labelvol_main_main_default.set_bg_color(lv.color_make(0x21,0x95,0xf6))
style_scrpowermeter_labelvol_main_main_default.set_bg_grad_color(lv.color_make(0x21,0x95,0xf6))
style_scrpowermeter_labelvol_main_main_default.set_bg_grad_dir(lv.GRAD_DIR.VER)
style_scrpowermeter_labelvol_main_main_default.set_bg_opa(0)
style_scrpowermeter_labelvol_main_main_default.set_text_color(lv.color_make(0x00,0x7f,0xff))
try:
    style_scrpowermeter_labelvol_main_main_default.set_text_font(lv.font_FiraCode_Retina_32)
except AttributeError:
    try:
        style_scrpowermeter_labelvol_main_main_default.set_text_font(lv.font_montserrat_32)
    except AttributeError:
        style_scrpowermeter_labelvol_main_main_default.set_text_font(lv.font_montserrat_16)
style_scrpowermeter_labelvol_main_main_default.set_text_letter_space(0)
style_scrpowermeter_labelvol_main_main_default.set_pad_left(0)
style_scrpowermeter_labelvol_main_main_default.set_pad_right(0)
style_scrpowermeter_labelvol_main_main_default.set_pad_top(0)
style_scrpowermeter_labelvol_main_main_default.set_pad_bottom(0)

# add style for scrPowerMeter_labelVol
scrPowerMeter_labelVol.add_style(style_scrpowermeter_labelvol_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

scrPowerMeter_labelCur = lv.label(scrPowerMeter)
scrPowerMeter_labelCur.set_pos(30,210)
scrPowerMeter_labelCur.set_size(40,32)
scrPowerMeter_labelCur.set_text("I:")
scrPowerMeter_labelCur.set_long_mode(lv.label.LONG.CLIP)
scrPowerMeter_labelCur.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
# create style style_scrpowermeter_labelcur_main_main_default
style_scrpowermeter_labelcur_main_main_default = lv.style_t()
style_scrpowermeter_labelcur_main_main_default.init()
style_scrpowermeter_labelcur_main_main_default.set_radius(0)
style_scrpowermeter_labelcur_main_main_default.set_bg_color(lv.color_make(0x21,0x95,0xf6))
style_scrpowermeter_labelcur_main_main_default.set_bg_grad_color(lv.color_make(0x21,0x95,0xf6))
style_scrpowermeter_labelcur_main_main_default.set_bg_grad_dir(lv.GRAD_DIR.VER)
style_scrpowermeter_labelcur_main_main_default.set_bg_opa(0)
style_scrpowermeter_labelcur_main_main_default.set_text_color(lv.color_make(0xff,0x00,0x00))
try:
    style_scrpowermeter_labelcur_main_main_default.set_text_font(lv.font_FiraCode_Retina_32)
except AttributeError:
    try:
        style_scrpowermeter_labelcur_main_main_default.set_text_font(lv.font_montserrat_32)
    except AttributeError:
        style_scrpowermeter_labelcur_main_main_default.set_text_font(lv.font_montserrat_16)
style_scrpowermeter_labelcur_main_main_default.set_text_letter_space(0)
style_scrpowermeter_labelcur_main_main_default.set_pad_left(0)
style_scrpowermeter_labelcur_main_main_default.set_pad_right(0)
style_scrpowermeter_labelcur_main_main_default.set_pad_top(0)
style_scrpowermeter_labelcur_main_main_default.set_pad_bottom(0)

# add style for scrPowerMeter_labelCur
scrPowerMeter_labelCur.add_style(style_scrpowermeter_labelcur_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

scrPowerMeter_labelPwr = lv.label(scrPowerMeter)
scrPowerMeter_labelPwr.set_pos(30,255)
scrPowerMeter_labelPwr.set_size(40,32)
scrPowerMeter_labelPwr.set_text("P:")
scrPowerMeter_labelPwr.set_long_mode(lv.label.LONG.WRAP)
scrPowerMeter_labelPwr.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
# create style style_scrpowermeter_labelpwr_main_main_default
style_scrpowermeter_labelpwr_main_main_default = lv.style_t()
style_scrpowermeter_labelpwr_main_main_default.init()
style_scrpowermeter_labelpwr_main_main_default.set_radius(0)
style_scrpowermeter_labelpwr_main_main_default.set_bg_color(lv.color_make(0x21,0x95,0xf6))
style_scrpowermeter_labelpwr_main_main_default.set_bg_grad_color(lv.color_make(0x21,0x95,0xf6))
style_scrpowermeter_labelpwr_main_main_default.set_bg_grad_dir(lv.GRAD_DIR.VER)
style_scrpowermeter_labelpwr_main_main_default.set_bg_opa(0)
style_scrpowermeter_labelpwr_main_main_default.set_text_color(lv.color_make(0xff,0x7f,0x00))
try:
    style_scrpowermeter_labelpwr_main_main_default.set_text_font(lv.font_FiraCode_Retina_32)
except AttributeError:
    try:
        style_scrpowermeter_labelpwr_main_main_default.set_text_font(lv.font_montserrat_32)
    except AttributeError:
        style_scrpowermeter_labelpwr_main_main_default.set_text_font(lv.font_montserrat_16)
style_scrpowermeter_labelpwr_main_main_default.set_text_letter_space(0)
style_scrpowermeter_labelpwr_main_main_default.set_pad_left(0)
style_scrpowermeter_labelpwr_main_main_default.set_pad_right(0)
style_scrpowermeter_labelpwr_main_main_default.set_pad_top(0)
style_scrpowermeter_labelpwr_main_main_default.set_pad_bottom(0)

# add style for scrPowerMeter_labelPwr
scrPowerMeter_labelPwr.add_style(style_scrpowermeter_labelpwr_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

scrPowerMeter_labelVolUnit = lv.label(scrPowerMeter)
scrPowerMeter_labelVolUnit.set_pos(190,165)
scrPowerMeter_labelVolUnit.set_size(20,40)
scrPowerMeter_labelVolUnit.set_text("V")
scrPowerMeter_labelVolUnit.set_long_mode(lv.label.LONG.CLIP)
scrPowerMeter_labelVolUnit.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
# create style style_scrpowermeter_labelvolunit_main_main_default
style_scrpowermeter_labelvolunit_main_main_default = lv.style_t()
style_scrpowermeter_labelvolunit_main_main_default.init()
style_scrpowermeter_labelvolunit_main_main_default.set_radius(0)
style_scrpowermeter_labelvolunit_main_main_default.set_bg_color(lv.color_make(0x21,0x95,0xf6))
style_scrpowermeter_labelvolunit_main_main_default.set_bg_grad_color(lv.color_make(0x21,0x95,0xf6))
style_scrpowermeter_labelvolunit_main_main_default.set_bg_grad_dir(lv.GRAD_DIR.VER)
style_scrpowermeter_labelvolunit_main_main_default.set_bg_opa(0)
style_scrpowermeter_labelvolunit_main_main_default.set_text_color(lv.color_make(0x00,0x7f,0xff))
try:
    style_scrpowermeter_labelvolunit_main_main_default.set_text_font(lv.font_FiraCode_Retina_32)
except AttributeError:
    try:
        style_scrpowermeter_labelvolunit_main_main_default.set_text_font(lv.font_montserrat_32)
    except AttributeError:
        style_scrpowermeter_labelvolunit_main_main_default.set_text_font(lv.font_montserrat_16)
style_scrpowermeter_labelvolunit_main_main_default.set_text_letter_space(0)
style_scrpowermeter_labelvolunit_main_main_default.set_pad_left(0)
style_scrpowermeter_labelvolunit_main_main_default.set_pad_right(0)
style_scrpowermeter_labelvolunit_main_main_default.set_pad_top(0)
style_scrpowermeter_labelvolunit_main_main_default.set_pad_bottom(0)

# add style for scrPowerMeter_labelVolUnit
scrPowerMeter_labelVolUnit.add_style(style_scrpowermeter_labelvolunit_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

scrPowerMeter_labelCurUnit = lv.label(scrPowerMeter)
scrPowerMeter_labelCurUnit.set_pos(190,210)
scrPowerMeter_labelCurUnit.set_size(20,32)
scrPowerMeter_labelCurUnit.set_text("A")
scrPowerMeter_labelCurUnit.set_long_mode(lv.label.LONG.CLIP)
scrPowerMeter_labelCurUnit.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
# create style style_scrpowermeter_labelcurunit_main_main_default
style_scrpowermeter_labelcurunit_main_main_default = lv.style_t()
style_scrpowermeter_labelcurunit_main_main_default.init()
style_scrpowermeter_labelcurunit_main_main_default.set_radius(0)
style_scrpowermeter_labelcurunit_main_main_default.set_bg_color(lv.color_make(0x21,0x95,0xf6))
style_scrpowermeter_labelcurunit_main_main_default.set_bg_grad_color(lv.color_make(0x21,0x95,0xf6))
style_scrpowermeter_labelcurunit_main_main_default.set_bg_grad_dir(lv.GRAD_DIR.VER)
style_scrpowermeter_labelcurunit_main_main_default.set_bg_opa(0)
style_scrpowermeter_labelcurunit_main_main_default.set_text_color(lv.color_make(0xff,0x00,0x00))
try:
    style_scrpowermeter_labelcurunit_main_main_default.set_text_font(lv.font_FiraCode_Retina_32)
except AttributeError:
    try:
        style_scrpowermeter_labelcurunit_main_main_default.set_text_font(lv.font_montserrat_32)
    except AttributeError:
        style_scrpowermeter_labelcurunit_main_main_default.set_text_font(lv.font_montserrat_16)
style_scrpowermeter_labelcurunit_main_main_default.set_text_letter_space(0)
style_scrpowermeter_labelcurunit_main_main_default.set_pad_left(0)
style_scrpowermeter_labelcurunit_main_main_default.set_pad_right(0)
style_scrpowermeter_labelcurunit_main_main_default.set_pad_top(0)
style_scrpowermeter_labelcurunit_main_main_default.set_pad_bottom(0)

# add style for scrPowerMeter_labelCurUnit
scrPowerMeter_labelCurUnit.add_style(style_scrpowermeter_labelcurunit_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

scrPowerMeter_labelPwrUnit = lv.label(scrPowerMeter)
scrPowerMeter_labelPwrUnit.set_pos(190,255)
scrPowerMeter_labelPwrUnit.set_size(20,32)
scrPowerMeter_labelPwrUnit.set_text("W")
scrPowerMeter_labelPwrUnit.set_long_mode(lv.label.LONG.CLIP)
scrPowerMeter_labelPwrUnit.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
# create style style_scrpowermeter_labelpwrunit_main_main_default
style_scrpowermeter_labelpwrunit_main_main_default = lv.style_t()
style_scrpowermeter_labelpwrunit_main_main_default.init()
style_scrpowermeter_labelpwrunit_main_main_default.set_radius(0)
style_scrpowermeter_labelpwrunit_main_main_default.set_bg_color(lv.color_make(0x21,0x95,0xf6))
style_scrpowermeter_labelpwrunit_main_main_default.set_bg_grad_color(lv.color_make(0x21,0x95,0xf6))
style_scrpowermeter_labelpwrunit_main_main_default.set_bg_grad_dir(lv.GRAD_DIR.VER)
style_scrpowermeter_labelpwrunit_main_main_default.set_bg_opa(0)
style_scrpowermeter_labelpwrunit_main_main_default.set_text_color(lv.color_make(0xff,0x7f,0x00))
try:
    style_scrpowermeter_labelpwrunit_main_main_default.set_text_font(lv.font_FiraCode_Retina_32)
except AttributeError:
    try:
        style_scrpowermeter_labelpwrunit_main_main_default.set_text_font(lv.font_montserrat_32)
    except AttributeError:
        style_scrpowermeter_labelpwrunit_main_main_default.set_text_font(lv.font_montserrat_16)
style_scrpowermeter_labelpwrunit_main_main_default.set_text_letter_space(0)
style_scrpowermeter_labelpwrunit_main_main_default.set_pad_left(0)
style_scrpowermeter_labelpwrunit_main_main_default.set_pad_right(0)
style_scrpowermeter_labelpwrunit_main_main_default.set_pad_top(0)
style_scrpowermeter_labelpwrunit_main_main_default.set_pad_bottom(0)

# add style for scrPowerMeter_labelPwrUnit
scrPowerMeter_labelPwrUnit.add_style(style_scrpowermeter_labelpwrunit_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

scrPowerMeter_imgLogo = lv.img(scrPowerMeter)
scrPowerMeter_imgLogo.set_pos(0,35)
scrPowerMeter_imgLogo.set_size(240,112)
scrPowerMeter_imgLogo.add_flag(lv.obj.FLAG.CLICKABLE)
try:
    with open('D:\\SRC\\gui-guider\\lvgl_ui\\generated\\mp461442711.png','rb') as f:
        scrPowerMeter_imgLogo_img_data = f.read()
except:
    print('Could not open D:\\SRC\\gui-guider\\lvgl_ui\\generated\\mp461442711.png')
    sys.exit()

scrPowerMeter_imgLogo_img = lv.img_dsc_t({
  'data_size': len(scrPowerMeter_imgLogo_img_data),
  'header': {'always_zero': 0, 'w': 240, 'h': 112, 'cf': lv.img.CF.TRUE_COLOR_ALPHA},
  'data': scrPowerMeter_imgLogo_img_data
})

scrPowerMeter_imgLogo.set_src(scrPowerMeter_imgLogo_img)
scrPowerMeter_imgLogo.set_pivot(0,0)
scrPowerMeter_imgLogo.set_angle(0)
# create style style_scrpowermeter_imglogo_main_main_default
style_scrpowermeter_imglogo_main_main_default = lv.style_t()
style_scrpowermeter_imglogo_main_main_default.init()
style_scrpowermeter_imglogo_main_main_default.set_img_recolor(lv.color_make(0xff,0xff,0xff))
style_scrpowermeter_imglogo_main_main_default.set_img_recolor_opa(0)
style_scrpowermeter_imglogo_main_main_default.set_img_opa(255)

# add style for scrPowerMeter_imgLogo
scrPowerMeter_imgLogo.add_style(style_scrpowermeter_imglogo_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)




# content from custom.py

# Load the default screen
lv.scr_load(scrWelcome)

while SDL.check():
    time.sleep_ms(5)
