#general_utilityfunctions

import math,random

class sobjectmethodsError(Exception):
	def __init__(self,parent):
		super().__init__(parent)

def distance(obj1,obj2):
	"""
	As general as possible, returns the distance between two objects on the map.
	Possibly, even the distance between an object and any tuple of coordinates.
	"""
	
	# transform obj1 and obj2 into tuples
	
	def redef(obj):
		if isinstance(obj,spaceship.Vessel) == True or isinstance(obj,spaceship.Fleet) == True or isinstance(obj,Building) == True:
			return obj.states['position']	
		elif isinstance(obj1,tuple):
			return obj
		
	obj1 = redef(obj1)
	obj2 = redef(obj2)	
	
	diffX = max(obj1[0],obj2[0]) - min(obj1[0],obj2[0])
	diffY = max(obj1[1],obj2[1]) - min(obj1[1],obj2[1])
	
	dist = int(sqrt(diffX ** 2 + diffY ** 2)) # pitagora
	return dist
	
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
