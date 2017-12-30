import random

SHAPE_OVAL = 0
SHAPE_DIAMOND = 1
SHAPE_S = 2

COLOR_GREEN = 0
COLOR_RED = 1
COLOR_PURPLE = 2

NUMBER_ONE = 0
NUMBER_TWO = 1
NUMBER_THREE = 2

SHADE_EMPTY = 0
SHADE_SHADED = 1
SHADE_SOLID = 2

SHAPES = { SHAPE_OVAL : "Oval", SHAPE_DIAMOND : "Diamond", SHAPE_S : "Squiggle" }
COLORS = { COLOR_GREEN : "Green", COLOR_RED : "Red", COLOR_PURPLE : "Purple" }
NUMBERS = { NUMBER_ONE : "One", NUMBER_TWO : "Two", NUMBER_THREE : "Three" }
SHADES = { SHADE_EMPTY : "Empty", SHADE_SHADED : "Shaded", SHADE_SOLID : "Solid" }

class Card:

	def __init__(self, shape, number, color, shade):
		self.shape = shape
		self.number = number
		self.color = color
		self.shade = shade

	def key(self):
		return (self.shape, self.number, self.color, self.shade)

	def __eq__(x, y):
		return x.key() == y.key()

	def __hash__(self):
		return hash(self.key())

	def __repr__(self):
		return NUMBERS[self.number] + " " + SHADES[self.shade] + " " \
			+ COLORS[self.color] + " " + SHAPES[self.shape] 

class Deck:

	def __init__(self):
		self.deck = []

		for shape in SHAPES:
			for color in COLORS:
				for number in NUMBERS:
					for shade in SHADES:
						self.deck.append(Card(shape, number, color, shade))

	def nextThree(self):
		three = []

		for i in range(0, 3):
			tmpIdx = random.randrange(0, len(self.deck))
			three.append(self.deck[tmpIdx])
			self.deck.remove(self.deck[tmpIdx])

		return three

	def empty(self):
		return len(self.deck) == 0