# dialogmethods
from namegenmethods import namegen
import objectmethods
import random

class DialogError(Exception):
	def __init__(self,parent):
		super().__init__(parent)


menu_tracker = []



def printOptions(dictionary):
	
	menu_tracker.append(dictionary) # keeps track of what's displayed
	
	if isinstance(dictionary,dict) == False:
		raise DialogError('dictionary is not a dictionary but a ' + str(type(dictionary)))
	
	for key in dictionary:
		description = dictionary[key][0]
		print('   ' + str(key) + ' > ' + description)
	
	print('\n')  											# 'b'	 back, protected choice character
	dictionary['b'] = ('Back', menu_back)
	description = dictionary['b'][0]
	print('     ' + 'b' + ' >> ' + description)
	
	choice = ''
	while choice not in dictionary.keys():
		choice = input("Choose from the available options {}".format(dictionary.keys()))
		if choice in dictionary.keys():
			break
	if len(dictionary[choice]) == 2:
		return dictionary[choice][1]() # function with no argument
	elif len(dictionary[choice]) == 3:
		return dictionary[choice][1](dictionary[choice][2]) # apply 1 to 2
	elif len(dictionary[choice]) == 4:
		return dictionary[choice][1](dictionary[choice][2]), dictionary[choice][3]() # 1 argument to the first, calls the second


def menu_back():
	previousmenu = menu_tracker[len(menu_tracker)-1]
	return printOptions(previousmenu)


def faction_mainMenu(faction):
	
	faction_main = {'1':('Save(not yet implemented)',print, 'not yet implemented'),
				'2':('Load(not yet implemented)',print, 'not yet implemented'),
				'3':('Faction Options', printOptions, faction_factionOptions(faction) ),	
				'4':('Your fleets',printOptions, faction_itemPicker(faction,'fleets' ) ),
				'5':('Your ships',printOptions, faction_itemPicker(faction,'ships' ) ),
				'6':('Your buildings',printOptions, faction_itemPicker(faction,'buildings' ) ),
				'7':('Your scores(not yet implemented)',print, 'not yet implemented')
																			}
	return faction_main

def faction_factionOptions(faction):
	
	choicedict = {'1':('Allies',printOptions, faction_itemPicker(faction,'allies' ) ),
				'2':('Hostiles',printOptions, faction_itemPicker(faction,'hostiles' ) ),
				'3':('Diplomacy screen', printOptions, faction_diplomacyOptions(faction) ),	
				'4':('Subterfuges',printOptions, faction_itemPicker(faction,'fleets' ) ),
				'5':('Strategic Options',printOptions, faction_strategy(faction) )	
					
					}
	
	
	return

def faction_diplomacyOptions(faction):
	"""Returns choicedict of available diplomacy options."""
	
	diplomacy_faction = {'1':('Bribe (nyi)',print, 'not yet implemented'),
				'2':('Pretend (nyi)',print, 'not yet implemented') }	
	
	return diplomacy_faction
	

def faction_itemPicker(faction,objectclass): # params : ships, fleets, allies, hostiles, all, buildings
	
	if objectclass == 'ships':
		objectlist = self.states['ships']
		function = ship_mainMenu
	elif objectclass == 'buildings':
		objectlist = self.states['buildings']
		function = building_mainMenu
	elif objectclass == 'fleets':
		objectlist = self.states['fleets']
		function = fleet_mainMenu
	elif objectclass == 'allies':
		objectlist = self.states['allies']
		function = allies_mainMenu
	elif objectclass == 'hostiles':
		objectlist = self.states['hostiles']
		function = hostiles_mainMenu
	elif objectclass == 'all': # literally all objects
		objectlist = objectmethods.sobject_tracker
		function = all_mainMenu
	else:
		raise DialogError('Unexpected input(s) for faction_itempicker dictionary builder : ' + str(faction) + str(objectclass))
	
	counter = 1
	choicedict = {}
	
	if objectlist == []:
		choicedict[''] = ('The chosen objectlist is empty: You have no ' + objectclass,  menu_back )
	
	else:	
		for obj in objectlist:
			choicedict[str(counter)] = (str(obj), printOptions, function(obj))
			counter += 1
			
	return printOptions(choicedict)



def fleet_mainMenu(fleet):
	
	print('header :: '+ ' fleet ' +str(fleet) + ' selected.')
	faction_main = {'1':('Status',printStatus, fleet),
				'2':('Move',print, 'not yet implemented'),
				'3':('Attack', printOptions, attackOptions(fleet,'fleet') ),	
				'4':('Sensors',printOptions, sensorsOptions(fleet,'fleet') ),
				'5':('Give orders (not yet implemented)',print, 'not yet implemented'),
				'6':('Surroundings-Options', surroundingsActionsOptions(fleet,'fleet'))
				#'7':('Back',faction_itemPicker, fleet.states['faction'])
																			}
	return faction_main


def sensorsOptions(sobject,objectclass):
	"""Returns options for the sensors of a fleet, a ship or a building."""
	if objectclass == 'fleet':
		choicedict = { 	'1' : ('Long range scan with whole fleet [4ap] ', sobject.scan, 'long'),
						'2' : ('Quick scan with best ship [2ap] ', sobject.scan, 'best' ),
						'3' : ('Display status of available sensors', printContent, sobject.scan('returnSensorsDict'))
							}
		return choicedict
	elif objectclass == 'ship':
		choicedict = { 	'1' : ('Long range scan [2ap] ', sobject.scan, 'long'),
						'2' : ('Display status of available sensors', printContent, sobject.scan('returnSensorsDict'))
							}
		return choicedict
	
	elif objectclass == 'building':
		choicedict = { 	'1' : ('Long range scan [2ap] ', sobject.scan, 'long'),
						'2' : ('Display status of available sensors', printContent, sobject.scan('returnSensorsDict'))
							}
		return choicedict
	else:
		raise Exception('Unrecognised objectclass : ' + objectclass)
	
	
def surroundingsActionsOptions(sobject,objectclass):
	"""Return options for surrounding objects. 
	1 - retrieves the surrounding objects (in a range of, say, 10 squares)
	2 - you choose one
	3 - you choose what to do with it"""
	
	


def printStatus(sobject):
	if isinstance(sobject,objectmethods.Sobject) == False:
		raise DialogError('Unexpected input. Sobject needed, got ' +type(sobject) + ' instead.')
	
	todisplay = sobject.states
	
	if len(todisplay) > 20:
		print('Too many values to display. Showing them in compact form instead.')
		# does nothing
		
	for key in todisplay:
		print('   ' + str(key) + '  :  ' + str(todisplay[key]))
	
	return None

def building_mainMenu(building):
	
	print('header :: ' +str(building) + ' selected.')
	faction_main = {'1':('Status',printStatus, building),
				'2':('Move',print, 'not yet implemented'),
				'3':('Attack', printOptions, attackOptions(building,'building') ),	
				'4':('Sensors', printOptions, sensorsOptions(building,'building') ),
				'5':('Give orders (not yet implemented)',print, 'not yet implemented'),
				'6':('Surroundings-Options', surroundingsActionsOptions(building,'building'))
				#'7':('Back',faction_itemPicker, building.states['faction'])
																			}
	return faction_main	
	
def ship_mainMenu(ship):
	
	print('header :: ' +str(ship) + ' selected.')
	faction_main = {'1':('Status',printStatus, ship),
				'2':('Move',print, 'not yet implemented'),
				'3':('Attack', printOptions, attackOptions(ship) ),	
				'4':('Sensors',printOptions, fleet_sensorsOptions(ship) ),
				'5':('Give orders (not yet implemented)',print, 'not yet implemented'),
				'6':('Surroundings-Options', fleet_surroundingsActionsOptions(ship))
				#'7':('Back',faction_itemPicker, ship.states['faction'])
																			}
	return faction_main	
