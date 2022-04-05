/*
 * Copyright 2022 NXP
 * SPDX-License-Identifier: MIT
 */

#ifndef GUI_GUIDER_H
#define GUI_GUIDER_H
#ifdef __cplusplus
extern "C" {
#endif

#include "lvgl/lvgl.h"
#include "guider_fonts.h"

typedef struct
{
	lv_obj_t *scrPowerMeter;
	lv_obj_t *scrPowerMeter_labelVolVal;
	lv_obj_t *scrPowerMeter_labelCurVal;
	lv_obj_t *scrPowerMeter_labelPwrVal;
	lv_obj_t *scrPowerMeter_labelVol;
	lv_obj_t *scrPowerMeter_labelCur;
	lv_obj_t *scrPowerMeter_labelPwr;
	lv_obj_t *scrPowerMeter_labelVolUnit;
	lv_obj_t *scrPowerMeter_labelCurUnit;
	lv_obj_t *scrPowerMeter_labelPwrUnit;
	lv_obj_t *scrPowerMeter_imgLogo;
	lv_obj_t *scrProg;
	lv_obj_t *scrProg_imgLogo;
	lv_obj_t *scrProg_labelTitle;
}lv_ui;

void setup_ui(lv_ui *ui);
extern lv_ui guider_ui;
void setup_scr_scrPowerMeter(lv_ui *ui);
void setup_scr_scrProg(lv_ui *ui);
LV_IMG_DECLARE(_nvt_240x112);

#ifdef __cplusplus
}
#endif
#endif