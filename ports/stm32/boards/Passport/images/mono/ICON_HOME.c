// SPDX-FileCopyrightText: © 2022 Foundation Devices, Inc. <hello@foundationdevices.com>
// SPDX-License-Identifier: GPL-3.0-or-later
//

#if defined(LV_LVGL_H_INCLUDE_SIMPLE)
#include "lvgl.h"
#else
#include "lvgl/lvgl.h"
#endif


#ifndef LV_ATTRIBUTE_MEM_ALIGN
#define LV_ATTRIBUTE_MEM_ALIGN
#endif

#ifndef LV_ATTRIBUTE_IMG_ICON_HOME
#define LV_ATTRIBUTE_IMG_ICON_HOME
#endif

const LV_ATTRIBUTE_MEM_ALIGN LV_ATTRIBUTE_LARGE_CONST LV_ATTRIBUTE_IMG_ICON_HOME uint8_t ICON_HOME_map[] = {
  0x00, 0x00, 0x00, 0x00, 	/*Color of index 0*/
  0xfe, 0xfe, 0xfe, 0xa4, 	/*Color of index 1*/

  0x00, 0x00, 0x00, 
  0x00, 0xf0, 0x00, 
  0x01, 0xf8, 0x00, 
  0x03, 0xfc, 0x00, 
  0x0f, 0x9f, 0x00, 
  0x1e, 0x07, 0x80, 
  0x3c, 0x03, 0xc0, 
  0x38, 0x01, 0xc0, 
  0x30, 0x00, 0xc0, 
  0x33, 0xfc, 0xc0, 
  0x33, 0xfc, 0xc0, 
  0x33, 0x9c, 0xc0, 
  0x33, 0x9c, 0xc0, 
  0x33, 0x9c, 0xc0, 
  0x33, 0x9c, 0xc0, 
  0x33, 0x9c, 0xc0, 
  0x33, 0x9c, 0xc0, 
  0x3f, 0xff, 0xc0, 
  0x3f, 0xff, 0xc0, 
  0x00, 0x00, 0x00, 
};

const lv_img_dsc_t ICON_HOME = {
  .header.cf = LV_IMG_CF_INDEXED_1BIT,
  .header.always_zero = 0,
  .header.reserved = 0,
  .header.w = 20,
  .header.h = 20,
  .data_size = 68,
  .data = ICON_HOME_map,
};
