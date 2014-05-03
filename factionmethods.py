# factionmethods
import dialogmethods
import namegenmethods
import objectmethods
import mapmethods
import utilityfunctions

protected_factions = ['Independent','GOD']
existing_factions = []

class Faction(object):
	
	def __init__(self,options = {}):
		
		global existing_factions		

		self.states = {}
		
		self.states['name'] = 'Noname'
		
		self.states['ships'] = []
		self.states['base'] = []
		self.states['buildings'] = []
		self.states['fleets'] = []
		self.states['allies'] = []
		self.states['hostiles'] = []

		if options == 'god_override':
			existing_factions.extend([self])
			return self.initGodMode()
		
		self.view = {}          # snapshot of what you currently see. smartly updated
		self.persistent_view = {} # snapshot of one-shot perceived objects such as enemies
		self.tracker = [] 		# keeps track of all objects which you have rights to see. smartly updated
		
	
		if options != {}: 	# if we provide some custom options
			bol = False 	# we won't be prompted to get random ones
		else:
			bol = True 
			
		existing_factions.extend([self])
		
	def name(self):
		return self.states['name']
		
	def __str__(self):
		
		return 'faction {}; with base at {}, and a fleet of {} ships.'.format(self.states['name'],self.states['base'],len(self.states['ships']))
	
	def initGodMode(self):
		
		self.view = objectmethods.mapcode_tracker
		self.persistent_view = objectmethods.mapcode_tracker
		self.tracker = objectmethods.sobject_tracker
		self.states['name'] = 'GOD'
		print("God is born. And is a factionmethods.faction instance.")
	
	def initFaction(self,options=None,bol=True):
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
			return self.initrandomZero()

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
	
		print("initialized faction " + self.states['name'])
				
	def initrandomZero(self):
		self.states['name'] = namegenmethods.namegen('F')
		self.states['base'] = objectmethods.Sobject('building',{'buildingclass':'base', 
															'position': utilityfunctions.randomasteroid().states['position'],
															'faction': self })
		
		self.states['base'].launch('swarmer',3,['override']) 
		self.states['base'].launch('fighter',1,['override'])
		
		
		[print(a.pos()) for a in self.allMyObjects()]
		self.updateView(False)


# FETCHER METHODS		
	def ships(self):
		return self.states['ships']
		
	def buildings(self):
		return self.states['buildings']

	def allMyObjects(self):
		"""Returns a faction's complete objectlist."""
		
		ships = self.states['ships']
		base = self.states['base']
		
		if base != []:
			base = [base]
			
		buildings = self.states['buildings'] 
		#fleets = self.states['fleets'] 	
		
		allList = ships + buildings + base
		
		return allList

	def factionEnemiesInRange(self):
		shipstoconsider = []
		for ship in self.states['ships']:
			if ship.states['can_attack'] == True:
				shipstoconsider.append(ship)
		enemiesinrangeoffaction = set()
		for ship in shipstoconsider:
			enemiesinrangeofship = set(ship.enemiesInRange())
			enemiesinrangeoffaction = enemiesinrangeoffaction.union(enemiesinrangeofship)
		
		return list(enemiesinrangeoffaction)
		
		
# VIEW METHODS

	def track(self,obj):
		if self not in obj.trackedBy:
			obj.trackedBy.append(self)

		if obj not in self.tracker:
			self.tracker.append(obj)
		
	def stopTracking(self,obj):
		if self in 	obj.trackedBy:
			obj.trackedBy.remove(self)

		if obj in self.tracker:
			self.tracker.remove(obj)

	def see(self,obj):
		"""Adds the object to the faction's view."""
		
		if isinstance(obj,objectmethods.Sobject) != True:
			raise Exception('Wrong. Received a non-sobject: ' +str(obj))
		

		if obj in self.tracker: # if it's already there.
			#if obj.pos() not in self.view[obj.pos()] # if the object is not where you see it ## should not happen!
			#self.updateView(obj.pos()) # you now see it exactly there
			pass
		else:
			self.tracker.append(obj)
			
		mapmethods.updatePoints(obj.pos(),self)
			
		return None

	def hide(self,obj):
		"""The object disappears from the faction's view."""
		
		if obj not in self.tracker:
			raise Exception('Cant hide an untracked object.')
		
		if obj not in self.view[obj.pos()]:
			raise Exception('Cant hide an unseen object.')
			
		self.view[obj.pos()].remove(obj)
		
	def updateView(self,bol=False):
		"""Tells the faction to see all of his own objects, and to see all they can see."""
		for i in self.allMyObjects():
			i.scan('lazy',['free'])
			self.see(i)
			mapmethods.updatePoints(i.pos(),self)      	# updates the view in a smart way
		
		for a in self.persistent_view:
			self.see(a)
			mapmethods.updatePoints(a.pos(),self)		# updates the view in a smart way
		
		if bol == True: self.dumpView()
	
	def dumpView(self):
		return mapmethods.map_smart_dump(self)
	
	def shareview(self,otherfaction):
		"""Gives an ally (or a hostile, btw) the possibility to see a snapshot of his own view."""
		
		for key in self.view:
			otherfaction.see(self.view[key])

# SPAWNER METHODS		
	def god_spawn(self,params = []):
		"""A religious function. Spawns some ships around the map, randomly. Can receive either a number of ships to spawn or a name-based shiplist"""
		
		if self is not mapmethods.GOD:
			print("You'd love that, wouldn't you.")
			return None
			
		
		if isinstance(params,int):
			shipclass = random.choice(['fighter','swarmer','bomber'])
			newship = objectmethods.Sobject(shipclass)
				
			newship.states['position'] = utilityfunctions.randomasteroid().pos() # places it on top of some asteroid
			newship.states['faction'] = self
			
		elif isinstance(params,list):
			if isinstance(params[0],objectmethods.Sobject):
				if len(params) <= 3:
					for sobject in params:
						sobject.states['position'] = utilityfunctions.randomasteroid().pos()
						sobject.states['faction'] = self
						self.states['ships'].append(sobject)
				else:
					shiplist = params
					position = utilityfunctions.randomasteroid().pos()
					newfleet = objectmethods.Sobject('fleet',{'shiplist':shiplist, 'position':position,'faction':self})					
					self.states['fleets'].append(newfleet)

			elif isinstance(params[0],str):
				# try passing the string as a shiplist of a fleet initializer
				
				shiplist = params #
				
				position = utilityfunctions.randomasteroid().pos()
				
				newfleet = objectmethods.Sobject('fleet',{'shiplist':shiplist, 'position':position,'faction':self})
				
				print('Now god has a holy fucking fleet to kick your ass with.')

			else:
				raise Exception('Unrecognised input for god_spawn function: received {}'.format(params))

		else:
			raise Exception('Unrecognised input for god_spawn function: received {}'.format(params))


		
