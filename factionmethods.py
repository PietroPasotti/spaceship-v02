# factionmethods
import dialogmethods
import namegenmethods
import objectmethods
import utilityfunctions

protected_factions = ['independent','Independent']
existing_factions = []

class Faction(object):
	
	def __init__(self,options = {}):
		
		self.states = {}

		self.states['name'] = None  # essential values! any faction must have them from the start
		self.states['ships'] = []
		self.states['base'] = None
		self.states['buildings'] = []
		self.states['fleets'] = []
		self.states['allies'] = []
		self.states['hostiles'] = []
		
		self.asteroidlist = [] 	# keeps track of all ever perceived asteroids, unmodifiable
		self.objectlist = [] # all other objects, modifiable
		
		self.view = {} # keeps precompiled copy of asteroid_tracker,plus all objects (not yours) which you have perceived
	
		
		if options != {}: 	# if we provide some custom options
			bol = False 	# we won't be prompted to get random ones
		else:
			bol = True 
		
		self.initFaction(options,bol) # will update the states dictionary and spawn the first things
		
		global existing_factions
		existing_factions.extend([self])
		

		
		print("initialized faction " + self.states['name'])
	
	def __str__(self):
		
		return 'faction {}; with base at {}, and a fleet of {} ships.'.format(self.states['name'],self.states['base'],len(self.states['ships']))
	
	def initFaction(self,options,bol):
		"""Essential values are name,base,ships."""
		
		if objectmethods.mapcode_tracker == {}:
			raise Exception("can't initialize without a ground mapcode.")
		
		print('Faction initializer prompted...')	
		if bol == True:
			if input('Do you want to automatically generate a random one? [Y/n]: ') in 'Yesyes':
				return self.initrandomZero()
			else:
				pass
		else:
			pass

		if options.get('name') == None:                            # name
			name = input('Enter the name of the faction: ')
			if isinstance(name,str) == False:
				return self.initFaction(options,False)
			else:
				options['name'] = name
				
		if options.get('base') == None:							# base
			basepos = input('Enter the approximate position of your base. Choose carefully. Form must be (x,y): ')
			
			try: 
				basepos = eval(basepos)
			except NameError:
				basepos = 'abc'
				
			if isinstance(basepos,tuple) == False or basepos not in objectmethods.sobject_tracker:
				print('Bad input.')
				return self.initFaction(options,False)
			else:
				nearbyplots = utilityfunctions.approx(basepos,3,'asteroid') #approx(point,threshold,oclass): retrieves all asteroids in a range of 3 squares from basepos
				base = objectmethods.Sobject('building',{'buildingclass':'base', 'position': random.choice(nearbyplots),'faction': faction })
				options['base'] = base
			
		if options.get('ships') == None:							# ships
			a = Sobject('ship',{'shipclass':'swarmer'})
			b = Sobject('ship',{'shipclass':'swarmer'})
			c = Sobject('ship',{'shipclass':'swarmer'})
			d = Sobject('ship',{'shipclass':'fighter'})
			
			options['ships'] = [a,b,c,d]
		
				
		for option in options:
			self.states[option] = options[option]
			
		for ship in self.states['ships']:
			self.states['base'].spawn(ship)
				
	def initrandomZero(self):
		self.states['name'] = namegenmethods.namegen('F')
		self.states['base'] = objectmethods.Sobject('building',{'buildingclass':'base', 
															'position': utilityfunctions.randomasteroid().states['position'],
															'faction': self })
		
		self.states['base'].launch('swarmer',3,['override']) 
		self.states['base'].launch('fighter',1,['override'])
		
	def ships(self):
		return self.states['ships']
		
	def buildings(self):
		return self.states['buildings']

	def allMyObjects(self):
		"""Returns a faction's complete objectlist."""
		
		ships = self.states['ships']
		base = self.states['base']
		buildings = self.states['buildings'] 
		#fleets = self.states['fleets'] 	
		
		allList = ships + buildings + [base]
		
		return allList

	def see(self,obj):
		"""Adds the object to the faction's view."""
		
		if isinstance(obj,objectmethods.Sobject) != True:
			raise Exception('Wrong. Received a non-sobject: ' +str(obj))
		
		if obj.objectclass == 'asteroid':
			if obj in self.asteroid_tracker: # if it's already there.
				return None
			else:
				self.asteroid_tracker[i.pos()] = i #  will never be touched again
				self.view.append(obj)
		else:
			self.view.append(obj)
			
		return None

	def updateView(self):
		"""Tells the faction to see all of his own objects, and to see all they can see."""
		for i in self.allMyObjects():
			self.see(obj)
		
		for a in self.asteroid_tracker:
			self.see(asteroid)
		
		mapmethods.map_smart_dump(self.view)
		
	def shareview(self,otherfaction):
		"""Gives an ally (or a hostile, btw) the possibility to see a snapshot of his own view."""
		
		for key in self.view:
			otherfaction.see(self.view[key])
		
