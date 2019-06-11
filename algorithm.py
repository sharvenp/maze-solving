

class MazeSolvingAlgorithm:

    def __init__(self, name, maze):
        self.name = name
        self.maze = maze
        self.i = 0

    def solve(self, start, end):
        raise NotImplementedError

class RecursiveBackTracker(MazeSolvingAlgorithm):

    def solve(self, start, end):
        self.i += 1