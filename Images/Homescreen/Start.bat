@echo off & python -x "%~f0" %* & goto :eof

#!/usr/bin/env python3

## Felix Michelis

import pygame as pg 
from pygame.locals import *
import os

## Define some colors
BLACK = pg.Color('black')
WHITE = pg.Color('white')
GRAY = pg.Color('grey20')
LIGHT_GRAY = pg.Color('grey39')
LIGHTER_GRAY = pg.Color('grey59')
LIGHTEST_GRAY = pg.Color('grey78')

## Define window size
window_width = 1024
window_height = 832

## Initialize pygame
pg.init()

## Chose Font
myfont = pg.font.SysFont(None, 160)

## Create window
window = pg.display.set_mode((window_width, window_height))
pg.display.set_caption("Prison Escape")

## Makes the text appear one letter after another
def display_text_animation(string, color):
    text = ''
    for i in range(len(string)):
        window.fill(BLACK)
        text += string[i]
        text_surface = myfont.render(text, True, color)
        text_surface.set_alpha(127)
        text_rect = text_surface.get_rect()
        text_rect.center = (int(window_width/2), int(window_height/2))
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
        text_rect.center = (int(window_width/2), int(window_height/2))

        text_border_surface1 = myfont.render(string, True, ((colorcode - 40), (colorcode - 40), (colorcode - 40)))
        text_border_rect1 = text_border_surface1.get_rect()
        text_border_rect1.center = (int((window_width/2)-1), int((window_height/2)-1))
        text_border_rect2 = text_border_surface1.get_rect()
        text_border_rect2.center = (int((window_width/2)-2), int((window_height/2)-2))
        text_border_rect3 = text_border_surface1.get_rect()
        text_border_rect3.center = (int((window_width/2)-3), int((window_height/2)-3))
        text_border_rect4 = text_border_surface1.get_rect()
        text_border_rect4.center = (int((window_width/2)-4), int((window_height/2)-4))
        text_border_rect5 = text_border_surface1.get_rect()
        text_border_rect5.center = (int((window_width/2)-5), int((window_height/2)-5))
        text_border_rect6 = text_border_surface1.get_rect()
        text_border_rect6.center = (int((window_width/2)-6), int((window_height/2)-6))
        text_border_rect7 = text_border_surface1.get_rect()
        text_border_rect7.center = (int((window_width/2)-7), int((window_height/2)-7))
        text_border_rect8 = text_border_surface1.get_rect()
        text_border_rect8.center = (int((window_width/2)-8), int((window_height/2)-8))

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
    text_rect.center = (int(window_width/2), int(window_height/2))
    #text_border_surface1 = myfont.render(string, True, (196, 164, 47))
    text_border_surface1 = myfont.render(string, True, pg.Color('steelblue'))
    text_border_rect1 = text_border_surface1.get_rect()
    text_border_rect1.center = (int((window_width/2)-1), int((window_height/2)-1))
    text_border_rect2 = text_border_surface1.get_rect()
    text_border_rect2.center = (int((window_width/2)-2), int((window_height/2)-2))
    text_border_rect3 = text_border_surface1.get_rect()
    text_border_rect3.center = (int((window_width/2)-3), int((window_height/2)-3))
    text_border_rect4 = text_border_surface1.get_rect()
    text_border_rect4.center = (int((window_width/2)-4), int((window_height/2)-4))
    text_border_rect5 = text_border_surface1.get_rect()
    text_border_rect5.center = (int((window_width/2)-5), int((window_height/2)-5))
    text_border_rect6 = text_border_surface1.get_rect()
    text_border_rect6.center = (int((window_width/2)-6), int((window_height/2)-6))
    text_border_rect7 = text_border_surface1.get_rect()
    text_border_rect7.center = (int((window_width/2)-7), int((window_height/2)-7))
    text_border_rect8 = text_border_surface1.get_rect()
    text_border_rect8.center = (int((window_width/2)-8), int((window_height/2)-8))

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



## Run all the functions
display_text_animation('Prison Escape', GRAY)
pg.time.wait(300) ## = 0.3 seconds
display_text_animation2('Prison Escape')
pg.time.wait(300)
display_text_color('Prison Escape', 100)
pg.time.wait(300)

pg.quit()



## Start the next script
os.startfile('Homescreen.py')