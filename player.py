#!/usr/bin/env python3

"""
    Felix Michelis
      07/04/2021
      dd/mm/yyyy
"""

import pygame as pg
from spritesheet import Spritesheet
import threading
import time
from tkinter import *
import re ## only for debug in self.commands()
from system_infos import get_screen_size
import pickle ##for inventory write to file
from tiles import returnlist

DISPLAY_W, DISPLAY_H = get_screen_size()

celldoors_draw = {}
simpledoors_draw = {}

drew_celldoors = 0
drew_simpledoors = 0


class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        ## Player pressed left key, right key, ...
        self.LEFT_KEY, self.RIGHT_KEY, self.UP_KEY, self.DOWN_KEY = False, False, False, False
        ## Player is looking to the left, right, ...
        self.FACING_LEFT, self.FACING_RIGHT, self.FACING_FRONT, self.FACING_BACK = False, False, True, False
        ## Load the images of the character
        self.load_frames()
        ## create a rect with an image representing the player
        self.rect = self.idle_frames_left[0].get_rect()
        ## Set the position of the player
        self.rect.midbottom = (int(DISPLAY_W / 10.6), int(DISPLAY_W / 10.6))
        ## Set width and height of the player (about 30x30 px)
        self.rect.w = int(DISPLAY_W / 40.96)
        self.rect.h = int(DISPLAY_W / 40.96)
        ## Set the current frame to 0. If the frame goes up by 1, the image changes. This creates an animation cycle
        self.current_frame = 0
        self.last_updated = 0
        self.velocity_x = 0
        self.velocity_y = 0
        ## Set the speed of the player to 6 px
        self.speed_x, self.speed_y = 6, 6
        ## Set the state to 'idle' = not moving
        self.state = 'idle'
        ## Set the current image of the player to be the image where the player does not walk and looks forward
        self.current_image = self.idle_frames_front[0]
        ## Load the player's inventory
        with open("Settings/Player_Inventory.pickle", "rb") as handle: self.inventory = pickle.load(handle)
        ## Create a variable that tells functions if another function is changing something on the inventory because there should always only be one function working on it
        self.working_on_inventory = False
        ## List of positions of the rectangles blitted onto the screen and creating an inventory image
        self.inventory_rects = []
        ## List that contains only one position of a rectangle from the inventory, the one that got clicked on
        self.chosen_rect = []

    ## Function to return some informations like the positions of the inventory rectangels in case the player clicks on one of them to take an item
    def player_return(self, what):
        to_return = None
        
        if what == "inventory_rects":
            to_return = self.inventory_rects


        return to_return
    
##-----DEBUG-----##
    def show_all_info(self):
        def show():
            results = ("KEY LEFT: " + str(self.LEFT_KEY), "KEY RIGHT: " + str(self.RIGHT_KEY), "KEY UP: " + str(self.UP_KEY), "KEY DOWN: " + str(self.DOWN_KEY),
                      "FACING LEFT: " + str(self.FACING_LEFT), "FACING RIGHT: " + str(self.FACING_RIGHT), "FACING FRONT: " + str(self.FACING_FRONT), "FACING BACK: " + str(self.FACING_BACK),
                      "POSITION (x,y): " + str(self.rect.x) + ", " + str(self.rect.y), "RECT SIZE (w,h): " + str(self.rect.w) + ", " + str(self.rect.h),
                      "CURRENT FRAME: " + str(self.current_frame), "CURRENT IMAGE: " + str(self.current_image),
                      "TIMES UPDATED: " + str(self.last_updated), "STATE: " + str(self.state),
                      "VELOCITY (X): " + str(self.velocity_x), "VELOCITY (Y): " + str(self.velocity_y))
            for result in results:
                if "NONE" in result:
                    E1 = Label(result_window, text = str(result))
                    E1.pack(side = TOP)
                    E1.after(1000, E1.destroy)
                                        
                E1 = Label(result_window, text = str(result))
                E1.pack(side = TOP)
                E1.after(1000, E1.destroy)

            result_window.after(1000, show)

        result_window = Tk()
        result_window.geometry("300x400")
        result_window.title("PLAYER")
        show()
        result_window.mainloop()
                
    def commands(self, command):
        if command == "PLAYER":
            show_player_info = threading.Thread(target = self.show_all_info)
            show_player_info.start()
        elif "PLAYER.rect=" in command:
            self.rect.x, self.rect.y = map(int, re.findall(r'\d+', command))
        elif command == "PLAYER ADD":
            self.add_to_inventory("Broom", {"level":1, "damage": [10], "durability":6})
        elif command == "PLAYER REMOVE":
            self.remove_from_inventory("Broom")
        elif command == "PLAYER CHANGE":
            self.modify_item("Broom", level=1, durability=1)
##-----DEBUG-----##

##-----DRAW-----##
    def draw(self, surface):
        surface.blit(self.current_image, self.rect)
##-----DRAW-----##

##-----UPDATE-----##
    def update(self, deltaTime):
        self.velocity_x, self.velocity_y = 0, 0
        
        if self.LEFT_KEY: self.velocity_x = -self.speed_x * deltaTime
        elif self.RIGHT_KEY: self.velocity_x = self.speed_x * deltaTime
        #self.rect.x += self.velocity_x
        if self.UP_KEY: self.velocity_y = -self.speed_y * deltaTime
        elif self.DOWN_KEY: self.velocity_y = self.speed_y * deltaTime
            
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        self.set_state()
        self.animate()

    def set_state(self):
        self.state = 'idle'
        
        if self.velocity_x > 0: self.state = 'moving right'
        elif self.velocity_x < 0: self.state = 'moving left'
        elif self.velocity_y > 0: self.state = 'moving down'
        elif self.velocity_y < 0: self.state = 'moving up'
##-----UPDATE-----##

##-----ANIMATION/IMAGE_LOADING-----##
    def animate(self):
        
        now = pg.time.get_ticks()
        
        if self.state == 'idle':
            
            if now - self.last_updated > 200:
                
                self.last_updated = now
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames_left)
                
                if self.FACING_LEFT: self.current_image = self.idle_frames_left[self.current_frame]
                elif self.FACING_RIGHT: self.current_image = self.idle_frames_right[self.current_frame]
                elif self.FACING_FRONT: self.current_image = self.idle_frames_front[self.current_frame]
                elif self.FACING_BACK: self.current_image = self.idle_frames_back[self.current_frame]
        else:
            if now - self.last_updated > 100:
                
                self.last_updated = now
                self.current_frame = (self.current_frame + 1) % len(self.walking_frames_left)
                
                if self.state == 'moving left': self.current_image = self.walking_frames_left[self.current_frame]
                elif self.state == 'moving right': self.current_image = self.walking_frames_right[self.current_frame]
                elif self.state == 'moving up': self.current_image = self.walking_frames_back[self.current_frame]
                elif self.state == 'moving down': self.current_image = self.walking_frames_front[self.current_frame]

    def load_frames(self):
        file_path_to_sheet = open("Settings/Character.txt", "r")
        path_to_sheet = file_path_to_sheet.read()
        file_path_to_sheet.close()
        
        my_spritesheet = Spritesheet("Images/Spritesheets/Players/" + path_to_sheet + ".png")
        
        self.idle_frames_left = [my_spritesheet.parse_sprite("Player_l_0.png")]
        
        self.walking_frames_left = [my_spritesheet.parse_sprite("Player_l_0.png"),
                                    my_spritesheet.parse_sprite("Player_l_1.png"),
                                    my_spritesheet.parse_sprite("Player_l_2.png")]

        self.idle_frames_right = [my_spritesheet.parse_sprite("Player_r_0.png")]
        
        self.walking_frames_right = [my_spritesheet.parse_sprite("Player_r_0.png"),
                                    my_spritesheet.parse_sprite("Player_r_1.png"),
                                    my_spritesheet.parse_sprite("Player_r_2.png")]

        self.idle_frames_front = [my_spritesheet.parse_sprite("Player_f_0.png")]
        
        self.walking_frames_front = [my_spritesheet.parse_sprite("Player_f_0.png"),
                                    my_spritesheet.parse_sprite("Player_f_1.png"),
                                    my_spritesheet.parse_sprite("Player_f_2.png")]

        self.idle_frames_back = [my_spritesheet.parse_sprite("Player_b_0.png")]
        
        self.walking_frames_back = [my_spritesheet.parse_sprite("Player_b_0.png"),
                                    my_spritesheet.parse_sprite("Player_b_1.png"),
                                    my_spritesheet.parse_sprite("Player_b_2.png")]
##-----ANIMATION/IMAGE_LOADING-----##

##-----DOORS-----##
    def openCelldoor(self, a, b):
        global celldoors_draw
        door_img = pg.transform.scale(pg.image.load("Images/GameImages/celldoor_2_opened.png"), (int(DISPLAY_W / 32), int(DISPLAY_W / 32)))
        door_rect = door_img.get_rect(x = a, y = b)

        celldoors_draw[door_img] = door_rect

    def draw_celldoors(self, display):
        global celldoors_draw
        global drew_celldoors
        ground_img = pg.transform.scale(pg.image.load("Images/GameImages/cell_floor.png"), (int(DISPLAY_W / 32), int(DISPLAY_W / 32)))
        try:
            for drawing, where in celldoors_draw.items():
                display.blit(ground_img, where)
                display.blit(drawing, where)
            drew_celldoors += 1

            if drew_celldoors > 100:
                celldoors_draw.clear()
                drew_celldoors = 0
        except:
            pass

    def openSimpledoor(self, a, b):
        global simpledoors_draw
        door_img = pg.transform.scale(pg.image.load("Images/GameImages/simpledoor_1_opened.png"), (int(DISPLAY_W / 32), int(DISPLAY_W / 32)))
        door_rect = door_img.get_rect(x = a, y = b)
        simpledoors_draw[door_img] = door_rect

    def draw_simpledoors(self, display):
        global simpledoors_draw
        global drew_simpledoors
        ground_img = pg.transform.scale(pg.image.load("Images/GameImages/cafeteria_floor.png"), (int(DISPLAY_W / 32), int(DISPLAY_W / 32)))
        try:
            for drawing, where in simpledoors_draw.items():
                display.blit(ground_img, where)
                display.blit(drawing, where)
            drew_simpledoors += 1
            if drew_simpledoors > 100:
                simpledoors_draw.clear()
                drew = 0
        except:
            pass
##-----DOORS-----##

##-----COLLISIONS-----##
    def check_collision(self, walls, celldoors, simpledoors, deltaTime):
        for a, b in walls:
            ## We don't draw the rectangle as we don't need it and it saves resources            
            if self.rect.colliderect(pg.Rect(a, b, int(DISPLAY_W / 34.13), int(DISPLAY_W / 34.13))):
                if self.velocity_x < 0: self.rect.x += self.speed_x * deltaTime
                if self.velocity_x > 0: self.rect.x -= self.speed_x * deltaTime
                if self.velocity_y < 0: self.rect.y += self.speed_y * deltaTime
                if self.velocity_y > 0: self.rect.y -= self.speed_y * deltaTime

        for a, b in celldoors:
            if self.rect.colliderect(pg.Rect(int(a-5), int(b-5), int(DISPLAY_W / 25.6), int(DISPLAY_W / 25.6))): self.openCelldoor(a, b)
                
        for a, b in simpledoors:
            if self.rect.colliderect(pg.Rect(int(a-5), int(b-5), int(DISPLAY_W / 25.6), int(DISPLAY_W / 25.6))): self.openSimpledoor(a, b)

##-----COLLISIONS-----##
                
##-----INVENTORY-----##
    def add_to_inventory(self, item, values):
        with open("Settings/Player_Inventory.pickle", "rb") as handle: self.inventory = pickle.load(handle)
            
        ## add an item and the level of the item and its durability

        """
            Check if another function is using the inventory dict to prevent errors
            because if the dict is modified while being used for example by the draw function,
            the draw function would raise an error
        """
        if self.working_on_inventory: self.add_to_inventory(item, values)
        
        if not self.working_on_inventory:
            ## Change the working_on_inventory value to True so that other functions do not change something while
            ## this function modifies the dict
            self.working_on_inventory = True
            ## here we add a key = item and its values= level and durability
            ## ex.: {"Item": {"level": 2, "durability": 6}, "Item2": {"level": 1, "durability": 1}}
            self.inventory[item] = values

        with open("Settings/Player_Inventory.pickle", "wb") as handle: pickle.dump(self.inventory, handle)
            
        ## Let other functions work on the inventory
        self.working_on_inventory = False


    def remove_from_inventory(self, item):
        with open("Settings/Player_Inventory.pickle", "rb") as handle: self.inventory = pickle.load(handle)
            
        ## delete an item from the inventory
        if self.working_on_inventory: self.remove_from_inventory(item)
        
        if not self.working_on_inventory:
            self.working_on_inventory = True
            ## check if item exists in inventory. If we did not check that there could be an error
            ## when trying to remove a non-existant item
            if item in self.inventory: del self.inventory[item] ## delete all values from the item in the dict self.inventory
            
            else:
                pass

        with open("Settings/Player_Inventory.pickle", "wb") as handle: pickle.dump(self.inventory, handle)
            
        self.working_on_inventory = False


    def modify_item(self, item, level=False, damage=False, durability=False):
        ## Modify the level or the durability of an item
        if self.working_on_inventory: self.modify_item(item, level, damage, durability)
        
        if not self.working_on_inventory:
            self.working_on_inventory = True
            ## check if item exists in inventory, otherwise we cannot modify its properties
            if item in self.inventory:
                ## check if the level, the damage or the durability has to be changed
                if level != False: self.inventory[item]["level"] = level ## change the value of the level for this item to the given value
                if damage != False: self.inventory[item]["damage"] = damage
                if durability != False: self.inventory[item]["durability"] = durability ## change the value of the durability for this item to the given value
                else:
                    pass
                    
            else:
                pass

        with open("Settings/Player_Inventory.pickle", "wb") as handle: pickle.dump(self.inventory, handle)
            
        self.working_on_inventory = False
        

    def draw_small_inventory(self, window, chosen=False):
        if chosen != False:
            self.chosen_rect = []
            self.chosen_rect.append(chosen)
        ## This function draws the inventory to the right bottom of the game window

        with open("Settings/Player_Inventory.pickle", "rb") as handle: self.inventory = pickle.load(handle)
        
        if self.working_on_inventory: self.draw_small_inventory(window, chosen)
        
        if not self.working_on_inventory:
            self.working_on_inventory = True
            
            surface = pg.display.get_surface()
            WINDOW_W, WINDOW_H = surface.get_width(), surface.get_height()
            ## WINDOW_W and WINDOW_H should be around 1194, 970 with game window size 1024x832 px
            
            number_of_boxes = 6
            box_w = box_h = int(DISPLAY_W/16) ## creates a box of 64x64 px when the game window has a size of 1024x832 px
            box_x = int(WINDOW_W - int(int(number_of_boxes + 1) * box_w)) ## set the x position of the box which is the Display width - ((the number of boxes+1) * the box width)
            box_y = int(WINDOW_H - int(1.2 * box_h)) ## set the y position of the box which is the height of the game window - half the height of a box

            box_x, box_y = int(WINDOW_W / 4.26), int(WINDOW_H / 24.25)

            for item in self.inventory:
                ## for each item draw a black not filled box with a border line of 5px
                itembox = pg.draw.rect(window, pg.Color('black'), (box_x, box_y, box_w, box_h), int(DISPLAY_W/204.8))
                
                ## get the filename of the image of the item and draw it to the screen
                itemimage = pg.transform.scale(pg.image.load(f'Images/Items/{item}.png'), (box_w, box_h))
                itemimage_rect = itemimage.get_rect(x = box_x, y = box_y)
                window.blit(itemimage, itemimage_rect)

                if (itembox.x, itembox.y) not in self.inventory_rects: self.inventory_rects.append((itembox.x, itembox.y))

                ## change the position of the next box to be more on the right so we have x boxes next to each other with a certain space between them
                box_x += int(box_w + 5)

            ## We always want to display a certain amount of boxes(=number_of_boxes). But the amount of items in the inventory can be smaller than the amount of boxes we want
            ## so we count how many boxes are missing and we draw the in this for loop
            if len(self.inventory) < number_of_boxes:
                ## calculate how many boxes are missing
                amount = int(number_of_boxes - len(self.inventory))

                for i in range(amount):
                    ## draw the boxes with a black border, not filled
                    itembox = pg.draw.rect(window, pg.Color('black'), (box_x, box_y, box_w, box_h), int(DISPLAY_W/204.8))

                    if (itembox.x, itembox.y) not in self.inventory_rects:
                        self.inventory_rects.append((itembox.x, itembox.y))

                    box_x += int(box_w + 5)
                    
        for x, y in self.chosen_rect: pg.draw.rect(window, pg.Color('red'), (x, y, box_w, box_h), int(DISPLAY_W/204.8))
            
        with open("Settings/Player_Inventory.pickle", "wb") as handle: pickle.dump(self.inventory, handle)
            
        self.working_on_inventory = False
##-----INVENTORY-----##
        



        



