import numpy as np
import math as m
import random as r
from PIL import Image, ImageDraw
import pygame as pg
import time as t
import threading

from algorithm import RecursiveBackTracker

class MazeGenerator:

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def get_new_maze(self):        

        maze = np.ones((self.height, self.width))
        maze[0][0] = 0
        self._step(maze, 0, 0)
        maze = np.pad(maze, [(1, (self.height % 2)), (1, (self.width % 2))], 'constant', constant_values=1)
        img = Image.fromarray(np.uint8((np.ones(maze.shape) - maze)*255) , 'L')
        img.save('resources/maze.png', 'PNG')

        return maze

    def _step(self, maze, row, col):
        
        while True:
            directions = []

            if 0 <= col + 2 <= self.width - 1 and maze[row][col + 2] == 1:  # Right
                directions.append((0, 2))
            if 0 <= col - 2 <= self.width - 1 and maze[row][col - 2] == 1:  # Left
                directions.append((0, -2))
            if 0 <= row - 2 <= self.height - 1 and maze[row - 2][col] == 1: # Up
                directions.append((-2, 0))
            if 0 <= row + 2 <= self.height - 1 and maze[row + 2][col] == 1: # Down
                directions.append((2, 0))
            
            if directions:
                chosen_direction = r.choice(directions)
                dr, dc = chosen_direction
                maze[row + dr][col + dc] = 0
                maze[row + (dr//2)][col + (dc//2)] = 0
                self._step(maze, row + dr, col + dc)
            else:
                break

class MazeSolver:

    def __init__(self, width, height):
        self.width, self.height = width, height
        self.maze_generator = MazeGenerator(width, height)

        # RGB Colors
        self.WALL_COLOR = (80, 80, 80)
        self.PATH_COLOR = (255, 255, 255)
        self.START_COLOR = (255, 0, 0)
        self.END_COLOR = (0, 255, 0)

    def convert_real_pos_to_grid(self, real_pos, scale):
        rx, ry = real_pos

        return (rx // scale, ry // scale)

    def draw_maze(self, screen, scale):

        self.start = (1,1)
        self.end = (self.maze.shape[1] - 2, self.maze.shape[0] - 2)

        for row in range(self.maze.shape[0]):
            for col in range(self.maze.shape[1]):
                val = self.maze[row][col]
                if val == 1:
                    c = self.WALL_COLOR
                elif val == 0:
                    c = self.PATH_COLOR
                pg.draw.rect(screen, c, (col * scale, row * scale, scale, scale))

        pg.draw.rect(screen, self.START_COLOR, (self.start[0] * scale, self.start[1] * scale, scale, scale))
        pg.draw.rect(screen, self.END_COLOR, (self.end[0] * scale, self.end[1] * scale, scale, scale))

    def run(self, scale, frame_rate):
        
        pg.init()        
        
        screen = pg.display.set_mode(((self.width + 2) * scale, (self.height + 2) * scale))    
        pg.display.set_caption('Maze Solving Algorithms')

        self.maze = self.maze_generator.get_new_maze()
        self.draw_maze(screen, scale)

        rbt = RecursiveBackTracker("Recursive Back Tracker", self.maze)

        while True:

            # Exit Condition
            e = pg.event.poll()
            if e.type == pg.QUIT:
                return
            keys = pg.key.get_pressed()
            if keys[pg.K_ESCAPE] or keys[pg.K_SLASH]:
                return

            solving = False

            if keys: # Change start and end position
                mx, my = self.convert_real_pos_to_grid(pg.mouse.get_pos(), scale)
                if 0 <= mx <= self.width and 0 <= my <= self.height and self.maze[my][mx] != 1:
                    if keys[pg.K_s]: # Left Mouse
                        pg.draw.rect(screen, self.PATH_COLOR, (self.start[0] * scale, self.start[1] * scale, scale, scale))
                        pg.draw.rect(screen, self.START_COLOR, (mx * scale, my * scale, scale, scale))
                        self.start = (mx, my)
                    elif keys[pg.K_e]: # Right Mouse
                        pg.draw.rect(screen, self.PATH_COLOR, (self.end[0] * scale, self.end[1] * scale, scale, scale))
                        pg.draw.rect(screen, self.END_COLOR, (mx * scale, my * scale, scale, scale))
                        self.end = (mx, my)

            if keys[pg.K_m]: # Generate new maze
                self.maze = self.maze_generator.get_new_maze()
                self.draw_maze(screen, scale)

                
            # solving = True
            # solving_thread = threading.Thread(target = rbt.solve, args = (start, end))

            while solving:
                print(rbt.i)


            t.sleep(1/frame_rate)
            pg.display.update()

def main():
    ms = MazeSolver(51, 51)
    ms.run(10, 60)

if __name__ == "__main__":
    main()