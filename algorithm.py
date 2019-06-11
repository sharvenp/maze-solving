
import time as t
import pygame as pg

class MazeSolvingAlgorithm:

    def __init__(self, maze):
        self.maze = maze
        self.height, self.width = maze.shape
        self.solving = False

        pg.init()

    def solve(self, start, end, screen, scale):
        raise NotImplementedError

class NoAlgorithm(MazeSolvingAlgorithm):

    def solve(self):
        print("Null Algorithm")
        raise NotImplementedError

class RecursiveBackTracker(MazeSolvingAlgorithm):

    def __init__(self, maze):

        MazeSolvingAlgorithm.__init__(self, maze)
        self.SOLVE_COLOR = (255, 0, 255)
        self.THINK_COLOR = (0, 0, 255)

    def solve(self, screen, scale, start, end):

        print("Starting Recursive Backtracking Maze Solver")
        self.solving = True
        self._solve_step(start[1], start[0], end, screen, scale)
        self.solving = False

    def _solve_step(self, row, col, end, screen, scale):

        while True:
            
            if not self.solving:
                pg.draw.rect(screen, self.SOLVE_COLOR, (col * scale, row * scale, scale, scale))
                break

            directions = []

            if 0 <= col + 1 <= self.width - 1 and self.maze[row][col + 1] == 0:  # Right
                directions.append((0, 1))
            if 0 <= col - 1 <= self.width - 1 and self.maze[row][col - 1] == 0:  # Left
                directions.append((0, -1))
            if 0 <= row - 1 <= self.height - 1 and self.maze[row - 1][col] == 0: # Up
                directions.append((-1, 0))
            if 0 <= row + 1 <= self.height - 1 and self.maze[row + 1][col] == 0: # Down
                directions.append((1, 0))
            
            if directions:

                for d in directions:
                    dr, dc = d
                    if row + dr == end[1] and col + dc == end[0]:
                        self.solving = False
                        break

                chosen_direction = directions.pop()
                dr, dc = chosen_direction
                nr, nc = row + dr, col + dc
                self.maze[nr][nc] = 2
                pg.draw.rect(screen, self.THINK_COLOR, (nc * scale, nr * scale, scale, scale))
                self._solve_step(nr, nc, end, screen, scale)
            else:
                break