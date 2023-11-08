import pygame as pygame
import json

from Character import Character

BLACK = (0, 0, 0)  # some color definitions
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

TileWidth = 20  # pixel sizes for grid squares
TileHeight = 20
TileMargin = 4

Screen = pygame.display.set_mode([650, 650])  # making the window


def any_lambda(iterable, function):
    return any(function(i) for i in iterable)

class MapTile(object):  # The main class for stationary things that inhabit the grid ... grass, trees, rocks and stuff.
    def __init__(self, Name, Column, Row):
        self.Name = Name
        self.Column = Column
        self.Row = Row

class Map(object):  # The main class; where the action happens

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

        self.Hero = Character("Hero", map['start_column'], map['start_row'], self)

    def update(self):

        for Row in range(self.height):
            for Column in range(self.width):
                for i in range(len(self.Grid[Column][Row])):
                    if self.Grid[Column][Row][i].Column != Column:
                        self.Grid[Column][Row].remove(self.Grid[Column][Row][i])
                    elif self.Grid[Column][Row][i].Name == "Hero":
                        self.Grid[Column][Row].remove(self.Grid[Column][Row][i])
        self.Grid[int(self.Hero.Column)][int(self.Hero.Row)].append(self.Hero)

    def draw(self):
        self.update()
        Screen.fill(BLACK)
        for Row in range(self.height):  # Drawing grid
            for Column in range(self.width):
                for i in range(0, len(self.Grid[Column][Row])):
                    Color = WHITE
                    if any_lambda(self.Grid[Column][Row], lambda x: x.Name == 'WALL'):
                        Color = RED
                    if self.Grid[Column][Row][i].Name == "Hero":
                        Color = GREEN

                pygame.draw.rect(Screen, Color, [(TileMargin + TileWidth) * Column + TileMargin,
                                                 (TileMargin + TileHeight) * Row + TileMargin,
                                                 TileWidth,
                                                 TileHeight])