import pygame

from src.nn_maze_solver import Solver

TileWidth = 20  # pixel sizes for grid squares
TileHeight = 20
TileMargin = 4

BLACK = (0, 0, 0)  # some color definitions
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

if __name__ == "__main__":
    solver = Solver("data/testowy.json")

    Screen = pygame.display.set_mode(
        [
            solver.maze.height * (TileWidth + TileMargin),
            solver.maze.height * (TileHeight + TileMargin),
        ]
    )  # making the window

    solver.start_learning()

    solver.predict()

    pygame.quit()
