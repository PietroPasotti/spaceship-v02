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




class Screen():
	
	def __init__(self):
		
		_currentscreen_ = self
		
		self.closetoggled = False
		
		self.body = []
		self.header = []
		self.protected_body = []
		self.header2 = ""
		self.footer = ""
		#self.printer = None
		#self.printer.screen = self
	
	def close(self):
		self.closetoggled = True
		
	def setFooter(self,string):
		self.footer =  string
	
	def addToBody(self,actionslist):
		
		if isinstance(actionslist,list):
			for action in actionslist:
				if isinstance(action,Action) or isinstance(action,HyperAction):
					self.body.append(action)
		elif isinstance(actionslist,Action) or isinstance(actionslist,HyperAction): 
			self.body.append(actionslist)
		else:
			raise Exception("Something bad received.")
			
	def addToProtected(self,actionslist):
		
		if isinstance(actionslist,list):
			for action in actionslist:
				if isinstance(action,Action) or isinstance(action,HyperAction):
					self.protected_body.append(action)
		elif isinstance(actionslist,Action) or isinstance(actionslist,HyperAction): 
			self.protected_body.append(actionslist)
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
	
	def __init__(self,function=None,arguments=[],key= None,name=None,screen = None,connectedto = [],protected = False):
		
		self.key = key
		self.name = name
		self.function = function
		self.arguments = arguments
		self.connectedto = connectedto
		
		if screen != None:
			if protected == True:
				screen.addToProtected(self)
			else:
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
			
	

_currentscreen_ = Screen()
_currentfaction_ = "godmode"


class Printer():
	
	def __init__(self):
		self.mode = 'choice'
		self.screen = _currentscreen_
		self.setFaction()
		
	def setFaction(self,faction = 'godmode'):
		self.faction = faction

	def printScreen(self,screen,faction = "godmode"):
		
		header,header2,screenbody,protected_body,footer = screen.All()
		
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
		#print("       " + "-"*100)
		if header2 != "":
			printcentered(header2)
		#	print("       " + "-"*100)
	
		voicecounter = 0
		lengthcounter = 0
		lengthofmenu = len(screenbody)
		for action in screenbody:  # body is a list of actions
			
			key = action.key
			
			if key == None or type(key) == int or len(key) > 5:
				key = voicecounter
				voicecounter += 1
			
			if isinstance(key,int):
				spaces = 5 - len(str(key))
			else:
				spaces = 5 - len(key)
				
				
			todisplay = spaces*" " + "{} ".format(key) + "  >>  {} ".format(action.name)
			choicedict[key] = action # now choicedict points from counter to action
			
			
			print("       " +todisplay + "        ")
			lengthcounter +=1
		
		if protected_body != []:
			for action in protected_body: # special voices, such as 'back', which are 3-tuples	
				key = action.key
				if key in choicedict.keys():
					key = lengthcounter
					lengthcounter += 1
				name = action.name
				
				todisplay = "    {} ".format(key) + "  *>  {} ".format(name)
				choicedict[key] = action
				print("       " +todisplay)

		
			
		#print("       " + "-"*100)			
		
		if footer != "":
			printcentered(footer)
			print("       " + "-"*100)
			
		return choicedict

	def printDoubleScreen(self,faction ="godmode", screenwidth = 120):
		header,header2,screenbody,protected_body,footer = _currentscreen_.All()
			
		screenwidth = 100
		screenheight = 29
		
		halfscreen = screenwidth // 2
		quarter = halfscreen // 2
		
		divline = 30 # where the line will be drawn
		Ndivline = screenwidth - divline # what's left to the right of the divline
		
		mapdict = mapmethods.map_smart_dump_doubleview(faction) # retrieves the view for the chosen faction
		# is a tuple ((height,width),listoflines)
		height,width = mapdict[0]
		listoflines = mapdict[1]
		
		choicedict = {} # this will collect the output
		mapdict = {}
		
		counter = 3
		for line in listoflines:
			mapdict[counter] = line
			counter += 1
			
		interpredict = {}
		interpredict[0] = "-" * screenwidth											# 0
		if header not in [""," ", "  "]:											# 1
			line = header + " "*(halfscreen - len(header))
			line = line[:halfscreen] #crops the line
			interpredict[1] = line	
		interpredict[2] = "-" * screenwidth											# 2
		if header2 not in [""," ", "  "]:
			line = header2 + " "*(halfscreen - len(header2))
			line = line[:halfscreen] #crops the line
			interpredict[3] = line													# 3
		counter = 5
		choicecounter = 1
		for action in screenbody:
			if action.key == None or len(str(action.key))>3:
				key = choicecounter
				choicecounter += 1
			else:
				key = action.key
			line = " [{}]  >>  {}".format(key,action.name) 
			line = line[:halfscreen] #crops the line
			lenline = len(line)
			interpredict[counter] = line + " "*(halfscreen - lenline)
			choicedict[key] = action
			counter += 1		
		
		counter = counter +2
		for action in protected_body:
			if action.key == None or len(str(action.key))>3:
				key = choicecounter
				choicecounter += 1
			else:
				key = action.key
			line = " [[{}]]  >> {}".format(key,action.name) 
			line = line[:halfscreen] #crops the line
			lenline = len(line)
			interpredict[counter] = line + " "*(divline - lenline)
			choicedict[key] = action
			counter += 1				
		
		interpredict[len(listoflines) +3 ] = " --> " + footer
		
		####
		for i in range(1,len(listoflines)+ 4):
			blankhalf = halfscreen*" "
			sx = interpredict.get(i,blankhalf)
			dx = mapdict.get(i, blankhalf)
			print(sx + dx)
		####
		
		
		
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
	
	def __init__(self,printmode = "single"):
		
		self.looping = False
		self.printer = Printer()
		self.halted = False
	
	def setPrinter(self,printer):
		self.printer = printer
	
	def halt(self):
			
		self.halted = True
	
	def startLooping(self,printmode = "single"):
		
		
		if self.printer == None:
			raise Exception("No printer.")
		
		self.looping = True
		
		if printmode == "single":
			printfunction = Printer.printScreen
		elif printmode == "double":
			printfunction = Printer.printDoubleScreen
			
		
		while True:
			
			self.screen = _currentscreen_
			faction = _currentfaction_
			
			if isinstance(faction,factionmethods.Faction) and faction.states['faction_points'] == 0:
				nextturn = Action(factionmethods.nextTurn,[],"p","Pass Turn")
				_currentscreen_.addToProtected(nextturn)
				
			mapdict = mapmethods.map_smart_dump(faction,True)
			
			for line in mapdict[1]:
				print(line)
			
			choicedict = self.printer.printScreen(self.screen)                
			 # we always print the same screen; actions will make it change
			
			if self.halted == True:
				print("byebye")
				break										

			choice = input(" >>> :: ")
			try:
				choice = int(choice)
			except ValueError: 
				pass
				
			
			if choice in  list(choicedict.keys()): # accepted inputs are...
				mychoice = choicedict[choice]
				
				mychoice() 							# calls the output
				
			else:
				comment = random.choice(["","","","","","","","","","","","","","","","","","","","","","","",""," You sure you're human?"," You're so stupid you wouldn't pass the Turing Test."," Oh come on."," I really don't get that crap."," Oh, please..."])
				insult = random.choice(["asshole","dickhead","bitch","sucker","zombie","loser","stupid","idiot","dwarf","neo","ladyboy","paperhand","orchinicer","dummy","nigga bro"])
				footer = "Bad input, {}. Available options are {}.{} ".format(insult, list(choicedict.keys()),comment) + self.screen.footer
				self.printer.screen.footer = footer[:100] + "||"


# utilities				
activelooper = LoopInterpreter()

def haltactivelooper():
	return activelooper.halt()
			
def cantPerform(reason = ""):
	_currentscreen_.footer = "Can't perform chosen action. {}".format(reason)







