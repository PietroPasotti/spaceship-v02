# mapmethods

import random

def createMapCode(height = 100,width = 100,asteroidratio = 0):
	"""Given height and width, plus optional asteroid ratio, produces a mapcode (randomized 0/1 matrix)."""	
	
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
def LdistX(point,Map):
	return {dot for dot in Map.body.keys() if dot[0] in [(point[0] + 1), (point[0] - 1), point[0]]}			
def LdistY(point,Map):	
	return {dot for dot in Map.body.keys() if dot[1] in [(point[1] + 1), (point[1] - 1), point[1]]}
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
def propagate2(mapcodeheightwidth,threshold,numiters):
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
	return croppedRounded_MAPCODE
def findfactor(dimension,number):
	"""Returns how many times number is in dimension."""
	
	number = sqrt(number ** 2)
	counter = 0	
	while dimension < number:
		number -= dimension
		counter += 1
			
	return counter
