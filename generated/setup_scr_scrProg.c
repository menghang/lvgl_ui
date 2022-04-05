/*
 * Copyright 2022 NXP
 * SPDX-License-Identifier: MIT
 */

#include "lvgl/lvgl.h"
#include <stdio.h>
#include "gui_guider.h"
#include "events_init.h"
#include "custom.h"


void setup_scr_scrProg(lv_ui *ui){

	//Write codes scrProg
	ui->scrProg = lv_obj_create(NULL);

	//Write style state: LV_STATE_DEFAULT for style_scrprog_main_main_default
	static lv_style_t style_scrprog_main_main_default;
	lv_style_reset(&style_scrprog_main_main_default);
	lv_style_set_bg_color(&style_scrprog_main_main_default, lv_color_make(0x00, 0x00, 0x00));
	lv_style_set_bg_opa(&style_scrprog_main_main_default, 255);
	lv_obj_add_style(ui->scrProg, &style_scrprog_main_main_default, LV_PART_MAIN|LV_STATE_DEFAULT);

	//Write codes scrProg_imgLogo
	ui->scrProg_imgLogo = lv_img_create(ui->scrProg);
	lv_obj_set_pos(ui->scrProg_imgLogo, 0, 66);
	lv_obj_set_size(ui->scrProg_imgLogo, 240, 112);

	//Write style state: LV_STATE_DEFAULT for style_scrprog_imglogo_main_main_default
	static lv_style_t style_scrprog_imglogo_main_main_default;
	lv_style_reset(&style_scrprog_imglogo_main_main_default);
	lv_style_set_img_recolor(&style_scrprog_imglogo_main_main_default, lv_color_make(0xff, 0xff, 0xff));
	lv_style_set_img_recolor_opa(&style_scrprog_imglogo_main_main_default, 0);
	lv_style_set_img_opa(&style_scrprog_imglogo_main_main_default, 255);
	lv_obj_add_style(ui->scrProg_imgLogo, &style_scrprog_imglogo_main_main_default, LV_PART_MAIN|LV_STATE_DEFAULT);
	lv_obj_add_flag(ui->scrProg_imgLogo, LV_OBJ_FLAG_CLICKABLE);
	lv_img_set_src(ui->scrProg_imgLogo,&_nvt_240x112);
	lv_img_set_pivot(ui->scrProg_imgLogo, 0,0);
	lv_img_set_angle(ui->scrProg_imgLogo, 0);

	//Write codes scrProg_labelTitle
	ui->scrProg_labelTitle = lv_label_create(ui->scrProg);
	lv_obj_set_pos(ui->scrProg_labelTitle, 0, 200);
	lv_obj_set_size(ui->scrProg_labelTitle, 240, 16);
	lv_label_set_text(ui->scrProg_labelTitle, "Designed by Hang MENG");
	lv_label_set_long_mode(ui->scrProg_labelTitle, LV_LABEL_LONG_CLIP);
	lv_obj_set_style_text_align(ui->scrProg_labelTitle, LV_TEXT_ALIGN_CENTER, 0);

	//Write style state: LV_STATE_DEFAULT for style_scrprog_labeltitle_main_main_default
	static lv_style_t style_scrprog_labeltitle_main_main_default;
	lv_style_reset(&style_scrprog_labeltitle_main_main_default);
	lv_style_set_radius(&style_scrprog_labeltitle_main_main_default, 0);
	lv_style_set_bg_color(&style_scrprog_labeltitle_main_main_default, lv_color_make(0x21, 0x95, 0xf6));
	lv_style_set_bg_grad_color(&style_scrprog_labeltitle_main_main_default, lv_color_make(0x21, 0x95, 0xf6));
	lv_style_set_bg_grad_dir(&style_scrprog_labeltitle_main_main_default, LV_GRAD_DIR_VER);
	lv_style_set_bg_opa(&style_scrprog_labeltitle_main_main_default, 0);
	lv_style_set_text_color(&style_scrprog_labeltitle_main_main_default, lv_color_make(0xff, 0xff, 0xff));
	lv_style_set_text_font(&style_scrprog_labeltitle_main_main_default, &lv_font_MONACO_12);
	lv_style_set_text_letter_space(&style_scrprog_labeltitle_main_main_default, 0);
	lv_style_set_pad_left(&style_scrprog_labeltitle_main_main_default, 0);
	lv_style_set_pad_right(&style_scrprog_labeltitle_main_main_default, 0);
	lv_style_set_pad_top(&style_scrprog_labeltitle_main_main_default, 0);
	lv_style_set_pad_bottom(&style_scrprog_labeltitle_main_main_default, 0);
	lv_obj_add_style(ui->scrProg_labelTitle, &style_scrprog_labeltitle_main_main_default, LV_PART_MAIN|LV_STATE_DEFAULT);
}