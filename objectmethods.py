# spaceship v02
# objectmethods
# will contain a single class for any object which may ever appear on a map


existing_all = []
_ships = []
_fleets = []
_asteroids = []


class Sobject(object):
	
	def __init__(self,objectclass_str,specialattrs_dict = {}):
		"""Takes as input an objectclass, and optional specialattrs"""
		
		self.states = {}
		self.objectclass = objectclass_str
		
		if self.objectclass == 'ship':
			self.initShip(specialattrs_dict)
			
		elif self.objectclass == 'fleet':
			self.initFleet(specialattrs_dict)
			
		elif self.objectclass == 'group':
			self.initGroup(specialattrs_dict)
			
		elif self.objectclass == 'asteroid':
			self.initAsteroid(specialattrs_dict)
			
		elif self.objectclass == 'building':
			self.initBuilding(specialattrs_dict)
			
		elif self.objectclass == 'debris':
			self.initDebris(specialattrs_dict)
			
		else:
			return 'Unsupported objectclass input for Sobject constructor'
		
		return None
			
	def initShip(self,specialattrs):
		"""Initializes the object as a ship."""
		self.states['shipclass'] = specialattrs.get('shipclass', 'fighter') # tries to get the specialattr 'shipclass'; otherwise it's a fighter
		
		shipMaxNos = {'fighter':500, 'mothership':2, 'bomber':100, 'cruiser':40,'destroyer':30}
		
		# now it should retrieve the fundamental attributes of the shipclass.
		shipdict = {'fighter' : 	{'max_attack':10,
									'max_speed':10,
									'max_hull_integrity':40.0,
									'max_range':1,
									'code':'f'},
									
					'mothership':	{'max_attack':100,
									'max_speed':5,
									'max_hull_integrity':500.0,
									'max_range':3,
									'max_spawn':1,
									'max_shields':20,
									'code': 'M'} }
									
		for a in ['max_attack', 'max_speed','max_health','max_range','max_warp','max_shields','max_spawn','cargo','code']:
			fetchedvalue = shipdict[self.states['shipclass']].get(a,None) 
			if fetchedvalue != None:
				self.states[a] = fetchedvalue
			else:
				pass
		
		self.name = 'Abelard' # namegen!
		
		# now we OVERRIDE the default parameters with the optional ones we have passed with specialattrs
		for key in specialattrs:
			self.states[key] = specialattrs[key] # for examples we may have wanted to create a non intact ship. specialattrs = {'health' = 'damaged'}
		
		# now we make the object check its properties, so that it updates automatically all dependencies between states
		self.checkStates()
		return None

		
	def initAsteroid(self, specialattrs)		
		
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
			return self.shipCheckStates()	
		# all other classes
		else:
			return None

	def shipCheckStates():
		"""Subfunction for ship's states"""
		
		life = self.states['max_hull_integrity']
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
		
		self.states['attack'] = self.states['max_attack'] * genericmodifier
		self.states['shields'] = self.states['max_shields'] + shieldmodifier
		self.states['speed'] = self.states['max_speed'] * genericmodifier # same as attack!
		
		if self.states['attack'] == 0:
			self.states['can_attack'] = False
		else:
			self.states['can_attack'] = True
			
			
		# parses states[conditionsmodifiers], to override all other conditions
		
		a = self.states.get('conditions_modifiers')
		if a != None:
			for condition in self.states['conditions_modifiers']:
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
		else:
			pass
















		

