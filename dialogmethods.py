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



class ActionsLoop():
	
	def __init__(self,screen):
		self.screen = screen
			
	def StartLooping(self):
		screen = self.screen
		retrievedvalues = None
		while True:
			if screen.closetriggered == True:
				return retrievedvalues
			else:
				retrievedvalues = PRINTER.display(_currentscreen_)
				

mainloop = None

	
class Action():
	""" Registers an action, and all of the arguments for the action to run smooth. """


## FUNDAMENTALS	
	def __init__(self,function=None,arguments=[],itertimes = 1,tag = None,name = 'generic action',screen = None):
		"""
		
		tag : an optional index for the voice selector. E.g.: '1', 1, 'ab', or 'next' :: determines what the user will have to input in order to call the action
		function : the function, bound or unbound method
		name : an optional name for the action. Useful for recalling later the same action, for example. Must be unique?
		times: number of times the action is to be executed each time it is called
		arguments: all arguments which must be given to the function, once it is called.
		
		"""
		
		ActionsList.append(self)
		
		self.outoffocus_actionstotrigger = []
		self.pointer = " << "
		self.focused = False
		self.connectedto = []
		self.setAll(function,arguments,itertimes,tag,name,screen)
				
	def __call__(self):
		"""Calls the function in content with all of his arguments."""
			
		returnvalue = self.function( * self.arguments)
		
		if self.connectedto != []:
			returnvalue = [returnvalue]
			for function_or_action in self.connectedto:
				returnother = function_or_action() # calls also what's connected to!
				returnvalue.append(returnother)
				
		return returnvalue
	
	def __str__(self):
		return "<{} {} {}: {} --> {}.>".format(self.itertimes,self.tag,self.name,str(self.function),str(self.arguments))

	def connect(self,action_or_function):
		self.connectedto.append(action_or_function)

	def dumpTo(self,where,what):
		where = what
	
	
## SETTERS	
	def setAll(self,function=None,arguments=[],itertimes = 1,tag = None,name = 'generic action',screen=None):
		self.arguments = arguments 
		self.function = function
		self.tag = tag 	# if present,overrides the number or index for the choice in the menu
		self.name = name
		
		if itertimes == None:
			self.itertimes = 1
		else:
			self.itertimes = itertimes
		
		if screen != None and function == Screen.Stop:
			screen.addToProtected(self)
		
		elif screen != None:
			screen.addToBody(self)
			
	def setFunction(self,function):
		self.function = function
		
	def setName(self,name):
		self.name = name

	def setTag(self,tag):
		self.tag = tag
	
	def setTimes(self,times):
		self.itertimes = times
	
	def setArguments(self,arguments):
		if isinstance(arguments,list):
			self.arguments = arguments
		else:
			self.arguments.append(arguments)

	def setPointer(self,string):
		self.pointer = string
	
	def unfocus(self):
		self.focused = False
		self.outoffocus_trigger()
	
	def focus(self):			
		self.focused = True
		
		print("Now {} is focused: {}".format(self.name, self.focused))

	def outoffocus_settriggers(self,actionlist):
		if isinstance(actionlist,list):
			if self.outoffocus_actionstotrigger == []:
				
				self.outoffocus_actionstotrigger = [action]
			else:
				self.outoffocus_actionstotrigger.extend(actionlist)
		else:
			self.outoffocus_actionstotrigger.append(actionlist)
						
	def outoffocus_trigger(self):
		for action in self.outoffocus_actionstotrigger:
			action()

			
## UTILITIES
	def destroy(self):
		ActionsList.remove(self)



class Condition():
	
	def __init__(self,name="condition",checklist = [],screen = None):
		self.name = name
		self.setScreen(screen)
		self.checklist = checklist
		self.isfulfilled = self.checkFulfilment()
		
	def setScreen(self,screen):
		self.screen = screen
		
	def setName(self,name):
		if isinstance(name,str):
			self.name = name
		else:
			raise Exception("What?")
			
	def setCheckList(self,checklist):
		if self.checklist is None:
			checklist = self.checklist
		else:
			if isinstance(checklist,list):
				self.checklist.extend(checklist)
			else:
				self.checklist.append(checklist)
	
	def checkFulfilment(self):
		fulfilled = True
		for tocheck in self.checklist:
			if isinstance(tocheck,bool) and tocheck is False:
				fulfilled = False
			if isinstance(tocheck,Condition) and tocheck() == False:
				fulfilled = False
			try:
				if tocheck() == False:
					fulfilled = False	
			except TypeError:
				pass
					
			try:
				if tocheck == False:
					fulfilled = False	
			except TypeError:
				pass
				
		self.isfulfilled = fulfilled
		return fulfilled
		
	def __call__(self):
		
		self.checkFulfilment()
		
		if self.isfulfilled:
			return True
		else:
			return False


_currentscreen_ = None

class Screen():
	
	def __init__(self,fulloptions = None):
		"""Initializes the main screen. Everything will happen in here."""
		
		global menu_tracker
		self.parentscreen = menu_tracker[len(menu_tracker)-1] # by default, the parent screen is the previously instantiated screen.
		
		if menu_tracker == [None]:
			menu_tracker = [self]
			
		menu_tracker.append(self)
		
		_currentscreen_ = self
		
		self.onsatisfied = []
		self.satisfied = None
		self.conditions = []
		self.closetriggered = False
		self.printer = PRINTER
		self.printer.screen = self
		self.clearAll()
		
		if fulloptions != None and len(fulloptions) == 5: 
			header,header2,body,protected_body,footer = fulloptions
			self.setAll( header,header2,body,protected_body,footer ) 				#setAll(self,header,header2,body,protected_body,footer)
			self.Start()
	
	def Back(self):
		"""Sends you to the previous screen. If there is none, this will raise an exception."""
		if self.checkConditions() == True:
			pass
		else:
			return None
			
		self.parentscreen.Start()
		self.closetriggered = True #actionsloop returns
		
	def setParent(self,parent):
		"""The screen which, when self gets terminated, is reloaded and inited."""
		self.parentscreen = parent


## LOOPING
	def waitForInput(self):
		#if _currentscreen_ is self:
		return self.printer.display()

	def Start(self):
		
		_currentscreen_ = self
		self.closetriggered == False
		
		#if self.parentscreen is not None:
		#	if self.parentscreen.closetriggered == False:
				#print("WARNING! My parent is still running underground. Halting it...")
		#		self.parentscreen.Stop()
		#		pass
				
		self.printer.screen = self
		
		global mainloop
		if mainloop == None:
			mainloop = ActionsLoop(self)
			mainloop.StartLooping()
	
	def Stop(self):
		
		if self.checkConditions() == True:
			self.closetriggered = True
		else:
			print("No. Not all actions have been performed correctly.")


## FOCUS

	def setFocus(self,action):
		for anyaction in self.body:
			anyaction.unfocus()
			
		action.focus()

## BODY	

	def setAll(self,header,header2,body,protected_body,footer):
		self.header = header
		self.header2 = header2
		self.body = body
		self.protected_body = protected_body
		self.footer = footer		
	
	def clearAll(self):
		self.header = ""
		self.header2 = ""
		self.body = []
		self.protected_body = []
		self.footer = ""
		
	def body_all(self):
		return [self.header,self.header2,self.body,self.protected_body,self.footer]

	def addToBody(self,action):
		if action in self.body:
			pass
		else:
			self.body.append(action)
	
	def removeFromBody(self,action):
		if action in self.body:
			self.body.remove(action)
		if action in self.protected_body:
			self.protected_body.remove(action)
		
	def addToProtected(self,action):
		if action in self.protected_body:
			pass
		else:
			self.protected_body.append(action)

	def setProtected(self,what):
		if isinstance(what,list):
			self.protected = what
		else:
			raise Exception("List expected")

	def addBack(self):
		back = Action(self.Back, [],1,"b",'Back')
		self.addToProtected(back)
		return back

	def addStop(self):
		stop = Action(self.Stop, [],1,"s",'Stop')
		self.addToProtected(stop)
		return stop		
	
	def satisfy(self):
		self.satisfied = True
		self.onsatisfied_trigger()
	
	def onsatisfied_trigger(self):
		if self.onsatisfied == []:
			pass
		else:
			self.onsatisfied() 
	
	def onsatisfied_connect(self,action):
		self.onsatisfied = action
	
		
## CONDITIONS

	def setCondition(self,condition):
		if isinstance(condition,Condition):
			if condition not in self.conditions:
				self.conditions.append(condition)
		else:
			raise Exception("Unknown input for setCondition")
			
	def checkConditions(self):
		accept = False
		
		unfulfilled = [ condition.name  for condition in self.conditions if condition() == False]
		
		if unfulfilled == []:
			self.satisfy()
			return True
		else:
			self.satisfied = False
			self.footer = "Unfulfilled conditions: {}".format(unfulfilled)
			return False


class Printer():
	
	def __init__(self):
		self.screen = None
		self.mode = 'choice'
	
	def body(self):
		return self.screen.body_all()
		
	def display(self,screen = None):
		"""Prints all there is to print in Screen's body, headers, protected_body and footer."""
		if screen == None:
			screen = self.screen
		else:
			self.screen = screen	

		
		choice = ""
		while True:
			
			
			self.printScreen(screen)
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
				
		chosenaction = choicedict[choice]
		if type(chosenaction) != Action:
			raise DialogError('What? Received a {}'.format(chosenaction))
		
		return chosenaction() #calls the action

	def printScreen(self,screen):
		
		# new screen for the printer!
		
		header,header2,screenbody,protected_body,footer = self.body()
		
		choicedict = {}
		self.choicedict = {}
		
		def printcentered(string):
			if string != "":
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
			
			key = action.tag
			
			if key == None or type(key) == int or len(key) > 5:
				key = voicecounter
				voicecounter += 1
			
			todisplay = "    {} ".format(key) + "  >>  {} ".format(action.name)
			choicedict[key] = action # now choicedict points from counter to action
			
			pointer = ""
			if action.focused == True:
				#print("Action {} is now focused {}, and pointer is {}".format(action.name,action.focused,action.pointer))
				pointer = action.pointer + "#"
			
			print("       " +todisplay + "        {}".format(pointer))
			lengthcounter +=1
		
		if protected_body != []:
			
			print('')
			
			for action in protected_body: # special voices, such as 'back', which are 3-tuples	
				key = action.tag
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
				
		self.choicedict = choicedict

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
		if self.Ask("bool","Confirm your choice [y/-]: {}".format(str(choice))):
			return True
		else:
			return False
	
PRINTER = Printer()
masterscreen = Screen()











