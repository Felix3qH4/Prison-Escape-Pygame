#!/usr/bin/env python3

"""
    Felix Michelis
      06/04/2021
      dd/mm/yyyy
"""

import pygame as pg
import csv
import os
from system_infos import get_screen_size

DISPLAY_W, DISPLAY_H = get_screen_size()

walllist = []
desklist = []
boxlist = []
automatlist = []
bedlist = []
celldoorlist = []
fencelist = []
pinkdoorlist = []
simpledoorlist = []

wallmatrix = []

def returnlist(which):
    ## returns a list containing all the positions of different objects like walls or doors
    #global wallslist; global desklist; global boxlist

    thislist = []
    barrierlist = []

    if which == "walls":
        thislist = wallslist
    elif which == "desks":
        thislist = desklist
        print(desklist)
    elif which == "boxes":
        thislist = boxlist
    elif which == "automaten":
        thislist = automatlist
    elif which == "beds":
        thislist = bedlist
    elif which == "celldoors":
        thislist = celldoorlist
    elif which == "fences":
        thislist = fencelist
    elif which == "pinkdoors":
        thislist = pinkdoorlist
    elif which == "simpledoors":
        thislist = simpledoorlist
    elif which == "barriers":
        ## We consider barriers a block through which the player can't move
        barrierlist.extend(walllist)
        #barrierlist.extend(desklist)
        barrierlist.extend(boxlist)
        barrierlist.extend(automatlist)
        barrierlist.extend(fencelist)
        thislist = barrierlist
    elif which == "wallmatrix":
        ## return a matrix map of the positions of the walls
        thislist = wallmatrix

    return thislist

class Tile(pg.sprite.Sprite):
    def __init__(self, image, x, y, spritesheet):
        pg.sprite.Sprite.__init__(self)
        self.image = spritesheet.parse_sprite(image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y


    def draw(self, surface):
        ## Draw the different objects to the screen
        surface.blit(self.image, (self.rect.x, self.rect.y))


class TileMap():
    def __init__(self, filename, spritesheet):
        self.tile_size = int(DISPLAY_W / 32)
        self.start_x, self.start_y = 0, 0
        self.spritesheet = spritesheet
        self.tiles = self.load_tiles(filename)
        self.map_surface = pg.Surface((self.map_w, self.map_h))
        self.map_surface.set_colorkey((0, 0, 0))
        self.load_map()

    def draw_map(self, surface):
        surface.blit(self.map_surface, (0, 0))

    def load_map(self):
        for tile in self.tiles:
            tile.draw(self.map_surface)


    def read_csv(self, filename):
        global wallmatrix
        map = []
        with open(os.path.join(filename)) as data:
            data = csv.reader(data, delimiter = ',')
            for row in data:
                map.append(list(row))
        ## When opening Walls.csv (the walls map) add the map as matrix to wallmatrix list
        ## for the NPC for pathfinding
        if "Walls" in filename:
            wallmatrix = map
    
        return map


    def load_tiles(self, filename):
        tiles = []
        map = self.read_csv(filename)
        x, y = 0, 0
        for row in map:
            x = 0
            for tile in row:
                ## Define which object has which number in our spritesheet
                if tile == '-1':
                    self.start_x, self.start_y = x * self.tile_size, y * self.tile_size
                elif tile == '0':
                    tiles.append(Tile('automat.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                    automatlist.append((x * self.tile_size, y * self.tile_size))
                elif tile == '1':
                    tiles.append(Tile('bed_left.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                    bedlist.append((x * self.tile_size, y * self.tile_size))
                elif tile == '2':
                    tiles.append(Tile('bed_right.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                    bedlist.append((x * self.tile_size, y * self.tile_size))
                elif tile == '3':
                    tiles.append(Tile('bin_grey_empty.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                    boxlist.append((x * self.tile_size, y * self.tile_size))
                elif tile == '4':
                    tiles.append(Tile('box_wood.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                    boxlist.append((x * self.tile_size, y * self.tile_size))
                elif tile == '5':
                    tiles.append(Tile('cafeteria_box_1.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                    boxlist.append((x * self.tile_size, y * self.tile_size))
                elif tile == '6':
                    tiles.append(Tile('cafeteria_box_2.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                    boxlist.append((x * self.tile_size, y * self.tile_size))
                elif tile == '7':
                    tiles.append(Tile('cafeteria_box_empty.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                    boxlist.append((x * self.tile_size, y * self.tile_size))
                elif tile == '8':
                    tiles.append(Tile('cafeteria_floor.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '9':
                    tiles.append(Tile('carton_empty_closed.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                    boxlist.append((x * self.tile_size, y * self.tile_size))
                elif tile == '10':
                    tiles.append(Tile('carton_empty_opened.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                    boxlist.append((x * self.tile_size, y * self.tile_size))
                elif tile == '11':
                    tiles.append(Tile('cell_floor.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '12':
                    tiles.append(Tile('celldoor_2_closed.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                    celldoorlist.append((x * self.tile_size, y * self.tile_size))
                elif tile == '13':
                    tiles.append(Tile('celldoor_2_opened.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '14':
                    tiles.append(Tile('cone.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '15':
                    tiles.append(Tile('cutting_board.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '16':
                    tiles.append(Tile('desk.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                    desklist.append((x * self.tile_size, y * self.tile_size))
                elif tile == '17':
                    tiles.append(Tile('fence_metal_left.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                    fencelist.append((x * self.tile_size, y * self.tile_size))
                elif tile == '18':
                    tiles.append(Tile('fence_metal_mid.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                    fencelist.append((x * self.tile_size, y * self.tile_size))
                elif tile == '19':
                    tiles.append(Tile('fence_metal_mid_pillar.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                    fencelist.append((x * self.tile_size, y * self.tile_size))
                elif tile == '20':
                    tiles.append(Tile('fence_metal_right.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                    fencelist.append((x * self.tile_size, y * self.tile_size))
                elif tile == '21':
                    tiles.append(Tile('floor.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '22':
                    tiles.append(Tile('grass.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '23':
                    tiles.append(Tile('grass_path_end_down.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '24':
                    tiles.append(Tile('grass_path_end_left.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '25':
                    tiles.append(Tile('grass_path_end_right.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '26':
                    tiles.append(Tile('grass_path_end_up.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '27':
                    tiles.append(Tile('grass_path_front.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '28':
                    tiles.append(Tile('grass_path_intersection_3_down.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '29':
                    tiles.append(Tile('grass_path_intersection_3_left.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '30':
                    tiles.append(Tile('grass_path_intersection_3_right.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '31':
                    tiles.append(Tile('grass_path_intersection_3_up.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '32':
                    tiles.append(Tile('grass_path_intersection_4.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '33':
                    tiles.append(Tile('grass_path_side.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '34':
                    tiles.append(Tile('grass_path_turn_down_left.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '35':
                    tiles.append(Tile('grass_path_turn_down_right.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '36':
                    tiles.append(Tile('grass_path_turn_up_left.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '37':
                    tiles.append(Tile('grass_path_turn_up_right.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '38':
                    tiles.append(Tile('oven.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                    boxlist.append((x * self.tile_size, y * self.tile_size))
                elif tile == '39':
                    tiles.append(Tile('parkett_1.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '40':
                    tiles.append(Tile('parkett_2.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '41':
                    tiles.append(Tile('parkett_3.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '42':
                    tiles.append(Tile('pinkdoor_1_closed.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                    pinkdoorlist.append((x * self.tile_size, y * self.tile_size))
                elif tile == '43':
                    tiles.append(Tile('pinkdoor_1_opened.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '44':
                    tiles.append(Tile('placeholder.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '45':
                    tiles.append(Tile('plant_interiour.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                    boxlist.append((x * self.tile_size, y * self.tile_size))
                elif tile == '46':
                    tiles.append(Tile('plate.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '47':
                    tiles.append(Tile('plates.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '48':
                    tiles.append(Tile('shelve.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                    boxlist.append((x * self.tile_size, y * self.tile_size))
                elif tile == '49':
                    tiles.append(Tile('shower_left.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '50':
                    tiles.append(Tile('shower_right.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '51':
                    tiles.append(Tile('simpledoor_1_closed.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                    simpledoorlist.append((x * self.tile_size, y * self.tile_size))
                elif tile == '52':
                    tiles.append(Tile('sink.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                    boxlist.append((x * self.tile_size, y * self.tile_size))
                elif tile == '53':
                    tiles.append(Tile('stairs_beton_left.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '54':
                    tiles.append(Tile('stairs_beton_right.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '55':
                    tiles.append(Tile('toilet_left.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '56':
                    tiles.append(Tile('toilet_right.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '57':
                    tiles.append(Tile('tree_down_1.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '58':
                    tiles.append(Tile('tree_down_2.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '59':
                    tiles.append(Tile('tree_down_3.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '60':
                    tiles.append(Tile('tree_small_1.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '61':
                    tiles.append(Tile('tree_small_2.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '62':
                    tiles.append(Tile('tree_small_3.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '63':
                    tiles.append(Tile('tree_up_1.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '64':
                    tiles.append(Tile('tree_up_2.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '65':
                    tiles.append(Tile('tree_up_3.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '66':
                    tiles.append(Tile('wall.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                    walllist.append((x * self.tile_size, y * self.tile_size))

                x += 1
            y += 1

        self.map_w, self.map_h = x * self.tile_size, y * self.tile_size
        return tiles
