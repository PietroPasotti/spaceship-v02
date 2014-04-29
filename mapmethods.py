# mapmethods

import random
from copy import deepcopy
from math import sqrt
import objectmethods
import utilityfunctions
import namegenmethods


def createMapCode(height = 40,width = 100,asteroidratio = 0.04):  # default values for the whole game
	"""Given height and width, plus optional asteroid ratio, produces a mapcode (randomized 0/1 matrix)."""	
	
	print('Mapcode initialized with input ' + str((height,width,asteroidratio)) + ', parsing sector with characteristic ' + str(objectmethods.map_specials))
	
	mapCode = {}
	
	probabPlotAsteroid = float( 0.01 + asteroidratio)
	
	print('Generating mapcode...')
	
	for y in range(height):
		for x in range(width):
			if random.random() > probabPlotAsteroid:
				pass
			else:
				mapCode[(x,y)] = 1
				pass
	
	return (mapCode,height,width)  
def	neighbourCount(point,dictionary):
	count = 0
	
	oripoint = deepcopy(point)
	
	if point in dictionary.keys():
		del dictionary[point]  #removes a dict entry from the mapcode
		pass
	else:
		pass
		
	pointX = point[0]
	pointY = point[1]
		 
		#set of dots which are max one column distant from point
	LdistX = {dot for dot in dictionary.keys() if dot[0] in [(pointX + 1), (pointX - 1), pointX]}
		#set of dots which are one row distant:
	LdistY = {dot for dot in dictionary.keys() if dot[1] in [(pointY + 1), (pointY - 1), pointY]}
	
	Lprox = LdistX.intersection(LdistY)
	
	dictionary[oripoint] = 1
	
	return len(Lprox)
def propagate2(mapcodeheightwidth,threshold=0.3,numiters=3):     # default values, not modifiable
	"""Propagation algorithm 2"""
	
	mapcode,height,width = mapcodeheightwidth
	
	# mapdode comes as a dictionary 'mapcode'	

	astrocount = 0

	print('Running mapcode experimental propagation algorithm... Looping ... ')
	
	Propagated_MAPCODE = deepcopy(mapcode)
	
	for a in range(numiters):
		for obj in mapcode.keys():
			for s in range(numiters):
				if random.random() > threshold:
					Propagated_MAPCODE[(obj[0]+random.randint(-1,1),obj[1]+random.randint(-1,1))] = 1
					astrocount += 1
				else:
					pass
		print( str(a) + ' ... ' )				
					
	print('Rounding algorithm running...')
	
	Rounded_MAPCODE = deepcopy(Propagated_MAPCODE) # initializes a new dictionary 
	
	for (x,y) in mapcode:
		if 6 >= neighbourCount((x,y), mapcode) >= 4:  # condition on the OLD dictionary
			for i in range(5):
				Rounded_MAPCODE[(x+random.randint(-1,1),y+random.randint(-1,1))] = 1	 # add to the NEW dictionary! otherwise...
	
	croppedRounded_MAPCODE = {pos : Rounded_MAPCODE[pos] for pos in Rounded_MAPCODE if pos[1] <= height and pos[0] <= width}
	
	print('\n ' + str(astrocount) + ' asteroids created!')
	
	croppedRounded_MAPCODE['specials'] = (height,width,namegenmethods.namegen('a'))
	
	return croppedRounded_MAPCODE
def findfactor(dimension,number):
	"""Returns how many times number is in dimension."""
	
	number = sqrt(number ** 2)
	counter = 0	
	while dimension < number:
		number -= dimension
		counter += 1
			
	return counter
def pruneDestroyed(Listofobjects):
	"""Removes all destroyed ships from a listof ships or from a Fleet's shiplist, and possibly destroys them.
	If the fleet gets empty by doing this, removes the Fleet as well from its map.
	Also accepts mixed lists of ships and Fleets (such as those you get in map.OBJECTS' dictionary).
	"""
	
	for item in Listofobjects:
		if isinstance(item,objectmethods.Sobject) == True and item.states['health'] == 'destroyed':
			Listofobjects.pop(item) # removes it
		elif isinstance(item,objectmethods.Sobject) == False:
			raise Exception('Wrong input for pruneDestroyed utility function. Only works on Sobjects.')
	
	return Listofobjects
def distance(obj1,obj2):
	"""
	As general as possible, returns the distance between two objects on the map.
	Possibly, even the distance between an object and any tuple of coordinates.
	"""

	# transform obj1 and obj2 into tuples
	def redef(obj):
		if isinstance(obj,objectmethods.Sobject) == True:
			try: 
				pos = obj.states['position']	
			except KeyError:
				raise KeyError('Wrong input for distance function; received a ' + str(obj1,obj2))
			return pos
		elif isinstance(obj,tuple):
			return obj
		
	obj1 = redef(obj1)
	obj2 = redef(obj2)	
	
	diffX = max(obj1[0],obj2[0]) - min(obj1[0],obj2[0])
	diffY = max(obj1[1],obj2[1]) - min(obj1[1],obj2[1])
	
	dist = int(sqrt(diffX ** 2 + diffY ** 2)) # pitagora
	return dist

def torusize(pos):
	"""Redefines the position so that it is in the frame."""
	height,width,name = objectmethods.map_specials
	
	X,Y = pos # should be a tuple.
	
	if X > width:
		factor = findfactor(width,X)
		X = int(X - X * factor)
		
	if Y > height:
		factor = findfactor(height,Y)
		Y = int(Y - Y * factor)
		
	return (X,Y)	
		
def newMapChoiceDict():
	
	MapDict = {'Create new map': mapmethods.newMap(mapmethods.newMapSizeChoice),
				'Create new map(default)': mapmethods.newMap(mapmethods.newMapSizeChoice(None,None,True)), # invokes the skip value
				'Open an old map: (unsupported)': 0 ,
				'Draw a custom map: (unsupported)': 0,}
		
	return MapDict

def newMapSizeChoice(height = None, width = None, skip = False):
	"""Guided initializer for mapcode generator."""
	
	if skip == True:
		return (None,None,None)
	
	print('Entering mapcode initializer...')
	if height == None and width == None: # if this is the first time
		choose1 = input('Want to use default settings? [Y/n] ')
		if choose1 in 'Yesyes':
			return (None,None,None)
		else:
			pass
	
	height  = int(input('Enter the height (y axis) of the new map: ' ))
	if not 0<height<=100:
		print('The parameter is out of range. Please enter a reasonable integer in interval (0, 100].')
		return newMapSizeChoice()
	else:
		pass
		
	width  = int(input('Now enter the width (x axis) of the new map: ' ))

	if not 0<width<=100:
		print('The parameter is out of range. Please enter a reasonable integer in interval (0, 100].')
		return newMapSizeChoice(height) # stores the previous parameter, as it is correct.
	else:
		pass
	
	choose = input('Do you want to define your own asteroidratio? WARNING: the resulting map could be horrible [Y/n]: ')
	if choose in 'Yesyes':
		asteroidratio = float(input('Then do it. Suggestion: should be a very small float, say, between 0.000001 and 0.3: '))	
		if not 0 > asteroidratio > 0.8:
			print('The parameter is out of range. Please enter a reasonable float in interval (0,0.8).')
			return newMapSizeChoice(height,width)
	else:
		asteroidratio = None
		
	counter = 0
	if counter == 0: # prevents the function (partly recursive) to return values more than once
		counter += 1
		return (height,width,asteroidratio)

def newMap(parameters = None):
	"""Takes as input a tuple xy and calls createmapcode, propagate2 to obtain a workable asteroid field."""
	
	if objectmethods.mapcode_tracker != {}:
		objectmethods.mapcode_tracker.clear() # cleans the tracker.
		
	if isinstance(parameters, tuple):
		height,width,asteroidratio = parameters # unpacks the tuple; can be None,None,None
		
		if height == None and width == None:
			mapcode = createMapCode()
		elif asteroidratio == None:
			mapcode = createMapCode(height,width) # only asteroidratio is to default settings
		else:
			mapcode = createMapCode(height,width,asteroidratio) # user-defined settings
			
	elif parameters == None:
		mapcode = createMapCode() # all default settings
	else:
		raise Exception('Bad bad bad.')		
		
	propagatedmapcode = propagate2(mapcode)
	
	# now we initialize a Sobject:asteroid for each dictionary entry in propagated mapcode
	
	print('Initializing asteroid Sobjects...')
	
	objectmethods.map_specials = propagatedmapcode.pop('specials')
	
	for entry in propagatedmapcode: # is a function: no duplicate entries
		newAsteroid = objectmethods.Sobject('asteroid',{'position':entry}) # the position is entry.
		objectmethods.mapcode_tracker[entry] =  newAsteroid
	
	print('Newmap procedure completed. Welcome to sector '+str(objectmethods.map_specials[2]))	

def topObjectAt(coordinates):
	"""Returns the object in the top layer for that position."""

	objectsatpos = [sobj for sobj in objectmethods.sobject_tracker if sobj.states.get('position') == coordinates]
	asteroid =  objectmethods.mapcode_tracker.get(coordinates) #can be none

	fleetsat = [fleet for fleet in objectsatpos if fleet.objectclass == 'fleet']
	if fleetsat == []: 																			# LAYER 3
		pass
	else:
		return fleetsat[0]  # returns the first fleet he can pick there

	shipsat = [ship for ship in objectsatpos if ship.objectclass == 'ship']
	if shipsat == []: 																			# LAYER 2
		pass
	else:
		return utilityfunctions.mostPowerful(shipsat) # returns the most powerful

	if asteroid != None: 																		# LAYERs 1-0
		if asteroid.states.get('building') == None:
			return asteroid  # if it is not built, returns itself.
		else:
			return asteroid.states['building'] # returns the building which is on it!
	else:
		return asteroid 																		# that is: None
		
def allObjectsAt(coordinates):
	"""Returns all objects at the position."""
	astr = objectmethods.mapcode_tracker.get(coordinates,[])
	if astr != []:
		astr = [astr]
	return [obj for obj in objectmethods.sobject_tracker if obj.states.get('position') == coordinates] + astr
		
def map_brutal_dump(view = 'godview'):
	"""Brutally dumps the codes of all Sobjects existing in the universe."""
	
	if objectmethods.map_specials == None:
		return 'No map to be dumped.'

	# todo : when godview is off, the visualized map depends on the player who calls the brutal-dump
	
	height,width,name = objectmethods.map_specials
	
	print('Brutal_Dump of ' + name)
	
	if view == 'godview':
		pass
	elif isinstance(view,factionmethods.Faction):
		# something will happen here
		pass
	
	header = '    ' + '_'*(int(width/2) - 4) + name + '_'*(int(width/2) - 4)
	print(header)
	
	linecounter = 0
	for y in range(height): # y, height
		line = '   |'
		for x in range(width): # x, width
			topobj = topObjectAt((x,y)) # does the hard work
			
			objectmethods.mapcode_tracker[(x,y)] = topobj # can be None or an object--- the mapcode_tracker tracks only VISIBLE TOP LAYER ITEMS
			
			if topobj == None:
				todisplay = ' '
			else:
				todisplay = topobj.states['code']
			
			line = line + str(todisplay)
		line = line + '|  ' + str(linecounter)
		linecounter +=1
		
		print(line)
	footer = '    ' + '_' *(width)
	print(footer)

def updatePoints(pos1, pos2 = None):
	"""Updates the mapcode register so as to keep track of small changes. Typical input can be oldposition, newposition of some moving object."""

	if pos2 != None:
		pointstoupdate = [pos1,pos2]
	else:
		if isinstance(pos1,list):
			pointstoupdate = pos1
		elif isinstance(pos1,tuple):
			pointstoupdate = [pos1] # can be generalized to take also lists as input
		else:
			raise Exception('Bad input for updatePoints function; received {} and {}.'.format(str(pos1),str(pos2)))
	
	for point in pointstoupdate:
		if isinstance(point,tuple) != True or len(point) > 2:
			raise Exception('Error here. received pointstoupdate :: ' +str(pointstoupdate) + ' where pos1 = {} and pos2 = {}'.format(str(pos1),str(pos2)))
		objectmethods.mapcode_tracker[point] = topObjectAt(point)
	
def map_smart_dump(view = 'godview'):
	"""Tries to dump the map in an intelligent way. If there is no map, returns a message. If the map has not been brutal_dumped before, 
	and the dictionary is thus too little, it brutal_dumps it automatically."""
	
	if objectmethods.map_specials == None:
		return 'No map to be dumped.'

	if len(objectmethods.mapcode_tracker) < objectmethods.map_specials[0] * objectmethods.map_specials[1] :
	# i.e. if the map has never been brutal_dumped before
		return map_brutal_dump(view)
	# todo : when godview is off, the visualized map depends on the player who calls the brutal-dump
	
	height,width,name = objectmethods.map_specials
	
	print('smart_dump of ' + name)
	
	header = '    ' + '_'*(int(width/2) - 4) + name + '_'*(int(width/2) - 4)
	print(header)
	
	linecounter = 0
	for y in range(height): # y, height
		line = '   |'
		for x in range(width): # x, width
		
			topobj = objectmethods.mapcode_tracker[(x,y)] # retrieves the object from the precompiled mapcode_tracker!
			
			if topobj == None:
				todisplay = ' '
			else:
				todisplay = topobj.states['code']
			
			line = line + str(todisplay)
		line = line + '|  ' + str(linecounter)
		linecounter +=1
		
		print(line)
	footer = '    ' + '^' *(width)
	print(footer)
