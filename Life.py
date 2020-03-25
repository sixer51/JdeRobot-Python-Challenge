# Game of Life
# python Challenge for GSOC 2020 JdeRobot
# author: Yijia Wu

# show changeable pattern in terminal(Done!)
# evolution mechanisim
# json read and write(Done!)
# test cases
# application

import json
import numpy as np
import time
import sys
import curses

LIVE = 1
DEAD = 0

class Life:
    def __init__(self, path):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)

        with open(path, 'r') as file:
            setting = json.load(file)
        #setting = json.loads(setting)

        self.init_pattern = np.matrix(setting['pattern'])
        self.curr_pattern = self.init_pattern
        self.next_pattern = self.init_pattern
        self.show_pattern()

    def show_pattern(self):
        # sys.stdout.write("\r" + str(self.next_pattern))
        # sys.stdout.flush()
        self.stdscr.clear()
        self.stdscr.addstr(str(self.next_pattern))
        self.stdscr.refresh()
        time.sleep(0.5)

    def end(self):
        curses.nocbreak()
        self.stdscr.keypad(True)
        curses.echo()
        curses.endwin()

    def count_live_neighbours(self, i, j):
        shape = self.init_pattern.shape
        row_min = max(0, i-1)
        row_max = min(i+1, shape[0]-1)
        col_min = max(0, j-1)
        col_max = min(j+1, shape[1]-1)

        # get the sum of surrounding cells
        sum_live_cells = self.curr_pattern[row_min:row_max+1, 
                    col_min:col_max+1].sum() - self.curr_pattern[i, j]

        return sum_live_cells

    def cell_is_live(self, i, j):
        num = self.count_live_neighbours(i, j)
        #print(num)
        if self.curr_pattern[i, j] == DEAD and num == 3:
            return True
        elif self.curr_pattern[i, j] == LIVE and (num == 2 or num == 3):
            return True
        return False

    def update(self):
        shape = self.init_pattern.shape
        self.curr_pattern = self.next_pattern
        for row in range(shape[0]):
            for col in range(shape[1]):
                if self.cell_is_live(row, col):
                    self.next_pattern[row, col] = LIVE
                else:
                    self.next_pattern[row, col] = DEAD
        self.show_pattern()
