#!/usr/bin/python3

# note to self include the SRD license in the repo

import random
import csv


# enemy class
# player class


def gridInit():
    col = []
    for i in range(0, 6):
        row = []
        for j in range(0, 6):
            row.append(0)
        col.append(row)
    return col


# makes a grid, populates it
# I really should just have a Grid class if I wanted to be a good OOP programmer
def grid():
    # make the grid to populate
    gr = gridInit()
    # read a csv file
    file = open('grid.csv', 'r', newline = '')
    obj = csv.reader(file)

    # every element in the gr 2D array should be populated with an array: the rows of obj
    n = 0
    m = 0
    for row in obj:
        print("n: ", n)
        print("m: ", m)
        print("-----------")
        gr[n][m] = row
        m = m + 1               # this was difficult to logic out but it works
        if((m + 1) % 7 == 0):
            m = 0
            n = n + 1
    return gr


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

    gridM = grid()
    # print the grid, for testing here only 
    # source: https://www.tutorialspoint.com/python_data_structure/python_2darray.htm
    for i in gridM:
        for j in i:
            print(j, end = " ")
        print()

    a = 0
    b = 0
#    print(gridM[4][4])
    return


main()
