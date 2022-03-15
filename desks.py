#!/usr/bin/env python3

import pygame as pg
from system_infos import get_screen_size
import random
from tiles import returnlist
import pickle
from player import Player


DISPLAY_W, DISPLAY_H = get_screen_size()

class Desk(object):
    def __init__(self):
        self.inventories = {}
        with open("Settings/Desks_content.pickle", "rb") as handle:
            ## Get the inventories of the desks
            self.inventories = pickle.load(handle)

        with open("Settings/Items.pickle", "rb") as handle:
            ## Get items and their levels
            self.itemlist = pickle.load(handle)

        self.size = 3 ## 3 * 3 big inventory of desks
        self.w, self.h = int(DISPLAY_W / 16), int(DISPLAY_W / 16)
        self.working_on_inventory = False
        self.positions = returnlist("desks")## Returns a list with the positions of the desks
                                            ## Something like this:
                                            ## self.positions = [(928, 192), (928, 288), (32, 352), (32, 448), (384, 448),
                                            ##                   (32, 544), (384, 544), (32, 640), (384, 640), (32, 736)]
        self.chosen_desk = None
        self.working = False
        self.images_rects = {}
        self.itemboxes = []
        self.clicked = []

    def generate_items(self):
        ## If another function is modifying the inventory we don't want to interfer
        ## So while another function is working on it, we wait
        while self.working_on_inventory:
            pass

        ## Tell the other functions that we are currently working on the inventory so they don't mess it up
        self.working_on_inventory = True

        ## For each desk in the game refill it
        for desk in self.positions:
            self.inventories[desk] = {}
            ## Create a provisory inventory for the desk
            provisory_inventory = []

            ## Now randomly chose an amount of items that should be in the desk
            amount_of_items = random.randrange(1, int(self.size*self.size))

            ## Create a list of items to chose from to put in the desk
            choice_of_items = list(self.itemlist.keys())

            ## For the number of items that should be in the desk: Chose item
            for i in range(amount_of_items):
                if len(choice_of_items) < 1:
                    ## If there are no more items to chose from
                    pass
                else:
                    ## If there are still items we can chose to put in the desk
                    chosen_item = random.choice(choice_of_items)
                    ## Add the chosen item to the provisory inventory list
                    provisory_inventory.append(chosen_item)

            ## Now for each item in the desk we need values for level, damage and durability
            for item in provisory_inventory:
                ## Randomly chose a level from the available levels for the item
                level = random.choice(self.itemlist[item]["level"])
                ## Get the position of the level numver to get the corresponding damage
                levelindex = self.itemlist[item]["level"].index(level)
                ## Get the damage corresponding to the level
                damage = self.itemlist[item]["damage"][levelindex]

                ## If the item can have more than durability 1 (= more than one time use)
                if len(self.itemlist[item]["durability"]) > 1:
                    ## Chose a random durability between the minimum durability [0] and the maximum durability [1]
                    durability = random.randrange(self.itemlist[item]["durability"][0],
                                                  self.itemlist[item]["durability"][1])
                    
                ## If the item is for single use, set durability to 1
                else:
                    durability = 1

                ## Create empty dict which will contain all the items of the current desk
                itemholder = {}
                ## Add the item to the dict
                itemholder[item] = {"level": level, "damage": damage, "durability": durability}

                ## Finally add the item with its level, damage and durability to the desk inventory
                for item in itemholder:
                    ## Make the itemholder dict the value for the desk (ex.: here the entire part with item etc is the itemholder dict
                    ## (321, 456): {item1 : {"level": 1, "damage": 3, "durability": 1},
                    ##              item2: {"level": 3, "damage": 5, "durability": 3}}
                    self.inventories[desk].update({item: itemholder[item]})


        ## Now write the new desk inventory to the file to save it
        with open("Settings/Desks_content.pickle", "wb") as handle:
            pickle.dump(self.inventories, handle)

        ## Allow other functions to work with the inventory again
        self.working_on_inventory  = False



    def add_item(self, desk, item, value):
        ## While another funciton is working wiht the inventory wait
        while self.working_on_inventory:
            pass

        ## Tell the other functions that we are currently working on the inventory so they don't mess it up
        self.working_on_inventory = True

        ## Get an up to date version of the inventories of the desks
        with open("Settings/Desks_content.pickle", "rb") as handle:
            self.inventory = pickle.load(handle)

        ## If there are any desks with an inventory:
        if len(self.inventory) > 0:
            ## If our desk is in the file:
            if desk in self.inventories:
                ## Take out the items and their values
                old_items = self.inventories[desk]
                ## Add the new item with its values
                old_items[item] = values
                ## Put the items with their values and the new item back in the desk
                self.inventories[desk] = old_items

            ## If our desk is not in the file:
            elif desk not in self.inventories:
                ## Add our desk with the item and the values of the item
                self.inventories[desk] = {item: values}

        ## If no desk in inventory file:
        elif len(self.inventory) < 1:
            ## Add our desk with the item and the values of the item
            self.inventory[desk] = {item: values}


        ## Update the file
        with open("Settings/Desks_content.pickle", "wb") as handle:
            pickle.dump(self.inventories, handle)

        self.working_on_inventory = False


    def remove_item(self, desk=False, item=False, itemdesk=None):
        while self.working_on_inventory:
            pass

        self.working_on_inventory = True

        with open("Settings/Desks_content.pickle", "rb") as handle:
            self.inventories = pickle.load(handle)

        ## If desk is given to be deleted in the function call and exists
        if desk != False and desk in self.inventories:
            del self.inventories[desk]
            
        ## If item should be deleted and the desk in which the item is (itemdesk) exists
        if item != False and item in self.inventories[itemdesk]:
            del self.inventories[itemdesk][item]

        else:
            pass


        with open("Settings/Desks_content.pickle", "wb") as handle:
            pickle.dump(self.inventories, handle)


        self.working_on_inventory = False


    def draw(self, surface, desk=False):
        
        box_w = box_h = int(DISPLAY_W / 16) ## creates a box of 64x64 px when the game window has a size of 1024x832 px
        surface_width, surface_height = surface.get_width(), surface.get_height() ## Get the width and height of the surface
        box_x = int(surface_width/2 - box_w/2)                          #-|
        box_y = int(-surface_height/2 + ((self.size*self.size)* box_h)) #-| Center the boxes on the surface

        ## draw self.size*self.size boxes on the screen (ex.: self.size = 3; self.size*self.size = 9; =9 boxes on the screen)
        for i in range(int(self.size*self.size)):
            itembox = pg.draw.rect(surface, pg.Color("black"), (box_x, box_y, box_w, box_h), int(DISPLAY_W/204.8))
            
            self.itemboxes.append((box_x, box_y))
            
            box_y += int(box_w + 5)


        if desk != False:
            self.chosen_desk = []
            self.images_rects = {}
            
            box_y = int(-surface_height/2 + ((self.size*self.size)* box_h))
            box_y = int(-surface_height/2 + ((self.size*self.size)* box_h))
            
            for item in self.inventories[desk]:
                imagefilename = f'Images/Items/{item}.png'
                itemimage = pg.transform.scale(pg.image.load(imagefilename), (box_w, box_h))
                                
                self.images_rects[item] = itemimage


        if self.chosen_desk != None:
            box_y = int(-surface_height/2 + ((self.size*self.size)* box_h))
            box_y = int(-surface_height/2 + ((self.size*self.size)* box_h))
            
            for item in self.images_rects:
                itemimage_rect = self.images_rects[item].get_rect(x = box_x, y = box_y)
                surface.blit(self.images_rects[item], itemimage_rect)
                
                box_y += int(box_w + 5)

    
##        if chosen != False:
##            self.clicked = []
##            for x in chosen:
##                self.clicked.append(x)
##                
##
        if len(self.clicked) > 1:
            clicked_on = pg.draw.rect(surface, pg.Color("red"), (int(self.clicked[0]), int(self.clicked[1]), box_w, box_h), int(DISPLAY_W/204.8))
            
        self.working = False


    def chosen(self, x, y):
        self.clicked = []
        self.clicked.append(x)
        self.clicked.append(y)
        #index = self.positions[(x, y)]
        
        
        #return self.inventories[(x, y)][index]
