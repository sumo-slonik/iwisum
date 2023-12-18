import json
import random

import numpy as np


def create_maze(dim):
    # Create a grid filled with walls
    maze = np.ones((dim * 2 + 1, dim * 2 + 1))

    # Define the starting point
    x, y = (0, 0)
    maze[2 * x + 1, 2 * y + 1] = 0

    # Initialize the stack with the starting point
    stack = [(x, y)]
    while len(stack) > 0:
        x, y = stack[-1]

        # Define possible directions
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < dim and 0 <= ny < dim and maze[2 * nx + 1, 2 * ny + 1] == 1:
                maze[2 * nx + 1, 2 * ny + 1] = 0
                maze[2 * x + 1 + dx, 2 * y + 1 + dy] = 0
                stack.append((nx, ny))
                break
        else:
            stack.pop()

    # Create an entrance and an exit
    maze[1, 0] = 0
    maze[-2, -1] = 0
    return maze


def generate_maze_to_json(name, size):
    maze = create_maze(size)
    maze = [[int(i) for i in maze_inn] for maze_inn in maze]
    json_maze = {
        "width": len(maze),
        "height": len(maze[0]),
        "start_row": 0,
        "start_column": 0,
        "map": maze,
    }
    with open(name, "w", encoding="utf-8") as file:
        json.dump(json_maze, file)


if __name__ == "__main__":
    generate_maze_to_json("testowy.json", 5)
