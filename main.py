#main

import objectmethods, namegenmethods, utilityfunctions, mapmethods
from objectmethods import Sobject
from mapmethods import newMap, map_smart_dump

# dialogmethods.init()
# dialogmethods.Start()
# dialogmethods.DisplayEndScreen()

a = Sobject('ship')

b = Sobject('ship',{'shipclass':'mothership'})

c = Sobject('ship',{'shipclass':'fighter'})

d = Sobject('fleet',{'shiplist':['fighter','destroyer','cruiser','swarmer',b]})

e = Sobject('fleet',{'shiplist':['fighter','fighter','destroyer','cruiser','mothership']})

a.attack(b)

b.attack(c)
c.attack(a)
a.attack(c)

newMap()

map_smart_dump()

a.states['position'],b.states['position'],c.states['position'] = (10,10),(10,10),(10,10)

a.move((10,40))
b.move((30,10))
a.move(b.states['position'])


