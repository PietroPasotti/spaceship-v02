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



def ActionsLoop():
	
	loops = 0
	while True:
		if currentscreen.closetriggered == True:
			
			return "Looped [{}] times.".format(loops)
		
		else:
			PRINTER.display() # returns None
			loops +=1
			

class Action():
	""" Registers an action, and all of the arguments for the action to run smooth. """
	
	def __init__(self,function=None,arguments=[],times = 1,tag = None,name = 'generic action'):
		"""
		
		tag : an optional index for the voice selector. E.g.: '1', 1, 'ab', or 'next' :: determines what the user will have to input in order to call the action
		function : the function, bound or unbound method
		name : an optional name for the action. Useful for recalling later the same action, for example. Must be unique?
		times: number of times the action is to be executed each time it is called
		arguments: all arguments which must be given to the function, once it is called.
		
		"""
		
		
		ActionsList.append(self)
			
		self.setAll(function,arguments,times,tag,name)
				
	def __call__(self):
		"""Calls the function in content with all of his arguments."""
		print("Action called, executing... ")
		numargs = len(self.arguments)
		
		function = self.function
		
		for i in range(self.itertimes):
			if numargs == 0:
				self.function()
			elif numargs == 1:
				self.function(self.arguments[0])
			elif numargs == 2:
				self.function(self.arguments[0],self.arguments[1])
			elif numargs == 3:
				self.function(self.arguments[0],self.arguments[1],self.arguments[2])
			elif numargs == 4:
				self.function(self.arguments[0],self.arguments[1],self.arguments[2],self.arguments[3])
			else:
				raise DialogError('Too many arguments to unpack.')

		return None
	
	def setAll(self,function=None,arguments=[],times = 1,tag = None,name = 'generic action'):
		self.arguments = arguments 
		self.function = function
		self.itertimes = times
		self.tag = tag 	# if present,overrides the number or index for the choice in the menu
		self.name = name
		
	def setFunction(self,function):
		self.function = function
		
	def setName(self,name):
		self.name = name

	def setTag(self,tag):
		self.tag = tag
	
	def setTimes(self,times):
		self.times = times
	
	def setArguments(self,arguments):
		if isinstance(arguments,list):
			self.arguments = arguments
		else:
			self.arguments.append(arguments)
	
	def destroy(self):
		ActionsList.remove(self)
	
	def __str__(self):
		return "<{} {}: {} --> {}.>".format(self.content,self.arguments,self.times,self.tag)



class Screen():
	
	def __init__(self):
		"""Initializes the main screen. Everything will happen in here."""
		
		self.closetriggered = False
		self.printer = PRINTER
		self.printer.screen = self
		self.clearAll()

	def Start(self):
		run = ActionsLoop()
		print("Action loop returned.")
		
		
	def Stop(self):
		self.closetriggered = True

	def clearAll(self):
		self.header = ""
		self.header2 = ""
		self.body = []
		self.protected_body = []
		self.footer = ""
		
	def body_all(self):
		return [self.header,self.header2,self.body,self.protected_body,self.footer]

	def addToBody(self,line):
		
		self.body.append(line)
	
	def addToProtected(self,line):
		
		self.protected_body.append(line)
	

class Printer():
	
	def __init__(self):
		self.screen = None
		self.mode = 'choice'
	
	@property
	def body(self):
		return self.screen.body_all()
		
	def display(self):
		"""Prints all there is to print in Screen's body, headers, protected_body and footer."""
		
		header,header2,screenbody,protected_body,footer = self.body
		
		choicedict = {}
		print("   header    " +header)
		print("       " + "-"*100)
		print("   header2    " +header2)
		voicecounter = 0
		lengthcounter = 0
		lengthofmenu = len(screenbody)
		for action in screenbody:  # body is a list of actions
			
			key = action.tag
			
			if key == None or type(key) == int or len(key) > 5:
				key = voicecounter
				voicecounter += 1
			
			todisplay = "    {} ".format(key) + " "*(( lengthofmenu - lengthcounter )//10) +  " >>  {} ".format(action.name)
			choicedict[key] = action # now choicedict points from counter to action
			print("       " +todisplay)
			lengthcounter +=1
			
		for action in protected_body: # special voices, such as 'back', which are 3-tuples
			
			key = action.tag
			if key in choicedict.keys():
				print("Warning: duplicates.")
				key = lengthcounter
				lengthcounter += 1
			
			name = action.name
			
			todisplay = "   {}  >protected>  {} ".format(key,name)
			choicedict[key] = link
			print(todisplay)
		
		print("   footer    " +footer)
		print("       " + "-"*100)
		
		choice = ""
		while True:
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
				
		chosenaction = choicedict[choice]
		if type(chosenaction) != Action:
			raise DialogError('What? Received a {}'.format(chosenlink))
		
		chosenaction() # calls the action



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
		
	def confirm(self,choice):
		if Ask(self,"bool","Confirm your choice [y/-]: {}".format(choice)):
			return True
		else:
			return False
	
PRINTER = Printer()
masterscreen = Screen()

ActionsList = []
menu_tracker = []









