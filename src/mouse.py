from enum import Enum
from src.rewards import Reward


class Mouse:  # Characters can move around and do cool stuff
    class Moves(Enum):
        UP = 0
        DOWN = 1
        LEFT = 2
        RIGHT = 3

        @classmethod
        def num_to_move(cls, number):
            return {0: cls.UP, 1: cls.DOWN, 2: cls.LEFT, 3: cls.RIGHT}[number]

    def __init__(self, column, row, maze):
        self.column = column
        self.row = row
        self.maze = maze
        self.tries = 0

        self.maze.grid[self.row][self.column] = 2

    def move(self, direction) -> Reward:
        """
        This function is how a character moves around in a certain direction
        """
        self.tries += 1
        return {
            self.Moves.UP: self.move_up,
            self.Moves.DOWN: self.move_down,
            self.Moves.LEFT: self.move_left,
            self.Moves.RIGHT: self.move_right,
        }[direction]()

    def move_up(self) -> Reward:
        if self.row > 0 and not self.collision(self.Moves.UP):
            self.maze.grid[self.row][self.column] = 4

            self.row -= 1

            was_end_reached = self.maze.grid[self.row][self.column] == 3
            was_visited = self.maze.grid[self.row][self.column] == 4

            self.maze.grid[self.row][self.column] = 2

            if was_visited:
                return Reward.VISITED
            elif was_end_reached:
                return Reward.FINISH
            else:
                return Reward.MOVE
        return Reward.COLLISION

    def move_down(self) -> Reward:
        if self.row < self.maze.height - 1 and not self.collision(self.Moves.DOWN):
            self.maze.grid[self.row][self.column] = 4

            self.row += 1

            was_end_reached = self.maze.grid[self.row][self.column] == 3
            was_visited = self.maze.grid[self.row][self.column] == 4

            self.maze.grid[self.row][self.column] = 2

            if was_visited:
                return Reward.VISITED
            elif was_end_reached:
                return Reward.FINISH
            else:
                return Reward.MOVE
        return Reward.COLLISION

    def move_left(self) -> Reward:
        if self.column > 0 and not self.collision(self.Moves.LEFT):
            self.maze.grid[self.row][self.column] = 4

            self.column -= 1

            was_end_reached = self.maze.grid[self.row][self.column] == 3
            was_visited = self.maze.grid[self.row][self.column] == 4

            self.maze.grid[self.row][self.column] = 2

            if was_visited:
                return Reward.VISITED
            elif was_end_reached:
                return Reward.FINISH
            else:
                return Reward.MOVE
        return Reward.COLLISION

    def move_right(self) -> Reward:
        if self.column < self.maze.width - 1 and not self.collision(self.Moves.RIGHT):
            self.maze.grid[self.row][self.column] = 4

            self.column += 1

            was_end_reached = self.maze.grid[self.row][self.column] == 3
            was_visited = self.maze.grid[self.row][self.column] == 4

            self.maze.grid[self.row][self.column] = 2

            if was_visited:
                return Reward.VISITED
            elif was_end_reached:
                return Reward.FINISH
            else:
                return Reward.MOVE
        return Reward.COLLISION

    def collision(self, direction: Moves) -> bool:
        """
        Checks if anything is on top of the grass in the direction
        that the character wants to move. Used in the move function
        """
        if direction == self.Moves.UP:
            if self.maze.grid[self.row - 1][self.column] == 1:
                return True
        elif direction == self.Moves.LEFT:
            if self.maze.grid[self.row][self.column - 1] == 1:
                return True
        elif direction == self.Moves.RIGHT:
            if self.maze.grid[self.row][self.column + 1] == 1:
                return True
        elif direction == self.Moves.DOWN:
            if self.maze.grid[self.row + 1][self.column] == 1:
                return True
        return False

    def reset(self, target_reached):
        for row in range(self.maze.height):
            for column in range(self.maze.width):
                if self.maze.grid[row][column] == 4:
                    self.maze.grid[row][column] = 0

        self.maze.grid[self.row][self.column] = 3 if target_reached else 0
        self.column = 0
        self.row = 0
        self.maze.grid[self.row][self.column] = 2
        self.tries = 0
