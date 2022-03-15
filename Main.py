#!/usr/bin/env python3

"""

    Felix Michelis
      18/06/2021
      dd/mm/yyyy

      
      The date indicates the last time a change in the code occured
      for all scipts in this project
"""

import pygame as pg
from spritesheet import Spritesheet
from tiles import *
from player import Player
import timemanager
#import multiprocessing
from npc import NPC
import os
import threading
from tkinter import *
import re
from system_infos import *
from desks import Desk

## For debugging
command : str = "NONE"

## Show infos in output like NPC position or framerate
## Pause the game
## running game
## NPCs or not
infos, pause, running, run_npc = False, False, True, True

## Create a list to store the coordinates of all the blocks which act as walls/barriers
barriers_list : list = []

## Center window
os.environ['SDL_VIDEO_CENTERED'] = '1'
## Initialize pygame
pg.init()

## Set Display WIDTH and HEIGHT
#DISPLAY_W = 1024 with a monitor of the size: 1920x1080
#DISPLAY_H = 832
DISPLAY_W, DISPLAY_H = get_screen_size()

## Define the surface on which everything will be blitted on and create a window
window, WINDOW_W, WINDOW_H, canvas, inventory_window, desk_window = create_window(DISPLAY_W, DISPLAY_H)

## Set FPS
## Set variable deltaTime which will be changed in main loop
## Block size
fps, deltaTime, size = 60, 0, 32

## Initialize pygame clock
clock = pg.time.Clock()

## Set p as Player
p = Player()
npc = NPC()
desk = Desk()
## Generate new items for the desk always when game starts so they don't stay the same
desk.generate_items()

## Tell the script where the spritesheet with all the images for the game is located
my_spritesheet = Spritesheet('Images/Spritesheets/GameImages/main_spritesheet.png')
#grass = my_spritesheet.parse_sprite('grass.png')

## Load the different layers of our map
## We have different layers so that we can blit things on top of other
Ground = TileMap('Images/Tilemaps/Ground.csv', my_spritesheet)
Walls = TileMap('Images/Tilemaps/Walls.csv', my_spritesheet)
Items = TileMap('Images/Tilemaps/Items.csv', my_spritesheet)

## Retrieve all the coordinates of the different blocks we need
barriers = returnlist("barriers")
barriers_list.extend(barriers)
celldoors_list = returnlist("celldoors")
simpledoors_list = returnlist("simpledoors")
#walls = returnlist("walls")

clicked_pinv, clicked_dinv = False, False

def get_commands():

    def show_result(result):
        result_window = Tk()
        result_window.geometry("100x100")
        E1 = Label(result_window, text = str(result))
        E1.pack(side = LEFT)
        result_window.mainloop()
        
    def execute_command(command):
        global fps; global deltaTime; global pause; global infos; global run_npc; global running
        
        if command == "EXIT": running = False
        elif "NPC" in command: npc.commands(command)
        elif "PLAYER" in command: p.commands(command)
        elif "FPS +" in command: fps = fps + int(re.search(r'\d+', command).group()); show_result(fps)
        elif "FPS -" in command: fps = fps - int(re.search(r'\d+', command).group()); show_result(fps)
        elif command == "deltaTime": show_result(deltaTime)
        elif command == "PAUSE": pause = True
        elif command == "CONTINUE": pause = False
        elif command == "PAUSE INFOS": infos = False; npc.infos = False
        elif command == "CONTINUE INFOS": infos = True; npc.infos = True
        elif command == "PAUSE NPC": run_npc = False
        elif command == "PAUSE SHOW NPC-PATH": npc.commands(command)
        elif command == "CONTINUE SHOW NPC-PATH": npc.commands(command)
        #elif command == "CONTINUE NPC":
            #run_npc = True
            ###   COMMAND NOT WORKING   ###
        elif command == "PLAYER ADD" or command == "PLAYER REMOVE": p.commands(command)
        else:
            pass
            

    def key_pressed(event):
        get_user_input()
        
    def get_user_input():
        global command
        command = E1.get()
        print(command)
        execute_command(command)
        E1.delete(0, END)
        E1.insert(0, "")

    root = Tk()
    root.geometry("50x50")

    L1 = Label(root, text = "$:")
    L1.pack(side = LEFT)

    E1 = Entry(root, bd = 10)
    E1.pack(side = RIGHT)

    root.bind("<Return>", key_pressed)
    root.mainloop()

## Start the tkinter window with input for the commands as a thread as we want it to act independently from the game
## and that way we can pause the game
start_getting_commands = threading.Thread(target = get_commands).start()
    
bg_image = pg.image.load("Images/Background.png")

## Fill the desks with random items
desk.generate_items()

while running:

    if pause == False:
        ## Run the game at 60 fps
        clock.tick(60)
        """
            get delaTime because on older pcs the game could run slower but the character should
            still move at the same speed. The contrary is true for fast pcs.
            Then divide the number we get by 10 so that we have a nnumber that starts with 1
            This will then be mutliplied with the character speed
        """
        deltaTime = (clock.tick(fps) / 10) - 1
        if infos == True:
            print(f'[MAIN][DeltaTime]: {deltaTime}')
            print(f'[MAIN][FPS]: {fps}')

        #Otherwise too slow
        if deltaTime < 1: deltaTime = 1

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                ########os.system("python Homescreen.py")######
                running = False
                
            elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                            pass
                    elif event.key == pg.K_LEFT or event.key == ord("a"):
                            p.LEFT_KEY = True
                            p.FACING_LEFT, p.FACING_RIGHT, p.FACING_FRONT, p.FACING_BACK = True, False, False, False
                    elif event.key == pg.K_RIGHT or event.key == ord("d"):
                            p.RIGHT_KEY = True
                            p.FACING_LEFT, p.FACING_RIGHT, p.FACING_FRONT, p.FACING_BACK = False, True, False, False
                    elif event.key == pg.K_UP or event.key == ord("w"):
                            p.UP_KEY = True
                            p.FACING_LEFT, p.FACING_RIGHT, p.FACING_FRONT, p.FACING_BACK = False, False, False, True
                    elif event.key == pg.K_DOWN or event.key == ord("s"):
                            p.DOWN_KEY = True
                            p.FACING_LEFT, p.FACING_RIGHT, p.FACING_FRONT, p.FACING_BACK = False, False, True, False

                    elif event.key == ord("e"):
                        for a, b in returnlist("desks"):
                            #create rect without drawing
                            deskholder = pg.Rect(a, b, int(DISPLAY_W / 25.6), int(DISPLAY_W / 25.6))
                            if p.rect.colliderect(deskholder):
                                desk.draw(canvas, (a, b))
                                print("DESK RUN")

                                
            elif event.type == pg.KEYUP:
                if event.key == pg.K_LEFT or event.key == ord("a"): p.LEFT_KEY = False
                elif event.key == pg.K_RIGHT or event.key == ord("d"): p.RIGHT_KEY = False
                elif event.key == pg.K_UP or event.key == ord("w"): p.UP_KEY = False
                elif event.key == pg.K_DOWN or event.key == ord("s"): p.DOWN_KEY = False

            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mposx, mposy = pg.mouse.get_pos()
                    #correct mouse position on y as we use a small window inside the big window but mouse pos is taken from big window
                    mposy_pinv = int(mposy - 835)
                    mposx_dinv = int(mposx - 1025)
                    
                    print("[MAIN][MOUSEBUTTONEVENT]: left click")
                    
                    rects = p.player_return("inventory_rects")
                    
                    for rectx, recty in rects:
                        #create rect without drawing
                        player_inventory_placeholder_rect = pg.Rect(int(rectx), int(recty), 64, 64)
                        
                        placeholder_mouse = pg.Rect(mposx, mposy_pinv, 1, 1)
                        if placeholder_mouse.colliderect(player_inventory_placeholder_rect):
                            p.draw_small_inventory(inventory_window, (rectx, recty))
                            clicked_pinv = True


                    rects = desk.itemboxes
                    print(mposx_dinv)
                    for rectx, recty in rects:
                        desk_inventory_placeholder_rect = pg.Rect(int(rectx), int(recty), 64, 64)
                        placeholder_mouse = pg.Rect(mposx_dinv, mposy, 1, 1)
                        if placeholder_mouse.colliderect(desk_inventory_placeholder_rect):
                            #item = desk.chosen(rectx, recty)
                            #print(item)
                            desk.chosen(rectx, recty)
                            
                            

                        
                        
                elif event.button == 2:
                    print("[MAIN][MOUSEBUTTONEVENT]: middle click")
                elif event.button == 3:
                    print("[MAIN][MOUSEBUTTONEVENT]: right click")
                                

        ## Clear the screen so we don't see any pixels fomr the frame before
        inventory_window.blit(pg.transform.scale(bg_image, (WINDOW_W, int(DISPLAY_H / 6))), (0, 0))
        desk_window.blit(pg.transform.scale(bg_image, (int(WINDOW_W / 6), DISPLAY_H)), (0, 0))
        canvas.fill(pg.Color("grey"))
        
        ## Draw our different layers on the screen
        Ground.draw_map(canvas)
        Walls.draw_map(canvas)
        Items.draw_map(canvas)

        ## draw gametime to the screen on the upper right corner
        timemanager.update_text(canvas, (DISPLAY_W / 1.077894736842105), (DISPLAY_H / 41.6))
        
        ## Update the player (if he moved)
        p.update(deltaTime)
        ## Check if the player collided with any important block (doors, walls,...)
        p.check_collision(barriers_list, celldoors_list, simpledoors_list, deltaTime)
        ## Draw the different opened doors onto the screen; the script goes through a list and blits all items in the list
        ## if the list is empty this function does nothing
        p.draw_celldoors(canvas)
        p.draw_simpledoors(canvas)
        ## Finally draw the player to the screen after checking if he moved and if he collided
        p.draw(canvas)
        
        if run_npc:
            npc.update(deltaTime)
            npc.check_collision(barriers_list, celldoors_list, simpledoors_list, deltaTime, canvas)
            npc.draw_celldoors(canvas)
            npc.draw_simpledoors(canvas)
            npc.draw(canvas)

        ## Finally draw the player to the screen after checking if he moved and if he collided
        p.draw(canvas)
        
        desk.draw(desk_window)
        p.draw_small_inventory(inventory_window)
        
        window.blit(canvas, (0, 0))
        window.blit(inventory_window, (0, int(WINDOW_H - int(WINDOW_H - DISPLAY_H))))
        window.blit(desk_window, (int(WINDOW_W - int(WINDOW_W - DISPLAY_W)), 0))
        
        ## Update the screen so that the user sees what has happened
        pg.display.update()
        

pg.quit()
