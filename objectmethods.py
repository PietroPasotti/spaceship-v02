# spaceship v02
# objectmethods
# will contain a single class for any object which may ever appear on a map
import random,math
import namegenmethods
from copy import deepcopy


sobject_tracker = []

class sobjectmethodsError(Exception):
	def __init__(self,parent):
		super().__init__(parent)
		
def roll(x):
	if x == 0:
		return 0
	else:
		x = int(math.sqrt(int(x) ** 2))
		try:
			num = random.randrange(1,int(x)+1,1)
		
		except ValueError:
			
			return 0
		
		return num

def canAttackers(listofships):
	return [ship for ship in listofships if ship.states['can_attack'] == True]
	
def canDefenders(listofships):
	return [ship for ship in listofships if ship.states['can_be_attacked'] == True]

class Sobject(object):
	
	def __init__(self,objectclass_str,specialattrs_dict = {}):
		"""Takes as input an objectclass, and optional specialattrs"""
		
		self.states = {}
		self.objectclass = objectclass_str
		
		if self.objectclass == 'ship':
			self.states['name'] = namegenmethods.namegen() # namegen!
			self.initShip(specialattrs_dict)
			
		elif self.objectclass == 'fleet':
			self.states['name'] = namegenmethods.namegen('f') # namegen!
			self.initFleet(specialattrs_dict)
			
		elif self.objectclass == 'asteroid':
			self.states['name'] = namegenmethods.namegen('a') # namegen!
			self.initAsteroid(specialattrs_dict)
			
		elif self.objectclass == 'building':
			self.states['name'] = namegenmethods.namegen('b') # namegen!
			self.initBuilding(specialattrs_dict)
			
		elif self.objectclass == 'debris':
			self.states['name'] == 'debris'
			self.initDebris(specialattrs_dict)
			
		else:
			return 'Unsupported objectclass input for Sobject constructor'
		
		sobject_tracker.extend([self])
		
		return None
	
	def __str__(self):
		return '{} {} ({}) '.format(self.objectclass, self.states.get('name', ''), self.states.get('code',''))
		
	def __repr__(self):
		return str(self.states) + str(self.objectclass)
			
	def initShip(self,specialattrs):
		"""Initializes the object as a ship."""
		self.states['shipclass'] = specialattrs.get('shipclass', 'fighter') # tries to get the specialattr 'shipclass'; otherwise it's a fighter
		
		#shipMaxNos = {'fighter':500, 'mothership':2, 'bomber':100, 'cruiser':40,'destroyer':30}
		
		# now it should retrieve the fundamental attributes of the shipclass.
		shipdict = {'fighter' : 	{'max_attack':10,
									'max_speed':10,
									'max_hull_integrity':40,
									'max_range':1,
									'max_shields': 0,
									'code':'f'},
									
					'mothership':	{'max_attack':100,
									'max_speed':5,
									'max_hull_integrity':500,
									'max_range':3,
									'max_spawn':1,
									'max_shields':20,
									'code': 'M'},
					
					'destroyer':	{'max_attack':50,
									'max_speed':4,
									'max_hull_integrity':120,
									'max_range':3,
									'max_shields':10,
									'code': 'd'},
		
					'cruiser':		{'max_attack':40,
									'max_speed':12,
									'max_hull_integrity':70,
									'max_range':5,
									'max_shields':5,
									'code': 'c'},
																		
					'swarmer':		{'max_attack':5,
									'max_speed':8,
									'max_hull_integrity':10,
									'max_range':1,
									'code': 's'},									
									
					'bomber':		{'max_attack':30,
									'max_speed':7,
									'max_hull_integrity':50,
									'max_range':5,
									'rockets':2,
									'max_shields':2,
									'code': 'b'}									
									}
								
		possiblestates = ['max_attack', 'max_speed','max_range','max_warp','max_shields','max_spawn','cargo','code','max_hull_integrity','max_range']
			
		for a in possiblestates: # list of all possible states a freshly initialized ship may have
			fetchedvalue = shipdict[self.states['shipclass']].get(a,None) 
			if fetchedvalue != None:
				self.states[a] = fetchedvalue 
			else:
				pass
		
		# now we OVERRIDE the default parameters with the optional ones we have passed with specialattrs
		for key in specialattrs:
			self.states[key] = specialattrs[key] # for examples we may have wanted to create a non intact ship. specialattrs = {'health' = 'damaged'}
		
		# now we define all the states which a ship must have no-matter-what, and that do not depend on shipclass
		self.states['hull_integrity'] = self.states['max_hull_integrity'] # sets life to maximum
		self.states['special_conditions'] = []                            # no special condition to begin with
		
		
		# now we make the object check its properties, so that it updates automatically all dependencies between states
		self.checkStates()
		return None
		
		
	def initFleet(self,specialattrs):
		"""Initializes a fleet-subclass object."""
		self.states['fleetmode'] = specialattrs.get('fleetmode', 'point') # the fleet can be a group of ships all in the same position, or a sparse one
		self.states['code'] = 'O'
		self.states['shiplist'] = []
		orishiplist = specialattrs.get('shiplist')
		
		if orishiplist == None:
			print('aborting... cannot initialize a fleet with no ships.')
			return None
			
		specialattrs.pop('shiplist')
																										
		supportedshipclassnames = ('fighter','swarmer','bomber','destroyer','mothership','cruiser','whatever')	
		for elem in orishiplist:
			if isinstance(elem,Sobject) == True:
				self.states['shiplist'].extend([elem])
			elif isinstance(elem,str) and elem in supportedshipclassnames: # parses it into a fresh ship		
				newship = Sobject('ship',{'shipclass':elem})
				self.states['shiplist'].extend([newship])
			else:
				raise sobjectmethodsError('Wrong input for fleet constructor: got an {}'.format(self.states['shiplist']))	
			
		
		# attributes any fleet must have
		
		self.states['special_conditions'] = []
		
		# overrides anything previously upped, if special params were passed
		for key in specialattrs:
			self.states[key] = specialattrs[key]
			
		self.fleet_CheckStates()
		print('{} initialized'.format(str(self)))

	def fleet_CheckStates(self):
		"""Updates all updateable states."""
		
		if self.objectclass != 'fleet':
			raise sobjectmethodsError('fleet_CheckStates called on non-fleet object.')
		
		# prunes away all destroyed players: they're not kept track of anymore
		self.states['shiplist'] = [ship for ship in self.states['shiplist'] if ship.states['health'] != 'destroyed']

		for ship in self.states['shiplist']:
			ship.ship_CheckStates()	
		
		if self.states['shiplist'] == []:
			# then it dies.
			self.states.clear()
			print('{} has been pulverized with honour.'.format(str(self)))
			return None
		
		self.states['speed'] = min([ship.states['speed'] for ship in self.states['shiplist']])
		self.states['attack'] = sum([ship.states['attack'] for ship in self.states['shiplist']])
		self.states['range'] = max([ship.states['range'] for ship in self.states['shiplist']])
		# sensor arrays quality and range
		
		if [ship for ship in self.states['shiplist'] if ship.states['can_attack'] == True] == []:
			self.states['can_attack'] = False
		else:
			 self.states['can_attack'] = True
		
		if [ship for ship in self.states['shiplist'] if ship.states['can_be_attacked'] == True] == []:
			self.states['can_be_attacked'] = False
		else:
			self.states['can_be_attacked'] = True
			
		if [ship for ship in self.states['shiplist'] if 'hidden' not in ship.states['special_conditions']] == []: # if everyone is hidden
			if 'hidden' not in self.states['special_conditions']:
				self.states['special_conditions'].extend(['hidden'])
			else:
				pass
		else:
			if 'hidden' in self.states['special_conditions']:
				self.states['special_conditions'].remove(['hidden'])
			else:
				pass		
					
	def initAsteroid(self, specialattrs):	
		
		self.built = False
		self.states['code'] = '1'
		self.states['attackable'] = False
		self.states['hostile'] = False
		self.checkStates()	
		
	def checkStates(self,params = None):
		"""Updates automatically all dependencies between states."""
		
		if self.objectclass == 'asteroid':
			if self.building.states['health'] == 'destroyed':
				self.built = False
			else:
				self.built = True
		elif self.objectclass == 'ship':
			return self.ship_CheckStates()
		elif self.objectclass == 'fleet':
			return self.fleet_CheckStates()
		# all other classes
		else:
			return None

	def ship_CheckStates(self):
		"""Subfunction for ship's states"""
		
		life = self.states['hull_integrity']
		maxlife = self.states['max_hull_integrity']
		
		if life<=-10:
			healthState = 'destroyed'
		elif -10<life<=0:
			healthState = 'severely_damaged'
		elif 0< life <= (maxlife / 3):
			healthState = 'seriously_damaged'
		elif (maxlife / 3) < life <= ((2 * maxlife) / 3):
			healthState = 'damaged'
		elif ((2 * maxlife) / 3) < life < maxlife:
			healthState = 'lightly_damaged'
		elif life == maxlife:
			healthState = 'intact'
		else:
			raise sobjectmethodsError('Something wrong with health Sobject.ship_CheckStates routine.')
		
		self.states['health'] = healthState
		
		attackmodifiers = {	'intact':1,
							'lightly_damaged':0.8,
							'damaged':0.6,
							'seriously_damaged':0.4,
							'severely_damaged':0.2,
							'destroyed':0}
							
		shieldsmodifiers = {'intact':0,
							'lightly_damaged':-3,
							'damaged':-7,
							'seriously_damaged':-12,
							'severely_damaged':-17,
							'destroyed':-23}
		
		genericmodifier = attackmodifiers[healthState] # a positive float
		
		shieldmodifier = shieldsmodifiers[healthState] # will be a negative integer
		
		self.states['attack'] = int(self.states['max_attack'] * genericmodifier)
		self.states['shields'] = max(int(self.states.get('max_shields',0) + shieldmodifier),0)
		self.states['speed'] = int(self.states['max_speed'] * genericmodifier) # same as attack!
		self.states['range'] = int(self.states['max_range'] * genericmodifier)
		
		if self.states['attack'] == 0:
			self.states['can_attack'] = False
		else:
			self.states['can_attack'] = True
			
		# parses states[conditionsmodifiers], to override all other conditions
		
		a = self.states.get('special_conditions')
		if a != None:
			for condition in self.states['special_conditions']:
				if condition == 'disabled': # DISABLED
					self.states['attack'] = 0
					self.states['can_attack'] = False
					self.states['speed'] = 0
					if self.states.get('warp') != None:
						self.states['warp'] = False
				if condition == 'jammed': # JAMMED
					self.states['range'] = 1
					self.states['speed'] -= 1
					if self.states.get('shields',None) != None and self.states.get('shields',None) > 1:
						self.states['shields'] -= 1
					if self.states.get('rockets',None) != None:
						self.states.pop('rockets')
				if condition == 'hidden': # HIDDEN
					self.states['visible'] = False
					
				
		else:
			pass
			
		#canbeattacked conditions:	
		
		if self.states['health'] == 'destroyed' or 'hidden' in self.states.get('special_conditions',[]) == True:
			self.states['can_be_attacked'] = False
		else:
			self.states['can_be_attacked'] = True




	def attack(self,other):
		"""Any combination of ship vs fleet vs building."""
		if isinstance(other,Sobject) == False:
			raise objectmethodsError('Bad input for Sobject.attack function: ' + str(other) + ' is not a Sobject.')
		
		if self.objectclass == 'fleet' and other.objectclass == 'fleet': # either is a fleet or is a non fleet(building or ships; they behave similarly)
			return self.generalizedAttack(other,'ff')
		elif self.objectclass == 'fleet' and other.objectclass != 'fleet':
			return self.generalizedAttack(other,'fs')
		elif self.objectclass != 'fleet' and other.objectclass == 'fleet':
			return self.generalizedAttack(other,'sf')
		else:
			return self.generalizedAttack(other,'ss')
			
	def generalizedAttack(self,other,params):
		"""Self attacks other."""
		if params not in ['ff','sf','fs','ss']:
			raise objectmethodsError('Bad input for Fight parameters: ' + str(params) + ' received.')
			
		if params[0] == 'f':
			Attackers = self.states['shiplist']
		else:
			Attackers = [self]
			
		if params[1] == 'f':
			Defenders = other.states['shiplist']
		else:
			Defenders = [other]
	
		Can_attackers = canAttackers(Attackers)
		Can_defenders = canDefenders(Defenders)
		
		if Can_attackers == [] or Can_defenders == []: # no fight can happen here!
			return None
		
		for ship in Can_attackers:

			enemy = random.choice(canDefenders(Defenders))
			
			damageDealt = roll(ship.states['attack']) - max(enemy.states.get('shields', 0),0)
			damageDealt = max(damageDealt,0)
			
			enemy.states['hull_integrity'] -= damageDealt
			enemy.ship_CheckStates() # updates all of his properties, over all attack
			
			damageSuffered = roll(enemy.states['attack']) - max(self.states.get('shields', 0),0)
			damageSuffered = max(damageSuffered,0)
			ship.states['hull_integrity'] -= damageSuffered
			ship.ship_CheckStates() # updates its own properties

			print(str(ship) + 'suffered ' + str(damageSuffered) + ' and inflicted ' + str(damageDealt))
		
		self.checkStates() # so that if they are fleets...
		other.checkStates()
		
		return None
		
	def battle(self,other):
		"""Any combination of ship vs fleet vs building."""
		if self.objectclass == 'fleet' and other.objectclass == 'fleet': # either is a fleet or is a non fleet(building or ships; they behave similarly)
			return self.generalizedBattle(other,'ff')
		elif self.objectclass == 'fleet' and other.objectclass != 'fleet':
			return self.generalizedBattle(other,'fs')
		elif self.objectclass != 'fleet' and other.objectclass == 'fleet':
			return self.generalizedBattle(other,'sf')
		else:
			return self.generalizedBattle(other,'ss')
	
	def generalizedBattle(self,other,params):
		"""Self fights other to death."""
		if params not in ['ff','sf','fs','ss']:
			raise objectmethodsError('Bad input for Fight parameters: ' + str(params) + ' received.')
		
		iniattackers = deepcopy(len(self.states.get('shiplist',[1])))
		inidefenders = deepcopy(len(other.states.get('shiplist',[1])))
		
		Attackers = self.states.get('shiplist', [self])
		Defenders = other.states.get('shiplist',[other])
		
		if canAttackers(Attackers) == [] or canDefenders(Defenders) == []:
			print('No battle: either group is not able to fight.')
			return None
		
		while not canAttackers(Attackers) == [] and not canDefenders(Defenders) == []: # keeps attacking until either team is empty
			self.generalizedAttack(other,params)

		selfloss = iniattackers - len(self.states.get('shiplist',[1]))
		enemyloss = inidefenders - len(other.states.get('shiplist',[1]))

		print('Attacker has lost {} ships, enemy has lost {} ships.'.format(str(selfloss),str(enemyloss)))


a = Sobject('ship')

b = Sobject('ship',{'shipclass':'mothership'})

c = Sobject('ship',{'shipclass':'fighter'})

d = Sobject('fleet',{'shiplist':['fighter','destroyer','cruiser','swarmer',b]})

e = Sobject('fleet',{'shiplist':['fighter','fighter','destroyer','cruiser','mothership']})

a.attack(b)

b.attack(c)
c.attack(a)
a.attack(c)
