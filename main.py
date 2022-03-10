import time
import random

name = ""
bg = ""
invmax = 0
inv = {}

#This func exists for efficiency sakes, it requires a lot less typing to call this instead of calling time.sleep
def w():
	time.sleep(0.5)

class entity:
	n = ""
	damagerange = []
	chance = []
	hp = 0
	dead =  False
	closecomb = False
	originchance = ()

	def __init__(self, entname, health, damagedeals, chanceofhit, close = False):
		self.n = entname
		self.damagerange = damagedeals
		self.chance = chanceofhit
		self.hp = health
		self.closecomb = close
		self.originchance = tuple(chanceofhit)

	#When the monster is damaged
	def Damaged(self, amount, printdam=True):
		if self.dead == True:
			return
		self.hp -= amount
		if printdam:
			print(self.n, "has taken", amount, "damage, they now have", self.hp, "HP Left")
		if self.hp <= 0:
			print(self.n, "has died")
			self.dead = True

	def hit(self, entitytohit, isPlayer=False, playerent=None, prox = 0):
		if self.dead == True or entitytohit.dead == True:
			print("Cannot hit, character is dead")
			return

		if isPlayer == False:
			print(self.n, "is attacking", entitytohit.n)
		else:
			if playerent.dead == True:
				print("Cannot hit, player is dead")
				return
			print("You are attacking", entitytohit.n, "with your", self.n)
	
			if self.closecomb == True and entitytohit.chance[1] == entitytohit.originchance[1]:
				print("You must move closer to", entitytohit.n+", they will be more likely to hit you next time they try.")
				entitytohit.chance[1] -= 1 

		isHit = random.randint(0, self.chance[1])
		if isHit <= self.chance[0]-prox:
			entitytohit.Damaged(random.randint(self.damagerange[0], self.damagerange[1]))
		else:
			print(self.n, "missed!")

def multichoicenum(options, retselnum=False, desc=False, descs=[]):
	i = 1
	x = None
	success = False
	while success == False:
		for x in options:
			if desc == False:
				print(str(i)+".", x)
			elif desc == True:
				print(str(i) + ".", x+", "+descs[i])
			i += 1
		try:
			x = input("Input the number of the option you want to choose: ")
			n = options[int(x)-1]
			success = True
			if retselnum == False:
				return n
			else:
				return x-1
		except:
			print("Enter a valid input!")
			i = 1
			continue

def multichoice(choicegiven, options):
	optioninits = []
	success = False
	for x in range(0, len(options)):
		optioninits.append(options[x][0])
	while success == False:
		c = input(choicegiven + ' ' + '/'.join(optioninits) + ": ")
		for x in options:
			if c.lower() == x or c.lower() == x[0]:
				return x
		print("Please select a valid option!")

def battle(monsters, playerent, inv):
	w()
	print("You have chosen to fight the monsters")
	selMon = False
	if len(monsters) > 1:
		selMon = True
	w()
	print("Please choose the weapon you would like to fight with:")
	weapon = None
	des = []

	wchoice = multichoicenum(list(inv))
	weapon = inv[wchoice]
	print(weapon.name)

player = entity(name, 100, [3, 8], [1, 3])

def start():	
	name = input("Welcome adventurer! What is your name?\n")
	w()
	print("Hello", name+"! What background would you like your character to have? ")
	w()
	print("The Local Guide background gives you an increased inventory capacity of 10 with a knife that deal a max 10 damage as a weapon.")
	w()
	print("The Soldier background gives you an inventory capacity of 5 items with a sword that deals a max 20 damage and is more likely to hit plus a bow which deals a max 15 damage and makes you less likely to be hit by a monster when used.")
	w()
	print("Please make your choice now: ")
	bg = multichoicenum(["Local Guide", "Soldier"])
	w()
	print("You have chosen to be a", bg)
	w()
	mc = multichoice("Does that sound correct?", ["yes", "no"])
	w()
	if mc == "no":
		print("Ok then, we'll restart")
		w()
		#not exactly elegant but this is the only way to clear the screen
		for x in range(0, 100):
			print("\n")
		start()
	if mc == "yes":
		if bg == "Local Guide":
			invmax = 10
			inv["Knife"] = entity("knife", None, [5, 10], [1, 3], True)
		elif bg == "Soldier":
			invmax = 5
			inv["Sword"] = entity("sword", None, [10, 20], [1, 2], True)
			inv["Bow"] = entity("bow", None, [5, 15], [1, 3])

		print("Good! Lets start!")
		w()
		for x in range(0, 100):
			print("\n")
		print("You wake up in camp!")
		w()
		print("Yesterday was a big day, today your hoping to reach your final destination!")
		w()
		print("You start getting ready for the day.")
		w()
		print("You brush your teeth, get dressed, eat breakfast and pack up your camp.")
		w()
		print("Now your ready for the day, you must decide whether you want to start out going left or right.")
		lr = multichoice("Would you like to go left or right?", ["left", "right"])
		if lr == "left":
			C1L()
		elif lr == "right":
			C1R()

def C1L():
	w()
	print("\nYou have chosen to go left")
	w()
	print("You come upon a clearing")
	w()
	print("In the clearing you can see two monsters.")
	w()
	fnopslg = ["Fight the monsters", "Try to pass through the clearing", "Use Local knowledge to pass around the clearing"]
	fnops = ["Fight the monsters", "Try to pass through the clearing"]
	if bg == "Local Guide":
		fn = multichoicenum(fnopslg)
	else:
		fn = multichoicenum(fnops)
	if fn == fnopslg[0]:
		Monster1 = entity("Monster 1", 40, [5, 10], [1, 3])
		Monster2 = entity("Monster 1", 40, [5, 10], [1, 3])
		battle([Monster1, Monster2], player, inv)

def C1R():
	print("ri")

start()