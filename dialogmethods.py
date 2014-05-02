# dialogmethods
from namegenmethods import namegen
import objectmethods
import random
import factionmethods
import mapmethods
import utilityfunctions


class DialogError(Exception):
	def __init__(self,parent):
		super().__init__(parent)

currentmenu = None
currentscreen = None

menu_tracker = []

TREE = """
faction_mainMenu:
			_save_
			_load_
			_scores_
			_credits_
			_ingameMenu_:		
					factionOptions:
								itemPicker(allies):
										allies_mainMenu:
								itemPicker(hostiles):
										hostiles_mainMenu:
								diplomacyOptions:
								subterfuges:
								strategy:
								
					itemPicker(fleets) == itemPicker(ships):
								printStatus
								_(move)_
								_(attackOptions -m)_
								sensorsOptions -m
								_give orders_
								surroundingsActionsOptions
								_(spawn)_
																
					itemPicker(buildings):
								_(spawn)_
								sensorsOptions -m
												




"""



def menuLoop(faction = None):
	
	global currentmenu
	
	if currentmenu == None:
		currentmenu = InteractiveMenu(faction)
	
	counter = 0
	while True:
		currentmenu.showScreen()
		close = currentmenu.closetoggled
		if close == True:
			break
		
		counter += 1
		
	return "menuLoop terminated. {} loops".format(counter)	




class InteractiveMenu():
	
	def __init__(self,faction = None):
		
		print('Initializing InteractiveMenu...')
		
		global currentmenu
		currentmenu = self
		
		self.closetoggled = False # trigger for menuLoop
		
		FirstMenu_NoFaction = [('0',("Bind Faction","self.bindFaction()")),
					('1',("Hi Pussy","print('Hi, Pussy.')"))]
		
		self.faction = faction
		
		if faction == None:
			INIbody = FirstMenu_NoFaction
		elif type(faction) == factionmethods.Faction:
			self.factionMenu()
		
		self.menuHistory = []
							
		self.screen = MenuScreen('choice','init', INIbody,False)  #(self,mode,tag,body,back):  # false: we don't add a back key there.
	
		
	def __str__(self):
		return self.screen.tag
	
	def __repr__(self):
		
		menulist = self.screenHistory() # automatically picks only non-choice screens
		rep = '$'
		for i in menulist:
			rep = rep + " -> " + i.tag
		
		if self.screen.mode == 'grab':
			rep = rep + " || -> " + self.screen.tag  # but if the current screen is a grabber, it will show it in the header
		
		return "[{}]".format(rep)

	def screenHistory(self,kyarg = None):  # by default, returns a list of all choice -only type screens
		"""returns a complete list of all (default: 'choice'-type) screens in the past display history, from first to last."""
		
		screenlist = [self.screen] 
		screen = self.screen
		while True:
			if screen.previousscreen is None:
				break
			else:
				screenlist = [screen.previousscreen] + screenlist
				screen = screen.previousscreen

		screentags = [ S.tag for S in screenlist ] # enumerates all tags in screenlist
		
		for screen in screenlist:    # check for duplicates. There should not be.
			
			if screenlist.count(screen) != 1:
				raise DialogError("Damn! there are {} screens {} in screenhistory".format(screenlist.count(screen),str(screen)))
	
		if kyarg == 'tag':
			onlychoicelist = [screen for screen in screenlist if screen.mode == 'choice' ]
			choicetypetags = [ S.tag for S in onlychoicelist ]
			
			for tag in choicetypetags:   # check for duplicates. There should not be.
				if choicetypetags.count(tag) > 1:
					raise DialogError("Damn! there are {} screens {} in screenhistory".format(choicetypetags.count(tag),str(tag)))
			
			return choicetypetags
		
		if kyarg == None: # prunes off 'grab' and 'action' - type menus
			screenlist = [screen for screen in screenlist if screen.mode == 'choice']

		return screenlist
		

# SCREEN MAIN
	
	def setupScreen(self,mode,tag,voiceslist):
		"""Creates a new screen with the given parameters and sets it as its current screen.
		Also, if the screen is already present in history, returns it instead."""
		
		if voiceslist == None:
			raise DialogError('Bad. My input was : ' + str(self) + str(tag) +str(voiceslist))
		
		oldercopies = [ screen for screen in self.screenHistory() if screen.tag == tag ]
		
		if oldercopies == []:
			newScreen = MenuScreen(mode,tag,voiceslist)
		elif len(oldercopies) == 1:
			newScreen = oldercopies[0]
		else:
			raise DialogError("Something wrong.")
			
		self.screen = newScreen
		
	def showScreen(self,options = []):
		
		print(repr(self))
		print("Now displaying :: " + self.screen.tag)
		print('     '+('-'*100))
		choicedict = {}
		for voice in self.screen.body:
			line = "  {}   >>   {}".format(voice[0],voice[1][0])
			print(line)
			choicedict[voice[0]] = voice[1][1]
		print('     '+('-'*100))
		
		while True:
			IN = input("Choose :: = ")
			
			if IN not in [choice for choice in list(choicedict.keys())]:
				print("Bad input, asshole. Possible choices are: " + str(list(choicedict.keys())))
				pass
			else:
				break
		
		print("Executing order... Mode is "+str(self.screen.mode))
		
		choice = choicedict[IN]
		
		
		# if the choice is a tuple (">>",boundmethod) and contains a special escape character, we will suddenly switch to action mode and pass
		
		if isinstance(choice,tuple) and choice[0] == ">>" or self.screen.mode == 'action':
			self.screen.mode = 'action' # in case it was a special escaped tuple
			method = choice[1] # crop the escape characters away
			if len(choice) == 3:
				argument1 = choice[2]
			if len(choice) == 4:
				argument2 = choice[3]
			if len(choice) == 5:
				argument3 = choice[4]  # takes up to 3 additional arguments
			if len(choice) > 5:
				raise DialogError('Bad. Received too long a tuple.')
				
			# method is a bound method of the object in focus
			FOCUS = self.sobjectinfocus
			
			if len(choice) == 5:
				FOCUS.choice(argument1,argument2,argument3)
				
			if len(choice) == 4:
				FOCUS.choice(argument1,argument2)
				
			if len(choice) == 3:
				FOCUS.choice(argument1)
			
			if len(choice) == 2:		
				FOCUS.choice() # apply the chosen action to the focused object
			
			return self.back()
			
		
		elif self.screen.mode == 'grab': # e.g. for itempick functions
			return choice
			
		elif self.screen.mode == 'choice':		
			#try:
			print('choice is '+str(choice))
			return exec(choice)
		#	finally:
		#		print(self.screen.body,self.screen.tag,self.screen.mode)
		#		raise DialogError("BAD. Received " + str(choice) + 'which is a {}'.format(type(choice)))
		else:
			raise DialogError('What?')

	def Close(self):
		self.closetoggled = True
		

	def Back(self): # goes back to the previous screen
		"""Goes back to the first screen available upstream of type 'choice'."""
		
		#self.menuHistory.remove(self.screen) # clean menuhistory
		
		print(self.menuHistory)
		print(self.screenHistory())
		
		while True: # looks for a previous screen in mode 'choice'
			self.screen = self.screen.previousscreen 
			if self.screen.mode == 'choice':
				break
			else:
				pass
				

	def backOption(self): # produces a menu voice to go back and returns it
		
		return ('b',("Back","self.Back()"))

# ITEMPICK
			
	def itemPick(self,keyarg):
		"""Returns a **Sobject**."""
		
		if self.faction == None and keyarg != 'faction':
			raise DialogError("Can't pick an object if you belong to no faction.")
		
		if keyarg == 'faction':
			choicelist = factionmethods.existing_factions
			
		elif keyarg == 'ship':
			choicelist = [ item for item in self.faction.states['ships'] ]
			
		elif keyarg == 'fleet':
			choicelist = [ item for item in self.faction.states['fleets'] ]
		
		else:
			raise DialogError('Unknown input: {}'.format(keyarg))		
			
		availableitems = []
		counter = 0
			
		for faction in choicelist:             							# generates the list of items
			values = (str(counter),(str(faction.name()) , faction))		# this assumes the object has a .name() method!
			counter += 1
			availableitems.append(values)
			 #(self,mode,tag,body):
					 
		self.screen = MenuScreen('grab','{}_itemPick'.format(keyarg),availableitems) # creates a brand new screen
		
		picked_object = self.showScreen() # returns a value!!
		
			
		if picked_object == "self.Back()": # we capture Back keys
			self.Back()
			return None
		
		if isinstance(picked_object,objectmethods.Sobject) or isinstance(picked_object,factionmethods.Faction):
			print("Chosen a "+str(type(picked_object)) +"...")
			return picked_object
		else:
			raise DialogError('Received a ' + str(picked_object) + ' instead. Cannot parse.')
				

# FACTION SETUP AND OPTIONS
	
	def bindFaction(self,faction = None):
		"""Ties the Menu to some faction."""
		
		if faction == None or self.faction == None:

			faction = self.itemPick('faction') # returns an object
		else:
			raise DialogError("You already have a bound faction, and is " + str(self.faction))
		
		self.faction = faction 					# ties the menutree with the faction
		
		if type(self.faction) != factionmethods.Faction:
			raise DialogError("Bad. Your faction now is " + str(self.faction))
		
		self.factionMenu() # sets the next screen to be the factionmenu
	
	def factionMenu(self,options = []):
		"""Displays the menu of choices available to a faction."""
		
		if type(self.faction) != factionmethods.Faction:
			raise DialogError("Bad. Your faction now is " + str(self.faction))
		
		factionchoicemenu = [
			# code  name   function 
			(  '1'   		,(  "_save_"				,	"savemethods.save()"		)),			
			(  '2'   		,(  "_load_"				,	"savemethods.load()"		)),			
			(  '3'   		,(  "_scores_"				,	"self.scoresScreen()"		)),			
			(  '4'   		,(  "_credits_"				,	"self.creditsScreen()"		)),			
			(  '5'   		,(  "in_game Main Menu"		,	"self.inGameMainMenu()"		))]
		
		
		tag = "faction >{}< Menu".format(self.faction.states['name'])
		
		self.setupScreen('choice',tag,factionchoicemenu)  #(self,mode,tag,body,back):
		
		#self.showScreen()


# INGAME MENU
		
	def inGameMainMenu(self):
		
		fc = len(self.faction.states['fleets'])
		bc = len(self.faction.states['buildings'])
		sc = len(self.faction.states['ships'])
		
		ingamemainmenu = [
			# code  name   function 
			(  '0'   		,(  "Fleets [{}]".format(fc)				,	"self.sobjectOptions('fleet')"		)),			
			(  '1'   		,(  "Buildings [{}]".format(bc)				,	"self.sobjectOptions('building')"	)),			
			(  '2'   		,(  "Ships [{}]".format(sc)					,	"self.sobjectOptions('ship')"		)),			
			(  '3'   		,(  "Command Center"						,	"self.factionOptions()"				))]
			
		
		if fc == 0:
			print("** No fleet to be chosen from. **")
			ingamemainmenu[0] = (  ' '   		,(  "Fleets [{}]".format(fc)				,	"self.inGameMainMenu()"	))
		
		if bc == 0:
			print("** No building to be chosen from. **")
			ingamemainmenu[1] = (  ' '   		,(  "Buildings [{}]".format(fc)				,	"self.inGameMainMenu()"	))			
		
		if sc == 0:
			print("** No ships to be chosen from. **")
			ingamemainmenu[2] = (  ' '   		,(  "Ships [{}]".format(fc)				,	"self.inGameMainMenu()"	))				
		
		self.setupScreen('choice','ingame Main Menu',ingamemainmenu) #(self,mode,tag,body):

		
	def sobjectOptions(self,objectclass):
		"""Displays your {fleets/ships/buildings}, call an itempick and passes the chosen fleet to {item}_Actions"""
		
		accepted_inputs = ["fleet",'building',"ship"]
		
		if objectclass not in accepted_inputs:
			raise DialogError('Bad. Received a ' + str(objectclass))

		choice = self.itemPick(objectclass) # lets you choose an item of the selected objectclass
		self.sobjectfocus = choice # puts the object in self.sobjectfocus !
		
		self.firstActionMenu(choice) 
		# the next-showed menu will be a menu with the options of the faction with respect to the item.
	
	def firstActionMenu(self,sobject):
		
		if not isinstance(sobject,objectmethods.Sobject):
			raise DialogError('Bad input: needed a sobject, received a '+ str(sobject) + ' instead.')
			
		if sobject.states['faction'] != self.faction:  # if the item you are choosing actions for is not yours, the actions available will be different.
			return self.actionOnEnemyObject(sobject)
			
		else:
			pass
		
		firstactionmenu = [
			# code  name   function 
			(  '1'   		,(  "Move [{}]".format(int(sobject.states['speed']))						,	"self.Action('move')"		)),			
			(  '2'   		,(  "Attack [{}]".format(int(sobject.enemiesInRange('number')))				,	"self.Action('attack')"		))]
		
		header = "action_menu for "+str(sobject)+ "  ::  available action_points  |->  "+str(sobject.states['action_points'])
		
		self.setupScreen('choice',header,firstactionmenu) #(self,mode,tag,body):
		
		#self.showScreen()

	def Action(self,actiontype):
		"""Retrieves the selected item (the item in self.focus)"""
		
		if isinstance(self.sobjectfocus,objectmethods.Sobject) == False:
			raise DialogError('Bad. self.sobjectfocus is ' +str(self.sobjectfocus ))
			
		if actiontype == 'move':
			
			OIF = self.sobjectfocus
			
			OM = objectmethods.Sobject
			sA = mapmethods.angles
			sO = self.sobjectfocus.pos()
			MO = mapmethods.orthogonals       # returns the right/left/up/down _most position w.r.t. the given object
			
			movechoice = [	( 	'1'	,( "Exit"					, 	None		)),
							( 	'2'	,( "SetSpeed"			, 	"self.quickchoice(int,'speed')"			)),
							( 	'3'	,( "Custom direction"	, 	(">>",	OM.move	)	)),
							( 	'2'	,( "Quick_go_DR"		, 	(">>",	OM.move,	sA("DR")	)			)),
							( 	'3'	,( "Quick_go_DL"		, 	(">>",	OM.move,	sA("DL")	)			)),
							( 	'2'	,( "Quick_go_UR"		, 	(">>",	OM.move,	sA("UR")	)			)),
							( 	'3'	,( "Quick_go_UL"		, 	(">>",	OM.move,	sA("UL")	)			)),
							( 	'4'	,( "Quick_go_up"		, 	(">>",	OM.move,	MO(OIF, "u")	)			)),
							( 	'5'	,( "Quick_go_down"		, 	(">>",	OM.move,	MO(OIF, "d")	)			)),
							( 	'6'	,( "Quick_go_right"		, 	(">>",	OM.move,	MO(OIF, "r")	)			)),
							( 	'7'	,( "Quick_go_left"		, 	(">>",	OM.move,	MO(OIF, "l")	)			))]
							
							
			choicemenu =  movechoice
			
		elif actiontype == 'attack':
			
			attackchoice = []
		
			choicemenu = attackchoice
			
		
		header = "action_menu: type 'action', actiontype is {} and sobjectfocus is {}".format(actiontype,str(self.sobjectfocus))
		
		self.setupScreen('action',header,choicemenu) #(self,mode,tag,body):
							# action mode will call a method of the object in self.sobjectfocus!
		
		#self.showScreen()		
			
		
		


class MenuScreen():
	
	def __init__(self,mode,tag,body,back = True):
		
		if not isinstance(mode,str) or not isinstance(tag,str) or not isinstance(body, list):
			
			raise DialogError('Bad. Interrupt. My input was: {} {} {}'.format(mode,tag,body) )

		self.body = body
		self.tag = tag
		self.mode = mode # modes are: choice, grab
		
		global currentscreen
		
		if currentscreen is None:
			self.previousscreen = None				# previous is self
		else:
			self.previousscreen = currentscreen 	# previous becomes current
			
		currentscreen = self					 	# current becomes self

		if self in currentmenu.menuHistory:
			print(str(currentmenu.menuHistory))
			print(repr(currentmenu))
			print("And finally... " + str(self))
			raise DialogError('Problem.')
		
		if back == True:
			self.addBack()
			
		currentmenu.menuHistory.append(self)


	def __str__(self): # just for backtraces
		
		return "<screen object>: mode {}, tag {}, \n >> body {}:".format(self.mode,self.tag,self.body)

	def addBack(self):
		
		if 'b' in self.listKeys():
			return None
		
		backoption = currentmenu.backOption()
		self.body.append(backoption)
		
	def listKeys(self):
		keys = [key[0] for key in self.body]
		return keys

