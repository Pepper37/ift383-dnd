#!/usr/bin/python3

# note to self include the SRD license in the repo

import random
import csv


# creature class, parent class to player classes and monster
class Creature:
    def __init__(self, name):
        self.name = name

    # setters
    def setHp(self, hp):
        self.hp = hp

    def setAc(self, ac):
        self.ac = ac

    def setToHit(self, toHit):
        self.toHit = toHit

    def setDmgDie(self, die):
        self.dmgDie = die

    def setDmgBonus(self, bonus):
        self.dmgBonus = bonus

    def setsaveBonus(self, bonus):
        self.saveBonus = bonus


# Monster class inherits from Creature
class Monster(Creature):
    def __init__(self, name):
        super().__init__(name)


# Player classes inherit from Creature
class Fighter(Creature):
    def __init__(self, name):
        super().__init__(name)
        self.maxHp = 38
        self.hp = 38
        self.ac = 16
        self.meleeToHit = 7
        self.meleeDmgDie = 10
        self.meleeDmgBonus = 5
        self.rangedToHit = 6
        self.rangedDmgDie = 8
        self.rangedDmgBonus = 4

    def attack(self, attackType):
        if(attackType == "melee"):
            damageDealt = random.randint(0, self.meleeDmgDie) + self.meleeDmgBonus
            return damageDealt
        elif(attackType == "ranged"):
            damageDealt = random.randint(0, self.rangedDmgDie) + self.rangedDmgBonus
            return damageDealt
        else:
            return 0


class Sorcerer(Creature):
    def __init__(self, name):
        super().__init__(name)
        self.maxHp = 28
        self.hp = 28
        self.ac = 15
        self.toHit = 4
        self.dmgDie = 6
        self.dmgBonus = 2
        # setting limits to the powerful spells
        self.maxFire = 3
        self.maxFear = 1
        self.fireRemaining = self.maxFire
        self.fearRemaining = self.maxFear

    # sorcerer has spells available
    def spellcast(self, spell):
        if(spell == "firebolt"):
            # a single fire bolt does 1d10
            return random.randint(0, 10)
        if(spell == "fireball"):
            if(self.fireRemaining == 0):
                return 0
            else:
                self.fireRemaining = self.fireRemaining - 1
                # fireballs do 8d6
                # This returns a more random number, as "8 * randomint(0,6)" always returns a multiple of 8"
                sum = 0
                for i in range(0, 8):
                    sum = sum + random.randint(0,6)
                return sum
        if(spell == "fear"):
            if(self.fearRemaining == 0):
                print("You have run out of Fears to use! Take a rest to regain")
                return 0
            else:
                self.fearRemaining = self.fearRemaining - 1
                return 1


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
    obj = csv.reader(file, delimiter='|')    # using | as a delimiter so I can write messages with commas

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


# function to allow the player to move about a 6x6 world map
# a and b are coordinates: a is the y axis, b is the x.
# a increases down the grid, b increases to the right. It's funky but it works
# boundaryReached is used to check if the player is about to go outside the grid
def worldMove(a, b, boundaryReached):
    dir = input("What direction would you like to move?\noptions are: north, east, south, west (case sensetive): ")
    if(dir == "north"):
        if(a == 0):
            boundaryReached = 0
            return(a, b, boundaryReached)
        else:
            a = a - 1
            return (a, b, boundaryReached)
    if(dir == "east"):
        if(b == 5):
            boundaryReached = 1
            return(a, b, boundaryReached)
        else:
            b = b + 1
            return (a, b, boundaryReached)
    if(dir == "south"):
        if(a == 5):
            boundaryReached = 2
            return(a, b, boundaryReached)
        else:
            a = a + 1
            return (a, b, boundaryReached)
    if(dir == "west"):
        if(b == 0):
            boundaryReached = 3
            return(a, b, boundaryReached)
        else:
            b = b - 1
            return (a, b, boundaryReached)
    return


def rollInitiative(mon, player, inMap, monPos1, monPos2, playerPos1, playerPos2):
    # do the battle, printing to stdout:
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

    # make a player character with input from user
    validName = 0
    while(validName == 0):
        playerClass = input("Welcome! would you like to play as a Fighter or a Sorcerer?\n")
        if(playerClass != "Fighter" and playerClass != "Sorcerer"):
            print("Invalid input! Please type either Fighter or Sorcerer (case sensitive)\n")
        else:
            print("Wonderful! What is your", playerClass, "'s name?")
            name = input()
            validName = 1
    if (playerClass == "Fighter"):
        player = Fighter(name)
    else:
        player = Sorcerer(name)
    world = worldMap()
    boundaryReached = -1
    winState = 0
    a = 4
    b = 3
    while (winState != 1):
        # (win state will become 1 in a specific encounter)
        pos = world[a][b]
        # nothing happens, basic dialog
        if(pos[0] == "dialog"):
            print(pos[1])
        # found a healing item!
        if(pos[0] == "healing"):
            print(pos[1])
            player.setHp(player.hp + pos[2])
        # weapon upgrade
        if(pos[0] == "weapon"):
            print(pos[1])
            player.setDmgBonus(player.dmgBonus + pos[2])
        # armor upgrade
        if(pos[0] == "armor"):
            print(pos[1])
            player.setAc(player.ac + pos[2])
        # A monster appears!
        if(pos[0] == "encounter"):
            # I will end up handling these arguments by simply passing a monster object
            monster = Monster(pos[11])
            # set monster attributes here
            rollInitiative(monster, player, pos[6], pos[7], pos[8], pos[9], pos[10])
            # the encounter may give a key item to the player, or the location of the goal (winstate trigger)
            # I should set a trigger to know if this encounter has happened already,
            # in the case the player back tracks
        # if the player is still alive after the encounter, let them move
        print("-----------------")
        print("a: ", a, "b: ", b)
        # pass current location data into worldMove(), then reassign any new values
        # !!!! throws a TypeError exception if an invalid value is input for direction- need to handle !!!!
        (a, b, boundaryReached) = worldMove(a, b, boundaryReached)
        # if player has reached the edge of the world, let them know 
        if(boundaryReached == 0):
            print("Mountains lie in your way, you've gone as far north as you can!")
        elif(boundaryReached == 1):
            print("The eastern swamps lay stagnant before you, you cannot continue east!")
        elif(boundaryReached == 2):
            print("The plains stretch on forever, you can go no further south.")
        elif(boundaryReached == 3):
            print("The forest grows dark and deep, it would be unwise to travel further west")
        # reset this check in case the player makes the mistake again. 
        boundaryReached = -1
    return


main()
