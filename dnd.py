#!/usr/bin/python3

# note to self include the SRD license in the repo

import random
import csv


# enemy class
# player class

# declare a pc outside of any functions?


# make a square grid of a given size using a 2D array, filled with 0's
def gridInit(size):
    col = []
    for i in range(0, size):
        row = []
        for j in range(0, size):
            row.append(0)
        col.append(row)
    return col


# makes a world map, populates it from a csv file
# This is meant to hold data, the player does not see this map
def worldMap():
    # make the grid to populate
    gr = gridInit(6)
    # read a csv file
    # source: https://www.tutorialspoint.com/reading-and-writing-csv-file-using-python
    file = open('grid.csv', 'r', newline='')
    obj = csv.reader(file)

    # every element in the gr 2D array should be populated with an array: the rows of obj
    n = 0
    m = 0
    for row in obj:
        gr[n][m] = row
        m = m + 1               # this was difficult to logic out but it works
        if((m + 1) % 7 == 0):   # the grid is 6x6
            m = 0
            n = n + 1
    return gr


# stub
def worldMove():
    dir = input("What direction would you like to move?\noptions are: north, east, south, west (case sensetive): ")
    if(dir == "north"):
        print("north")
    if(dir == "east"):
        print("east")
    if(dir == "south"):
        print("south")
    if(dir == "west"):
        print("west")
    return


def rollInitiative(hp, ac, speed, toHit, damageDie, damageBonus,
                    inMap, pcPos1, pcPos2, monPos1, monPos2, name):
    # do the battle, printing to stdout
    # --------------instantiate a monster object here-----------------
    # make a grid for the battle map
    battleMap = gridInit(7)
    battleIn = open(inMap, 'r', newline='')
    battle = csv.reader(battleIn)
    # fill the map with the background in the given csv file
    q = 0
    r = 0
    for row in battle:
        battleMap[q][r] = row
        r = r + 1
        if((r + 1) % 8 == 0):
            r = 0
            q = q + 1
    # print the map
    # source: https://www.tutorialspoint.com/python_data_structure/python_2darray.htm
    for g in battleMap:
        for h in g:
            print(''.join(h), " ", end = "")
        print()

    # battle loop:
    # player and enemy drawn on map
    # each have stats managed by their objects
    # monster behaves very simple: if ranged, move away and attack, 
    # if melee type, get close and attack
    # player will be given a list of options as well as an updated battle
    # map at the start of each turn. 
    # when player moves, I need a way to save the spot's previous icon, so I can
    # replace the icon on the drawing of the map
    # also need to figure out pathing for the enemy "ai"
    # if player hp goes to 0, game over, return 1. If player succeeds, reward? and 
    # return 0. Calling function can check the return value and 
    # give either a game over or continue main loop

    return


def main():

    world = worldMap()
    a = 0
    b = 0
    # declare playerCharacter object, assign values <-- should this happen outside of function?
    # while (winState != 1)
    # (win state will become 1 in a specific encounter)
    pos = world[a][b]
    if(pos[0] == "dialog"):
        print(pos[1])
    # the position on the map can also have:
        # healing
        # weapon upgrade
        # armor upgrade
    if(pos[0] == "encounter"):
        # I will end up handling these arguments by simply passing a monster object
        rollInitiative(pos[1], pos[2], pos[3], pos[4], pos[5], pos[6], pos[7], pos[8], pos[9], pos[10], pos[11], pos[11])
        # the encounter may give a key item to the player, or the location of the goal (winstate trigger)
    #if the player is still alive after the encounter...
    worldMove()

    return


main()
