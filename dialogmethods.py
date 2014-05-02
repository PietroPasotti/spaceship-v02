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

































