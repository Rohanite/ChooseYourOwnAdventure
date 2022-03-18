import time
import random

name = ""
bg = ""
invmax = 0
inv = {}
Debug = False

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

	leave = False
	while True:
		i = 1
		x = ""
		for x in options:
			if desc == False:
				print(str(i)+".", x)
			elif desc == True:
				print(str(i) + ".", x+", "+str(descs[i-1]))
			i += 1
		try:
			x = input("Input the number of the option you want to choose: ")
			if x.lower() == "restart":
				start()
			if x.lower() == "quit":
				leave = True
				break
			if x.lower() == "inv" or x.lower() == "inventory":
				print("You have decided to check your inventory")
				print("Your currently usable items are: ")
				n = 1
				for x in list(inv):
					i = inv[x]
					if i.healer == True:
						print(str(n)+". "+i.n+ ", Heals: "+str(i.hp)+"HP (You have "+str(player.hp)+"HP left)")
						n += 1
				print(str(n)+". Actually I'd rather not use any of these items")
				j = input("Enter the number of the item you would like to use: \n")
				try:
					if int(j) == n:
						print("You have chosen not to use any of these items")
						continue
					it = inv[list(inv)[int(j)]]
					player.hp += it.hp
					inv.pop(list(inv)[int(j)])
					print("Your HP is now at",player.hp)
					continue
				except:
					print("Please select a valid option!")
					continue
			n = options[int(x)-1]
			if retselnum == False:
				return n
			else:
				return int(x)-1
		except:
			print("Enter a valid input!")
			i = 1
			continue
	if leave == True:
		exit(1)


def multichoice(choicegiven, options):
	optioninits = []
	success = False
	for x in range(0, len(options)):
		optioninits.append(options[x][0])
	while success == False:
		c = input(choicegiven + ' ' + '/'.join(optioninits) + ": ")
		if c.lower() == "restart":
			start()
		if c.lower() == "quit":
			exit(1)
		if c.lower() == "inv" or c.lower() == "inventory":
			print("You have decided to check your inventory")
			print("Your currently usable items are: ")
			n = 1
			for x in list(inv):
				i = inv[x]
				if i.healer == True:
					print(str(n)+". "+i.n+ ", Heals: "+str(i.hp)+"HP (You have "+str(player.hp)+"HP left)")
					n += 1
			print(str(n)+". Actually I'd rather not use any of these items")
			j = input("Enter the number of the item you would like to use: \n")
			try:
				if int(j) == n:
					print("You have chosen not to use any of these items")
					continue
				it = inv[list(inv)[int(j)]]
				player.hp += it.hp
				inv.pop(list(inv)[int(j)])
				print("Your HP is now at",player.hp)
				continue
			except:
				print("Please select a valid option!")
				continue
					
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
		exit(1)
	if qr == 1:
		start()

def battle(monsters):

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

	for x in items:
		w()
		print("You have found a", x.n)
	w()
	
	print("Your inventory has the capacity for", invmax-len(inv), "more items")
	for x in items:
		w()
		if x.healer == True:
			pu = multichoice("Would you like to pick up "+x.n+": Heals: "+str(x.hp)+"HP (You have "+str(player.hp)+"HP left)", ["yes", "no"])
		else:
			pu = multichoice("Would you like to pick up "+x.n+": Damage: " + str(x.damagerange[0]) + " - " + str(x.damagerange[1]) + ", Chance of hitting target: " + str(x.chance[0]) + " in " + str(x.chance[1]) + ", is getting close required to hit: " + str(x.closecomb), ["yes", "no"])
		if pu == "yes":
			if len(inv) < invmax:
				inv[x.n.replace(" ", "")] = x
				print(x.n+" has been added to your inventory")
			else:
				print("Your inventory is full!")
				w()
				print("To put this item in your inventory you're going to need to drop an item!")
				des = []
				for c in list(inv):
					i = inv[c]
					if i.healer == True:
						des.append("Heals: "+str(i.hp)+"HP (You have "+str(player.hp)+"HP left)")
					else:
						des.append("Damage: " + str(i.damagerange[0]) + " - " + str(i.damagerange[1]) + ", Chance of hitting target: " + str(i.chance[0]) + " in " + str(i.chance[1]) + ", is getting close required to hit: " + str(i.closecomb))
				nas = []
				k = []
						
				for g in list(inv):
					nas.append(inv[g].n)
					k.append(g)
				nas.append("Actually never mind, I won't pick this item up")
				des.append("")
				choice = multichoicenum(nas, True, desc=True, descs=des)
				if nas[choice] == nas[len(nas)-1]:
					print("You have decided not to pick this item up.")
					continue
				else:
					inv.pop(k[choice])
					inv[x.n.replace(" ", "")] = x
					print(x.n+" has been added to your inventory")
		else:
			print("You have decided not to pick this item up.")
				
					
				


def start():
	global invmax
	global bg
	inv.clear()
	name = input("Welcome adventurer! What is your name?\n")
	player.n = name
	w()
	print("Hello", name+"! What background would you like your character to have? ")
	w()
	print("Please make your choice now: ")
	bg = multichoicenum(["Local Guide", "Soldier"], desc=True, descs=["Max inventory capacity: 10, Starting weapon: Knife which deals 10 to 15 damage, plus a 20HP healing potion", "Max inventory capacity: 5. Starting weapons: Sword which deals 15 to 25 damage plus a bow which deals 10 to 15 damage but saves you from having to get close to monsters"])
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
			inv["Knife"] = entity("Knife", None, [10, 15], [1, 2], True)
			inv["HealingPotion"] = entity("20HP Healing Potion", 20, None, None, hItem=True)

		elif bg == "Soldier":
			if Debug == False:
				invmax = 5
			else:
				invmax = 2
			inv["Sword"] = entity("Sword", None, [15, 25], [1, 2], True)
			inv["Bow"] = entity("Bow", None, [10, 15], [1, 3])

		print("Good! Lets start!")
		w()
		for x in range(0, 100):
			print("\n")
		print("(Do note that you can type quit or restart at any input prompt to do that and you can type inv at any input prompt to open your inventory and use healing items)")
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
	if bg == 'Local Guide':
		fn = multichoicenum(fnopslg)
	else:
		fn = multichoicenum(fnops)
	if fn == fnopslg[0]:
		Monster1 = entity("Monster 1", 50, [5, 10], [1, 3])
		Monster2 = entity("Monster 2", 50, [5, 10], [1, 3])
		w()
		print("You have chosen to fight the monsters")
		battle([Monster1, Monster2])
		print("You search the area to see if the monsters had any valuable possessions")
		StrSword = entity("Strong Sword", None, [20, 35], [1, 2], True)
		HPotion = entity("40HP Healing Potion", 40, None, None, hItem=True)
		invItems([StrSword, HPotion])
	if fn == fnopslg[1]:
		print("You have chosen to try and pass through the clearing")
		w()
		print("As you try to sneak through the clearing a monster suddenly turns around")
		w()
		print("He sees you and starts heading towards you looking angry")
		w()
		print("The other monster has noticed and now both are going after you!")
		w()
		print("Your only choice now is to fight!")
		Monster1 = entity("Monster 1", 50, [5, 10], [1, 3])
		Monster2 = entity("Monster 2", 50, [5, 10], [1, 3])
		w()
		battle([Monster1, Monster2])
		print("You search the area to see if the monsters had any valuable possessions")
		StrSword = entity("Strong Sword", None, [20, 35], [1, 2], True)
		HPotion = entity("40HP Healing Potion", 40, None, None, hItem=True)
		invItems([StrSword, HPotion])
	if fn == fnopslg[2]:
		w()
		print("You decide to try and find a way around the clearing.")
		w()
		print("You know of a very rough track around here that should allow you to pass problem free.")
		w()
		print("The path successfully gets you out of the way of the monsters!")
	w()
	print("You continue on your path")
	w()
	print("You stumble upon a cabin")
	w()
	ch = multichoice("Would you like to enter the cabin?", ["yes", "no"])
	if ch == "yes":
		w()
		print("You decide to enter the cabin")
		w()
		print("When you enter you are relieved to find no monsters")
		w()
		print("You decide to see if you can find anything")
		WkBow = entity("Weak Bow", None, [5, 10], [1, 3])
		Sword = entity("Sword", None, [15, 25], [1, 2], True)
		HPot = entity("20HP Healing Potion", 20, None, None, hItem = True)
		invItems([WkBow, Sword, HPot])
		w()
		print("After going through everything in the cabin you leave")
		w()
		print("You continue on you path")
		RMP()
	else:
		w()
		print("You have decided not to enter the cabin")
		w()
		print("You continue on your path")
		RMP()

def C1R():
	w()
	print("You decide to go right from camp")
	w()
	if bg == 'Soldier':
		print("You notice a trap up ahead!")
		w()
		print("You can try and defuse the trap if you want or you could try and run away")
		w()
		choi = multichoicenum(["Run away", "Defuse"], True)
		if choi == 0:
			print('You decide to try and run away')
			w()
			print("As you try to run some monsters see you")


def RMP():
	print("remeet")

start()
