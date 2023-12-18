import pygame

from src.maze import Maze

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

if __name__ == "__main__":

    maze = Maze("data/testowy.json")
    Screen = pygame.display.set_mode(
        [
            maze.height * (TileWidth + TileMargin),
            maze.height * (TileHeight + TileMargin),
        ]
    )  # making the window

    while not Done:  # Main pygame loop
        for event in pygame.event.get():  # catching events
            if event.type == pygame.QUIT:
                Done = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    maze.mouse.move("LEFT")
                if event.key == pygame.K_RIGHT:
                    maze.mouse.move("RIGHT")
                if event.key == pygame.K_UP:
                    maze.mouse.move("UP")
                if event.key == pygame.K_DOWN:
                    maze.mouse.move("DOWN")
        maze.draw()
        clock.tick(60)  # Limit to 60 fps or something
        pygame.display.flip()  # Honestly not sure what this does, but it breaks if I remove it

    pygame.quit()
