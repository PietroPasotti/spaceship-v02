#main

import objectmethods, namegenmethods, utilityfunctions, mapmethods,dialogmethods,factionmethods
from objectmethods import Sobject
from mapmethods import newMap, map_smart_dump

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




