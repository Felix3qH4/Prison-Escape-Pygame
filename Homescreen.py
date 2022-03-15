#!/usr/bin/env python3

"""
    Felix Michelis
      07/04/2021
      dd/mm/yyyy
"""

import pygame as pg 
import os
from system_infos import get_screen_size


## Center the window on the screen
os.environ['SDL_VIDEO_CENTERED'] = '1'

homescreenrun = True

## Define window size
#DISPLAY_W = 1024
#DISPLAY_H = 832
DISPLAY_W, DISPLAY_H = get_screen_size()

bg_color = (27, 25, 46)

## Initialize pygame
pg.init()

## Create a new window and change its Title
Homescreen = pg.display.set_mode((DISPLAY_W, DISPLAY_H))
pg.display.set_caption("Prison Escape - Homescreen")

Homescreen.fill(pg.Color('black'))

title_text_font = pg.font.Font('Fonts/Kristen ITC.ttf', 96)
text_text_font = pg.font.SysFont('Fonts/Ink Free.ttf', 50)

def bg():
	bg_img = pg.transform.scale(pg.image.load("Images/Logo_empty.png"), (DISPLAY_W, DISPLAY_H))
	bg_rect = bg_img.get_rect()
	Homescreen.blit(bg_img, bg_rect)
	pg.display.update()

def show_text():
	title_text_surface = title_text_font.render("Prison Escape", True, pg.Color('royalblue1'))
	title_text_rect = title_text_surface.get_rect()
	title_text_rect.center = (int(DISPLAY_W/2), int(DISPLAY_H/14))

	start_text_surface = text_text_font.render("START", True, pg.Color('blue'))
	start_text_rect = start_text_surface.get_rect()
	start_text_rect.center = (int(DISPLAY_W / 4.654), int(DISPLAY_H / 3.8697674418604))

	load_text_surface = text_text_font.render("LOAD", True, pg.Color('blue'))
	load_text_rect = load_text_surface.get_rect()
	load_text_rect.center = (int(DISPLAY_W / 10.24), int(DISPLAY_H / 1.4596491228070))

	shop_text_surface = text_text_font.render("SHOP", True, pg.Color('blue'))
	shop_text_rect = shop_text_surface.get_rect()
	shop_text_rect.center = (int(DISPLAY_W / 3.0117647058823), int(DISPLAY_H / 1.459649122807))

	Homescreen.blit(title_text_surface, title_text_rect)
	pg.draw.rect(Homescreen, pg.Color('dodgerblue'), (int(DISPLAY_W / 6.4), int(DISPLAY_H / 6.93), int(DISPLAY_W / 1.46285714), int(DISPLAY_H / 83.2)))
	Homescreen.blit(start_text_surface, start_text_rect)
	Homescreen.blit(load_text_surface, load_text_rect)
	Homescreen.blit(shop_text_surface, shop_text_rect)
	pg.display.update()

def open_door(which):
	Homescreen.blit(door_img1, which)
	show_text()
	pg.display.update()
	pg.time.wait(100)
	Homescreen.blit(door_img2, which)
	show_text()
	pg.display.update()
	pg.time.wait(100)
	Homescreen.blit(door_img3, which)
	show_text()
	pg.display.update()
	pg.time.wait(100)
	Homescreen.blit(door_img4, which)
	show_text()
	pg.display.update()
	pg.time.wait(100)

	Homescreen.fill(pg.Color('black'))
	bg()
	
	Homescreen.blit(settings_img0, settings_rect)
	Homescreen.blit(door_img0, start_rect)
	Homescreen.blit(door_img0, load_rect)
	Homescreen.blit(door_img0, shop_rect)
	show_text()
	pg.display.update()

def rotate_settings():
	rotateby = 20
	for i in range(7):
		pg.draw.rect(Homescreen, bg_color, (int(DISPLAY_W / 1.06), 0, int(DISPLAY_W / 17.06), int(DISPLAY_W / 17.6)))
		pg.display.update()
		rotated_img = pg.transform.rotate(settings_img0, -rotateby)
		new_rect = rotated_img.get_rect(center = settings_rect.center)
		Homescreen.blit(rotated_img, new_rect)
		pg.display.update()
		pg.time.wait(100)

		rotateby += 20




door_img0 = pg.transform.scale(pg.image.load("Images/Homescreen/door_0.png"), (int(DISPLAY_W / 5.12), int(DISPLAY_H / 2.773)))
door_img1 = pg.transform.scale(pg.image.load("Images/Homescreen/door_1.png"), (int(DISPLAY_W / 5.12), int(DISPLAY_H / 2.773)))
door_img2 = pg.transform.scale(pg.image.load("Images/Homescreen/door_2.png"), (int(DISPLAY_W / 5.12), int(DISPLAY_H / 2.773)))
door_img3 = pg.transform.scale(pg.image.load("Images/Homescreen/door_3.png"), (int(DISPLAY_W / 5.12), int(DISPLAY_H / 2.773)))
door_img4 = pg.transform.scale(pg.image.load("Images/Homescreen/door_4.png"), (int(DISPLAY_W / 5.12), int(DISPLAY_H / 2.773)))

start_rect = door_img0.get_rect()
start_rect.center = (int(DISPLAY_W / 4.654), int(DISPLAY_H / 2.521))
load_rect = door_img0.get_rect()
load_rect.center = (int(DISPLAY_W / 10.24), int(DISPLAY_H / 1.214598540))
shop_rect = door_img0.get_rect()
shop_rect.center = (int(DISPLAY_W / 3.0117647058823), int(DISPLAY_H / 1.214598540))

settings_img0 = pg.transform.scale(pg.image.load("Images/Homescreen/settings_0.png"), (int(DISPLAY_W / 20.48), int(DISPLAY_W / 20.48)))
settings_rect = settings_img0.get_rect()
settings_rect.center = (int(DISPLAY_W / 1.034), int(DISPLAY_W / 27.73))

bg()
Homescreen.blit(door_img0, start_rect)
Homescreen.blit(door_img0, load_rect)
Homescreen.blit(door_img0, shop_rect)
Homescreen.blit(settings_img0, settings_rect)
show_text()
pg.display.update()

start_timer = pg.time.get_ticks()
load_timer = pg.time.get_ticks()
shop_timer = pg.time.get_ticks()
settings_timer = pg.time.get_ticks()

while homescreenrun == True:
	mouse_pos = pg.mouse.get_pos()
	show_text()

	if start_rect.collidepoint(mouse_pos):
		if ((pg.time.get_ticks() - start_timer)/1000) > 2:
			open_door(start_rect)
			start_timer = pg.time.get_ticks()
		else:
			pass
	if load_rect.collidepoint(mouse_pos):
		if ((pg.time.get_ticks() - load_timer)/1000) > 2:
			open_door(load_rect)
			load_timer = pg.time.get_ticks()
		else:
			pass
	if shop_rect.collidepoint(mouse_pos):
		if ((pg.time.get_ticks() - shop_timer)/1000) > 2:
			open_door(shop_rect)
			shop_timer = pg.time.get_ticks()
		else:
			pass
	if settings_rect.collidepoint(mouse_pos):
		if ((pg.time.get_ticks() - settings_timer)/1000) > 2:
			rotate_settings()
			settings_timer = pg.time.get_ticks()
		else:
			pass


	for event in pg.event.get():
		if event.type == pg.QUIT:
			pg.quit()
			homescreenrun = False
		if event.type == pg.MOUSEBUTTONDOWN:
			if start_rect.collidepoint(mouse_pos):
				pg.quit()
				os.system("python Main.py")
				homescreenrun = False
			if load_rect.collidepoint(mouse_pos):
				print("[HOMESCREEN][BUTTON]: LOAD")
			if shop_rect.collidepoint(mouse_pos):
				pg.quit()
				os.system("python Shop.py")
				homescreenrun = False

			if settings_rect.collidepoint(mouse_pos):
				print("[HOMESCREEN][BUTTON]: SETTINGS")

pg.quit()
