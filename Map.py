import random as random
import pygame as pygame

from Character import Character

MapSize = 25  # how many tiles in either direction of grid


class MapTile(object):  # The main class for stationary things that inhabit the grid ... grass, trees, rocks and stuff.
    def __init__(self, Name, Column, Row):
        self.Name = Name
        self.Column = Column
        self.Row = Row


class Map(object):  # The main class; where the action happens
    global MapSize

    Grid = []

    for Row in range(MapSize):  # Creating grid
        Grid.append([])
        for Column in range(MapSize):
            Grid[Row].append([])

    for Row in range(MapSize):  # Filling grid with grass
        for Column in range(MapSize):
            TempTile = MapTile("Grass", Column, Row)
            Grid[Column][Row].append(TempTile)

    for Row in range(MapSize):  # Putting some rocks near the top
        for Column in range(MapSize):
            TempTile = MapTile("Rock", Column, Row)
            if Row == 1:
                Grid[Column][Row].append(TempTile)

    for i in range(10):  # Placing Random trees
        RandomRow = random.randint(0, MapSize - 1)
        RandomColumn = random.randint(0, MapSize - 1)
        TempTile = MapTile("Tree", RandomColumn, RandomRow)
        Grid[RandomColumn][RandomRow].append(TempTile)

    RandomRow = random.randint(0, MapSize - 1)  # Dropping the hero in
    RandomColumn = random.randint(0, MapSize - 1)
    Hero = Character("Hero", 10, RandomColumn, RandomRow)

    def update(self):  # Very important function
        # This function goes through the entire grid
        # And checks to see if any object's internal coordinates
        # Disagree with its current position in the grid
        # If they do, it removes the objects and places it
        # on the grid according to its internal coordinates

        for Column in range(MapSize):
            for Row in range(MapSize):
                for i in range(len(Map.Grid[Column][Row])):
                    if Map.Grid[Column][Row][i].Column != Column:
                        Map.Grid[Column][Row].remove(Map.Grid[Column][Row][i])
                    elif Map.Grid[Column][Row][i].Name == "Hero":
                        Map.Grid[Column][Row].remove(Map.Grid[Column][Row][i])
        Map.Grid[int(Map.Hero.Column)][int(Map.Hero.Row)].append(Map.Hero)
