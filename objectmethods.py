# spaceship v02
# objectmethods
# will contain a single class for any object which may ever appear on a map
import random,math
import namegenmethods
import dialogmethods
from utilityfunctions import *
import utilityfunctions
from copy import deepcopy
import mapmethods

sobject_tracker = []
map_specials = None   # stores the map's height and width
mapcode_tracker = {}  # stores asteroids

class Sobject(object):
	
	def __init__(self,objectclass_str,specialattrs_dict = {}):
		"""Takes as input an objectclass, and optional specialattrs"""
		
		self.states = {'position':None}  # initial position is none by default
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
		
		elif self.objectclass == "externality":
			self.states['objectclass'] == 'externality'
			self.initExternality(specialattrs_dict)
			
		else:
			return 'Unsupported objectclass input for Sobject constructor'
		if self.objectclass != 'asteroid':
			sobject_tracker.extend([self])
		
		
		self.circle = None
		self.trackedBy = [] # the list of factions which have the rights to see the object
		
		return None
	
	def __str__(self):
		if self.objectclass == 'ship':
			return '{} {} {} ({})'.format(self.objectclass, self.states.get('shipclass'), self.states.get('name', ''), self.states.get('code',''))
			
		elif self.objectclass == 'building':
			return '{} {} {} ({})'.format(self.objectclass, self.states['buildingclass'], self.states['position'], self.states.get('code',''))
			
		elif self.objectclass == 'fleet':
			return '{} in mode {} {} ({})'.format(self.objectclass,self.states.get('mode', "'normal'"), self.states.get('position',''), self.states.get('code',''))	
		
		elif self.objectclass == 'asteroid':
			return 'asteroid {}, floating at {}'.format(self.states['name'],self.pos())
		
		else:
			return str(self.states)
		
	def __repr__(self):
		return str((self.objectclass, self.states))
	
	def name(self):
		return self.states['name']		
	
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
									'warp':(True,10), # warp! (ability_to_warp, cooldown) 
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
		self.states['action_points'] = 5.0								  # sets the action points to 10, which is half the maximum
		
		
		self.setupSensorArrays() # Sets up default sensor arrays
		
		
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
		self.states['action_points'] = 5.0
		
		# overrides anything previously upped, if special params were passed
		for key in specialattrs:
			self.states[key] = specialattrs[key]
			
		self.fleet_CheckStates()
		print('{} initialized'.format(str(self)))

	def initAsteroid(self, specialattrs):	
		"""Initializes an asteroid object."""
		
		self.states['building'] = None
		self.states['code'] = '1'
		self.states['name'] = namegenmethods.namegen('a')
		self.states['can_be_attacked'] = False
		self.states['inhert'] = True # can not be interacted with, and should not appear in menu voices
		self.states['hostile'] = False # not tracked as enemy by AI and sensors
		
		for entry in specialattrs: # we override the default with the optional parameters
			self.states[entry] = specialattrs[entry]
		
		self.checkStates()

	def initExternality(self,specialattrs):
		"""Initializes your favourite externality, from a superstring to a black hole, to an old alien wreckage."""
		
		self.states['codename'] = "ext_" + namegenmethods.namegen('a')
		
		for entry in specialattrs:  # most of the work here must be done by custom work!
			self.states[entry] = specialattrs[entry]		
		
		
	def initBuilding(self,specialattrs):
		"""Building Sobject initializer."""
		buildingclass = specialattrs.get('buildingclass')
		self.states['buildingclass'] = buildingclass
		
		if buildingclass == None:
			raise Exception('Building constructor wants a buildingclass; no default building.')
		else:
			pass
		
		buildingdict = {'base' : 	{'max_attack':150,
									'max_hull_integrity':500,
									'max_range':4,
									'max_shields': 20,
									'max_spawn':1,
									'code':'H'},
									
					'battery':		{'max_attack':100,
									'max_hull_integrity':200,
									'max_range':5,
									'max_shields':15,
									'code': 'B'},
					
					'buoy':			{'max_attack':0,
									'max_hull_integrity':5,
									'max_range':0,
									'max_shields':0,
									'code': 'b'}
									
									}
		
		possiblestates = ['max_attack', 'max_speed','max_range','max_warp','max_shields','max_spawn','cargo','code','max_hull_integrity','max_range']
			
		for a in possiblestates: # list of all possible states a freshly initialized building may have		
			fetchedvalue = buildingdict[buildingclass].get(a,None) 
			if fetchedvalue != None:
				self.states[a] = fetchedvalue 
			else:
				pass

		for key in specialattrs: # here we should retrieve the position!
			self.states[key] = specialattrs[key]
			
		selfpos = self.states.get('position')
		if selfpos == None:
			raise Exception('Bad bad bad.')
		
		myasteroid = mapcode_tracker[selfpos]			# finds his asteroid
		self.states['asteroid'] = myasteroid			
		sobject_tracker.append(self)					#### updates sobject_tracker
		
		if myasteroid.states['building'] != None:
			raise Exception('Trying to place a building on an already built asteroid.')
		
		myasteroid.states['building'] = self # tells the asteroid that now there is a building on it
			
			
		
		self.states['hull_integrity'] = self.states['max_hull_integrity'] # sets life to maximum
		self.states['special_conditions'] = []                            # no special condition to begin with
		self.states['action_points'] = 5.0								  # sets the action points to 10, which is half the maximum 	
		
		
		self.setupSensorArrays() # Sets up default sensor arrays
		
		
		self.checkStates()
		mapmethods.updatePoints(self.states['position'])
	
	def checkStates(self,params = None):
		"""Updates automatically all dependencies between states, of any subclass of Sobject, by calling their specific subfunctions."""
		
		if self.objectclass == 'asteroid': # DOES NOTHING; they are so small and simple that other methods can take care of that.
			pass 
		elif self.objectclass == 'ship':
			return self.ship_CheckStates()
		elif self.objectclass == 'fleet':
			return self.fleet_CheckStates()
		elif self.objectclass == 'building':
			return self.building_CheckStates()
		# all other classes
		else:
			return None

	def fleet_CheckStates(self):
		"""Updates all updateable states."""
		
		if self.objectclass != 'fleet':
			raise sobjectmethodsError('fleet_CheckStates called on non-fleet object.')
		
		# prunes away all destroyed players: they're not kept track of anymore
		self.states['shiplist'] = [ship for ship in self.states['shiplist'] if ship.states['health'] != 'destroyed']

		for ship in self.states['shiplist']:
			ship.ship_CheckStates()
			
		# ACTIONPOINTS:
		if sum([ship.states['action_points'] for ship in self.states['shiplist']]) == 0:
			self.states['action_points'] = 0 # there must be at least one ship able to act there in order for the fleet to do the same.	
			
		
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
	
	def building_CheckStates(self):
		"""Subfunction for buildings' states."""
		
		life = self.states['hull_integrity']
		maxlife = self.states['max_hull_integrity']
		self.states['health'] = utilityfunctions.computelife(life,maxlife)
		
		self.states = utilityfunctions.determinemodifiedvalues(self.states)
		
		if self.states['health'] == 'destroyed':
			self.states['can_be_attacked'] = False
		else:
			self.states['can_be_attacked'] = True
		
	def ship_CheckStates(self):
		"""Subfunction for ship's states."""
		
		life = self.states['hull_integrity']
		maxlife = self.states['max_hull_integrity']
		
		self.states['health'] = utilityfunctions.computelife(life,maxlife)
		
		self.states = utilityfunctions.determinemodifiedvalues(self.states) # updates the states depending on life and modifiers
			
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


# MOVEMENT FUNCTIONS
	def pos(self):
		return self.states['position']

	def canMove(self,arg=None):
		"""Checks whether the object can move (to somewhere, if give in params)"""
		switch = True

		if self.states.get('speed',0) == 0: 							# disabler 1 : speed
			switch = False
			
		if self.states['action_points'] == 0:							# disabler 2 : ap
			switch = False

		return switch

	def move(self,arg):
		"""Takes as input a position tuple, a direction, a sobject or a list of instructions.
		position tuple: goes there if it is not out of range, otherwise it moves as close as possible.
		direction: goes in that direction as far as it can
		list of instructions: it follows it as far as it can
		sobject: transforms it into a tuple (its position)."""
		
		if self.canMove(arg) == True:
			pass
		else:
			return None
		
		if arg != None:
			if isinstance(arg,Sobject):
				arg = arg.states['position']	
		else:
			raise Exception('No direction to move to. Arg is None.')
		
		if self.states.get('position') == None:						# only for utility
			self.warp(arg,['silent','override'])
		
		if self.states['position'] == arg:
			return None
		
		oripos = deepcopy(self.states['position'])
		
		instructionsDict = {'u':(0,-1),'d':(0,1),'l':(-1,0),'r':(1,0),'ul':(-1,-1),'ur':(1,-1),'dl' : (-1,1), 'dr':(1,1)}
		
		if isinstance(arg,str):
			if not [ letter in 'udlr' for letter in arg ] == [True for i in range(len(arg))]: # checks the syntax
				raise Exception('Input error for move function: received' + arg)
			else:
				counter = 0
				while counter < len(arg): # until the end of the string or the end of its speed; the shortest
					if counter >= self.states['speed']:
						print('The object cannot move that much: breaking...')
						break
					
					syllable = 'guruguru'
					
					if len(arg) >= counter + 2:
						syllable = arg[counter] + arg[counter + 1] # picks the next two letters.
						
					if syllable in ['ul','ur','dl','dr']:						# recognize		
						X,Y = self.states['position']
						X = X + instructionsDict[letter][0]
						Y = Y + instructionsDict[letter][1]
						
						if self.ap_pay('move2') == True: 						# AP checkpoint
							pass
						else:
							return 'The ship has no more action_points'
						
							
						self.states['position'] = mapmethods.torusize((X,Y))
						counter +2												# counter goes 2 up
					else:							
						letter = arg[counter] # parses the string from 0 to end
						X,Y = self.states['position']
						X = X + instructionsDict[letter][0]
						Y = Y + instructionsDict[letter][1]
						
						if self.ap_pay('move1') == True:						 # AP checkpoint
							pass
						else:
							return 'The ship has no more action_points'						
						
						self.states['position'] = mapmethods.torusize((X,Y))
						counter +=1
		
		elif isinstance(arg,tuple):
	
			arg = self.closestTowards(arg)
			dist = mapmethods.distance(oripos,arg)
			if self.ap_pay(dist)	 == True:				# AP checkpoint
				pass
			else:
				raise Exception('Something wrong here. My APs are {}; oripos = {}, arg = {}'.format(self.actionpoints(), oripos, arg))
			self.states['position'] = arg
			
			pass
		
		else:
			raise Exception('Unrecognized argument for move routine: ' +str(arg))	
			
		if self.objectclass != 'fleet':
			pass
		else:
			for ship in self.states['shiplist']:
				ship.states['position'] = self.states['position'] # moves all ships in the shiplist at its new position
		
		self.scan("lazy") # automatically scans
		
		newpos = deepcopy(self.states['position'])
		
		mapmethods.updatePoints(oripos,self)
		mapmethods.updatePoints(newpos,self) # important! updates the mapcode_tracker
	
	def actionpoints(self):
		return self.states.get('action_points',None)
	
	def closestTowards(self,arg,overrides = []):
		"""Finds and returns the closest point to the destination it can reach in a single move."""
		
		path = utilityfunctions.findpath(self,arg)
		
		if 'override' in overrides:
			maxbearablecost = 1000000.0
		else:	
			maxbearablecost = self.actionpoints()

		dist = mapmethods.distance
		pos = self.pos()
		
		costForPoint = { point : dist(pos,point) for point in path} # now we have a dictionary of point : cost for all points in path
		
		if len(path) == 1:
			return path[0]
		elif len(path) <= self.states['speed']: 	# if speed is shorter than path
			pass

		else:
			path = path[:self.states['speed']] 		# crops the list at the last reachable position
		
		counter = len(path) - 1
		while counter >= 0:
			
			tryPoint = path[counter]
			counter -= 1 # the counter goes one position backwards
			
			if maxbearablecost >= costForPoint[tryPoint]:
				return tryPoint
			else:
				pass
		
		raise Exception('Error: something went wrong. Counter stopped at ' + str(counter) + ' and path was ' + str(path))
			
	def warp(self,newpos,specialargslist = []):
		"""Warp!"""
		if 'override' in specialargslist:
			pass
		elif self.states.get('warp') != None and self.states['warp'][1] >= 10:
			pass
		elif len(newpos) != 2:
			raise Exception('Bad input: received newpos = ',str(newpos))
		else:
			return None # this ship cannot warp
		
		if self.states['position']!= None:  # if for some reason this was the first warp...
			oripos = self.states['position'] 
			mapmethods.updatePoints(oripos)
		else:
			pass
		
		self.states['position'] = newpos # sets the position to the new position	
		mapmethods.updatePoints(newpos)
		
		if 'silent' in specialargslist:
			return None
		else:
			print(self.states['name'] + ' warped to ' + str(newpos))
				
	def land(self,pos):
		"""The fleet or vessel goes to land to a position."""
		self.move(pos)
		
		asteroidshere = [ astr for astr in mapmethods.allObjectsAt(self.states['position']) if astr.objectclass == 'asteroid' ]
		
		if asteroidshere == []:
			return 'Nowhere to land there.'
		else:
			asteroid = asteroidshere[0] # there should be only one... however...
			self.states['special_conditions'].extend(['landed'])
	
	def leave(self):
		"""Takes off, if it was landed."""
		if 'landed' in self.states['special_conditions']:
			self.states['special_conditions'].remove('landed')
		else:
			return None

				
# FIGHT FUNCTIONS
	def attack(self,other):
		"""Any combination of ship vs fleet vs building."""
		inrange = self.enemiesInRange()
		if other == "auto" and inrange == []:
			return None
		elif other == "auto" and inrange != []:
			self.attack(inrange[0])
			
		
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

	def diffactions(self,other):
		"""Returns true iff the other's faction is different from yours, or either one has no faction, or either one is an Independent"""
		otherfaction = other.states.get('faction', None)
		
		myfaction  = self.states.get('faction', None)
		
		if otherfaction is None or myfaction is None:
			return True
		elif otherfaction == 'Independent' or myfaction == 'Independent':
			return True
		elif myfaction != otherfaction:
			return True
		else:
			return False	
	
	def heal(self,amount,overrides):
		
		# will check for APs and situation...
		
		if 'max' in overrides:
			amount = self.states['max_hull_integrity']
		
		if 'override' in overrides:
			self.states['health'] = amount
		
		else:
			self.ap_pay('heal')	
		
			
# SPAWN FUNCTIONS
	def size(self):
		"""Returns an integer, depending on the size of the vessel."""
		if self.objectclass != 'ship':
			raise Exception('Only ships have a size')
		
		smallships = "swarmer fighter bomber healer".split(' ')
		
		mediumships = "cruiser destroyer".split(' ')
		
		bigships = ["mothership"]
		
		valuesdict = {}
		
		for i in smallships:
			valuesdict[i] = 1
		for i in mediumships:
			valuesdict[i] = 2
		for i in bigships:
			valuesdict[i] = 3
			
		return valuesdict[self.states['shipclass']]
		
	def spawn(self,sobject):
		"""Makes self spawn one or more sobjects."""
		
		if isinstance(sobject,list):	
			for elem in sobject:
				if isinstance(elem,Sobject) == False or elem.objectclass != 'ship':
					return 'Not a spawnable object: received a '+ str(elem)
				else:
					return self.spawn(elem)
		elif isinstance(sobject,Sobject):
			pass # passes only if the sobject is a Sobject object
		else:
			raise Exception('Bad input for spawn function; received a ' + str(sobject) + ' instead of a spawnable.')
		 
		def dodge(tpl):
			"""Returns all eight squares adjacent to a x,y position tuple."""
			x,y = tpl # unpack
			return random.choice([((x+1),(y+1)),((x-1),(y-1)),((x+1),(y-1)),((x-1),(y+1)), ((x-1),(y)), ((x+1),(y)), ((x-1),(y)),((x+1),(y))])
		
		selfpos = self.states['position']
		
		if len(selfpos) != 2:
			raise Exception('Something wrong here, my position is ' + str(selfpos))
		
		pos = dodge(selfpos)		
		
		sobject.states['position'] = mapmethods.torusize(pos)  # torusize! 
		mapmethods.updatePoints(pos) # UPDATES the map!
		
		print(str(sobject) + ' spawned from ' +str(self) + ' at position '+ str(pos))
		
	def launch(self, shipclass, shipnumber, overrides):
		"""Buys and spawns shipnumber ships of shipclass class."""
		listofships = []
			
		for i in range(shipnumber):
			a = objectmethods.Sobject('ship',{'shipclass':shipclass})
			listofships.extend([a])
			
			myfaction = self.states['faction']
			
			a.trackedBy.append(myfaction)
			a.states['faction'] = myfaction
			myfaction.states['ships'].extend([a])
			self.spawn(a)

		
# SCAN FUNCTIONS
	def maxsensorsrange(self):
		"""Name says it all."""
		
		choicelist = []
		
		for i in self.states['sensors']:
			maxdist = i[3]
			choicelist.append(maxdist)
		
		maxrange = max(choicelist)
		return maxrange

	def enemiesInRange(self,keyarg = 'list'):
		circle = self.circle
		
		myfaction = self.states['faction']
		
		self.updatecircle()
		
		sobjectsInView = [ sobj for sobj in myfaction.tracker if sobj.pos() in self.circle and sobj.objectclass in ['ship','fleet','building'] ]
		# sobjects in your circle
		
		enemiesinview = [sobj for sobj in sobjectsInView if self.diffactions(sobj) ]
		# enemies in your circle
		
		myrange = self.states['range']
		
		enemiesinrange = [ sobj for sobj in enemiesinview if mapmethods.distance( self, sobj ) <=  myrange ]
		# enemies in your circle and in weapons' range
		
		if keyarg == 'list':
			return enemiesinrange # a list, btw.
		elif keyarg == 'number':
			return len(enemiesinrange) # the number of enemies in range
			
	def updatecircle(self,ray = None):
		"""Returns the list of absolute positions in which we can safely assume the ship's viewrange is contained."""
		
		if ray == None:	
			ray = self.maxsensorsrange()

		dodgex = range(-ray, ray+1)
		dodgey = range(-ray, ray+1)
		centerx,centery = self.pos()
		
		poslist = []
		
		for x in dodgex:
			for y in dodgey:
				poslist.append((centerx+x,centery+y))
		
		self.circle = poslist

	def visibility(self):
		"""Determines its visibility based on its special_conditions and other factors. The lower, the more the object is hidden."""
		
		if self.objectclass == 'asteroid':
			return 1 # asteroids are always visible at max (and once discovered should stay visible)
		
		if 'hidden' in self.states['special_conditions']:
			return 8.0 # this means that it is barely visible! 20% chances only if distance <= 1. Very low!
			
		return 0.0

	def setupSensorArrays(self,standardgroup_or_models=[],overrides=[]):
		"""Accepted inputs: 'dummy', 'basic_arrays', 'average_arrays', 'advanced_arrays', '*some-model*'; equips the object with such sensors."""
		#model, number, quality, maxdist, chanceatmax, specialattrs = ship.states['sensors'][i]
		
		
		sensorArrays = { 	'zero_sensor_mono': 		('zero_sensor',1,1,4,2,[]),
							'basic_sensor_mono':   		('basic_sensor',1,1,6,2,[]),
							'basic_sensor_double': 		('basic_sensor',2,1,6,2,[]),
							'basic_sensor_triple': 		('basic_sensor',3,1,6,2,[]),
							'medium_sensor_mono' : 		('medium_sensor',1,2,7,3,[]),	
							'medium_sensor_double' : 	('medium_sensor',2,2,7,3,[]),	
							'medium_sensor_triple' : 	('medium_sensor',3,2,7,3,[]),
							'advanced_sensor_mono' : 	('advanced_sensor',1,3,10,5,[]),
							'advanced_sensor_double' : 	('advanced_sensor',2,2,10,5,[]),
							'advanced_sensor_triple' : 	('advanced_sensor',3,2,10,5,[]),
							'gundam_array_double' : 	('gundam_sensor',2,4,15,6,[])		
									}
		
		# we assume we only have to give to a ship a sensor array
		
		if standardgroup_or_models == [] or 'newship' in overrides:
			if self.objectclass in ['ship', 'building']:
				defaultArrays = {'ship' : { 'destroyer': 	'basic_sensor_double',
											'cruiser' : 	'basic_sensor_double',
											'mothership': 	'medium_sensor_double',
											'generic' :		'basic_sensor_mono'	},
												
												
								'building' : { 'base': 		'medium_sensor_mono',
												'battery': 	'medium_sensor_mono',
												'buoy': 	'zero_sensor_mono',
												'generic' :		'basic_sensor_mono' }					
										}
				
				recognizedClasses = list(defaultArrays['ship'].keys()) + list(defaultArrays['building'].keys()) 
				
				if self.objectclass not in ['ship','building']:
					raise Exception('Unrecognised object class for sensors to set up: ' + str(self) + self.objectclass)
					
				if self.states.get('shipclass',self.states.get('buildingclass')) not in recognizedClasses:
					pass # will give the GENERIC sensor
				
				objectclassSensors = defaultArrays[self.objectclass]
				
				mybuildingclass = self.states.get('buildingclass')
				myshipclass = self.states.get('shipclass')
				
				if mybuildingclass != None:
					mysensors = objectclassSensors.get(mybuildingclass, objectclassSensors['generic']) # if mybuildingclass is not recognized...
				elif myshipclass != None:
					mysensors = objectclassSensors.get(myshipclass, objectclassSensors['generic']) # ... gives the generic sensor arrays.
				else: 	
					raise Exception('Unrecognised object class for sensors to set up: ' + str(self) + self.objectclass)
					
				self.states['sensors'] = [sensorArrays[mysensors]]  # if this is the first time... creates a new list
				
				
				# sensor is now set up
				return None
			
			else:
				raise Exception('Bad sobject input for setupSensorArrays: received a ' + str(self))
			
		elif standardgroup_or_models != []:
			
			for keyword in standardgroup_or_models:
				if sensorArrays.get(keyword) != None:
					self.states['sensors'].append(sensorArrays[keyword])
				else:
					raise Exception('Unrecognised input for setupSensorArrays: {} {}'.format(standardgroup_or_models,overrides))
		
				return None
		
	
		else:
			raise Exception('Bad input for setupSensorArrays: {} {}'.format(standardgroup_or_models,overrides))
		
		
		return None

	def perceivables(self,ray = None):
		"""Returns a smartly generated list of objects on which the ship can scan."""
		
		if self.circle == None: # redundant
			self.updatecircle()
		if ray != None and isinstance(ray,int):
			self.updatecircle(ray)
			
		
		mycircle = self.circle
		
		objlist = []
		
		for pos in mycircle:
			sobjects = [ obj for obj in sobject_tracker if obj.pos() == pos ]
			asteroid = mapcode_tracker.get(pos)
			objlist.extend(sobjects)
			if asteroid == None:
				pass
			else:
				objlist.append(asteroid)
			
		objlist.remove(self)
		
		return objlist
		
	def scan(self, params = None ,  overrides = []):
		"""Accepted params are 'long', 'best', 'returnSensorsDict','lazy'."""
		
		if params == 'lazy': # performs a quick passive scan, very weak
			if self.objectclass in ['ship','building']:
				overrides.append('lazy')
				self.runScan(overrides) # calls a scan bypassing the pay-APs step
			elif self.objectclass == 'fleet':	
				scanning = random.choice(self.states['shiplist'])
				return scanning.scan('lazy') # recurse
			
			else:
				raise Exception('This object cannot scan: ' + str(self))
		
		elif params == 'returnSensorsDict': # returns a dictionary of all sensors for self's shiplist or self
			sensorsdict = {}
			
			if self.objectclass in ['ship','building']:
				for i in self.states['sensors']:
					model, number, quality, maxdist, chanceat1, specialattrs = self.states['sensors'][i]
					sensorsdict['{} {} sensors'.format(number,model)] = "quality: {}, maxdist: {}, chance at 1: {}; specialattrs = {}".format( quality, maxdist, chanceat1, specialattrs)
				return sensorsdict
				
			elif self.objectclass == 'fleet':
				for ship in self.states['shiplist']:
					for i in ship.states['sensors']:
						model, number, quality, maxdist, chanceat1, specialattrs = ship.states['sensors'][i]
						sensorsdict['{} {} sensors'.format(number,model)] = "quality: {}, maxdist: {}, chance at 1: {}; specialattrs = {}".format( quality, maxdist, chanceat1, specialattrs)
				
				return sensorsdict
		
			else:
				raise Exception('Unsupported objectclass for scan function: received a ' + str(self)+ str(params) + str(overrides))
		
		elif params == 'long': # makes a long scan; if called on a fleet, each of its ships do a long scan
			if self.objectclass in ['ship','building']:
				pass
			elif self.objectclass == 'fleet':
				for i in self.states['shiplist']:
					return i.scan('long',overrides)
			else:
				raise Exception('Unsupported objectclass for scan function: received a ' + str(self)+ str(params) + str(overrides))
		
		elif params == 'best': # makes the best of your ships do a long scan
			if self.objectclass in ['ship','building']:
				return self.scan('long', overrides)
			elif self.objectclass == 'fleet':
				sensorsdict = {}
				for ship in self.states['shiplist']:
					for i in ship.states['sensors']:
						model, number, quality, maxdist, chanceat1, specialattrs = ship.states['sensors'][i]
						sensorsdict[quality] = ship
						
				best_sensor_ship = sensorsdict[max(sensorsdict.keys())]
				return best_sensor_ship.scan('long', overrides)

			else:
				raise Exception('Unsupported objectclass for scan function: received a ' + str(self)+ str(params) + str(overrides))
		
		else:
			pass
		
		if 'free' in overrides: # passes without paying aps
			return self.runScan(overrides)
			
		if self.ap_pay('scan') == True:
			pass
		else:
			return dialogmethods.cantPerform() # can't perform action	
		
		# does nothing

		return self.runScan(overrides)
		
	def runScan(self,overrides):
		"""Does the hard work of determining which objects are in view; communicates this to the faction."""
		
		print(str(self) + ' is scanning...')
		
		dist = mapmethods.distance
		pos = self.pos()
		
		for sensor in range(len(self.states['sensors'])):															# picks one by one all mounted sensors
			model, number, quality, maxdist, chanceatmax, specialattrs = self.states['sensors'][sensor]	
			#('basic_sensor',1,1	,6		,2,				[])
			if 'lazy' in overrides:
				maxdist = 3
				chanceatmax = 0.7
				number = 1
				perceivables = self.perceivables(3)
			else:
				perceivables = self.perceivables() 
			
			objectsInRange = [ (dist(self.pos(),obj.pos()),obj) for obj in perceivables ]
			
			for numiters in range(number): 																# each sensor_array scans once per 
																										# number of sensors mounted on the array
				for target in objectsInRange:
					targetdistance = target[0]
					steps = maxdist
					
					chanceincrementperstep = 1.0 - (chanceatmax/10.0) # should be a positive float in (0,1]
					if not 0 < chanceincrementperstep <= 1:
						raise Exception('Something wrong : chanceincrementperstep = ' + str(chanceincrementperstep))
					
					distanceinsteps = float(targetdistance // steps) # how many steps there are in distance
					target_chanceToBeSeen = 1.0 - (distanceinsteps * chanceincrementperstep) # the farther it is, the harder it is to see it
					
					if not 0 < target_chanceToBeSeen <= 1: # doesn't even try.
						#raise Exception('Something wrong : target_chanceToBeSeen = {},distanceinsteps = {} chanceincrementperstep = {}, steps = {}, distance = {} '.format(str(target_chanceToBeSeen),distanceinsteps,chanceincrementperstep,steps,targetdistance)  )
						pass
					else:
						target_chanceToBeSeen_final = target_chanceToBeSeen - target[1].visibility() # diminishes the chances by target's visibility factor
					
						if random.random() <= target_chanceToBeSeen: #  the harder to see it, the lower target_chancetobeseen is
							for faction in self.trackedBy:
								faction.see(target[1])
							
							#self.states['faction'].see(target[1])
							objectsInRange.remove(target)
							
							print('perceived '+ str(target[1]) + ' at a distance of ' + str(targetdistance))
							
						else:
							pass


# APs	
	def ap_gain(self,what):
		"""Rewards a ship with action points. If the operation is successful, returns True. Else, False."""
		
		selfAP = self.states['action_points']
		
		if what + selfAP >= 10: #### CAP
			self.states['action_points'] = 10.0
		else:
			self.states['action_points'] += what
			return True
		
	def ap_pay(self,what):
		"""Makes a ship spend its aps for some action. If that is feasible (the cost can be paid), returns True; else, False."""
		
		selfAP = self.states['action_points']
		
		prices = {	'scanlong' : 3.0,
					"scan" : 2.0,
					'move1':1.0,
					'move2': 1.5,
					'warp':10.0,
					'attack':4.0,
					'heal': 6,
					'battle':10.0}
		
		if isinstance(what,float) or isinstance(what,int): # tries to pay what.
			cost = what
			pass
		elif what in list(prices.keys()):
			cost = prices[what]
		else:
			raise Exception('Bad input for ap_pay: received {} {}'.format(self,what))
			
			
		if cost <= selfAP:
			self.states['action_points'] -= cost
			return True
		
		else:
			return False

	def ap_topup(self):
		self.states['action_points'] = 10

# BUILDING-SPECIFIC FUNCTIONS		
	def autoattack(self):
		"""This function is a switch."""
		
		if hasattr(self,"autoattack") == False:
			self.autoattack = False
			
		self.autoattack = not self.autoattack
	
	def canspawn(self):
		
		if self.states.get("spawn",0) > 0:
			return True
		else:
			return False
			















