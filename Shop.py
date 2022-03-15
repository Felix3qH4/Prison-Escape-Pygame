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

## If this is set to True, script can run
shoprun = True

## To now which image of which player has to be displayed we count +1 always when the user clicks on arrow_right'number'
player1_image = 0
player2_image = 0
player3_image = 0
player4_image = 0
player5_image = 0
player6_image = 0

## Set the color of the boxes to white so that when the player clicks on a box we can change the color
box1_color = "white"
box2_color = "white"
box3_color = "white"
box4_color = "white"
box5_color = "white"
box6_color = "white"

## Define window size
#DISPLAY_W = 1024
#DISPLAY_H = 832
DISPLAY_W, DISPLAY_H = get_screen_size()

## Initialize pygame
pg.init()

## Create a new window and change its Title
Shopscreen = pg.display.set_mode((DISPLAY_W, DISPLAY_H))
pg.display.set_caption("Prison Escape - Shop")

## Set a font for the title
title_text_font = pg.font.Font('Fonts/Kristen ITC.ttf', 96)

## To easily blit the title to the screen
def show_title():
	title_text_surface = title_text_font.render("Shop", True, pg.Color('royalblue1'))
	title_text_rect = title_text_surface.get_rect()
	title_text_rect.center = (int(DISPLAY_W/2), int(DISPLAY_H/14))

	Shopscreen.blit(title_text_surface, title_text_rect)
	## Underline the title
	pg.draw.rect(Shopscreen, pg.Color('dodgerblue'), (int(DISPLAY_W/2.84), int(DISPLAY_W/8.53), int(DISPLAY_W/3.413), int(DISPLAY_W/102.4)))	
	pg.display.update()

## The box'number' are rectangles that will create the effect of a box in which the characters are displayed
## We have to draw them once outside the function so that we can use the box.collidepoint(mouse_pos)
box1 = pg.draw.rect(Shopscreen, pg.Color(box1_color), (int(DISPLAY_W/6.826), int(DISPLAY_W/5.3894736842105), int(DISPLAY_W/5.12), int(DISPLAY_W/3.5310344827)), int(DISPLAY_W/204.8))
## The arrows point to the right side and are inside each box to turn around he displayed characters
arrow_right1 = pg.transform.scale(pg.image.load("Images/Shop/arrow_right.png"), (int(DISPLAY_W/34.13), int(DISPLAY_W/34.13)))
arrow_right1_rect = arrow_right1.get_rect(x = int(DISPLAY_W/3.3032258), y = int(DISPLAY_W/5.12))

box2 = pg.draw.rect(Shopscreen, pg.Color(box2_color), (int(DISPLAY_W/2.7675), int(DISPLAY_W/5.3894736842105), int(DISPLAY_W/5.12), int(DISPLAY_W/3.5310344837)), int(DISPLAY_W/204.8))
arrow_right2_rect = arrow_right1.get_rect(x = int(DISPLAY_W/1.9320754), y = int(DISPLAY_W/5.12))

box3 = pg.draw.rect(Shopscreen, pg.Color(box3_color), (int(DISPLAY_W/1.735593220), int(DISPLAY_W/5.3894736842105), int(DISPLAY_W/5.12), int(DISPLAY_W/3.5310344837)), int(DISPLAY_W/204.8))
arrow_right3_rect = arrow_right1.get_rect(x = int(DISPLAY_W/1.3653), y = int(DISPLAY_W/5.12))

box4 = pg.draw.rect(Shopscreen, pg.Color(box4_color), (int(DISPLAY_W/6.826), int(DISPLAY_W/2.048), int(DISPLAY_W/5.12), int(DISPLAY_W/3.510344837)), int(DISPLAY_W/204.8))
arrow_right4_rect = arrow_right1.get_rect(x = int(DISPLAY_W/3.3032258), y = int(DISPLAY_W/2.0078431))

box5 = pg.draw.rect(Shopscreen, pg.Color(box5_color), (int(DISPLAY_W/2.7675), int(DISPLAY_W/2.048), int(DISPLAY_W/5.12), int(DISPLAY_W/3.510344837)), int(DISPLAY_W/204.8))
arrow_right5_rect = arrow_right1.get_rect(x = int(DISPLAY_W/1.9320754), y = int(DISPLAY_W/2.0078431))

box6 = pg.draw.rect(Shopscreen, pg.Color(box6_color), (int(DISPLAY_W/1.735593220), int(DISPLAY_W/2.048), int(DISPLAY_W/5.12), int(DISPLAY_W/3.510344837)), int(DISPLAY_W/204.8))
arrow_right6_rect = arrow_right1.get_rect(x = int(DISPLAY_W/1.3653), y = int(DISPLAY_W/2.0078431))

def draw_boxes():
	## The box'number' are rectangles that will create the effect of a box in which the characters are displayed
	box1 = pg.draw.rect(Shopscreen, pg.Color(box1_color), (int(DISPLAY_W/6.826), int(DISPLAY_W/5.3894736842105), int(DISPLAY_W/5.12), int(DISPLAY_W/3.5310344837)), int(DISPLAY_W/204.8))
	## The arrows point to the right side and are inside each box to turn around he displayed characters
	arrow_right1 = pg.transform.scale(pg.image.load("Images/Shop/arrow_right.png"), (int(DISPLAY_W/34.13), int(DISPLAY_W/34.13)))
	arrow_right1_rect = arrow_right1.get_rect(x = int(DISPLAY_W/3.3032258), y = int(DISPLAY_W/5.12))

	box2 = pg.draw.rect(Shopscreen, pg.Color(box2_color), (int(DISPLAY_W/2.7675), int(DISPLAY_W/5.3894736842105), int(DISPLAY_W/5.12), int(DISPLAY_W/3.5310344837)), int(DISPLAY_W/204.8))
	arrow_right2_rect = arrow_right1.get_rect(x = int(DISPLAY_W/1.9320754), y = int(DISPLAY_W/5.12))

	box3 = pg.draw.rect(Shopscreen, pg.Color(box3_color), (int(DISPLAY_W/1.735593220), int(DISPLAY_W/5.3894736842105), int(DISPLAY_W/5.12), int(DISPLAY_W/3.5310344837)), int(DISPLAY_W/204.8))
	arrow_right3_rect = arrow_right1.get_rect(x = int(DISPLAY_W/1.3653), y = int(DISPLAY_W/5.12))

	box4 = pg.draw.rect(Shopscreen, pg.Color(box4_color), (int(DISPLAY_W/6.826), int(DISPLAY_W/2.048), int(DISPLAY_W/5.12), int(DISPLAY_W/3.510344837)), int(DISPLAY_W/204.8))
	arrow_right4_rect = arrow_right1.get_rect(x = int(DISPLAY_W/3.3032258), y = int(DISPLAY_W/2.0078431))

	box5 = pg.draw.rect(Shopscreen, pg.Color(box5_color), (int(DISPLAY_W/2.7675), int(DISPLAY_W/2.048), int(DISPLAY_W/5.12), int(DISPLAY_W/3.510344837)), int(DISPLAY_W/204.8))
	arrow_right5_rect = arrow_right1.get_rect(x = int(DISPLAY_W/1.9320754), y = int(DISPLAY_W/2.0078431))

	box6 = pg.draw.rect(Shopscreen, pg.Color(box6_color), (int(DISPLAY_W/1.735593220), int(DISPLAY_W/2.048), int(DISPLAY_W/5.12), int(DISPLAY_W/3.510344837)), int(DISPLAY_W/204.8))
	arrow_right6_rect = arrow_right1.get_rect(x = int(DISPLAY_W/1.3653), y = int(DISPLAY_W/2.0078431))

## The following and the above can be made cleaner but I am too lazy and there are similar parts which can also be done better
## Here we load the different perspectives of each character to later display them
player1_f_0 = pg.transform.scale(pg.image.load("Images/Players/original size/Player_1/player_f_0.png"), (int(DISPLAY_W/6.826), int(DISPLAY_W/4.26)))
player1_rect = player1_f_0.get_rect()
player1_r_0 = pg.transform.scale(pg.image.load("Images/Players/original size/Player_1/player_r_0.png"), (int(DISPLAY_W/6.826), int(DISPLAY_W/4.26)))
player1_b_0 = pg.transform.scale(pg.image.load("Images/Players/original size/Player_1/player_b_0.png"), (int(DISPLAY_W/6.826), int(DISPLAY_W/4.26)))
player1_l_0 = pg.transform.scale(pg.image.load("Images/Players/original size/Player_1/player_l_0.png"), (int(DISPLAY_W/6.826), int(DISPLAY_W/4.26)))
## We tell the images to take the center of the box as their own center; that way they are always centered
player1_rect.center = box1.center

player2_f_0 = pg.transform.scale(pg.image.load("Images/Players/original size/Player_2/player_f_0.png"), (int(DISPLAY_W/6.826), int(DISPLAY_W/4.26)))
player2_rect = player2_f_0.get_rect()
player2_r_0 = pg.transform.scale(pg.image.load("Images/Players/original size/Player_2/player_r_0.png"), (int(DISPLAY_W/6.826), int(DISPLAY_W/4.26)))
player2_b_0 = pg.transform.scale(pg.image.load("Images/Players/original size/Player_2/player_b_0.png"), (int(DISPLAY_W/6.826), int(DISPLAY_W/4.26)))
player2_l_0 = pg.transform.scale(pg.image.load("Images/Players/original size/Player_2/player_l_0.png"), (int(DISPLAY_W/6.826), int(DISPLAY_W/4.26)))
player2_rect.center = box2.center

player3_f_0 = pg.transform.scale(pg.image.load("Images/Players/original size/Player_3/player_f_0.png"), (int(DISPLAY_W/6.826), int(DISPLAY_W/4.26)))
player3_rect = player3_f_0.get_rect()
player3_r_0 = pg.transform.scale(pg.image.load("Images/Players/original size/Player_3/player_r_0.png"), (int(DISPLAY_W/6.826), int(DISPLAY_W/4.26)))
player3_b_0 = pg.transform.scale(pg.image.load("Images/Players/original size/Player_3/player_b_0.png"), (int(DISPLAY_W/6.826), int(DISPLAY_W/4.26)))
player3_l_0 = pg.transform.scale(pg.image.load("Images/Players/original size/Player_3/player_l_0.png"), (int(DISPLAY_W/6.826), int(DISPLAY_W/4.26)))
player3_rect.center = box3.center

player4_f_0 = pg.transform.scale(pg.image.load("Images/Players/original size/Player_4/player_f_0.png"), (int(DISPLAY_W/6.826), int(DISPLAY_W/4.26)))
player4_rect = player4_f_0.get_rect()
player4_r_0 = pg.transform.scale(pg.image.load("Images/Players/original size/Player_4/player_r_0.png"), (int(DISPLAY_W/6.826), int(DISPLAY_W/4.26)))
player4_b_0 = pg.transform.scale(pg.image.load("Images/Players/original size/Player_4/player_b_0.png"), (int(DISPLAY_W/6.826), int(DISPLAY_W/4.26)))
player4_l_0 = pg.transform.scale(pg.image.load("Images/Players/original size/Player_4/player_l_0.png"), (int(DISPLAY_W/6.826), int(DISPLAY_W/4.26)))
player4_rect.center = box4.center

player5_f_0 = pg.transform.scale(pg.image.load("Images/Players/original size/Player_5/player_f_0.png"), (int(DISPLAY_W/6.826), int(DISPLAY_W/4.26)))
player5_rect = player5_f_0.get_rect()
player5_r_0 = pg.transform.scale(pg.image.load("Images/Players/original size/Player_5/player_r_0.png"), (int(DISPLAY_W/6.826), int(DISPLAY_W/4.26)))
player5_b_0 = pg.transform.scale(pg.image.load("Images/Players/original size/Player_5/player_b_0.png"), (int(DISPLAY_W/6.826), int(DISPLAY_W/4.26)))
player5_l_0 = pg.transform.scale(pg.image.load("Images/Players/original size/Player_5/player_l_0.png"), (int(DISPLAY_W/6.826), int(DISPLAY_W/4.26)))
player5_rect.center = box5.center

player6_f_0 = pg.transform.scale(pg.image.load("Images/Players/original size/Player_6/player_f_0.png"), (int(DISPLAY_W/6.826), int(DISPLAY_W/4.26)))
player6_rect = player6_f_0.get_rect()
player6_r_0 = pg.transform.scale(pg.image.load("Images/Players/original size/Player_6/player_r_0.png"), (int(DISPLAY_W/6.826), int(DISPLAY_W/4.26)))
player6_b_0 = pg.transform.scale(pg.image.load("Images/Players/original size/Player_6/player_b_0.png"), (int(DISPLAY_W/6.826), int(DISPLAY_W/4.26)))
player6_l_0 = pg.transform.scale(pg.image.load("Images/Players/original size/Player_6/player_l_0.png"), (int(DISPLAY_W/6.826), int(DISPLAY_W/4.26)))
player6_rect.center = box6.center

## Always when the user clicks on an arrow to view a character from another perspective, we update the image
def player_1():
	global player1_image; global player2_image; global player3_image; global player4_image; global player5_image; global player6_image
	## First of all we draw a black rectangel on top of the old image in case that the new image is smaller
	erase1 = pg.draw.rect(Shopscreen, pg.Color('black'), (160, int(DISPLAY_W/5.12), int(DISPLAY_W/5.68), int(DISPLAY_W/3.7925)))
	erase2 = pg.draw.rect(Shopscreen, pg.Color('black'), (380, int(DISPLAY_W/5.12), int(DISPLAY_W/5.68), int(DISPLAY_W/3.7925)))
	erase3 = pg.draw.rect(Shopscreen, pg.Color('black'), (600, int(DISPLAY_W/5.12), int(DISPLAY_W/5.68), int(DISPLAY_W/3.7925)))
	erase4 = pg.draw.rect(Shopscreen, pg.Color('black'), (160, int(DISPLAY_W/2.0078431), int(DISPLAY_W/5.68), int(DISPLAY_W/3.7925)))
	erase5 = pg.draw.rect(Shopscreen, pg.Color('black'), (380, int(DISPLAY_W/2.0078431), int(DISPLAY_W/5.68), int(DISPLAY_W/3.7925)))
	erase6 = pg.draw.rect(Shopscreen, pg.Color('black'), (600, int(DISPLAY_W/2.0078431), int(DISPLAY_W/5.68), int(DISPLAY_W/3.7925)))

	## Here we check which of the 4 images has to be shown
	if player1_image > 3:
		player1_image = 0
	if player1_image == 0:
		Shopscreen.blit(player1_f_0, player1_rect)
	if player1_image == 1:
		Shopscreen.blit(player1_r_0, player1_rect)
	if player1_image == 2:
		Shopscreen.blit(player1_b_0, player1_rect)
	if player1_image == 3:
		Shopscreen.blit(player1_l_0, player1_rect)

	if player2_image > 3:
		player2_image = 0
	if player2_image == 0:
		Shopscreen.blit(player2_f_0, player2_rect)
	if player2_image == 1:
		Shopscreen.blit(player2_r_0, player2_rect)
	if player2_image == 2:
		Shopscreen.blit(player2_b_0, player2_rect)
	if player2_image == 3:
		Shopscreen.blit(player2_l_0, player2_rect)

	if player3_image > 3:
		player3_image = 0
	if player3_image == 0:
		Shopscreen.blit(player3_f_0, player3_rect)
	if player3_image == 1:
		Shopscreen.blit(player3_r_0, player3_rect)
	if player3_image == 2:
		Shopscreen.blit(player3_b_0, player3_rect)
	if player3_image == 3:
		Shopscreen.blit(player3_l_0, player3_rect)

	if player4_image > 3:
		player4_image = 0
	if player4_image == 0:
		Shopscreen.blit(player4_f_0, player4_rect)
	if player4_image == 1:
		Shopscreen.blit(player4_r_0, player4_rect)
	if player4_image == 2:
		Shopscreen.blit(player4_b_0, player4_rect)
	if player4_image == 3:
		Shopscreen.blit(player4_l_0, player4_rect)

	if player5_image > 3:
		player5_image = 0
	if player5_image == 0:
		Shopscreen.blit(player5_f_0, player5_rect)
	if player5_image == 1:
		Shopscreen.blit(player5_r_0, player5_rect)
	if player5_image == 2:
		Shopscreen.blit(player5_b_0, player5_rect)
	if player5_image == 3:
		Shopscreen.blit(player5_l_0, player5_rect)

	if player6_image > 3:
		player6_image = 0
	if player6_image == 0:
		Shopscreen.blit(player6_f_0, player6_rect)
	if player6_image == 1:
		Shopscreen.blit(player6_r_0, player6_rect)
	if player6_image == 2:
		Shopscreen.blit(player6_b_0, player6_rect)
	if player6_image == 3:
		Shopscreen.blit(player6_l_0, player6_rect)

	pg.display.update()

def update_choice(new_choice):
	f = open("Settings/Character.txt", "w")
	f.write(new_choice)
	f.close()

## This function animates the arrow which leads to the Homescreen
def animation_arrow_left_back():
	Shopscreen.blit(arrow_left_back_1, arrow_left_rect)
	pg.display.update()
	pg.time.wait(100)
	Shopscreen.blit(arrow_left_back_2, arrow_left_rect)
	pg.display.update()
	pg.time.wait(100)
	Shopscreen.blit(arrow_left_back_3, arrow_left_rect)
	pg.display.update()
	pg.time.wait(100)
	Shopscreen.blit(arrow_left_back_4, arrow_left_rect)
	pg.display.update()
	pg.time.wait(100)
	Shopscreen.blit(arrow_left_back_0, arrow_left_rect)
	pg.display.update()

## We load the different arrows for the animation in animation_arrow_left_back
arrow_left_back_0 = pg.transform.scale(pg.image.load("Images/Shop/arrow_left_back_0.png"), (int(DISPLAY_W/14.6285714), int(DISPLAY_W/25.6)))
arrow_left_back_1 = pg.transform.scale(pg.image.load("Images/Shop/arrow_left_back_1.png"), (int(DISPLAY_W/14.6285714), int(DISPLAY_W/25.6)))
arrow_left_back_2 = pg.transform.scale(pg.image.load("Images/Shop/arrow_left_back_2.png"), (int(DISPLAY_W/14.6285714), int(DISPLAY_W/25.6)))
arrow_left_back_3 = pg.transform.scale(pg.image.load("Images/Shop/arrow_left_back_3.png"), (int(DISPLAY_W/14.6285714), int(DISPLAY_W/25.6)))
arrow_left_back_4 = pg.transform.scale(pg.image.load("Images/Shop/arrow_left_back_4.png"), (int(DISPLAY_W/14.6285714), int(DISPLAY_W/25.6)))

arrow_left_rect = arrow_left_back_0.get_rect()
arrow_left_rect.center = (int(DISPLAY_W/20.48), int(DISPLAY_W/25.6))

Shopscreen.blit(arrow_left_back_0, arrow_left_rect)
pg.display.update()

show_title()
player_1()

## Starting timer for the animation
arrow_left_back_timer = pg.time.get_ticks()

while shoprun == True:
	Shopscreen.blit(arrow_right1, arrow_right1_rect)
	Shopscreen.blit(arrow_right1, arrow_right2_rect)
	Shopscreen.blit(arrow_right1, arrow_right3_rect)
	Shopscreen.blit(arrow_right1, arrow_right4_rect)
	Shopscreen.blit(arrow_right1, arrow_right5_rect)
	Shopscreen.blit(arrow_right1, arrow_right6_rect)
	pg.display.update()
	mouse_pos = pg.mouse.get_pos()

	if arrow_left_rect.collidepoint(mouse_pos):
		## If more than 2 seconds passed since the last animation, the animation can start
		if ((pg.time.get_ticks() - arrow_left_back_timer)/1000) > 1:
			animation_arrow_left_back()
			## reset the timer
			arrow_left_back_timer = pg.time.get_ticks()
		else:
			pass


	for event in pg.event.get():
		if event.type == pg.QUIT:
			pg.quit()
			shoprun = False

		if event.type == pg.MOUSEBUTTONDOWN:
			## If user clicks on the arrow to go back, Homescreen is loaded
			if arrow_left_rect.collidepoint(mouse_pos):
				pg.quit()
				os.system("python Homescreen.py")
				shoprun = False

			## if player clicks on an arrow in a box, the character of that box changes it image
			if arrow_right1_rect.collidepoint(mouse_pos):
				player1_image += 1
				player_1()
			if arrow_right2_rect.collidepoint(mouse_pos):
				player2_image += 1
				player_1()
			if arrow_right3_rect.collidepoint(mouse_pos):
				player3_image += 1
				player_1()
			if arrow_right4_rect.collidepoint(mouse_pos):
				player4_image += 1
				player_1()
			if arrow_right5_rect.collidepoint(mouse_pos):
				player5_image += 1
				player_1()
			if arrow_right6_rect.collidepoint(mouse_pos):
				player6_image += 1
				player_1()

			if box1.collidepoint(mouse_pos):
				box1_color = "red"
				box2_color = "white"
				box3_color = "white"
				box4_color = "white"
				box5_color = "white"
				box6_color = "white"
				draw_boxes()
				update_choice("Player_1")
			if box2.collidepoint(mouse_pos):
				box1_color = "white"
				box2_color = "red"
				box3_color = "white"
				box4_color = "white"
				box5_color = "white"
				box6_color = "white"
				draw_boxes()
				update_choice("Player_2")
			if box3.collidepoint(mouse_pos):
				box1_color = "white"
				box2_color = "white"
				box3_color = "red"
				box4_color = "white"
				box5_color = "white"
				box6_color = "white"
				draw_boxes()
				update_choice("Player_3")
			if box4.collidepoint(mouse_pos):
				box1_color = "white"
				box2_color = "white"
				box3_color = "white"
				box4_color = "red"
				box5_color = "white"
				box6_color = "white"
				draw_boxes()
				update_choice("Player_4")
			if box5.collidepoint(mouse_pos):
				box1_color = "white"
				box2_color = "white"
				box3_color = "white"
				box4_color = "white"
				box5_color = "red"
				box6_color = "white"
				draw_boxes()
				update_choice("Player_5")
			if box6.collidepoint(mouse_pos):
				box1_color = "white"
				box2_color = "white"
				box3_color = "white"
				box4_color = "white"
				box5_color = "white"
				box6_color = "red"
				draw_boxes()
				update_choice("Player_6")
			else:
				pass


pg.quit()
