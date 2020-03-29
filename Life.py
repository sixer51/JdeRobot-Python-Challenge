# Game of Life
# python Challenge for GSOC 2020 JdeRobot
# author: Yijia Wu

import json
import numpy as np
import random
from copy import copy
import time
import sys
import curses

DEAD = 0
LIVE = 1

class GameofLife:
    def __init__(self):
        self.stdscr = 0
        default_path = 'config.json'

        with open(default_path, 'r') as file:
            setting = json.load(file)
        self.row = setting['size'][0]
        self.column = setting['size'][1]
        self.percent_dead = setting['dead']['percentage']
        self.percent_live = setting['live']['percentage']
        self.dead_symbol = setting['dead']['symbol']
        self.live_symbol = setting['live']['symbol']
        self.title = setting['title']
        self.introduction = setting['introduction']
        self.iteration = setting['iteration']
        self.mode = "random"

        if setting['world'] != []:
            self.init_world = np.matrix(setting['world'])
        else:
            world = np.random.choice([DEAD, LIVE], self.row*self.column, 
                p = [self.percent_dead, self.percent_live]).reshape(self.row, self.column)
            self.init_world = np.matrix(world.tolist())

        self.curr_world = self.init_world
        self.next_world = self.init_world
        self.time_interval = 0.3

    # load new config file
    def load(self, path):
        print("loaded "+path)
        with open(path, 'r') as file:
            setting = json.load(file)
        self.row = setting['size'][0]
        self.column = setting['size'][1]
        self.percent_dead = setting['dead']['percentage']
        self.percent_live = setting['live']['percentage']
        self.dead_symbol = setting['dead']['symbol']
        self.live_symbol = setting['live']['symbol']
        self.title = setting['title']
        self.introduction = setting['introduction']
        self.iteration = setting['iteration']
        self.mode = "random"

        if setting['world'] != []:
            self.init_world = np.matrix(setting['world'])
        else:
            world = np.random.choice([DEAD, LIVE], self.row*self.column, 
                p = [self.percent_dead, self.percent_live]).reshape(self.row, self.column)
            self.init_world = np.matrix(world.tolist())

        self.curr_world = self.init_world
        self.next_world = self.init_world

    # generate new initial world
    def generate_new_world(self):
        # in random mode: generate a random new world
        if self.mode == "random":
            world = np.random.choice([DEAD, LIVE], self.row*self.column, 
                    p = [self.percent_dead, self.percent_live]).reshape(self.row, self.column)
            self.init_world = np.matrix(world.tolist())
        # in pattern mode: generate a empty world and add new patterns
        elif self.mode == "pattern":
            self.init_world = np.zeros([self.row, self.column])
        self.curr_world = self.init_world
        self.next_world = self.init_world
    
    # show current world in terminal
    def show_world(self, iter):
        self.stdscr.clear()
        self.stdscr.addstr(self.title+'\n')
        self.stdscr.addstr(self.introduction+'\n')
        self.stdscr.addstr("iteration / total iteration: "+str(iter)+
                            "/"+str(self.iteration)+'\n')

        for i in range(self.next_world.shape[0]):
            for j in range(self.next_world.shape[1]):
                if self.next_world[i, j] == LIVE:
                    self.stdscr.addstr(self.live_symbol+' ')
                else:
                    self.stdscr.addstr(self.dead_symbol+' ')
            self.stdscr.addstr('\n') 

        self.stdscr.refresh()
        time.sleep(self.time_interval)

    # print initial world in terminal when changing setting
    def print_init_world(self):
        for i in range(self.init_world.shape[0]):
            for j in range(self.init_world.shape[1]):
                if self.init_world[i, j] == LIVE:
                    print(self.live_symbol, end=' ')
                else:
                    print(self.dead_symbol, end=' ')
            print('') 

    # print all available settings
    def print_setting(self):
        print("1: size = "+str(self.row)+"*"+str(self.column))
        print("2: iteration = "+str(self.iteration))
        print("3: init mode = "+self.mode)
        print("world:"+str(self.live_symbol)+" is live cell, "
                +str(self.dead_symbol)+" is dead cell")
        self.print_init_world()

    # change the settings
    def change_setting(self):
        self.print_setting()
        finish = False

        while not finish:
            task = input("Please input the index of setting you want to change: ")
            if task == "1":
                self.row = int(input("row = "))
                self.column = int(input("column = "))
                self.generate_new_world()
            elif task == "2":
                self.iteration = int(input("iteration = "))
            elif task == "3":
                mode = int(input("Choose world init mode: 0 for random, 1 for pattern"))
                if mode == 0: self.mode = "random"
                elif mode == 1: self.mode = "pattern"
                self.generate_new_world()
                self.add_block(int(input("Enter number of block: ")))
                self.print_init_world()
                self.add_blinker(int(input("Enter number of blinker: ")))
                self.print_init_world()
                self.add_glider(int(input("Enter number of glider: ")))
                self.print_init_world()

            self.print_setting()
            finish = True if input("Finish setting?(y or n)") == 'y' else False

    # initialize curse and update the world
    def auto_generate(self):
        self.stdscr = curses.initscr()
        win_size = self.stdscr.getmaxyx()
        if self.row+4 >= win_size[0] or self.column*2 >= win_size[1]:
            self.end()
            print("[ERROR] The size of world is too large. Please reduce the size or maximize your windows")
            return
        if self.row <= 0 or self.column <= 0:
            self.end()
            print("[ERROR] The size of world is too small.")
            return

        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)
        self.show_world(0)
        for iter in range(self.iteration):
            self.update(iter+1)   
        self.end()  

    # end current game
    def end(self):
        curses.nocbreak()
        self.stdscr.keypad(True)
        curses.echo()
        curses.endwin()
        self.generate_new_world()

    # count live neighbour of a cell
    def count_live_neighbours(self, i, j):
        shape = self.init_world.shape
        row_min = max(0, i-1)
        row_max = min(i+1, shape[0]-1)
        col_min = max(0, j-1)
        col_max = min(j+1, shape[1]-1)

        # get the sum of surrounding cells
        sum_live_cells = self.curr_world[row_min:row_max+1, 
                    col_min:col_max+1].sum() - self.curr_world[i, j]

        return sum_live_cells

    # find if the cell will be live in next generation
    def cell_is_live(self, i, j):
        num = self.count_live_neighbours(i, j)
        if self.curr_world[i, j] == DEAD and num == 3:
            return True
        elif self.curr_world[i, j] == LIVE and (num == 2 or num == 3):
            return True
        return False

    # update current world to the nect generation
    def update(self, iter):
        shape = self.init_world.shape
        self.curr_world = copy(self.next_world)
        for row in range(shape[0]):
            for col in range(shape[1]):
                if self.cell_is_live(row, col):
                    self.next_world[row, col] = LIVE
                else:
                    self.next_world[row, col] = DEAD
        self.show_world(iter)

    # check if the size of the world can contain the pattern
    def check_size(self, world_shape, pattern_shape):
        if world_shape[0] < pattern_shape[0] or world_shape[1] < pattern_shape[1]:
            print("[ERROR] The world is too small to contain this pattern")
            return True
        return False

    # add block pattern in random position
    def add_block(self, num):
        shape = self.init_world.shape
        if self.check_size(shape, (2, 2)): return
        for _ in range(num):
            row = random.randrange(shape[0]-1)
            column = random.randrange(shape[1]-1)
            self.init_world[row:row+2, column:column+2] = np.array([[1, 1], [1, 1]])

    # add blinker pattern in random position
    def add_blinker(self, num):
        shape = self.init_world.shape
        if self.check_size(shape, (3, 3)): return
        for _ in range(num):
            row = random.randrange(shape[0]-2)
            column = random.randrange(shape[1]-2)
            self.init_world[row:row+3, column:column+3] = np.array([[0, 0, 0], [1, 1, 1], [0, 0, 0]])

    # add glider pattern in random position
    def add_glider(self, num):
        shape = self.init_world.shape
        if self.check_size(shape, (3, 3)): return
        for _ in range(num):
            row = random.randrange(shape[0]-2)
            column = random.randrange(shape[1]-2)
            self.init_world[row:row+3, column:column+3] = np.array([[0, 0, 1], [1, 0, 1], [0, 1, 1]])

    # start the game
    def main(self):
        print("Welcome to Game of Life")

        # use default setting?
        self.print_setting()
        default = True if input("Use default setting?(y or n)") == 'y' else False
        if not default: self.change_setting()

        print("======================================")
        start = True if input("Start?(y or n)") == 'y' else False
        while start:
            self.auto_generate()
            end = True if input("End?(y or n)") == 'y' else False
            if end: break

            change = True if input("Change setting?(y or n)") == 'y' else False
            if change: self.change_setting()
            print("======================================")
            start = True if input("Start?(y or n)") == 'y' else False