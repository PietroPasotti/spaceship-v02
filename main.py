#main

import objectmethods, namegenmethods, utilityfunctions, mapmethods,dialogmethods,factionmethods
from objectmethods import Sobject
from mapmethods import newMap, map_smart_dump

dm = dialogmethods
om = objectmethods


def doublescreencheck():
	
	screen = dm.Screen()
	screen.header = "double screen"
	dm.Action(screen.setFooter,["I work"],1,"Test",screen)
	dm._currentscreen_ = screen
	
	looper = dm.LoopInterpreter("double")
	

class Screener:
	"""
	Wrapper / decorator.
	Initializes a new screen.
	Waits for the wrapped function to modify the screen as needed.
	Sets dm._currentscreen_ to the newly initialized screen.
	If the looper is not already acrive, starts it.
	"""
	
	def __init__(self,function):
		self.function = function
	
	def __call__(self):
		screen = dm.Screen()
	
		self.function( screen )
	
		dm._currentscreen_ = screen	
	
		if dm.activelooper is "None":
			activelooper = dm.LoopInterpreter() #inits a looper
		
		if dm.activelooper.looping == False:   #begins looping 
			dm.activelooper.startLooping()


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
	
def ship_move_by_wasd(faction,ship):
	screen = dm.Screen()
	screen.header = ">> wasd moving {} <<".format(str(ship))
	screen.header2 = " ap :: {} ".format(ship.states['action_points'])
	
	dm.Action(objectmethods.Sobject.move,[ship,"u"],"w","Up" ,screen)
	dm.Action(objectmethods.Sobject.move,[ship,"l"],"a","Left" ,screen)
	dm.Action(objectmethods.Sobject.move,[ship,"d"],"s","Down" ,screen)
	dm.Action(objectmethods.Sobject.move,[ship,"r"],"d","Right" ,screen)
	dm.Action(ship_move_interactive,[faction,ship],"b","Back",screen )
	
	dm._currentscreen_ = screen

def ship_move_by_coordinates(faction,ship):
	screen = dm.Screen()
	screen.header = ">> {} <<".format(str(ship))
	screen.header2 = " ap :: {} ".format(ship.states['action_points'])
	
	global x
	global y
	x = 0
	y = 0
	
	def upx(n):
		global x
		x += n
	def upy(n):
		global x
		x += n
		
	dm.Action(upx,[1],"x","Increment x" , screen)
	dm.Action(upy,[1],"y","Increment y" , screen)
	dm.Action(upx,[3],"x+","Increment x +" , screen)
	dm.Action(upy,[3],"y+","Increment y +" , screen)
	dm.Action(upx,[10],"x++","Increment x ++" , screen)
	dm.Action(upy,[10],"y++","Increment y ++" , screen)			
	dm.Action(upx,[20],"X","Increment x +" , screen)
	dm.Action(upy,[20],"Y","Increment y +" , screen)	
	dm.Action(upx,[-10],"X","Decrement x -" , screen)
	dm.Action(upy,[-10],"Y","Decrement y -" , screen)
	dm.Action(ship_move_interactive,[faction,ship],"b","Back",screen )		
	
	screen.footer = " ({},{})".format(x,y)
	dm._currentscreen_ = screen	
	
def ship_move_interactive(faction,ship):
	screen = dm.Screen()
	screen.header = ">> {} <<".format(str(ship))
	screen.header2 = " ap :: {} ".format(ship.states['action_points'])
	
	def cheat_AP(somebody):
		somebody.states['action_points'] = 10
	
	dm.Action(ship_move_by_wasd,[faction,ship],None,"Move by wasd keys",screen)
	dm.Action(ship_move_by_coordinates,[faction,ship],None,"Move by coordinates",screen)
	dm.Action(cheat_AP,[ship],"ap","cheat_ap",screen)
	dm.Action(shipOptions_main,[faction,ship],"b","Back",screen )	
	
	dm._currentscreen_ = screen

def shipOptions_main(faction,ship):
	screen = dm.Screen()
	screen.header = ">> {} <<".format(str(ship))

	a = ship.enemiesInRange()
	if a != []:
		dm.Action( ship.attack,["auto"],None,"Attack closest in range",screen)
	dm.Action( ship_move_interactive,[faction,ship],None,"Move",screen)
	dm.Action(shipselectionscreen,[faction],"b","Back",screen )	
	
	dm._currentscreen_ = screen


def buildingattackscreen(faction,building):
	screen = dm.Screen()
	screen.header = ">> {} <<".format(str(building))
	a = building.autoattack()
	screen.header2 = " autoattack is {}".format(a)
	
	dm._currentscreen_ = screen	
	dm.Action(buildingsOptions_main,[faction,building],"b","Back",screen )	

def buildingsOptions_main(faction,building):
	screen = dm.Screen()
	screen.header = ">> {} <<".format(str(building))
	a = building.autoattack()
	
	def reloadheader2(screen):
		screen.header2 = " autoattack is {}".format(a)
	
	reloadheader2()
		
	reload_me =  dm.Action(reloadheader2,[screen])
	
	a = building.autoattack()
	dm.Action( building.autoattack,[],None,"Toggle building autoattack.",screen,[reloadheader2])
	dm.Action( buildingattackscreen,[],None,"Select attack target manually.",screen)
	
	
	if a != []:
		dm.Action( ship.attack,["auto"],None,"Attack closest in range",screen)
	
	if building.canspawn() == True:
		dm.Action( spawn_screen,[faction,building],None,"Spawn",screen)
	
	dm.Action(buildingsselectionscreen,[faction],"b","Back",screen )	
	
	dm._currentscreen_ = screen	



def buildingsselectionscreen(faction):
	screen = dm.Screen()
	screen.header = "Pick a building from {}'s shiplist".format(faction.states['name'])
	
	for building in faction.states['buildings']:
		dm.Action(buildingsOptions_main,[faction,building], None, "{}".format(str(building)),screen)
	
	dm.Action(buildingsactionsscreen,[faction],"b","Back.",screen)
	dm._currentscreen_ = screen


def buildingsactionsscreen(faction):
	screen = dm.Screen()
	dm.Action(buildingsselectionscreen ,[faction],None,"Select a specific building.",screen)
	
	dm.Action(factionscreen_main,[faction],"b","Back.",screen)
	dm._currentscreen_ = screen
	

def strategyscreen(faction):
	screen = dm.Screen()
	screen.header = "Strategic options of {}".format(faction.states['name'])
	reload_view = dm.Action(map_smart_dump,[faction])
	dm.Action(factionscreen_main,[faction],None,"Go back, nothing to do yet.",screen)	
	dm._currentscreen_ = screen
	
def fleetselectionscreen(faction):
	screen = dm.Screen()
	screen.header = "Pick a fleet from {}'s shiplist".format(faction.states['name'])
	dm.Action(factionscreen_main,[faction],None,"Go back, nothing to do yet.",screen)	
	dm._currentscreen_ = screen
	
def shipselectionscreen(faction):
	screen = dm.Screen()
	screen.header = "Pick a ship from {}'s shiplist".format(faction.states['name'])
	
	for ship in faction.states['ships']:
		dm.Action(shipOptions_main,[faction,ship], None, "{}".format(str(ship)),screen)
	
	dm.Action(shipactionsscreen,[faction],"b","Back.",screen)
	dm._currentscreen_ = screen
		
def shipactionsscreen(faction):
	screen = dm.Screen()
	dm.Action(shipselectionscreen ,[faction],None,"Choose an individual ship.",screen)
	dm.Action(faction.complete_scan,[],None,"Have each of your ships do a complete scan. [2ap,2fp]",screen)
	dm.Action(factionscreen_main,[faction],"b","Back.",screen)
	dm._currentscreen_ = screen

def factionscreen_main(faction):
	screen = dm.Screen()
	dm._currentfaction_ = faction
	
	screen.header = "Faction {}".format(faction.states['name'])
	
	howmany_ships = len(faction.states['ships'])
	howmany_fleets = len(faction.states['fleets'])
	howmany_buildings = len(faction.states['buildings'])
	
	if howmany_ships != 0:
		dm.Action(shipactionsscreen,[faction],None,"Ships actions",screen)
		
	if howmany_buildings != 0:
		dm.Action(buildingsactionsscreen,[faction],None,"Building actions",screen)	
		
	if howmany_fleets != 0:
		dm.Action(fleetselectionscreen,[faction],None,"Fleets actions",screen)
	dm.Action(strategyscreen,[faction],None,"Strategy",screen)
	dm.Action(dialogmethods.LoopInterpreter.halt,[dm.activelooper],"halt","Exit LoopInterpreter",screen, protected = True) # protected
	
	dm._currentscreen_ = screen


# if decommented starts the menu automatically
#@Screener
def initialize(screen):	
	screen.header = "Initializer"
	
	for faction in [ faction for faction in factionmethods.existing_factions if faction.states['name'] not in factionmethods.protected_factions]:	
		accept = dm.Action(screen.setFooter,["Chosen faction {}".format(faction.states['name'])])
		dm.Action(factionscreen_main,[faction],None,"{}".format(faction.states['name']) ,screen,[accept])
		
	dm.Action(dialogmethods.LoopInterpreter.halt,[dm.activelooper],"halt","Exit LoopInterpreter",screen, protected = True) # protected
	
	
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

d = Sobject('fleet',{'shiplist':['fighter','destroyer','cruiser','swarmer',b], 'position':(20,20)})

e = Sobject('fleet',{'shiplist':['fighter','fighter','destroyer','cruiser','mothership'], 'position' :(22,23)})

#newMap()

#mapmethods.GOD.god_spawn([a,b,c])

#me = factionmethods.Faction()
#me.initFaction(None,False)
#you = factionmethods.Faction()
#you.initFaction(None,False)



