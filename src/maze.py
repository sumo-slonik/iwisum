import json

import pygame

from src.character import Character

BLACK = (0, 0, 0)  # some color definitions
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

TileWidth = 20  # pixel sizes for grid squares
TileHeight = 20
TileMargin = 4

Screen = pygame.display.set_mode([650, 650])  # making the window


class Maze(object):  # The main class; where the action happens
    def __init__(self, file_name):
        f = open(file_name)
        maze = json.load(f)
        self.width = maze["width"]
        self.height = maze["height"]
        self.grid = maze["map"]

        self.mouse = Character(maze["start_column"], maze["start_row"], self)

    def draw(self):
        Screen.fill(BLACK)
        for row in range(self.height):  # Drawing grid
            for column in range(self.width):
                cases = {0: WHITE, 1: RED, 2: GREEN}

                pygame.draw.rect(
                    Screen,
                    cases[self.grid[row][column]],
                    [
                        (TileMargin + TileWidth) * column + TileMargin,
                        (TileMargin + TileHeight) * row + TileMargin,
                        TileWidth,
                        TileHeight,
                    ],
                )
