class Mouse:  # Characters can move around and do cool stuff
    def __init__(self, column, row, maze):
        self.column = column
        self.row = row
        self.maze = maze

        self.maze.grid[self.row][self.column] = 2

    def move(
        self, direction
    ):  # This function is how a character moves around in a certain direction
        {
            "UP": self.move_up,
            "DOWN": self.move_down,
            "LEFT": self.move_left,
            "RIGHT": self.move_right,
        }[direction]()

    def move_up(self):
        if self.row > 0 and not self.collision("UP"):
            self.maze.grid[self.row][self.column] = 0
            self.row -= 1
            self.maze.grid[self.row][self.column] = 2

    def move_down(self):
        if self.row < self.maze.height - 1 and not self.collision("DOWN"):
            self.maze.grid[self.row][self.column] = 0
            self.row += 1
            self.maze.grid[self.row][self.column] = 2

    def move_left(self):
        if self.column > 0 and not self.collision("LEFT"):
            self.maze.grid[self.row][self.column] = 0
            self.column -= 1
            self.maze.grid[self.row][self.column] = 2

    def move_right(self):
        if self.column < self.maze.width - 1 and not self.collision("RIGHT"):
            self.maze.grid[self.row][self.column] = 0
            self.column += 1
            self.maze.grid[self.row][self.column] = 2

    def collision(self, direction) -> bool:
        """
        Checks if anything is on top of the grass in the direction
        that the character wants to move. Used in the move function
        """
        if direction == "UP":
            if self.maze.grid[self.row - 1][self.column] != 0:
                return True
        elif direction == "LEFT":
            if self.maze.grid[self.row][self.column - 1] != 0:
                return True
        elif direction == "RIGHT":
            if self.maze.grid[self.row][self.column + 1] != 0:
                return True
        elif direction == "DOWN":
            if self.maze.grid[self.row + 1][self.column] != 0:
                return True
        return False
