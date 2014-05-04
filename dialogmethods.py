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

ActionsList = []
menu_tracker = [None]


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


_currentscreen_ = None

class Screen():
	
	def __init__(self):
		
		_currentscreen_ = self
		
		self.closetoggled = False
		
		self.body = []
		self.header = []
		self.protected_body = []
		self.header2 = ""
		self.footer = ""
		self.printer = Printer()
		self.printer.screen = self
	
	def close(self):
		self.closetoggled = True
	
	def addToBody(self,actionslist):
		
		if isinstance(actionslist,list):
			for action in actionslist:
				if isinstance(action,Action) or isinstance(action,HyperAction):
					self.body.append(action)
		elif isinstance(actionslist,Action) or isinstance(actionslist,HyperAction): 
			self.body.append(actionslist)
		else:
			raise Exception("Something bad received.")
			
	def All(self):
		return (self.header,self.header2,self.body,self.protected_body,self.footer)

class Menu(Screen):
	
	def __init__(self):
		super().__init__()
		
	def setBody(self,listofactions):
		self.body = listofactions
		
	
	

class Action():
	
	def __init__(self,function=None,arguments=[],key= None,name=None,screen = None,connectedto = []):
		
		self.key = key
		self.name = name
		self.function = function
		self.arguments = arguments
		self.connectedto = connectedto
		
		if screen != None:
			screen.addToBody(self)
		
		self.screen = screen
		
	def __call__(self):
		
		result = self.function( * self.arguments)
		
		for action in self.connectedto:
			action()
		
		return result
		
	def connect(self,other):
		if isinstance(other,list):
			self.connectedto.extend(other)
		elif isinstance(other,Action):
			self.conectedto.append(other)
			
		else:
			raise Exception("Unrecognized input.")
		
		
		
class HyperAction():
	
	def __init__(self):
		super().__init__()
		
	def setFunctions(self,functions = []):
		"""Sets more than one function to run, and all have to be readable by exec."""
		if not isinstance(functions,list):
			raise Exception("Bad input.")
			
		self.functions = functions
		
	def __call__(self):
		resultslist = []
		for function in self.functions:
			if isinstance(function,str):
				result = exec(function)
			else:
				result = super().__call__(function)
				
			resultslist.append(result)
		
		return resultslist
			
	


class Printer():
	
	def __init__(self):
		self.mode = 'choice'
		self.screen = _currentscreen_
		
	def display(self,screen = None):
		"""Prints all there is to print in Screen's body, headers, protected_body and footer."""
		if screen == None:
			screen = self.screen
		else:
			self.screen = screen	

		
		choice = None
		while True: # waitforinput loop
			
			self.printScreen()
			choicedict = self.choicedict # defined by printScreen call
			
			choice = input(" >>> :: = ")
			try:
				choice = int(choice)
			except ValueError: # we try to convert it into an integer, which will be captured if the key index is given by the counter
				pass
				
			# we accept not only strings but also integers
			if choice in  list(choicedict.keys()):
				break
			else:
				insult = random.choice(["asshole","dickhead","bitch","sucker","zombie","loser","stupid","idiot","dwarf"])
				print("Bad input, {}. Available options are {}.".format(insult, list(choicedict.keys()) ))
				
		mychoice = choicedict[choice]
		
		return mychoice()

	def printScreen(self):
		
		header,header2,screenbody,protected_body,footer = self.screen.All()
		
		choicedict = {} # this will collect the output
		
		def printcentered(string):
			if string != "":
				if len(string)%2 != 0:
					string = " {}  ".format(string)
				else:
					string = " {} ".format(string)
			P = 50 - ((len(string) +1) // 2)
			print("       " + '-'*P + "{}".format(string) + '-'*P)
		
		printcentered(header)
		print("       " + "-"*100)
		if header2 != "":
			printcentered(header2)
			print("       " + "-"*100)
	
		voicecounter = 0
		lengthcounter = 0
		lengthofmenu = len(screenbody)
		for action in screenbody:  # body is a list of actions
			
			key = action.key
			
			if key == None or type(key) == int or len(key) > 5:
				key = voicecounter
				voicecounter += 1
			
			if isinstance(key,int):
				spaces = 5- len(str(key))
			else:
				spaces = 5 - len(key)
				
				
			todisplay = spaces*" " + "{} ".format(key) + "  >>  {} ".format(action.name)
			choicedict[key] = action # now choicedict points from counter to action
			
			
			print("       " +todisplay + "        ")
			lengthcounter +=1
		
		if protected_body != []:
			
			print('')
			
			for action in protected_body: # special voices, such as 'back', which are 3-tuples	
				key = action.key
				if key in choicedict.keys():
					key = lengthcounter
					lengthcounter += 1
				name = action.name
				
				todisplay = "    {} ".format(key) + "  *>  {} ".format(name)
				choicedict[key] = action
				print("       " +todisplay)

		
			
		print("       " + "-"*100)			
		
		if footer != "":
			printcentered(footer)
			print("       " + "-"*100)
			
		return choicedict

	def Ask(self,outputtype,message,availableoptions=[]):
		
		print(message)
		while True:
			choice = input(" >>> :: = ")
			
			if outputtype in ["string","str"]: # what type of output is required from Ask.
				if self.confirm(choice):
					return choice
			
			elif outputtype in ['bool','boolean']:
				
				try:
					return eval(choice) # if the choice is evaluable, returns the evaluation straightaway
				except NameError:
					pass
				
				acceptedTrueValues = "yes,y,Y,YES,Yes,YeS,yEs".split(',')
				acceptedFalseValues = "no,nO,No,N,n,NO".split(',')
				if choice in acceptedTrueValues:
					return True
				elif choice in acceptedFalseValues:
					return False
				else:
					print("Bad input. Accepted values are: {} and {}".format(acceptedTrueValues, acceptedFalseValues))
				
			#elif outputtype in ["sobject","Sobject"]:
				
				
			else:
				raise DialogError('Unrecognized outputtype. Received: {}'.format(str(outputtype)))
				
		
		return choice	
		
	
class LoopInterpreter():
	
	def __init__(self):
		
		self.screen = _currentscreen_
		self.printer = Printer()
		self.startLooping()
		
	def startLooping(self):
		self.looping = True
		
		while True:
			
			self.printer.screen = _currentscreen_
			choicedict = self.printer.printScreen()                          # will be filled in by printScreen call
			 # we always print the same screen; actions will make it change
													

			choice = input(" >>> :: = ")
			try:
				choice = int(choice)									# we accept not only strings but also integers
			except ValueError: # we try to convert it into an integer, which will be captured for example if the key index is given by the counter
				pass
				
			
			if choice in  list(choicedict.keys()): # accepted inputs are...
				mychoice = choicedict[choice]
				
				mychoice() 							# calls the output
				
			else:
				insult = random.choice(["asshole","dickhead","bitch","sucker","zombie","loser","stupid","idiot","dwarf"])
				print("Bad input, {}. Available options are {}.".format(insult, list(choicedict.keys()) ))
				
			








