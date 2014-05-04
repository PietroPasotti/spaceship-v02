#main

import objectmethods, namegenmethods, utilityfunctions, mapmethods,dialogmethods,factionmethods
from objectmethods import Sobject
from mapmethods import newMap, map_smart_dump

dm = dialogmethods
om = objectmethods


def attackscreen():
	
	a = om.Sobject('ship',{"shipclass":"swarmer","position":(20,20)})
	b = om.Sobject('ship',{"shipclass":"fighter","position":(20,21)})

	screen = dm.Screen()
	screen.header = "Attack screen"
	dm.Action(om.Sobject.attack,[a,b],1,"A attacks B",screen)
	dm.Action(om.Sobject.attack,[b,a],2,"B attacks A",screen)
	dm.Action(setupscreen,[],4,"Go to previous screen",screen)
	dm.Action(attackscreen,[],None,"Go to attack screen",screen)
	dm.Action(map_smart_dump,[],None,"Refresh map",screen)
	dm._currentscreen_ = screen
	
	
	
def ship_move_interactive(faction,ship):
	screen = dm.Screen()
	screen.header = ">> {} <<".format(str(ship))
	screen.header2 = " ap :: {} ".format(ship.states['action_points'])
	reload_view = dm.Action(map_smart_dump,[faction])
	
	def cheat_AP(somebody):
		somebody.states['action_points'] = 10
	
	reload_screen = dm.Action(ship_move_interactive,[faction,ship])
	
	dm.Action(objectmethods.Sobject.move,[ship,"u"],"w","Up",screen,[reload_view,reload_screen] )
	dm.Action(objectmethods.Sobject.move,[ship,"l"],"a","Left",screen,[reload_view,reload_screen] )
	dm.Action(objectmethods.Sobject.move,[ship,"d"],"s","Down",screen,[reload_view,reload_screen] )
	dm.Action(objectmethods.Sobject.move,[ship,"r"],"d","Right",screen,[reload_view,reload_screen] )
	
	
	dm.Action(cheat_AP,[ship],"ap","cheat_ap",screen,[reload_view,reload_screen])
	dm.Action(shipOptions_main,[faction,ship],"b","Back",screen,[reload_view] )	
	

	dm._currentscreen_ = screen

def shipOptions_main(faction,ship):
	screen = dm.Screen()
	screen.header = ">> {} <<".format(str(ship))
	reload_view = dm.Action(map_smart_dump,[faction])
	
	# a = ship.closestinrange()
	#dm.Action( ship.attack,[a],None,"Attack closest in range",screen,[reload_view] )
	dm.Action( ship_move_interactive,[faction,ship],None,"Move",screen,[reload_view] )
	dm.Action(factionscreen_main,[faction],"b","Back",screen,[reload_view] )	
	
	dm._currentscreen_ = screen

def strategyscreen(faction):
	screen = dm.Screen()
	screen.header = "Strategic options of {}".format(faction.states['name'])
	reload_view = dm.Action(map_smart_dump,[faction])
	dm.Action(factionscreen_main,[faction],None,"Go back, nothing to do yet.",screen,[reload_view])	
	dm._currentscreen_ = screen
	
def fleetselectionscreen(faction):
	screen = dm.Screen()
	screen.header = "Pick a fleet from {}'s shiplist".format(faction.states['name'])
	reload_view = dm.Action(map_smart_dump,[faction])
	dm.Action(factionscreen_main,[faction],None,"Go back, nothing to do yet.",screen,[reload_view])	
	dm._currentscreen_ = screen
	
def shipselectionscreen(faction):
	screen = dm.Screen()
	screen.header = "Pick a ship from {}'s shiplist".format(faction.states['name'])
	reload_view = dm.Action(map_smart_dump,[faction])
	
	for ship in faction.states['ships']:
		dm.Action(shipOptions_main,[faction,ship], None, "choose {}".format(str(ship)),screen,[reload_view])
	
	dm.Action(factionscreen_main,[faction],"b","Back.",screen,[reload_view])
	dm._currentscreen_ = screen
	
def factionscreen_main(faction):
	screen = dm.Screen()
	screen.header = "Faction {}".format(faction.states['name'])
	
	howmany_ships = len(faction.states['ships'])
	howmany_fleets = len(faction.states['fleets'])
	reload_view = dm.Action(map_smart_dump,[faction])
	
	if howmany_ships != 0:
		dm.Action(shipselectionscreen,[faction],None,"Ships actions",screen,[reload_view])
		
	if howmany_fleets != 0:
		dm.Action(fleetselectionscreen,[faction],None,"Fleets actions",screen,[reload_view])
	
	dm.Action(strategyscreen,[faction],None,"Strategy",screen,[reload_view])
	#screen.printer.display()
	dm._currentscreen_ = screen
	
def initialize():
	''''''
	
	dm._currentscreen_ = dm.Screen()
	screen = dm._currentscreen_ 
	screen.header = "Initializer"
	
	refresh = dm.Action(map_smart_dump)
	
	for faction in factionmethods.existing_factions:
		accept = dm.Action(print,[''],None,"Chosen faction {}".format(faction.states['name']))
		reload_view = dm.Action(map_smart_dump,[faction])
		dm.Action(factionscreen_main,[faction],None,"{}".format(faction.states['name']) ,screen,[refresh,accept,reload_view])
		
	looper = dm.LoopInterpreter()
	
	
	
def clear_all():
	factionmethods.existing_factions = []
	objectmethods.mapcode_tracker = {}
	mapmethods.sobject_tracker = []
	objectmethods.map_specials = None
	mapmethods.GOD = None
	
def menu():
	menu = dialogmethods.currentmenu
	menu.showScreen()

a = Sobject('ship',{'position':(15,15)})

b = Sobject('ship',{'shipclass':'mothership', 'position':(15,15)})

c = Sobject('ship',{'shipclass':'fighter', 'position':(13,12)})

#d = Sobject('fleet',{'shiplist':['fighter','destroyer','cruiser','swarmer',b], 'position':(20,20)})

#e = Sobject('fleet',{'shiplist':['fighter','fighter','destroyer','cruiser','mothership'], 'position' :(22,23)})

newMap()

mapmethods.GOD.god_spawn([a,b,c])


me = factionmethods.Faction()
me.initFaction(None,False)
you = factionmethods.Faction()
you.initFaction(None,False)
#map_smart_dump()




