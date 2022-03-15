#!/usr/bin/env python3

"""
    Felix Michelis
      30/03/2021
      dd/mm/yyyy
"""

import pygame as pg 
from pygame.locals import *
import os
from system_infos import get_screen_size

## Center the window on the screen
os.environ['SDL_VIDEO_CENTERED'] = '1'


## Define some colors
BLACK = pg.Color('black')
WHITE = pg.Color('white')
GRAY = pg.Color('grey20')
LIGHT_GRAY = pg.Color('grey39')
LIGHTER_GRAY = pg.Color('grey59')
LIGHTEST_GRAY = pg.Color('grey78')

## Define window size
#DISPLAY_W = 1024
#DISPLAY_H = 832
DISPLAY_W, DISPLAY_H = get_screen_size()

## Initialize pygame
pg.init()

## Chose Font
myfont = pg.font.SysFont(None, 160)

## Create window
window = pg.display.set_mode((DISPLAY_W, DISPLAY_H))
pg.display.set_caption("Prison Escape")

## Makes the text appear one letter after another
def display_text_animation(string, color):
    text = ''
    for i in range(len(string)):
        window.fill(BLACK)
        text += string[i]
        text_surface = myfont.render(text, False, color)
        text_surface.set_alpha(127)
        text_rect = text_surface.get_rect()
        text_rect.center = (int(DISPLAY_W/2), int(DISPLAY_H/2))
        window.blit(text_surface, text_rect)
        pg.display.update()
        pg.time.wait(100)


## Makes the text chagning in a smooth transition from grey to white
def display_text_animation2(string):
    colorcode = 40
    while colorcode < 255:
        window.fill(BLACK)
        text_surface = myfont.render(string, True, (colorcode, colorcode, colorcode))
        text_rect = text_surface.get_rect()
        text_rect.center = (int(DISPLAY_W/2), int(DISPLAY_H/2))

        text_border_surface1 = myfont.render(string, True, ((colorcode - 40), (colorcode - 40), (colorcode - 40)))
        text_border_rect1 = text_border_surface1.get_rect()
        text_border_rect1.center = (int((DISPLAY_W/2)-1), int((DISPLAY_H/2)-1))
        text_border_rect2 = text_border_surface1.get_rect()
        text_border_rect2.center = (int((DISPLAY_W/2)-2), int((DISPLAY_H/2)-2))
        text_border_rect3 = text_border_surface1.get_rect()
        text_border_rect3.center = (int((DISPLAY_W/2)-3), int((DISPLAY_H/2)-3))
        text_border_rect4 = text_border_surface1.get_rect()
        text_border_rect4.center = (int((DISPLAY_W/2)-4), int((DISPLAY_H/2)-4))
        text_border_rect5 = text_border_surface1.get_rect()
        text_border_rect5.center = (int((DISPLAY_W/2)-5), int((DISPLAY_H/2)-5))
        text_border_rect6 = text_border_surface1.get_rect()
        text_border_rect6.center = (int((DISPLAY_W/2)-6), int((DISPLAY_H/2)-6))
        text_border_rect7 = text_border_surface1.get_rect()
        text_border_rect7.center = (int((DISPLAY_W/2)-7), int((DISPLAY_H/2)-7))
        text_border_rect8 = text_border_surface1.get_rect()
        text_border_rect8.center = (int((DISPLAY_W/2)-8), int((DISPLAY_H/2)-8))

        window.blit(text_border_surface1, text_border_rect1)
        window.blit(text_border_surface1, text_border_rect2)
        window.blit(text_border_surface1, text_border_rect3)
        window.blit(text_border_surface1, text_border_rect4)
        window.blit(text_border_surface1, text_border_rect5)
        window.blit(text_border_surface1, text_border_rect6)
        window.blit(text_border_surface1, text_border_rect7)
        window.blit(text_border_surface1, text_border_rect8)
        window.blit(text_surface, text_rect)
        pg.display.update()
        pg.time.wait(80)
        
        colorcode += 5


## Change the text color
def display_text_color(string, colorcode):
    window.fill(BLACK)
    #text_surface = myfont.render(string, True, (232, 200, 39))
    text_surface = myfont.render(string, True, pg.Color('royalblue3'))
    text_rect = text_surface.get_rect()
    text_rect.center = (int(DISPLAY_W/2), int(DISPLAY_H/2))
    #text_border_surface1 = myfont.render(string, True, (196, 164, 47))
    text_border_surface1 = myfont.render(string, True, pg.Color('steelblue'))
    text_border_rect1 = text_border_surface1.get_rect()
    text_border_rect1.center = (int((DISPLAY_W/2)-1), int((DISPLAY_H/2)-1))
    text_border_rect2 = text_border_surface1.get_rect()
    text_border_rect2.center = (int((DISPLAY_W/2)-2), int((DISPLAY_H/2)-2))
    text_border_rect3 = text_border_surface1.get_rect()
    text_border_rect3.center = (int((DISPLAY_W/2)-3), int((DISPLAY_H/2)-3))
    text_border_rect4 = text_border_surface1.get_rect()
    text_border_rect4.center = (int((DISPLAY_W/2)-4), int((DISPLAY_H/2)-4))
    text_border_rect5 = text_border_surface1.get_rect()
    text_border_rect5.center = (int((DISPLAY_W/2)-5), int((DISPLAY_H/2)-5))
    text_border_rect6 = text_border_surface1.get_rect()
    text_border_rect6.center = (int((DISPLAY_W/2)-6), int((DISPLAY_H/2)-6))
    text_border_rect7 = text_border_surface1.get_rect()
    text_border_rect7.center = (int((DISPLAY_W/2)-7), int((DISPLAY_H/2)-7))
    text_border_rect8 = text_border_surface1.get_rect()
    text_border_rect8.center = (int((DISPLAY_W/2)-8), int((DISPLAY_H/2)-8))

    window.blit(text_border_surface1, text_border_rect1)
    window.blit(text_border_surface1, text_border_rect2)
    window.blit(text_border_surface1, text_border_rect3)
    window.blit(text_border_surface1, text_border_rect4)
    window.blit(text_border_surface1, text_border_rect5)
    window.blit(text_border_surface1, text_border_rect6)
    window.blit(text_border_surface1, text_border_rect7)
    window.blit(text_border_surface1, text_border_rect8)
    window.blit(text_surface, text_rect)
    pg.display.update()

def show_image():
    img = pg.transform.scale(pg.image.load("Images/Logo.png"), (DISPLAY_W, DISPLAY_H))
    img_rect = img.get_rect(x = 0, y = 0)

    window.blit(img, img_rect)
    pg.display.update()

## Run all the functions
display_text_animation('Prison Escape', GRAY)
pg.time.wait(300) ## = 0.3 seconds
display_text_animation2('Prison Escape')
pg.time.wait(300)
show_image()
pg.time.wait(5000)## 5 seconds

pg.quit()



## Start the next script
os.system("python Homescreen.py")
