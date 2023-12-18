from enum import Enum


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

        self.maze.grid[self.row][self.column] = 2

    def move(self, direction) -> int:
        """
        This function is how a character moves around in a certain direction
        """
        return {
            self.Moves.UP: self.move_up,
            self.Moves.DOWN: self.move_down,
            self.Moves.LEFT: self.move_left,
            self.Moves.RIGHT: self.move_right,
        }[direction]()

    def move_up(self) -> int:
        if self.row > 0 and not self.collision(self.Moves.UP):
            self.maze.grid[self.row][self.column] = 0
            self.row -= 1

            self.end_reached()

            self.maze.grid[self.row][self.column] = 2
            return 5
        return -5

    def move_down(self) -> int:
        if self.row < self.maze.height - 1 and not self.collision(self.Moves.DOWN):
            self.maze.grid[self.row][self.column] = 0
            self.row += 1

            self.end_reached()

            self.maze.grid[self.row][self.column] = 2
            return 5
        return -5

    def move_left(self) -> int:
        if self.column > 0 and not self.collision(self.Moves.LEFT):
            self.maze.grid[self.row][self.column] = 0
            self.column -= 1

            self.end_reached()

            self.maze.grid[self.row][self.column] = 2
            return 5
        return -5

    def move_right(self) -> int:
        if self.column < self.maze.width - 1 and not self.collision(self.Moves.RIGHT):
            self.maze.grid[self.row][self.column] = 0
            self.column += 1

            self.end_reached()

            self.maze.grid[self.row][self.column] = 2
            return 5
        return -5

    def collision(self, direction: Moves) -> bool:
        """
        Checks if anything is on top of the grass in the direction
        that the character wants to move. Used in the move function
        """
        if direction == self.Moves.UP:
            if self.maze.grid[self.row - 1][self.column] != 0:
                return True
        elif direction == self.Moves.LEFT:
            if self.maze.grid[self.row][self.column - 1] != 0:
                return True
        elif direction == self.Moves.RIGHT:
            if self.maze.grid[self.row][self.column + 1] != 0:
                return True
        elif direction == self.Moves.DOWN:
            if self.maze.grid[self.row + 1][self.column] != 0:
                return True
        return False

    def reset(self):
        self.maze.grid[self.row][self.column] = 0
        self.column = 0
        self.row = 0
        self.maze.grid[self.row][self.column] = 2

    def end_reached(self) -> int:
        if self.maze.grid[self.row][self.column] == 3:
            return 10
        return 0
