#!/usr/bin/python3

# note to self include the SRD license in the repo

import random


def gridInit():
    col = []
    for i in range(0, 6):
        row = []
        for j in range(0, 6):
            row.append(0)
        col.append(row)
    return col


def movement(direction):
    if(direction == "north"):
        print("north")
    if(direction == "south"):
        print("south")
    return


# stub
def rollInitiative(hp, ac, speed, toHit, damageDie, damageBonus):
    # do the battle, printing to stdout
    return


def main():

    grid = gridInit()
    # print the grid, for testing here only 
    # source: https://www.tutorialspoint.com/python_data_structure/python_2darray.htm
    for i in grid:
        for j in i:
            print(j, end = " ")
        print()

    a = 0
    b = 0
    print(grid[4][4])
    return


main()
