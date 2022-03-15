#!/usr/bin/env python3

"""
    Felix Michelis
      30/03/2021
      dd/mm/yyyy
"""

## One day(=24 h) in game = +- 30 min in real life
## One hour in game = +- 1:40 min

import pygame as pg
import time
import threading

## We start at 09:00 am and for each number we create a variable to be able to control the time
time_hour_1 = 0
time_hour_2 = 9
time_minute_1 = 0
time_minute_2 = 0

## Initialize pygame
pg.init()
pg.font.init()
running = True

clock = pg.time.Clock()
## Define our font
textfont = pg.font.Font(None, 45)

def update_text(window, x, y):
    #global time_hour_1; global time_hour_2; global time_minute1; global time_minute_2; global updating
    ## change the time variables from int to str
    text_1 = str(time_hour_1)
    text_2 = str(time_hour_2)
    text_3 = ":"
    text_4 = str(time_minute_1)
    text_5 = str(int(time_minute_2))
    ## Create a single str out of 5
    text = text_1 + text_2 + text_3 + text_4 + text_5
    ## Create a textsurface
    title_text_surface = textfont.render(text, True, pg.Color('black'))
    title_text_rect = title_text_surface.get_rect()
    title_text_rect.center = (int(x), int(y))

    window.blit(title_text_surface, title_text_rect)
    pg.display.update()
    ## Call the function update_time() to update the time(= + 0.02)
    update_time()

def update_time():
    global time_hour_1; global time_hour_2; global time_minute_1; global time_minute_2; global updating

    ## Update the time (=add + 0.02 each time the game goes through the loop)
    time_minute_2 += 0.02

    if time_minute_2 > 9.9:
        time_minute_2 = 0
        time_minute_1 += 1
    if time_minute_1 > 5:
        time_minute_1 = 0
        time_hour_2 += 1
    if time_hour_2 > 9:
        time_hour_2 = 0
        time_hour_1 += 1
    if time_hour_1 == 2 and time_hour_2 > 3:
        time_hour_1 = 0
        time_hour_2 = 0

    #print(time_hour_1, time_hour_2, ":", time_minute_1, time_minute_2)
    


