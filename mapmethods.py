# mapmethods

import random
from copy import deepcopy
from math import sqrt
import objectmethods
import utilityfunctions
import namegenmethods
import factionmethods

GOD = 'god_override'
 
def createMapCode(height = 24,width = 60,asteroidratio = 0.04):  # default values for the whole game
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
				raise KeyError('Wrong input for distance function; received a ' + str(obj1)+str(obj2))
			return pos
		elif isinstance(obj,tuple):
			return obj
		else:
			raise Exception('Unsupported object type: received ' + str(obj1)+str(obj2))
	
	obj1 = redef(obj1)
	obj2 = redef(obj2)	
	
	diffX = max(obj1[0],obj2[0]) - min(obj1[0],obj2[0])
	diffY = max(obj1[1],obj2[1]) - min(obj1[1],obj2[1])
	
	dist = int(sqrt(diffX ** 2 + diffY ** 2)) # pitagora
	return dist

def curMapSizes(kwarg = None):
	# height,width
	if kwarg == 'x':
		return objectmethods.map_specials[1]
	elif kwarg == 'y':	
		return objectmethods.map_specials[0]
	else:
		return objectmethods.map_specials
	
def orthogonals(sobject,string):
	"""Returns the rightmost point IN THE MAP BOUNDARIES w.r.t. the given sobject."""
	
	posx,posy = sobject.pos()
	
	if string == 'u':
		return (posx,0)
	elif string == 'd':
		return (posx,curMapSizes("y"))
	elif string == 'r':	
		return (curMapSizes("x"),posy)
	elif string == 'r':	
		return (0,curMapSizes("y"))
	else:
		raise Exception("Unrecognised string: "  +  str(string))	

	
def angles(string):
	"""Returns the angles of the currently loaded map."""
	if string == "UL":
		return (0,0)
	elif string == "DL":
		return (0,curMapSizes("y"))
	elif string == "DR":	
		return curMapSizes()
	elif string == "UR":
		return (curMapSizes("x"),0)
	else:
		raise Exception("Unrecognised string: "  +  str(string))
	
	
def torusize(pos):
	"""Redefines the position so that it is in the frame."""
	height,width,name = objectmethods.map_specials
	
	X,Y = pos # should be a tuple.
	
	if X + Y > 100000000:
		raise Exception("Wtf?")
	
	while True:
		if  X > width: # x out of range up
			X = X - width
				
		elif Y > height:
			Y = Y - height
		
		elif X < 0:
			X = X + width
			
		elif Y < 0:
			Y = Y + height
		
		else:
			break
		
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
	
	global GOD
		
	GOD = factionmethods.Faction(GOD)
	
	print('Newmap procedure completed. Welcome to sector '+str(objectmethods.map_specials[2]))	

def topObjectAt(coordinates,faction='god'):
	"""Returns the object in the top layer for that position in the given dictionary."""
	
	if faction == 'god':
		dictionary = objectmethods.sobject_tracker # all objects
	else:
		dictionary = faction.tracker
		
	objectsatpos = [sobj for sobj in dictionary if sobj.pos() == coordinates] # retrieves the objects in the faction's tracker
	
	if objectsatpos == []:
		objectsatpos = faction.persistent_view.get(coordinates, []) # if there is an object in the persistent_view
		if objectsatpos == []:
			return None
		else:
			return objectsatpos

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
	
	building  = [astr for astr in objectsatpos if astr.objectclass == 'building'] 				# LAYER 1
	if building != []:
		return building[0] # there can be only one. thus...
	
	
	asteroid = [astr for astr in objectsatpos if astr.objectclass == 'asteroid']				# LAYER 0
	if asteroid != []:
		if len(asteroid) != 1:
			raise('Error: {} asteroids per square at {}'.format(len(asteroid),str(coordinates)))
		return asteroid[0] # not a list anymore!
	else:
		return None																
		
def allObjectsAt(coordinates,dictionary='default'):
	"""Returns all objects at the position."""
	if dictionary == 'default':	
		astr = objectmethods.mapcode_tracker.get(coordinates,[])
		if astr != []:
			astr = [astr]
		return [obj for obj in objectmethods.sobject_tracker if obj.states.get('position') == coordinates] + astr
		
	else: # returns all objects in view at point
		return dictionary[coordinates]
	
def map_brutal_dump(faction = 'godview'):
	"""Brutally dumps the codes of all Sobjects existing in the universe."""
	
	if objectmethods.map_specials == None:
		return 'No map to be dumped.'

	# todo : when godview is off, the visualized map depends on the player who calls the brutal-dump
	
	height,width,name = objectmethods.map_specials
	
	print('Brutal_Dump of ' + name + ' pov : ' + str(faction))
	
	if faction == 'godview':
		destinationDict = objectmethods.mapcode_tracker
	elif isinstance(faction,factionmethods.Faction):
		destinationDict = faction.view   	# retrieves the faction's view
	else:
		raise Exception('Bad bad bad.')	
	
	header = '    ' + '_'*(int(width/2) - 4) + name + '_'*(int(width/2) - 4)
	print(header)
	
	linecounter = 0
	for y in range(height): # y, height
		line = '   |'
		for x in range(width): # x, width
			topobj = topObjectAt((x,y),destinationDict) # does the hard work
			
			destinationDict[(x,y)] = topobj # can be None or an object--- the mapcode_tracker tracks only VISIBLE TOP LAYER ITEMS
			
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

def updatePoints(pos1, faction_or_sobject = 'god'):
	"""Updates the mapcode register so as to keep track of small changes."""

	if isinstance(pos1,list):
		pointstoupdate = pos1
	elif isinstance(pos1,tuple) and len(pos1) == 2:
		pointstoupdate = [pos1] # can be generalized to take also lists as input
	else:
		raise Exception('Bad input for updatePoints function; received {} and {}.'.format(str(pos1),str(pos2)))	

#	if  faction == 'god':
#		print("Updating god's eyes...")
#		faction = GOD  # the all-seeing I
#		dictionary = objectmethods.mapcode_tracker
#	else:
#		dictionary = faction.view

	
	god = GOD
	godsview = objectmethods.mapcode_tracker	# god sees everything nonetheless

	factionstoupdate = [god]
	
	# if the object is tracked by more than one view...
	
	if faction_or_sobject != None:
		if isinstance(faction_or_sobject,objectmethods.Sobject):
			factionstoupdate.append(faction_or_sobject.states['faction'])
		elif isinstance(faction_or_sobject, factionmethods.Faction):
			factionstoupdate.append(faction_or_sobject)
	
	for point in pointstoupdate:
		for faction in factionstoupdate:
			if isinstance(point,tuple) != True or len(point) > 2:
				raise Exception('Error here. received pointstoupdate :: ' +str(pointstoupdate))
			
			ontop = topObjectAt(point,faction)
			
			if ontop != None:
				faction.view[point] = ontop
			elif ontop == None:
				faction.view[point] = faction.persistent_view.get(point,None)
			else:
				raise Exception('Error here. received ontop :: ' +str(ontop))
	
	return None
	
def map_smart_dump(faction = 'godview'):
	"""Tries to dump the map in an intelligent way. If there is no map, returns a message. If the map has not been brutal_dumped before, 
	and the dictionary is thus too little, it brutal_dumps it automatically."""
	
	if objectmethods.map_specials == None:
		return 'No map to be dumped.'

	
	if faction != 'godview':
		dictionary = faction.view
	elif faction == 'godview':
		global GOD
		dictionary = GOD.view
	
	height,width,name = objectmethods.map_specials
	
	listoflines = []
		
	header = '    ' + '_'*(int(width/2) - 4) + name + '_'*(int(width/2) - 4)
	print(header)
	
	listoflines.append(header)
	
	linecounter = 0
	for y in range(height): # y, height
		line = '   |'
		for x in range(width): # x, width
		
			topobj = dictionary.get((x,y)) # retrieves the object from the dictionary!
			
			if topobj == None:
				todisplay = ' '
			else:
				todisplay = topobj.states['code']
			
			line = line + str(todisplay)
		line = line + '| ' #+ str(linecounter)
		linecounter +=1
		
		
		print(line)
		listoflines.append(line)

	footer = '    ' + '^' *(width)
	print(footer)
	
	listoflines.append(footer)
	totalwidth = width + 2
	totalheight = height + 2
	
	myMAP = ((height,width),listoflines)
	
	return myMAP
	
	
	
	
	
	
	
