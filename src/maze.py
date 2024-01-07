import json

import pygame

from src.mouse import Mouse

BLACK = (0, 0, 0)  # some color definitions
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (127, 127, 127)

TILE_WIDTH = 20  # pixel sizes for grid squares
TILE_HEIGHT = 20
TILE_MARGIN = 4

Screen = pygame.display.set_mode([650, 650])  # making the window


class Maze:  # The main class; where the action happens
    def __init__(self, file_name):
        with open(file_name, encoding="utf-8") as f:
            maze = json.load(f)

        self.width = maze["width"]
        self.height = maze["height"]
        self.grid = maze["map"]

        self.mouse = Mouse(maze["start_column"], maze["start_row"], self)

        self.clock = pygame.time.Clock()

    def draw(self):
        Screen.fill(BLACK)
        for row in range(self.height):  # Drawing grid
            for column in range(self.width):
                cases = {0: WHITE, 1: RED, 2: GREEN, 3: BLUE, 4: GRAY}

                pygame.draw.rect(
                    Screen,
                    cases[self.grid[row][column]],
                    [
                        (TILE_MARGIN + TILE_WIDTH) * column + TILE_MARGIN,
                        (TILE_MARGIN + TILE_HEIGHT) * row + TILE_MARGIN,
                        TILE_WIDTH,
                        TILE_HEIGHT,
                    ],
                )

        self.clock.tick(60)  # Limit to 60 fps or something
        pygame.display.flip()
