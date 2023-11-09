class Character(object):  # Characters can move around and do cool stuff
    def __init__(self, column, row, map):
        self.column = column
        self.row = row
        self.map = map

        self.map.grid[self.row][self.column] = 2

    def move(
        self, direction
    ):  # This function is how a character moves around in a certain direction
        if direction == "UP":
            if self.row > 0:  # If within boundaries of grid
                if not self.collision("UP"):  # And nothing in the way
                    self.map.grid[self.row][self.column] = 0
                    self.row -= 1  # Go ahead and move
                    self.map.grid[self.row][self.column] = 2

        elif direction == "LEFT":
            if self.column > 0:
                if not self.collision("LEFT"):
                    self.map.grid[self.row][self.column] = 0
                    self.column -= 1
                    self.map.grid[self.row][self.column] = 2

        elif direction == "RIGHT":
            if self.column < self.map.width - 1:
                if not self.collision("RIGHT"):
                    self.map.grid[self.row][self.column] = 0
                    self.column += 1
                    self.map.grid[self.row][self.column] = 2

        elif direction == "DOWN":
            if self.row < self.map.height - 1:
                if not self.collision("DOWN"):
                    self.map.grid[self.row][self.column] = 0
                    self.row += 1
                    self.map.grid[self.row][self.column] = 2

    def collision(self, direction) -> bool:
        """
        Checks if anything is on top of the grass in the direction
        that the character wants to move. Used in the move function
        """
        if direction == "UP":
            if self.map.grid[self.row - 1][self.column] != 0:
                return True
        elif direction == "LEFT":
            if self.map.grid[self.row][self.column - 1] != 0:
                return True
        elif direction == "RIGHT":
            if self.map.grid[self.row][self.column + 1] != 0:
                return True
        elif direction == "DOWN":
            if self.map.grid[self.row + 1][self.column] != 0:
                return True
        return False

    def Location(self):
        print("Coordinates: " + str(self.column) + ", " + str(self.row))
