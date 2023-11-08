import random as random
import pygame as pygame
import json

pygame.init()  # start up dat pygame
clock = pygame.time.Clock()  # for framerate or something? still not very sure
Screen = pygame.display.set_mode([650, 650])  # making the window
Done = False  # variable to keep track if window is open
TileWidth = 20  # pixel sizes for grid squares
TileHeight = 20
TileMargin = 4

BLACK = (0, 0, 0)  # some color definitions
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


def any_lambda(iterable, function):
    return any(function(i) for i in iterable)

class MapTile(object):  # The main class for stationary things that inhabit the grid ... grass, trees, rocks and stuff.
    def __init__(self, Name, Column, Row):
        self.Name = Name
        self.Column = Column
        self.Row = Row


class Character(object):  # Characters can move around and do cool stuff
    def __init__(self, Name, HP, Column, Row, Map):
        self.Name = Name
        self.HP = HP
        self.Column = Column
        self.Row = Row
        self.Map = Map
        self.Grid = Map.Grid

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
            if self.Column < Map.width - 1:
                if self.CollisionCheck("RIGHT") == False:
                    self.Column += 1

        elif Direction == "DOWN":
            if self.Row < Map.height - 1:
                if self.CollisionCheck("DOWN") == False:
                    self.Row += 1

        self.Map.update()

    def CollisionCheck(self,
                       Direction):  # Checks if anything is on top of the grass in the direction that the character wants to move. Used in the move function
        if Direction == "UP":
            if any_lambda(self.Grid[self.Column][self.Row - 1], lambda x: x.Name == 'WALL'):
                return True
        elif Direction == "LEFT":
            if any_lambda(self.Grid[self.Column - 1][self.Row], lambda x: x.Name == 'WALL'):
                return True
        elif Direction == "RIGHT":
            if any_lambda(self.Grid[self.Column + 1][self.Row], lambda x: x.Name == 'WALL'):
                return True
        elif Direction == "DOWN":
            if any_lambda(self.Grid[self.Column][self.Row + 1], lambda x: x.Name == 'WALL'):
                return True
        return False

    def Location(self):
        print("Coordinates: " + str(self.Column) + ", " + str(self.Row))


class Map(object):  # The main class; where the action happens
    global MapSize
    width = 0

    Grid = []

    def __init__(self, file_name):
        f = open(file_name)
        map = json.load(f)
        self.width = map['width']
        self.height = map['height']
        self.Grid = map['map']

        for id_r, Row in enumerate(self.Grid):  # Filling grid with grass
            for id_c, Column in enumerate(Row):
                TempTile = MapTile("WALL", id_c, id_r)
                if Column == 1:
                    self.Grid[id_c][id_r] = [TempTile]
                    TempTile = MapTile("NORMAL", id_c, id_r)
                    self.Grid[id_c][id_r].append(TempTile)
                else:
                    TempTile = MapTile("NORMAL", id_c, id_r)
                    self.Grid[id_c][id_r] = [TempTile]

        self.Hero = Character("Hero", 10, map['start_column'], map['start_row'], self)

    def update(self):  # Very important function
        # This function goes through the entire grid
        # And checks to see if any object's internal coordinates
        # Disagree with its current position in the grid
        # If they do, it removes the objects and places it
        # on the grid according to its internal coordinates

        for Row in range(self.height):  # Drawing grid
            for Column in range(self.width):
                for i in range(len(Map.Grid[Column][Row])):
                    if Map.Grid[Column][Row][i].Column != Column:
                        Map.Grid[Column][Row].remove(Map.Grid[Column][Row][i])
                    elif Map.Grid[Column][Row][i].Name == "Hero":
                        Map.Grid[Column][Row].remove(Map.Grid[Column][Row][i])
        Map.Grid[int(Map.Hero.Column)][int(Map.Hero.Row)].append(Map.Hero)


if __name__ == '__main__':
    Map = Map("map.json")
    Screen = pygame.display.set_mode(
        [Map.height * (TileWidth + TileMargin), Map.height * (TileHeight + TileMargin)])  # making the window

    while not Done:  # Main pygame loop
        for event in pygame.event.get():  # catching events
            if event.type == pygame.QUIT:
                Done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                Pos = pygame.mouse.get_pos()
                Column = Pos[0] // (
                        TileWidth + TileMargin)  # Translating the position of the mouse into rows and columns
                Row = Pos[1] // (TileHeight + TileMargin)
                print(str(Row) + ", " + str(Column))

                for i in range(len(Map.Grid[Column][Row])):
                    print(str(Map.Grid[Column][Row][i].Name))  # print stuff that inhabits that square

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    Map.Hero.Move("LEFT")
                if event.key == pygame.K_RIGHT:
                    Map.Hero.Move("RIGHT")
                if event.key == pygame.K_UP:
                    Map.Hero.Move("UP")
                if event.key == pygame.K_DOWN:
                    Map.Hero.Move("DOWN")
        Screen.fill(BLACK)

        for Row in range(Map.height):  # Drawing grid
            for Column in range(Map.width):
                for i in range(0, len(Map.Grid[Column][Row])):
                    Color = WHITE
                    if any_lambda(Map.Grid[Column][Row], lambda x: x.Name == 'WALL'):
                        Color = RED
                    if Map.Grid[Column][Row][i].Name == "Hero":
                        Color = GREEN

                pygame.draw.rect(Screen, Color, [(TileMargin + TileWidth) * Column + TileMargin,
                                                 (TileMargin + TileHeight) * Row + TileMargin,
                                                 TileWidth,
                                                 TileHeight])

        clock.tick(60)  # Limit to 60 fps or something

        pygame.display.flip()  # Honestly not sure what this does, but it breaks if I remove it
        Map.update()

    pygame.quit()
