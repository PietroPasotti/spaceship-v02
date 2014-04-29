#namegenmethods

import random

normal_adjectives = """Cold Hot Grievous Grand Big Shiny Silent Noisy Sparkling Little Tiny Shady Mysterious Feminine Masculine Childish Poor 
Red Black White Yellow Blue Azure Emerald Coral Green Orange Purple Cyan Magenta""".split(' ')

tamarr_adjectives = """Brutalized Inspired Gorgeous Superb Zenital Mindblowing Mindfucking""".split(' ')

philosophical_adjectives = """Wittgensteinian Nietzschean Hegelian Marxian Leninian Communist Atheistic Religious""".split(' ')

common_nouns = """Bed Sword House Glass Word Sentence Poem Crop Field Plant Grass Leaf Tree Vase Cushion Pillow Napkin Newspaper Tabloid Character 
Duvet Sun Moon Star Ceiling Floor Constellation Letter Postcard Blossom Sky Ocean Land Earth Ground Hill Heart Pancreas Colon Brain Skull Wallpaper 
Plane Wing Gull Feather Father Mother Sister Daughter Son Uncle Nephew Niece Barbarian Warrior Druid""".split(' ')

philosophical_nouns = """Ludwig Karl Friedrich Gustav August Austin Schiller John-Stuart Abelard JohnBuridan SaintThomas Plato Socrates Aristoteles""".split(' ')

animal_nouns = """Gorilla Lion Zebra Tiger Cat Dog Cheetah Eagle Sparrow Whale Dolphin Human Alien SeaLion Seal Fish Horse Donkey Mule Camel""".split(' ')

def namegen(kwarg=None):
	
	name = ''
	
	if kwarg == None or kwarg == 'n':  # any disposable name, including ships
		pass
	elif kwarg == 'a': # an asteroid
		for i in range(8):
			name = name + random.choice(list('0123456789'))
		return name
	elif kwarg == 'f': # a fleet
		num = random.random() 
		if num > 0.8:
			randigits = random.choice(list('0123456789')) + random.choice(list('0123456789')) + random.choice(list('0123456789'))
			name = random.choice(tamarr_adjectives) + random.choice(common_nouns) + '_' + randigits
		elif num > 0.6:
			name = random.choice(philosophical_adjectives) + random.choice(tamarr_adjectives) + random.choice(common_nouns)
		elif num > 0.4:
			name = 'The'+random.choice(animal_nouns)+'s'
		elif num > 0.2:
			name = 'A'+random.choice(tamarr_adjectives)+random.choice(animal_nouns)
		else:
			name = random.choice(common_nouns)+'s' + 'Of' + random.choice(philosophical_nouns)
	elif kwarg == 'b': # a building
		return 'Building_name' # the building's name will be the building buildingclass, plus maybe a code derived from the asteroid?
	else:
		pass
	
	num = random.random()
	
	code = ''
	for i in range(random.choice([3,4,5])):
		code = code + random.choice(list('0123456789'))
	
	if num > 0.5:
		name = random.choice(normal_adjectives) + random.choice(common_nouns) + '_' + code
	else:
		name = code + '_' + random.choice(normal_adjectives) + random.choice(common_nouns)
	
	return str(name)




