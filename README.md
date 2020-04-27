# ift383-dnd
A simple python text adventure and dnd combat simulator

You are an adventurer looking to find a fabled treasure in a lost valley. 
You are either a Sorcerer, weilding powerful magic, or a Fighter: stronger, and equipped with a bow!.

The game is partially a text adventure, with a 7x7 world map that the player navigates via text inputs on the terminal. 
The player can use magic potions, rest (getting the sorcerer's spells back at the cost of respawaning enemies), or move to a new location.

There is a key item that needs to be found, and a location to bring it to in order to win. You can find upgrades for your
armor or weapons, and magic potions to heal hp along the way. There are also many dangerous monsters that litter the landscape,
from angry centaurs, to mischevious kobolds. 

When the player encounters an enemy, a battle map is drawn and a battle begins. 
Combat is simplified from dnd rules: The player can move up to three spaces by typing the direction they want to go. 
They can attack, cast a spell, dodge, or heal.
The enemy AI is super simple: if it is a ranged type, they just move back and forth and lob arrows at you.
If they're a melee type, they hunt the player down and attack once they're adjacent with the player. 

The game tracks hp, ac, damage bonuses, damage die, and all other stats necessary for slightly complex and interesting combat. 
