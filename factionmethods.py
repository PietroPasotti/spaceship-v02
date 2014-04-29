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

