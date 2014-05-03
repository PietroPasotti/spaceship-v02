#main

import objectmethods, namegenmethods, utilityfunctions, mapmethods,dialogmethods,factionmethods
from objectmethods import Sobject
from mapmethods import newMap, map_smart_dump

dm = dialogmethods

def removeduplicates(alist):
	for item in alist:
		if alist.count(item) > 1:
			alist.remove(item)


def itempick(listofoptions,choice = []):
			
	chooseashipscreen = dialogmethods.Screen()
	
	# invisible actions:
	invisibacktrigger = dm.Action(chooseashipscreen.Back)
	invisibacktrigger.setName("-- press Enter to confirm and go back --")
	invisibacktrigger.setTag('')
	backbutton = chooseashipscreen.addBack()
	invisibacktrigger.connect(dm.Action(chooseashipscreen.satisfy,[]))
	
	
	# abstract actions:
	confirmtrigger = dm.Action(dm.PRINTER.screen.removeFromBody,[backbutton])
	confirmtrigger2 = dm.Action(chooseashipscreen.addToProtected,[invisibacktrigger])
	
	listofactions = []
		
	for elem in listofoptions:
		
		chooseelem = dm.Action(choice.append, [elem],None,None,"choose {}".format(str(elem)),chooseashipscreen)
		chooseelem.connect(dm.Action( chooseashipscreen.setFocus ,[ chooseelem ]  ) )
		
		def setheader():
			choicestr = choice[len(choice)-1] # last element
			chooseashipscreen.header = "{} selected.".format(choicestr )
			
		chooseelem.connect(dm.Action( setheader, []  ))
		chooseelem.connect(confirmtrigger)
		chooseelem.connect(confirmtrigger2)
		listofactions.append(chooseelem)
	
	def condition1():
		if len(choice) != 1:
			return False
		else:
			return True
			
	#condition1 = dm.Condition("Too many items are selected."  ,[condition1])
	
	chooseashipscreen.Start()

def attackscreen(ship):
	print("here")

def basetest():
	
	#situation setup
	b = me.states['ships'][0] 
	a.warp(b.pos(),['override'])	
	a.heal(1,['max','override'])
	a.checkStates()
	
	# ms init
	ms = dm.Screen()
	
	choice = [] # what will be returned
	
	# buttons definitions for ms
	f = dm.Action(itempick,[(b,c),choice],1,None,'Choose a ship',ms)
	e = dm.Action(print,["Idling..."],1,None,"Idle",ms)
	
	
	d = dm.Action(attackscreen,[choice])
	g = dm.Action(ms.addToBody,[d])
	ms.onsatisfied_connect(g)
	
	
	ms.Start()
	
	choice = choice[len(choice)-1]
	strchoices = str(choice) 
	
	print("good, you have chosen {}".format(  strchoices  ))
	return choice
	


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


a.attack(b)
b.attack(c)
c.attack(a)
a.attack(c)

newMap()

mapmethods.GOD.god_spawn([a,b,c])


me = factionmethods.Faction()
me.initFaction(None,False)
you = factionmethods.Faction()
you.initFaction(None,False)
map_smart_dump()


basetest()

