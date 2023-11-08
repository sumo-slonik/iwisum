
MapSize = 25  # how many tiles in either direction of grid


class Character(object):  # Characters can move around and do cool stuff
    def __init__(self, Name, Column, Row,Map):
        self.Name = Name
        self.Column = Column
        self.Row = Row
        self.Map = Map

    def Move(self, Direction):  # This function is how a character moves around in a certain direction

        if Direction == "UP":
            if self.Row > 0:  # If within boundaries of grid
                if self.CollisionCheck("UP") == False:  # And nothing in the way
                    self.Row -= 1  # Go ahead and move

        elif Direction == "LEFT":
            if self.Column > 0:
                if self.CollisionCheck("LEFT") == False:
                    self.Column -= 1

        elif Direction == "RIGHT":
            if self.Column < MapSize - 1:
                if self.CollisionCheck("RIGHT") == False:
                    self.Column += 1

        elif Direction == "DOWN":
            if self.Row < MapSize - 1:
                if self.CollisionCheck("DOWN") == False:
                    self.Row += 1

    def CollisionCheck(self,
                       Direction):  # Checks if anything is on top of the grass in the direction that the character wants to move. Used in the move function
        if Direction == "UP":
            if len(self.Map.Grid[self.Column][(self.Row) - 1]) > 1:
                return True
        elif Direction == "LEFT":
            if len(self.Map.Grid[self.Column - 1][(self.Row)]) > 1:
                return True
        elif Direction == "RIGHT":
            if len(self.Map.Grid[self.Column + 1][(self.Row)]) > 1:
                return True
        elif Direction == "DOWN":
            if len(self.Map.Grid[self.Column][(self.Row) + 1]) > 1:
                return True
        return False

    def Location(self):
        print("Coordinates: " + str(self.Column) + ", " + str(self.Row))
