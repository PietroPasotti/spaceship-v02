#general_utilityfunctions

import math,random
from copy import deepcopy
import objectmethods

class sobjectmethodsError(Exception):
	def __init__(self,parent):
		super().__init__(parent)

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
		
		
		





		
