#main

import objectmethods, namegenmethods, utilityfunctions, mapmethods,dialogmethods,factionmethods
from objectmethods import Sobject
from mapmethods import newMap, map_smart_dump

def basetest():
	dm = dialogmethods
	ms = dm.masterscreen
	f = dm.Action(print,["hello","world"],2,None,'Print hello world thrice')
	ms.addToBody(f)
	f = dm.Action(print,["hello","world"],9,None,'Print hello world nine times')
	ms.addToBody(f)
	f = dm.Action(print,["hello","world"],1,'once','Print hello world once,tagged')
	ms.addToBody(f)
	f = dm.Action(print,["hello","world"],2,"thrice",'Print hello world thrice,tagged')
	ms.addToBody(f)
	ms.printer.display()
	a.warp(b.pos(),['override'])
	a.heal(1,['max','override'])
	b.heal(1,['max','override'])
	f = dialogmethods.Action(a.attack,[b],1,'ab',"a attacks b")
	ms.addToBody(f)


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

