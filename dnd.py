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
                sum = 0
                for i in range(0, 8):
                    sum = sum + random.randint(0,6)
                return sum
        if(spell == "fear"):
            if(self.fearRemaining == 0):
                print("You have run out of Fireballs to use! Take a rest to regain")
                return 0
            else:
                self.fearRemaining = self.fearRemaining - 1

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


def rollInitiative(hp, ac, toHit, damageDie, damageBonus,
                    inMap, pcPos1, pcPos2, monPos1, monPos2, name, save, player):
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
    print(player.spellcast("fireball"))

    # # testing
    # mon = Monster("skeleton")
    # # print(mon.name)
    # mon.setHp(20)
    # print(mon.hp)
    # mon.setHp(mon.hp - 4)
    # print(mon.hp)

    # zombie = Monster("zombie")
    # zombie.setHp(50)
    # # print(zombie.hp)
    # # print(mon.hp)

    # sorc = Sorcerer("Phillip")
    # # print(sorc.hp, " ", sorc.fireRemaining)
    # print(sorc.spellcast("firebolt"))

    # jane = Fighter("Jane")
    # print(jane.hp)
    # print(jane.attack("melee"))


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
    maple = Sorcerer("Maple")
    print(maple.hp)
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
        rollInitiative(pos[1], pos[2], pos[3], pos[4], pos[5], pos[6], pos[7], pos[8], pos[9], pos[10], pos[11], pos[12], maple)
        # the encounter may give a key item to the player, or the location of the goal (winstate trigger)
        # I should set a trigger to know if this encounter has happened already,
        # in the case the player back tracks
    #if the player is still alive after the encounter...
    #worldMove()

    return


main()
