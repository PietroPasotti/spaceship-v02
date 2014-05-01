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

class InteractiveMenu():
	
	def __init__(self):
		
		print('Initializing InteractiveMenu...')
		
		global currentmenu
		currentmenu = self
		
		INIbody = [('0',("Bind Faction","self.bindFaction()")),
					('1',("Hi Pussy","print('Hi, Pussy.')"))]
		
		self.menuHistory = []
							
		self.screen = MenuScreen('choice','init', INIbody)  #(self,mode,tag,body,number = None):
		
		self.showScreen()
		
	def __str__(self):
		return self.screen.tag
	
	def __repr__(self):
		menulist = [screen for screen in self.menuHistory]
		rep = ''
		for i in menulist:
			rep = rep + " -> " + i.tag

		return "[{}]".format(rep)
		
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
		
		if self.screen.mode == 'grab': # e.g. for itempick functions
			return choice
			
		elif self.screen.mode == 'choice':		
			try:
				return exec(choice)
			except TypeError:
				print(self.screen.body,self.screen.tag,self.screen.mode)
				raise DialogError("BAD. Received " + str(choice) + 'which is a {}'.format(type(choice)))
		else:
			raise DialogError('What?')

	def close(self):
		return None
	
	def setupScreen(self,mode,tag,voiceslist,number=None):
		"""Creates a new screen with the given parameters and sets it as its current screen."""
		
		if number == None:
			number = self.curNumber()
		
		if voiceslist == None:
			raise DialogError('Bad. My input was : ' + str(self) + str(tag) + str(number) +str(voiceslist))
		
		newScreen = MenuScreen(mode,tag,voiceslist,number)
		self.screen = newScreen		

	def curNumber(self,keyarg = None):
		
		if keyarg == 'grabber':
			
			return len(self.menuHistory)
			
		else:
			return len(self.menuHistory)
			
	def itemPick(self,keyarg):
		"""Returns a **Sobject**."""
		
		if keyarg == 'faction':
			choicelist = factionmethods.existing_factions
			
		elif keyarg == 'ship':
			choicelist = [ item for item in objectmethods.sobject_tracker if item.objectclass == 'ship' ]
			
		elif keyarg == 'fleet':
			choicelist = [ item for item in objectmethods.sobject_tracker if item.objectclass == 'ship' ]
		
		else:
			raise DialogError('Unknown input: {}'.format(keyarg))		
			
		availableitems = []
		counter = 0
			
		for faction in choicelist:             							# generates the list of items
			values = (str(counter),(str(faction.name()) , faction))		# this assumes the object has a .name() method!
			counter += 1
			availableitems.append(values)
			 #(self,mode,tag,body,number = None):
			 
		self.setupScreen('grab','{}_itemPick'.format(keyarg),availableitems)
		self.screen.mode = 'grab' # redundant, but...
		picked_object = self.showScreen() # returns a value!!
		
		return picked_object
	
	def bindFaction(self,faction = None):
		"""Ties the Menu to some faction."""
		
		if faction == None:

			faction = self.itemPick('faction') 
		
		self.faction = faction 					# ties the menutree with the faction
		self.factionMenu()
	
	def factionMenu(self,options = []):
		"""Displays the menu of choices available to a faction."""
		
		factionchoicemenu = [
			# code  name   function 
			(  '1'   		,(  "_save_"		,	"savemethods.save()"		)),			
			(  '2'   		,(  "_load_"		,	"savemethods.load()"		)),			
			(  '3'   		,(  "_scores_"		,	"self.scoresScreen()"		)),			
			(  '4'   		,(  "_credits_"		,	"self.creditsScreen()"		)),			
			(  '5'   		,(  "_ingameMenu_"	,	"self.inGameMainMenu()"		)),
			(  '6'   		,(  "Back"	,	"self.Back()"		))]
		
		
		self.setupScreen('choice','faction Menu',factionchoicemenu)  #(self,mode,tag,body,number = None):
		
		self.showScreen()
		
	def inGameMainMenu(self):
		ingamemainmenu = [
			# code  name   function 
			(  '1'   		,(  "_save_"		,	"savemethods.save()"		)),			
			(  '2'   		,(  "_load_"		,	"savemethods.load()"		)),			
			(  '3'   		,(  "_scores_"		,	"self.scoresScreen()"		)),			
			(  '4'   		,(  "_credits_"		,	"self.creditsScreen()"		)),			
			(  '5'   		,(  "_ingameMenu_"	,	"self.inGameMainMenu()"		)),
			(  '6'   		,(  "Back"	,	"self.Back()"		))]
			
			
		self.setupScreen('choice','ingame Main Menu',ingamemainmenu) #(self,mode,tag,body,number = None):
		
		self.showScreen()		

	def Back(self):
		
		self.menuHistory.remove(self.screen) # clean menuhistory
		self.screen = self.screen.previousscreen
		
		if self.screen.mode == 'grab':
			print('Trying to resume a grabber optionsMenu... What was the parent doing?')
				
			print("Going back to previousmenu's previousmenu instead.")
			self.menuHistory.remove(self.screen)
			self.screen = self.screen.previousscreen
			
			if self.screen.mode == 'grab':
				print('Another grabber. Go back to the previous menu.')
				self.menuHistory.remove(self.screen)
				self.screen = self.screen.previousscreen
		
		self.showScreen()


class MenuScreen():
	
	def __init__(self,mode,tag,body,number = None):
		
		if not isinstance(mode,str) or not isinstance(tag,str) or not isinstance(body, list):
			
			raise DialogError('Bad. Interrupt. My input was: {} {} {}'.format(mode,tag,body) )
		
		currentmenu.menuHistory.append(self)
		
		self.body = body
		self.tag = tag
		self.mode = mode # modes are: choice, grab
		
		if number == None:
			if self.mode == 'grab':
				number = len(currentmenu.menuHistory)
			else:
				number = len(currentmenu.menuHistory) + 1
			
		self.number = number
		
		global currentscreen
		
		if currentscreen is None:
			self.previousscreen = self				# previous is self
		else:
			self.previousscreen = currentscreen 	# previous becomes current
			
		currentscreen = self					 	# current becomes self




