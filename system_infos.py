#!/usr/bin/env python3

"""
    Felix Michelis
      07/04/2021
      dd/mm/yyyy
"""

import sys
from tkinter import *
import pygame as pg

def get_screen_size():
    
    if sys.platform.startswith('win32'):

        ## create a tkinter window in order to get the screen size
        root = Tk()
        ## get screen width and height
        width = root.winfo_screenwidth()
        height = root.winfo_screenheight()
        ## immediatly destroy the window after detection of size as we do not want
        ## the user to see a bad looking little window
        root.destroy()

        ## Calculate the size of the game window proportionnally to the screen size
        DISPLAY_W = int(width / 1.875)
        DISPLAY_H = int(height / 1.298076923)
        """
            With a screen size of 1920x1080 you should have these results:
            DISPLAY_W = 1024
            DISPLAY_H = 832
        """

    elif sys.platform.startswith('linux'):
        ## create a tkinter window in order to get the screen size
        root = Tk()
        ## get screen width and height
        width = root.winfo_screenwidth()
        height = root.winfo_screenheight()
        ## immediatly destroy the window after detection of size as we do not want
        ## the user to see a bad looking little window
        root.destroy()

        ## Calculate the size of the game window proportionnally to the screen size
        DISPLAY_W = int(width / 1.875)
        DISPLAY_H = int(height / 1.298076923)
        """
            With a screen size of 1920x1080 you should have these results:
            DISPLAY_W = 1024
            DISPLAY_H = 832
        """

    return DISPLAY_W, DISPLAY_H


def create_window(DISPLAY_W, DISPLAY_H):
    pg.init()
    pg.font.init()
    
    WINDOW_W = int(DISPLAY_W + int(DISPLAY_W / 6))
    WINDOW_H = int(DISPLAY_H + int(DISPLAY_H / 6))
    
    window = pg.display.set_mode((WINDOW_W, WINDOW_H), pg.RESIZABLE)
    main_window = pg.Surface((DISPLAY_W, DISPLAY_H))
    inventory_window = pg.Surface((WINDOW_W, int(DISPLAY_H / 6)))
    desk_window = pg.Surface((int(DISPLAY_W / 6), WINDOW_H))
    
    return window, WINDOW_W, WINDOW_H, main_window, inventory_window, desk_window
