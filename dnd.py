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

    def attack(self, enemyAc):
        self.damageDealt = 0
        hit = ((random.randint(0, 20) + self.toHit) >= enemyAc)
        if(hit):
            # roll damage
            self.damageDealt = self.damageDealt + random.randint(0, self.dmgDie) + self.dmgBonus
        return self.damageDealt


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

    def printOptions(self):
        return "/move: move up to three spaces \n /attack -attack using longsword (need to be adjacent to enemy) \n    or using longbow \
(less accurate but you can have distance)\n /dodge -less likely to be hit \
for a turn\n /heal -quaff a healing potion"


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

    # quaff a potion of healing
    def healing(self):
        self.hp = self.hp + random.randint(0, 4) + 4

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
    def printOptions(self):
        return "-Fire Bolt (unlimited uses, ranged spell attack\n -Fireball (much stronger, enemy rolls a saving throw\
and takes half damage on a save, limited to 3 uses per rest\n -Fear (if enemy fails save, causes them to run away from the encounter\
, only one use per rest\n -Attack (pitiful for a sorcerer to attempt to attack with a dagger, but I mean \
you could if you want...\n -Dodge (less likely to be hit \
for a turn)\n -Heal (quaff a healing potion)"


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
        m = m + 1               # this was difficult to logic out but it works!
        if((m + 1) % 7 == 0):   # the grid is 6x6
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


# Called when the player encounters a monster
# makes a battle map, prints it to the console
# gives the player a list of options, movement rules are enforced
# enemy "ai" is very simple, and ranged attacks are simpllified from the SRD
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

    # battle loop:
    victor = 0
    while(victor == 0):
        tookAction = 0
        battleMap[pp1][pp2] = playerIc
        battleMap[mp1][mp2] = monIc
        boundReached = -1
        print("---------------------------------\n")
        # print the battleMap with creature locations
        for g in battleMap:
            for h in g:
                print(''.join(h), " ", end = "")
            print()

        playerMove = 3
        monsterMove = 3

        while(tookAction == 0):
            attacked = 0
            print("\nYou are @. The ", monster.name, "is &. You may move 3 spaces and take an action.\nYour actions are:\n", '\n', player.printOptions())
            action = input()

            if(action == "move"):
                while(player.movement > 0):
                    print("pp1: ", pp1, "pp2: ", pp2, "\n mp1: ", mp1, " mp2: ", mp2, "\n")

                    # previous value is used to draw iconc after the player moves away, and to check against when 
                    # player tries to move into an enemy space
                    previous = (pp1, pp2)
                    playerDir = input("Which direction? north, east, south, west, or stop (case sensitive)? \n")
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

            elif(action == "attack"):
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
                                    print("You swing your longsword, dealing ", dmg, " points of damage to the ", monster.name, "\n", sep = '')
                                elif(dmg == 0):
                                    print("You swing your longsword, but the ", monster.name, " deftly leaps clear of the blade!\n", sep = '')
                            else:
                                print("\nYou need to be adjacent to the monster!\n")
                        if(temp == "ranged"):
                            attacked = 1
                            dmg = player.attack("ranged", monster.ac)
                            monster.setHp(monster.hp - dmg)
                            if(dmg > 0):
                                print("You loose an arrow, striking the foul creature and dealing ", dmg, " points of damage\n", sep = '')
                            elif(dmg == 0):
                                print("You loose an arrow, it strikes the ", monster.name, "'s armored gauntlet, destroyed on impact, dealing no damage \n", sep = '')
                    print("player hp: ", player.hp, " monster hp: ", monster.hp)
                    tookAction = 1
            elif(action == "dodge"):
                tookAction = 1
            elif(action == "spell"):
                #ask which spell
                #account for spell usage limits
                pass 

            #etc 

        # enemy turn melee type
        if(monster.attackType == "melee"):
            for i in range(0, 3):
                monsterWaited = 0
                print("pp1: ", pp1, "pp2: ", pp2, "\n mp1: ", mp1, " mp2: ", mp2, "\n")
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
                        # move north
                    elif(diff1 < -1):
                        monsDir = "south"
                        # move south
                elif(abs(diff2) >= abs(diff1)):
                    # move along b axis
                    if(diff2 > 1):
                        monsDir = "west"
                        # move west
                    elif(diff2 < -1):
                        monsDir = "east"
                        # move east

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
                    print("---------------------------------\n")
                    print("Monster movement!\n")
                    for g in battleMap:
                        for h in g:
                            print(''.join(h), " ", end = "")
                        print()
                    print("---------------------------------\n")
                    time.sleep(2)

            # Monster attacks player
            if(adjacent(pp1, pp2, mp1, mp2) == 1):
                dmg = monster.attack(player.ac)
                dmg2 = monster.attack(player.ac)
                # disadvantage if player took dodge action
                if(action == "dodge"):
                    dmg = min(dmg, dmg2)
                player.setHp(player.hp - dmg)
                # more stuff
                print("monster attacks!\nYou take ", dmg, " points of damage")
                print("player hp: ", player.hp, " monster hp: ", monster.hp)

        # ranged attack type
        # ranged monster just moves left and right on the map. simple.

        elif(monster.attackType == "ranged"):
            if(monMoveTicker == 0):
                for i in range(0, 2):
                    mPrevious = (mp1, mp2)
                    (mp1, mp2, none) = worldMove(mp1, mp2, 7, "west")
                    # fixes a bug whereby monster waiting would not draw the monsIc
                    if(monsterWaited == 0):
                        mapBackupM2 = battleMap[mp1][mp2]
                        battleMap[mp1][mp2] = monIc
                        battleMap[mPrevious[0]][mPrevious[1]] = mapBackupM1
                        # swap bucket values for the next loop
                        mapBackupM1 = mapBackupM2
                    # print the battleMap with updated creature locations
                        print("---------------------------------\n")
                        print("Monster movement!\n")
                        for g in battleMap:
                            for h in g:
                                print(''.join(h), " ", end = "")
                            print()
                        print("---------------------------------\n")
                        time.sleep(2)
                monMoveTicker = 1
            # I know this is not good practice, I should refactor this movement block into a function
            # I might do that later, or I might just leave this as-is
            elif(monMoveTicker == 1):
                for i in range(0, 2):
                    mPrevious = (mp1, mp2)
                    (mp1, mp2, none) = worldMove(mp1, mp2, 7, "east")
                    # fixes a bug whereby monster waiting would not draw the monsIc
                    if(monsterWaited == 0):
                        mapBackupM2 = battleMap[mp1][mp2]
                        battleMap[mp1][mp2] = monIc
                        battleMap[mPrevious[0]][mPrevious[1]] = mapBackupM1
                        # swap bucket values for the next loop
                        mapBackupM1 = mapBackupM2
                    # print the battleMap with updated creature locations
                        print("---------------------------------\n")
                        print("Monster movement!\n")
                        for g in battleMap:
                            for h in g:
                                print(''.join(h), " ", end = "")
                            print()
                        print("---------------------------------\n")
                        time.sleep(2)
                monMoveTicker = 0

            dmg = monster.attack(player.ac)
            player.setHp(player.hp - dmg)
            if(dmg > 0):
                print("\nThe ", monster.name, " shoots an arrow from its longbow, you take ", dmg,
                    " points of damage as the arrow strikes a joint between you armor!\n", sep = '')
            elif(dmg == 0):
                print("\nAn arrow flies at you, but you lunge forward, ducking out of the missile's way\n")

        player.movement = 3
        if(monster.hp < 0):
            print("\n The ", monster.name, " has been vanquished! \n")
            victor = 1
        elif(player.hp < 0):
            print("You have died. Sad. \n")
            victor = 2
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
    a = 4
    b = 3
    while (winState != 1):
        # (win state will become 1 in a specific encounter)
        # set player position values to the new values at beginning of loop
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
        #print(pos[0])
        #print(pos[13])
        if(pos[0] == "encounter" and int(pos[13]) == 0):
            monster = Monster(pos[11])
            # set monster attributes here
            monster.setHp(pos[1])
            monster.setAc(pos[2])
            monster.setToHit(pos[3])
            monster.setDmgDie(pos[4])
            monster.setDmgBonus(pos[5])
            monster.setsaveBonus(pos[12])
            monster.setAttackType(pos[15])
            # return the player object with updated battle damage/ updated rewards
            print("before: ", player.hp)
            var = rollInitiative(monster, player, pos[6], pos[7], pos[8], pos[9], pos[10])
            print("victor: ", var)
            print("after: ", player.hp)
            # the encounter may give a key item to the player, or the location of the goal (winstate trigger)
            # I should set a trigger to know if this encounter has happened already,
            # in the case the player back tracks
        # if the player is still alive after the encounter, let them move
        # setting this to 1 should ensure player doesn't repeat encounters when backtracking
        pos[13] = 1
        print(pos[14])
        print("--------------------------------------------------------")
        print("a: ", a, "b: ", b)
        # pass current location data into worldMove(), then reassign any new values
        # !!!! throws a TypeError exception if an invalid value is input for direction- need to handle !!!!
        dir = input("What direction would you like to move?\noptions are: north, east, south, west (case sensetive): ")
        (a, b, boundaryReached) = worldMove(a, b, 6, dir)
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
