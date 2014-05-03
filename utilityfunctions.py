#general_utilityfunctions

import math,random
from copy import deepcopy
import objectmethods

class sobjectmethodsError(Exception):
	def __init__(self,parent):
		super().__init__(parent)


def flatten(l, ltypes=(list, tuple)):
	ltype = type(l)
	l = list(l)
	i = 0
	while i < len(l):
		while isinstance(l[i], ltypes):
			if not l[i]:
				l.pop(i)
				i -= 1
				break
			else:
				l[i:i + 1] = l[i]
		i += 1
	return ltype(l)



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

def mostPowerful(listofSobjects):
	"""Returns the most powerful (attack-based) sobject in the list."""
	
	pwdict = {obj.states.get('attack', 0 ) : obj for obj in listofSobjects}
	
	maxitem = pwdict.pop(max(pwdict))
	
	return maxitem
	
def leastPowerful(listofSobjects):
	"""Returns the weakest (attack-based) sobject in the list."""
	
	pwdict = {obj.states.get('attack', 0 ) : obj for obj in T}
	
	minitem = pwdict.pop(min(pwdict))
	
	return minitem

def sortbypower(listofSobjects):
	"""Returns the list, from the least powerful to the most."""
	
	powerdict = {sobj.states.get('attack', 0 ) : sobj for sobj in listofSobjects} # assigns either his attack or 0
	
	newlist = []
	
	while len(powerdict) != 0:
		minitem = powerdict.pop(min(powerdict))
		newlist.extend([minitem])
		
	return newlist

def findpath(obj,other):
	"""Returns a list of positions, following which you can move square by square to reach other from obj."""
	
	if isinstance(obj,tuple):
		pass
	elif isinstance(obj,objectmethods.Sobject):
		obj = obj.states['position']  # if it has no position, this will rise a keyerror.
	else:
		raise Exception('Bad input for findpath: received ' +str((obj,other)))
	
	if isinstance(other,tuple):
		pass
	elif isinstance(other,objectmethods.Sobject):
		other = other.states['position']  # if it has no position, this will rise a keyerror.
	else:
		raise Exception('Bad input for findpath: received ' +str((obj,other)))

	# now they both are tuples of (x,y) coords
	
	if obj == other:
		return [obj] # the path is to stay still, as they are at the same position. # may return none instead?
	
	objX,objY = obj
	
	otherX,otherY = other
	
	head = (objX,objY)
	tail = [head]
	curhead = deepcopy(head)
	while curhead != other:
		shouldgo = ''
		curheadX = curhead[0]
		curheadY = curhead[1]
		
		if curheadX > otherX: # should go left
			shouldgo += 'l'
		elif curheadX < otherX: # should go right
			shouldgo += 'r'
		else: 
			pass
			
		if curheadY > otherY: # should go up
			shouldgo  += 'u' 
		elif curheadY < otherY: #should go down
			shouldgo += 'd'
		else:
			pass
		
		if shouldgo == '':
			break # the position is reached!
		
		elif shouldgo == 'lu':  # lu	
			curheadY -= 1
			curheadX -= 1
		elif shouldgo == 'ru':  # ru 
			curheadY -= 1
			curheadX += 1
		elif shouldgo == 'ld':  # ld 
			curheadY += 1
			curheadX -= 1
		elif shouldgo == 'rd':  # rd 
			curheadY += 1
			curheadX += 1			
		elif 'l' in shouldgo:   # l
			curheadX -= 1
		elif 'r' in shouldgo:	 # r
			curheadX += 1
		elif 'u' in shouldgo:   # u
			curheadY -= 1
		elif 'd' in shouldgo:   # d
			curheadY +=1
		else:
			raise Exception('Bad input for findpath function: shouldgo is {}, curhead is {}, tail so far is {}'.format(str(shouldgo),str(curhead),str(tail)))
		curhead = (curheadX,curheadY)
		tail.extend([curhead])
	
	return tail
		
def computelife(currentvalue,maximum):
	life = currentvalue
	maxlife = maximum

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
		raise Exception('Something wrong with computelife routine.')
	
	return healthState

def determinemodifiedvalues(dictionary):
	"""Modifies some values of the dictionary, and returns it."""
	
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
	
	healthState = dictionary['health']
	
	genericmodifier = attackmodifiers[healthState] # a positive float
	shieldmodifier = shieldsmodifiers[healthState] # will be a negative integer
	
	if dictionary.get('max_shields') != None:
		dictionary['shields'] = max(int(dictionary.get('max_shields',0) + shieldmodifier),0)	

	if dictionary.get('max_attack') != None:
		dictionary['attack'] = int(dictionary['max_attack'] * genericmodifier)
	
	if dictionary.get('max_range') != None:
		dictionary['range'] = int(dictionary['max_range'] * genericmodifier)
		
	if dictionary.get('max_speed') != None:
		dictionary['speed'] = int(dictionary['max_speed'] * genericmodifier)	

	if dictionary.get('max_spawn') != None:
		dictionary['spawn'] = int(dictionary['max_spawn'] * genericmodifier)
	
	if dictionary['attack'] == 0:
		dictionary['can_attack'] = False
	else:
		dictionary['can_attack'] = True	
	
	return dictionary

def randomasteroid():
	return random.choice(list(objectmethods.mapcode_tracker.values()))

def approx(point,threshold,oclass):
	"""Returns as a list the sobjects of objectclass oclass which are within distance threshold from the give point."""
	simobjects = [obj for obj in objectmethods.sobject_tracker if obj.objectclass == oclass] # e.g. all asteroids, all ships...
	
	posX = point[0]
	posY = point[1]
	
	nearX = {obj for obj in simobjects if  posX - threshold < obj.states['position'][0] < posX +threshold}
	nearY = {obj for obj in simobjects if  posY - threshold < obj.states['position'][1] < posY +threshold}
	
	neighbours = nearX.intersection(nearY)
	
	return list(neighbours)






