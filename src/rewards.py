from enum import Enum


class Reward(Enum):
    MOVE = -1
    VISITED = -10
    COLLISION = -50
    FINISH = 500
