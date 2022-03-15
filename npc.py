#!/usr/bin/env python3

"""
    Felix Michelis
      07/04/2021
      dd/mm/yyyy
"""

import pygame as pg
from spritesheet import Spritesheet
from tiles import returnlist
import threading
import concurrent.futures
import random
import itertools
from tkinter import *
import time
from tiles import *
## /* Pathfinding algorithm
from system_infos import get_screen_size
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
## Pathfinding algorithm *\

## Window size
#DISPLAY_W = 1024
#DISPLAY_H = 832
DISPLAY_W, DISPLAY_H = get_screen_size()

celldoors_draw = {}
simpledoors_draw = {}

drew_celldoors = 0
drew_simpledoors = 0


class NPC(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.LEFT_KEY, self.RIGHT_KEY, self.UP_KEY, self.DOWN_KEY = False, False, False, False
        self.FACING_LEFT, self.FACING_RIGHT, self.FACING_FRONT, self.FACING_BACK = False, False, True, False
        self.load_frames()
        self.rect = self.idle_frames_left[0].get_rect()
        #self.rect.midbottom = (int(DISPLAY_W / 4.551), int(DISPLAY_H / 2.773))
        ## Set NPC position
        self.rect.x = 96
        self.rect.y = 96
        #self.rect.w = int(DISPLAY_W / 40.96)
        #self.rect.h = int(DISPLAY_W / 40.96)
        self.rect.w = 30
        self.rect.h = 30
        self.radius = 30
        self.current_frame = 0
        self.last_updated = 0
        self.velocity_x = 0
        self.velocity_y = 0
        self.speed_x = 5
        self.speed_y = 5
        self.state = 'idle'
        self.current_image = self.idle_frames_front[0]
        self.positions = []
        self.infos = False
        self.show_next_point_of_path = False
        self.path = ()
        ## To which side NPC should move that means that on the other side there is a wall
        self.move_to = 'None'
        
    ##-----DEBUG-----##
        
    def show_result(self, result):
        result_window = Tk()
        result_window.geometry("80x80")
        E1 = Label(result_window, text = str(result))
        E1.pack(side = LEFT)
        result_window.mainloop()
        
    def show_many_results(self):
        def show():
            results = ("FACING LEFT: " + str(self.FACING_LEFT), "FACING RIGHT: " + str(self.FACING_RIGHT), "FACING FRONT: " + str(self.FACING_FRONT), "FACING BACK: " + str(self.FACING_BACK),
                       "POSITION (x,y): " + str(self.rect.x) + ", " + str(self.rect.y), "POSITION/32: " + str(int(self.rect.x/int(DISPLAY_W/32))) + "," + str(int(self.rect.y/int(DISPLAY_W/32))),
                       "RECT SIZE (w,h): " + str(self.rect.w) + ", " + str(self.rect.h),
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
        result_window.title("NPC")
        show()
        result_window.mainloop()
        
    def commands(self, command):
        if command == "NPC":
            show_npc_info = threading.Thread(target = self.show_many_results)
            show_npc_info.start()
        elif "NPC.rect=" in command:
            self.rect.x, self.rect.y = map(int, re.findall(r'\d+', command))
        elif command == "PAUSE INFOS":
            self.infos = False
        elif command == "CONTINUE INFOS":
            self.infos = True
        elif command == "PAUSE SHOW NPC-PATH":
            self.show_next_point_of_path = False
        elif command == "CONTINUE SHOW NPC-PATH":
            self.show_next_point_of_path = True
        
    ##-----DEBUG-----##
    
    def draw(self, display):
        ## Draw the image of the NPC to the screen
        display.blit(self.current_image, self.rect)
        if self.show_next_point_of_path:
            try:
                point = pg.draw.rect(display, pg.Color('red'), (int(self.path[0][0] * 32), int(self.path[0][1] * 32), 32, 32))
            except:
                pass
        if self.infos:
            print(f'[NPC][PATH]: Length is, {len(self.path)}')
        
    ##-----MOVEMENT/UPDATE-----##

    def process_wallmapmatrix(self):
        ## Ask the tiles.py programm to give us a matrix map with the positions of the walls
        ## The matrix has a size of 32x26 and all information in it is a string
        get_wallmapmatrix = returnlist("wallmatrix")
        if self.infos:
            print("[NPC][MATRIX]: returned matrix")
            print(get_wallmapmatrix)

        """
            Create empty matrix of the size of the matrix we get because if we use the same matrix
            inside this function we have the problem that when we try to get the matrix a second time,
            the matrix is already defined and converted to 0 and 1. So when replacing in the for loop,
            everything will be set to 0 and we are stuck in an infinite while loop in self.choose_endpoint()
        """
        wallmapmatrix = [[0 for x in range(len(get_wallmapmatrix[0]))] for y in range(len(get_wallmapmatrix))]

        """        
            change the information inside the matrix to be a integer
            and replace the values 66 (=wall) to 0 and -1 (=floor) to 1
            i = y and j = x as matrices take y first (there also is 67 which is
            an empty rectangle which works as barrier for example on a place where
            there is a flower pot or something else that is not a wall and 18 and
            19 which are fences
        """
        for i in range(len(get_wallmapmatrix)):
            for j in range(len(get_wallmapmatrix[0])):
                if get_wallmapmatrix[i][j] == '66':
                    wallmapmatrix[i][j] = 0
                elif get_wallmapmatrix[i][j] == '-1':
                    wallmapmatrix[i][j] = 1
                else:
                    ## in case there is an unknown information we set it as wall to be sure to not go there in case there is an error
                    wallmapmatrix[i][j] = 0

        if self.infos:
            print("\n")
            print("[NPC][MATRIX]: FINISHED MATRIX")
            print(wallmapmatrix)
        ## Delete the matrix with the walls we got to be sure that the next time this function is executed,
        ## the other script will be asked again for a matrix so we have a recent matrix (Because of the problem explained above)
        del get_wallmapmatrix
        
        return wallmapmatrix

    def calculate_position_from32(self):
        position_x = int(self.rect.x/32)
        position_y = int(self.rect.y/32)
        if self.infos:
            print("[NPC][CALCULATE_POSITION_FROM32]: POSITION TRANSFORMED")
            
        return position_x, position_y
    
    def choose_endpoint(self, matrix):
        choosing = True
        while choosing:
            ## As matrices take y first and the x we have to tell the matrix that we want x
            endpoint_x = random.randrange(0, len(matrix[0]))
            endpoint_y = random.randrange(0, len(matrix))
            if self.infos:
                print(f'[NPC][ENDPOINTS]: POINTS CHOSEN; {endpoint_x}, {endpoint_y}')

            if matrix[endpoint_y][endpoint_x] == 0:
                if self.infos:
                    print(f'[NPC][ENDPOINTS]: RESULT IN MATRIX: {matrix[endpoint_y][endpoint_x]}')
                    print("[NPC][ENDPOINTS]: POINTS NOT ACCEPTABLE")
                continue
            else:
                if self.infos:
                    print("[NPC][ENDPOINTS]: FOUND ACCEPTABLE EDNPOINT")
                    
                choosing = False
        
        return endpoint_x, endpoint_y
            
    def pathfinder(self):
        ## Find the shortest path from start (=NPC position) to end (=random point that changes as soon as NPC arrives there)

        ## Tell our algorithm which matrix to use
        matrix = self.process_wallmapmatrix()
        grid = Grid(matrix = matrix)

        ## Define start and end points for the way
        startpoint_x, startpoint_y = self.calculate_position_from32()
        start = grid.node(int(startpoint_x), int(startpoint_y))

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(self.choose_endpoint, matrix)
            endpoint_x, endpoint_y = future.result()
            
        #endpoint_x, endpoint_y = self.choose_endpoint(matrix)
        end = grid.node(int(endpoint_x), int(endpoint_y))

        ## Define which algorithm to use and if NPC is allowed to move diagonally which we do not want as he could be stuck
        finder = AStarFinder(diagonal_movement = DiagonalMovement.never)
        path, runs = finder.find_path(start, end, grid)

        if self.infos == True:
            print(grid.grid_str(path=path, start=start, end=end))
            ## Path is a list of the coordinates of each step of the size of 32 px the NPC has to make to reach the end
            print(path)

        self.path = path
        
    def calculate_position_to32(self):
        path = self.path

        ## Take x and y from the first tuple from the list
        pos_x = path[0][0]
        pos_y = path[0][1]

        ## Convert the coordinates from 1, 3 to px (= 32, 96)
        goto_x = int(pos_x * 32)
        goto_y = int(pos_y * 32)

        return goto_x, goto_y
    
    def update(self, deltaTime):
        ## Set NPC movement to 0 in both directions (x, y)
        self.velocity_x, self.velocity_y = 0, 0
        
        ## Check if NPC has reached the end of the path
        if len(self.path) < 1:
            self.pathfinder()

        pos_x, pos_y = self.calculate_position_to32()

        if self.rect.x < pos_x:
            self.velocity_x += self.speed_x * deltaTime
        elif self.rect.x > pos_x:
            self.velocity_x -= self.speed_x * deltaTime
        if self.rect.y < pos_y:
            self.velocity_y += self.speed_y * deltaTime
        elif self.rect.y > pos_y:
            self.velocity_y -= self.speed_y * deltaTime

        ## Apply movement to the position of the image
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        ## Find out in which direction NPC is moving
        self.set_state()
        ## Make the NPC look animated (= change the image each frame)
        self.animate()

    def set_state(self):
        ## REset the state to 'idle' = not moving
    	self.state = 'idle'
    	## If moving to the right: self.state = 'moving right'
    	if self.velocity_x > 0:
    		self.state = 'moving right'
    	## If moving left ...
    	elif self.velocity_x < 0:
    		self.state = 'moving left'
    	## If moving down ...
    	elif self.velocity_y > 0:
    		self.state = 'moving down'
    	## If moving up ...
    	elif self.velocity_y < 0:
    		self.state = 'moving up'
    		
    ##-----MOVEMENT/UPDATE-----##
    		
    def animate(self):
        ## Change the image of the NPC according to the direction he is walking or if he is walking
        try:
            ## get the actual time passed since the start of the programm
            now = pg.time.get_ticks()
            ## If NPC not moving he should look to the front
            if self.state == 'idle':
                """
                    If the time passed by since the start of the programm - the time animate() was last called > 200
                    Set self.last_updated to the time passed until now since the start of the programm
                    Then find the matching frame to the direction NPC is facing
                """
                if now - self.last_updated > 200:
                    self.last_updated = now
                    self.current_frame = (self.current_frame + 1) % len(self.idle_frames_left)
                if self.FACING_LEFT:
                    self.current_image = self.idle_frames_left[self.current_frame]
                elif self.FACING_RIGHT:
                    self.current_image = self.idle_frames_right[self.current_frame]
                elif self.FACING_FRONT:
                    self.current_image = self.idle_frames_front[self.current_frame]
                elif self.FACING_BACK:
                    self.current_image = self.idle_frames_back[self.current_frame]
            else:
                if now - self.last_updated > 100:
                    self.last_updated = now
                    self.current_frame = (self.current_frame + 1) % len(self.walking_frames_left)
                    if self.state == 'moving left':
                        self.current_image = self.walking_frames_left[self.current_frame]
                    elif self.state == 'moving right':
                        self.current_image = self.walking_frames_right[self.current_frame]
                    elif self.state == 'moving up':
                        self.current_image = self.walking_frames_back[self.current_frame]
                    elif self.state == 'moving down':
                        self.current_image = self.walking_frames_front[self.current_frame]
        except:
            ## As sometimes there is the error 'list out of range self.idle_frames_front[]' we skip the error as it does not affect the movement or the look of the NPC
            self.current_image = self.idle_frames_front[0]
            print("[NPC][Self.Animate]: ERROR | usually 'list out of range' in self.idle_frames_front[]")

    def load_frames(self):
        ## Load the images of the NPC character
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

    def openCelldoor(self, a, b):
        ## Add the doors that should be open to a list
        global celldoors_draw
        door_img = pg.transform.scale(pg.image.load("Images/GameImages/celldoor_2_opened.png"), (int(DISPLAY_W / 32), int(DISPLAY_W / 32)))
        door_rect = door_img.get_rect(x = a, y = b)

        celldoors_draw[door_img] = door_rect
		#self.draw_celldoors(display)

    def draw_celldoors(self, display):
        ## Draw the doors that should be open from list to screen
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
        ## Add the position of all the opened door to a list
        global simpledoors_draw
        door_img = pg.transform.scale(pg.image.load("Images/GameImages/simpledoor_1_opened.png"), (int(DISPLAY_W / 32), int(DISPLAY_W / 32)))
        door_rect = door_img.get_rect(x = a, y = b)
        simpledoors_draw[door_img] = door_rect

    def draw_simpledoors(self, display):
        ## Draw all opened doors from the list to the screen
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

    def check_collision(self, walls, celldoors, simpledoors, deltaTime, display):
        if self.infos:
            print(f'[NPC][Self.Position]: {self.rect.x}, {self.rect.y}')
        ## Collision with wall
        for a, b in walls:
            wallholder = pg.Rect(a, b, int(DISPLAY_W / 34.13), int(DISPLAY_W / 34.13))
            if self.rect.colliderect(wallholder):
                if self.rect.collidepoint(wallholder.midleft):
                    self.rect.x -= self.speed_x * deltaTime
                    #self.rect.x = wallholder.x + wallholder.w
                    self.move_to = "right"
                elif self.rect.collidepoint(wallholder.midright):
                    self.rect.x += self.speed_x * deltaTime
                    #self.rect.x = wallholder.x - wallholder.w
                    self.move_to = "left"
                    
                elif self.rect.collidepoint(wallholder.topleft):
                    self.rect.x -= self.speed_x * deltaTime
                    self.rect.y -= self.speed_y * deltaTime
                elif self.rect.collidepoint(wallholder.topright):
                    self.rect.x += self.speed_x * deltaTime
                    self.rect.y -= self.speed_y * deltaTime
                elif self.rect.collidepoint(wallholder.bottomleft):
                    self.rect.x -= self.speed_x * deltaTime
                    self.rect.y += self.speed_y * deltaTime
                elif self.rect.collidepoint(wallholder.bottomright):
                    self.rect.x += self.speed_x * deltaTime
                    self.rect.y += self.speed_y * deltaTime
                    
                elif self.rect.collidepoint(wallholder.midbottom):
                    self.rect.y += self.speed_y * deltaTime
                    #self.rect.y = wallholder.y + wallholder.h
                    self.move_to = "down"
                elif self.rect.collidepoint(wallholder.midtop):
                    self.rect.y -= self.speed_y * deltaTime
                    #self.rect.y = wallholder.y - wallholder.h
                    self.move_to = "up"

        ## If comes near to door, door should open
        for a, b in celldoors:
            celldoorholder = pg.Rect(int(a-5), int(b-5), int(DISPLAY_W / 25.6), int(DISPLAY_W / 25.6))
            if self.rect.colliderect(celldoorholder):
                self.openCelldoor(a, b)
        for a, b in simpledoors:
            simpledoorholder = pg.Rect(int(a-5), int(b-5), int(DISPLAY_W / 25.6), int(DISPLAY_W / 25.6))
            if self.rect.colliderect(simpledoorholder):
                self.openSimpledoor(a, b)

        ## Next point to go from path
        point = pg.Rect(int(self.path[0][0] * 32), int(self.path[0][1] * 32), 32, 32)
        if self.rect.colliderect(point):
            del self.path[0]




