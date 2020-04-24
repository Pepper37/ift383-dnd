#!/usr/bin/python3

# note to self include the SRD license in the repo

import random
import csv
import time


# parent class to player classes and monster class
class Creature:
    def __init__(self, name):
        self.name = name

    # setters
    def setHp(self, hp):
        self.hp = int(hp)

    def setAc(self, ac):
        self.ac = int(ac)

    def setToHit(self, toHit):
        self.toHit = int(toHit)

    def setDmgDie(self, die):
        self.dmgDie = int(die)

    def setDmgBonus(self, bonus):
        self.dmgBonus = int(bonus)

    def setDex(self, dex):
        self.dexBonus = int(dex)

    def attack(self, enemyAc):
        self.damageDealt = 0
        hit = ((random.randint(0, 20) + self.toHit) >= enemyAc)
        if(hit):
            # roll damage
            self.damageDealt = self.damageDealt + random.randint(0, self.dmgDie) + self.dmgBonus
        return self.damageDealt

    def initiative(self):
        init = ((random.randint(0, 20) + self.dexBonus))
        return init


# Monster class inherits from Creature
class Monster(Creature):
    def __init__(self, name):
        super().__init__(name)
        self.movement = 3

    # player characters don't need this in this sim, only monsters
    def setsaveBonus(self, bonus):
        self.saveBonus = int(bonus)

    # melee or ranged?
    def setAttackType(self, attack):
        self.attackType = attack


# Player classes inherit from Creature
class Fighter(Creature):
    def __init__(self, name):
        super().__init__(name)
        self.pcType = "fighter"
        self.maxHp = 38
        self.hp = 38
        self.ac = 16
        self.meleeToHit = 7
        self.meleeDmgDie = 10
        self.meleeDmgBonus = 5
        self.rangedToHit = 6
        self.rangedDmgDie = 8
        self.rangedDmgBonus = 4
        self.healingPotions = 2
        self.movement = 3
        self.dexBonus = 3

    # overload the attack function: fighters have two kinds of attacks
    def attack(self, attackType, enemyAc):
        self.damageDealt = 0
        if(attackType == "melee"):
            # fighter get two attacks
            for i in range(0, 2):
                # roll a d20 to hit
                hit = ((random.randint(0, 20) + self.meleeToHit) >= enemyAc)
                if(hit):
                    # roll damage
                    self.damageDealt = self.damageDealt + random.randint(0, self.meleeDmgDie) + self.meleeDmgBonus
            return self.damageDealt

        elif(attackType == "ranged"):
            for i in range(0, 2):
                hit = ((random.randint(0, 20) + self.meleeToHit) >= enemyAc)
                if(hit):
                    self.damageDealt = self.damageDealt + random.randint(0, self.rangedDmgDie) + self.rangedDmgBonus
            return self.damageDealt
        else:
            # in case something went wrong, return -1
            return -1

    # quaff a potion of healing
    def healing(self):
        # potion of healing is 1d4 + 4
        self.hp = self.hp + random.randint(0, 4) + 4
        self.healingPotions = self.healingPotions - 1

    def printOptions(self):
        return "/move: move up to three spaces, then: \n /attack -attack using longsword (need to be adjacent to enemy) \n    or using longbow \
(less accurate but you can have distance)\n /dodge -less likely to be hit \
for a turn\n /heal -quaff a healing potion\n"


class Sorcerer(Creature):
    def __init__(self, name):
        super().__init__(name)
        self.pcType = "sorcerer"
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
        self.healingPotions = 3
        self.movement = 3
        self.spellSaveDc = 15
        self.dexBonus = 2

    # quaff a potion of healing
    def healing(self):
        self.hp = self.hp + random.randint(0, 4) + 4
        self.healingPotions = self.healingPotions - 1

    # sorcerer has spells available
    def spellcast(self, spell, stat):
        if(spell == "firebolt"):
            # a single fire bolt does 1d10
            hit = ((random.randint(0, 20) + self.toHit + 2) >= int(stat)) # stat is enemy ac
            if(hit):
                return random.randint(0, 10)
            else:
                return 0
        elif(spell == "fireball"):
            if(self.fireRemaining == 0):
                return 0
            else:
                self.fireRemaining = self.fireRemaining - 1
                # fireballs do 8d6
                # This returns a more random number, as "8 * randomint(0,6)" always returns a multiple of 8"
                monSave = ((random.randint(0, 20) + int(stat)))
                sum = 0
                for i in range(0, 8):
                    sum = sum + random.randint(0, 6)
                    # if monster succeeds on its saving throw, it takes half damage
                if(monSave >= self.spellSaveDc):
                    sum = sum // 2
                return sum

        elif(spell == "fear"):
            if(self.fearRemaining == 0):
                return 0
            else:
                self.fearRemaining = self.fearRemaining - 1
                monSave = ((random.randint(0, 20) + int(stat)))
                # if monster succeeds on its saving throw, it does not run away
                if(monSave >= self.spellSaveDc):
                    return 1
                else:
                    return 2

    def printOptions(self):
        return "/move -move up to three spaces, then:\n /firebolt -unlimited uses, ranged spell attack\n /fireball -much stronger than Firebolt,\
 enemy rolls a saving throw and takes half damage on a save,\
 limited to 3 uses per rest\n /fear -if enemy fails save, causes them to run away from the encounter,\
 only one use per rest\n /attack -pitiful for a sorcerer to attempt to attack with a dagger, but you can if you really want to...\n \
 /dodge -less likely to be hit for a turn\n /heal -quaff a healing potion\n"


# make a square grid of a given size using a 2D array, filled with 0's
# used to make the world map and the battle maps
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
    gr = gridInit(7)
    # read a csv file
    # source: https://www.tutorialspoint.com/reading-and-writing-csv-file-using-python
    file = open('grid.csv', 'r', newline='')
    obj = csv.reader(file, delimiter='|')    # using | as a delimiter so I can write messages with commas

    # every element in the gr 2D array should be populated with an array: the rows of obj
    n = 0
    m = 0
    for row in obj:
        gr[n][m] = row
        m = m + 1               # this was difficult to logic out but it works!
        if((m + 1) % 8 == 0):   # the grid is 7x7
            m = 0
            n = n + 1
    return gr


# function to allow a creature to move about a map/ grid
# a and b are coordinates: a is the y axis, b is the x.
# a increases down the grid, b increases to the right. It's funky but it works
# boundaryReached is used to check if the player is about to go outside the grid
# size is the length of a squre grid
# inDir is the direction the creature wants to move
def worldMove(a, b, size, inDir):
    boundReached = -1
    if(inDir == "north"):
        if(a == 0):
            boundReached = 0
            return(a, b, boundReached)
        else:
            a = a - 1
            return (a, b, boundReached)
    if(inDir == "east"):
        if(b == size - 1):
            boundReached = 1
            return(a, b, boundReached)
        else:
            b = b + 1
            return (a, b, boundReached)
    if(inDir == "south"):
        if(a == size - 1):
            boundReached = 2
            return(a, b, boundReached)
        else:
            a = a + 1
            return (a, b, boundReached)
    if(inDir == "west"):
        if(b == 0):
            boundReached = 3
            return(a, b, boundReached)
        else:
            b = b - 1
            return (a, b, boundReached)
    if(inDir == "stop"):
        boundReached = 5
        return (a, b, boundReached)
    return


# returns true if two icons are adjacent to one another on a grid
def adjacent(in1, in2, in3, in4):
    if(((in1 - in3 == 1) and (in2 == in4)) or
            ((in3 - in1 == 1) and (in2 == in4)) or
            ((in2 - in4 == 1) and (in1 == in3)) or
            ((in4 - in2 == 1) and (in1 == in3)) or
            ((abs(in1 - in3) == 1) and (abs(in2 - in4) == 1))):
        return 1
    else:
        return 0


# return a random melee weapon, for purposes of immersion
def randomWeapon():
    num = random.randint(0, 5)
    if(num == 0):
        return "sword"
    elif(num == 1):
        return "mace"
    elif(num == 2):
        return "dagger"
    elif(num == 3):
        return "axe"
    elif(num == 4):
        return "club"
    elif(num == 5):
        return "pike"

# Called when the player encounters a monster
# makes a battle map, prints it to the console
# gives the player a list of options, movement rules are enforced
# enemy "ai" is very simple, and ranged attacks are simplified from the SRD
def rollInitiative(inMonster, inPlayer, inMap, monPos1, monPos2, playerPos1, playerPos2):
    # source for the code for printing the map:
    # https://www.tutorialspoint.com/python_data_structure/python_2darray.htm
    mp1 = int(monPos1)
    mp2 = int(monPos2)
    pp1 = int(playerPos1)
    pp2 = int(playerPos2)
    monIc = "&"
    playerIc = "@"
    battleMap = gridInit(7)
    battleIn = open(inMap, 'r', newline='')
    battle = csv.reader(battleIn)
    player = inPlayer
    monster = inMonster
    action = ""
    # fill the map with the background in the given csv file
    q = 0
    r = 0
    for row in battle:
        battleMap[q][r] = row
        r = r + 1
        if((r + 1) % 8 == 0):
            r = 0
            q = q + 1
    mapBackupP1 = battleMap[pp1][pp2]
    mapBackupM1 = battleMap[mp1][mp2]
    monsterWaited = 0
    monMoveTicker = 0

    # actually roll for initiative
    monsterInit = int(monster.initiative())
    playerInit = int(player.initiative())
    initVictor = max(monsterInit, playerInit)
    print("\n---------------------------------\n")
    if(initVictor == playerInit):
        print("\n", player.name, " won initiative and will act first\n", sep = '')
    else:
        print("\nThe ", monster.name, " won initiative and will act first\n", sep = '')
    print("\n---------------------------------\n")
    # battle loop:
    victor = 0
    while(victor == 0):
        tookAction = 0
        battleMap[pp1][pp2] = playerIc
        battleMap[mp1][mp2] = monIc
        boundReached = -1
        # print the battleMap with creature locations
        # output format inspired by https://stackoverflow.com/questions/11178061/print-list-without-brackets-in-a-single-row
        for g in battleMap:
            for h in g:
                print(''.join(h), " ", end = "")
            print()
        print("\n---------------------------------\n")

        playerMove = 3
        monsterMove = 3

        if(player.hp > 0 and monster.hp > 0 and initVictor == playerInit):
            while(tookAction == 0):
                attacked = 0
                print("\nYou are @. The ", monster.name, " is &. You may move 3 spaces and take an action.\nYour actions are:\n", '\n', player.printOptions(), sep = '')
                action = input()

                if(action == "/move"):
                    while(player.movement > 0):

                        # previous value is used to draw iconc after the player moves away, and to check against when 
                        # player tries to move into an enemy space
                        previous = (pp1, pp2)
                        validDir = 0
                        while(validDir == 0):  # input validation
                            playerDir = input("Which direction? north, east, south, west, or stop (case sensitive)? \n")
                            #  exception handling
                            if(playerDir != "north" and playerDir != "east" and playerDir != "south" and playerDir != "west" and playerDir != "stop"):
                                print("Invalid input")
                            else:
                                validDir = 1
                        (pp1, pp2, boundReached) = worldMove(pp1, pp2, 7, playerDir)

                        # make sure player stays on the grid
                        if(boundReached != -1 and boundReached != 5):
                            print("\nCannot go off the map!")
                        elif(boundReached == 5):
                            break

                        # make sure player doesn't bump into monster
                        elif((pp1, pp2) == (mp1, mp2)):
                            print("\nCannot enter another creature's space")
                            pp1 = previous[0]
                            pp2 = previous[1]

                        # allow the player to move in a cardinal direction
                        else:
                            # decrement player's remaining movement
                            player.movement = player.movement - 1
                            # fill a bucket to store icons
                            mapBackupP2 = battleMap[pp1][pp2]
                            # move the player icon to the new location
                            battleMap[pp1][pp2] = playerIc
                            # the previous player location is overwritten with its previous icon
                            battleMap[previous[0]][previous[1]] = mapBackupP1
                            # swap bucket values for the next loop
                            mapBackupP1 = mapBackupP2

                            # print the battleMap with updated creature locations
                            print("---------------------------------\n")
                            for g in battleMap:
                                for h in g:
                                    print(''.join(h), " ", end = "")
                                print()
                            print("---------------------------------\n")

                elif(action == "/attack"):
                    while(attacked == 0):
                        dmg = 0
                        temp = ""
                        if(player.pcType == "fighter"):
                            temp = input("melee or ranged? ")
                            print("---------------------------------\n")
                            if(temp == "melee"):
                                if(adjacent(mp1, mp2, pp1, pp2) == 1):
                                    attacked = 1
                                    dmg = player.attack("melee", monster.ac)
                                    monster.setHp(monster.hp - dmg)
                                    if(dmg > 0):
                                        print("---------------------------------\n")
                                        print("\nYou swing twice with your longsword, dealing ", dmg, " points of damage to the ", monster.name, "\n", sep = '')
                                    elif(dmg == 0):
                                        print("---------------------------------\n")
                                        print("\nYou swing your longsword, but the ", monster.name, " deftly leaps clear of the blade!\n", sep = '')
                                else:
                                    print("---------------------------------\n")
                                    print("\nYou need to be adjacent to the monster!\n")
                            if(temp == "ranged"):
                                attacked = 1
                                dmg = player.attack("ranged", monster.ac)
                                monster.setHp(monster.hp - dmg)
                                if(dmg > 0):
                                    print("---------------------------------\n")
                                    print("\nYou loose two arrows, striking the foul creature and dealing ", dmg, " points of damage\n", sep = '')
                                elif(dmg == 0):
                                    print("---------------------------------\n")
                                    print("\nYou loose two arrows, both strike the ", monster.name, "'s armored gauntlet, destroyed on impact, dealing no damage \n", sep = '')
                        # sorcerer attack is only a single melee attack
                        else:
                            if(adjacent(mp1, mp2, pp1, pp2) == 1):
                                attacked = 1
                                dmg = player.attack(monster.ac)
                                monster.setHp(monster.hp - dmg)
                                if(dmg > 0):
                                    print("---------------------------------\n")
                                    print("\nYou strike out with your dagger, dealing ", dmg, " points of damage to the ", monster.name, "\n", sep = '')
                                elif(dmg == 0):
                                    print("---------------------------------\n")
                                    print("\nYou swipe out with your dagger, but the ", monster.name, " deftly leaps clear of the blade!\n", sep = '')
                            else:
                                print("---------------------------------\n")
                                print("\nYou need to be adjacent to the monster!\n")
                                break
                        tookAction = 1
                # dodge disadvantage is handled when the monster attacks
                elif(action == "/dodge"):
                    tookAction = 1
                elif(action == "/heal"):
                    if(player.healingPotions == 0):
                        print("---------------------------------\n")
                        print("\nYou have no more healing potions!\n")
                    else:
                        player.healing()
                        tookAction = 1

                # spellcasting
                elif(action == "/firebolt"):
                    dmg = player.spellcast("firebolt", monster.ac)
                    monster.setHp(monster.hp - dmg)
                    if(dmg > 0):
                        print("---------------------------------\n")
                        print("\nYou shoot a burst of flames, striking the creature and dealing ", dmg, " points of damage to the ", monster.name, "\n", sep = '')
                    elif(dmg == 0):
                        print("---------------------------------\n")
                        print("\nYou shoot a gout of flames, but the ", monster.name, " deftly leaps clear of the burst!\n", sep = '')
                    tookAction = 1
                elif(action == "/fireball"):
                    print("---------------------------------\n")
                    dmg = player.spellcast("fireball", monster.dex)
                    monster.setHp(monster.hp - dmg)
                    if(dmg == 0):
                        print("---------------------------------\n")
                        print("You have no more uses of fireball left!")
                    else:
                        print("---------------------------------\n")
                        print("\nA huge ball of flames engulfs the monster, dealing ", dmg, " points of fire damage!\n", sep = '')
                        tookAction = 1

                elif(action == "/fear"):
                    print("---------------------------------\n")
                    fear = player.spellcast("fear", monster.saveBonus)
                    if(fear == 0):
                        print("You have no more uses of fear left!")
                    elif(fear == 1):
                        print("---------------------------------\n")
                        print("\nThe ", monster.name, " shudders for a moment, looks at you in the eyes, and holds its ground,\
                            barely resisting your arcane power.\n", sep = '')
                        tookAction = 1
                    elif(fear == 2):
                        print("---------------------------------\n")
                        print("\nThe ", monster.name, " pauses, looks you in the eyes, drops its weapons to the ground, and sprints into the wilderness. You are left alone\n", sep = '')
                        tookAction = 1
                        monster.setHp(0)

        time.sleep(5)
        if(monster.hp > 0):

            # enemy turn melee type
            if(monster.attackType == "melee"):
                for i in range(0, 3):
                    monsterWaited = 0
                    # move towards the player
                    # calculate differences between coordinates
                    diff1 = mp1 - pp1
                    diff2 = mp2 - pp2
                    # if monster is adjacent to player
                    if(adjacent(pp1, pp2, mp1, mp2) == 1):
                        monsDir = "stop"
                        monsterWaited = 1
                    # decide in which direction to move
                    elif(abs(diff1) > abs(diff2)):
                        # move along a axis
                        if(diff1 > 1):
                            monsDir = "north"
                        elif(diff1 < -1):
                            monsDir = "south"
                    elif(abs(diff2) >= abs(diff1)):
                        # move along b axis
                        if(diff2 > 1):
                            monsDir = "west"
                        elif(diff2 < -1):
                            monsDir = "east"
                    mPrevious = (mp1, mp2)
                    (mp1, mp2, none) = worldMove(mp1, mp2, 7, monsDir)
                    # fixes a bug whereby monster waiting would not draw the monsIc
                    if(monsterWaited == 0):
                        mapBackupM2 = battleMap[mp1][mp2]
                        battleMap[mp1][mp2] = monIc
                        battleMap[mPrevious[0]][mPrevious[1]] = mapBackupM1
                        # swap bucket values for the next loop
                        mapBackupM1 = mapBackupM2
                    # print the battleMap with updated creature locations
                        print("\nThe ", monster.name, " moves\n")
                        for g in battleMap:
                            for h in g:
                                print(''.join(h), " ", end = "")
                            print()
                        print("\n---------------------------------\n")
                        time.sleep(2)

                # Monster attacks player
                if(adjacent(pp1, pp2, mp1, mp2) == 1):
                    dmg = monster.attack(player.ac)
                    dmg2 = monster.attack(player.ac)
                    # disadvantage if player took dodge action
                    if(action == "dodge"):
                        dmg = min(dmg, dmg2)
                    player.setHp(player.hp - dmg)
                    weap = randomWeapon()
                    print("\n The ", monster.name, " attacks with a ", randomWeapon(), "!\nYou take ", dmg, " points of damage\n", sep = '')
                    print("---------------------------------\n")

            # ranged attack type
            # ranged monster just moves left and right on the map. simple.
            elif(monster.attackType == "ranged"):
                if(monMoveTicker == 0):
                    monstDir = "west"
                else:
                    monstDir = "east"
                for i in range(0, 3):
                    # print("pp1: ", pp1, "pp2: ", pp2, "\n mp1: ", mp1, " mp2: ", mp2, "\n")
                    mPrevious = (mp1, mp2)
                    (mp1, mp2, none) = worldMove(mp1, mp2, 7, monstDir)
                    if((mp1, mp2) == (pp1, pp2)):
                        mp1 = mPrevious[0]
                        mp2 = mPrevious[1]
                    else:
                        mapBackupM2 = battleMap[mp1][mp2]
                        battleMap[mp1][mp2] = monIc
                        battleMap[mPrevious[0]][mPrevious[1]] = mapBackupM1
                        mapBackupM1 = mapBackupM2
                    # print the battleMap with updated creature locations
                        print("---------------------------------\n")
                        print("The ", monster.name, " moves\n")
                        for g in battleMap:
                            for h in g:
                                print(''.join(h), " ", end = "")
                            print()
                        print("\n---------------------------------\n")
                        time.sleep(2)
                if(monMoveTicker == 0):
                    monMoveTicker = 1
                else:
                    monMoveTicker = 0

                dmg = monster.attack(player.ac)
                dmg2 = monster.attack(player.ac)
                # disadvantage if player took dodge action
                if(action == "dodge"):
                    dmg = min(dmg, dmg2)
                player.setHp(player.hp - dmg)
                if(dmg > 0):
                    print("\nThe ", monster.name, " shoots an arrow from its longbow, you take ", dmg,
                        " points of damage as the arrow strikes a joint between you armor!\n", sep = '')
                elif(dmg == 0):
                    print("\nAn arrow flies at you, but you lunge forward, ducking out of the missile's way\n")

        player.movement = 3
        if(monster.hp <= 0):
            print("\n The ", monster.name, " has been vanquished! \n")
            victor = 1
        elif(player.hp <= 0):
            print("You have died. You will never know the riches that laid in wait.\n")
            victor = 2
        playerInit = initVictor
    return victor


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
    foundMagguffin = 0
    a = 5
    b = 4
    while (winState != 1):
        # (win state will become 1 in a specific encounter)
        # set player position values to the new values at beginning of loop
        pos = world[a][b]
        # nothing happens, basic dialog
        if(pos[0] == "dialog"):
            print(pos[1])

        # found a healing item!
        if(pos[0] == "potion" and int(pos[3]) == 0):
            print("\n", pos[1], "\n")
            player.healingPotions = player.healingPotions + 1
            pos[3] = 1
        elif(pos[0] == "potion" and int(pos[3]) == 1):
            print("\n", pos[2], "\n")

        if(pos[0] == "healing" and int(pos[3]) == 0):
            print("\n", pos[1], "\n")
            player.hp = player.hp + 7
            pos[3] = 1
        elif(pos[0] == "healing" and int(pos[3]) == 1):
            print("\n", pos[2], "\n")

        # weapon upgrade
        if(pos[0] == "weapon" and int(pos[3]) == 0):
            print("\n", pos[1], "\n")
            if(playerClass == "Fighter"):
                player.meleeDmgBonus = player.meleeDmgBonus + 1
            else:
                player.dmgBonus = player.dmgBonus + 1
            pos[3] = 1
        elif(pos[0] == "weapon" and int(pos[3]) == 1):
            print("\n", pos[2], "\n")

        # armor upgrade
        if(pos[0] == "armor" and int(pos[3]) == 0):
            print("\n", pos[1], "\n")
            player.setAc(player.ac + 1)
            pos[3] = 1
        elif(pos[0] == "armor" and int(pos[3]) == 1):
            print("\n", pos[2], "\n")

        # key item (needs to be found to acquire the treasure)
        if(pos[0] == "key" and int(pos[3]) == 0):
            print("\n", pos[1], "\n")
            pos[3] = 1
            foundMagguffin = 1
        elif(pos[0] == "key" and int(pos[3]) == 1):
            print("\n", pos[2], "\n")

        #  ending
        if(pos[0] == "end" and foundMagguffin == 0):
            print("\n", pos[1], "\n")
        elif(pos[0] == "end" and foundMagguffin == 1):
            print("\n", pos[2], "\n")
            winState = 1

        # A monster appears!
        if(pos[0] == "encounter" and int(pos[13]) == 0):
            monster = Monster(pos[11])
            # make a monster object for the encounter
            monster.setHp(pos[1])
            monster.setAc(pos[2])
            monster.setToHit(pos[3])
            monster.setDmgDie(pos[4])
            monster.setDmgBonus(pos[5])
            monster.setsaveBonus(pos[12])
            monster.setAttackType(pos[15])
            monster.setDex(pos[16])
            print("A ", monster.name, " stands menacingly before you! Prepare for battle.")
            time.sleep(3)  # dramatic effect
            # return the player object with updated battle damage/ updated rewards
            var = rollInitiative(monster, player, pos[6], pos[7], pos[8], pos[9], pos[10])
            if(var == 2):
                print("Game Over")
                time.sleep(10)
                quit()
            pos[13] = 1  # encounter has been encountered
            print(pos[14])  # victory text
        # if player has encountered the encounter already
        elif(pos[0] == "encounter" and int(pos[13]) == 1):
            print(pos[14])
        print("--------------------------------------------------------")

        # pass current location data into worldMove(), then reassign any new values
        validDir = 0
        while(validDir == 0):
            dir = input("Where would you like to go?\noptions are: north, east, south, west (case sensetive): ")
            if(dir != "north" and dir != "east" and dir != "south" and dir != "west"):
                print("Invalid input")
            else:
                validDir = 1
                print("--------------------------------------------------------")
        (a, b, boundaryReached) = worldMove(a, b, 7, dir)
        # if player has reached the edge of the world, let them know
        if(boundaryReached == 0):
            print("\n Mountains lie in your way, you've gone as far north as you can!")
        elif(boundaryReached == 1):
            print("\n The mountains here are sheer cliff faces, you cannot continue east!")
        elif(boundaryReached == 2):
            print("\n The plains stretch on forever, you can go no further south.")
        elif(boundaryReached == 3):
            print("\n The forest grows dark and deep, it would be unwise to travel further west")
        # reset this check in case the player tries going oob again.
        boundaryReached = -1
    print("You take your reward, more treasure than you know what to do with,\n \
            make your way home, and are recieved like the legendary \
            hero that you are!")
    return


main()
