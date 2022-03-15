import time
import random

name = ""
bg = ""
invmax = 0
inv = {}

#This func exists for efficiency sakes, it requires a lot less typing to call this instead of calling time.sleep
def w():
	time.sleep(1)


class entity:
	n = ""
	damagerange = []
	chance = []
	hp = 0
	dead =  False
	closecomb = False
	originchance = ()
	healer = False

	def __init__(self, entname, health, damagedeals, chanceofhit, close=False, hItem=False):
		self.n = entname
		self.damagerange = damagedeals
		self.chance = chanceofhit
		self.hp = health
		self.closecomb = close
		self.healer = hItem
		try:
			self.originchance = tuple(chanceofhit)
		except:
			self.originchance = chanceofhit

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
		w()
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
				w()
				print("You must move closer to", entitytohit.n+", they will be more likely to hit you next time they try.")
				entitytohit.chance[1] -= 1 
		w()
		isHit = random.randint(0, self.chance[1])
		if isHit <= self.chance[0]-prox:
			entitytohit.Damaged(random.randint(self.damagerange[0], self.damagerange[1]))
		else:
			print(self.n, "missed!")

player = entity(name, 100, [3, 8], [1, 3])

def multichoicenum(options, retselnum=False, desc=False, descs=[]):
	i = 1
	x = ""
	while True:
		for x in options:
			if desc == False:
				print(str(i)+".", x)
			elif desc == True:
				print(str(i) + ".", x+", "+str(descs[i-1]))
			i += 1
		try:
			x = input("Input the number of the option you want to choose: ")
			n = options[int(x)-1]
			if retselnum == False:
				return n
			else:
				return int(x)-1
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

def dead():
	w()
	print("You have died!")
	w()
	print("Would you like to restart the game or quit?")
	qr = multichoicenum(["Quit", "Restart"], True)
	if qr == 0:
		quit()
	if qr == 1:
		start()

def battle(monsters):
	w()
	print("You have chosen to fight the monsters")
	selMon = False
	while True:
		if player.dead == True:
			dead()

		if len(monsters) > 1:
			selMon = True
		else:
			selMon = False
		w()
		print("\nPlease choose the weapon/item you would like to use/fight with:")
		weapon = None
		des = []
		for x in list(inv):
			i = inv[x]
			if i.healer == True:
				des.append("Heals: "+str(i.hp)+"HP (You have "+str(player.hp)+"HP left)")
			else:
				des.append("Damage: " + str(i.damagerange[0]) + " - " + str(i.damagerange[1]) + ", Chance of hitting target: " + str(i.chance[0]) + " in " + str(i.chance[1]) + ", is getting close required to hit: " + str(i.closecomb))
		nas = []
		k = []
				
		for x in list(inv):
			nas.append(inv[x].n)
			k.append(x)
		wchoice = multichoicenum(nas, True, desc=True, descs=des)
		weapon = inv[k[wchoice]]
		mfight = 0
		w()
		if weapon.healer == True:
			player.hp += weapon.hp
			inv.pop(k[wchoice])
			print("Your HP is now at",player.hp)
		else:

			if selMon == True:
				print("\nWhich monster would you like to attack?")
				de = []
				mn = []
				k = []
				for x in monsters:
					de.append(str(x.hp)+"HP left")
					mn.append(x.n)
				mfight = multichoicenum(mn, True, desc=True, descs=de)
			weapon.hit(monsters[mfight], True, player)

		i = 0
		for x in monsters:
			if x.dead == True:
				monsters.pop(i)
				continue
			x.hit(player)
			i += 1
		if bool(monsters) == False:
			w()
			print("You have won this battle! Congratulations!")
			break
	return

def invItems(items):
	multiIt = False
	if len(items) > 1:
		muliIt = True
	for x in items:
		w()
		print("You have found a", x.n)
	w()
	#FURTHER TESTING NEEDED HERE
	print("Your inventory has the capacity for", len(inv)-invmax, "more items")
		


def start():
	inv.clear()
	name = input("Welcome adventurer! What is your name?\n")
	player.n = name
	w()
	print("Hello", name+"! What background would you like your character to have? ")
	w()
	print("Please make your choice now: ")
	bg = multichoicenum(["Local Guide", "Soldier"], desc=True, descs=["Max inventory capacity: 10, Starting weapon: Knife which deals 5 to 10 damage, plus a 20HP healing potion", "Max inventory capacity: 5. Starting weapons: Sword which deals 10 to 20 damage plus a bow which deals 5 to 15 damage but saves you from having to get close to monsters"])
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
			inv["Knife"] = entity("Knife", None, [5, 10], [1, 3], True)
			inv["HealingPotion"] = entity("20HP Healing Potion", 20, None, None, hItem=True)
		elif bg == "Soldier":
			invmax = 5
			inv["Sword"] = entity("Sword", None, [10, 20], [1, 2], True)
			inv["Bow"] = entity("Bow", None, [5, 15], [1, 3])

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
		Monster2 = entity("Monster 2", 40, [5, 10], [1, 3])
		battle([Monster1, Monster2])
		print("You search the area to see if the monsters had any valuable possessions")
		StrSword = entity("Strong Sword", None, [15, 30], [1, 2], True)
		HPotion = entity("40HP Healing Potion", 40, None, None, hItem=True)
		invItems([StrSword, HPotion])

def C1R():
	print("ri")

start()