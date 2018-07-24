from cards import *
import time
import sys
from itertools import combinations

def validateSet(card1, card2, card3):
	"""
	Three cards qualify as a set if and only if, for every trait, they are
	either all different, or all the same. Since trait variants are encoded
	as the values 0, 1, and 2; in this case, the sum of the variant codes
	will be evenly divisible by 3 if and only if they are all the same
	or all different. 
	"""
	return (card1.shape + card2.shape + card3.shape) % 3 == 0 and \
		(card1.number + card2.number + card3.number) % 3 == 0 and \
		(card1.color + card2.color + card3.color) % 3 == 0 and \
		(card1.shade + card2.shade + card3.shade) % 3 == 0

def completeSet(card1, card2):
	"""
	If card1 and card2 are the same for a given trait, set the same value for that trait.
	If card1 and card2 are different for a given trait, set 3 - the sum of card1 and card2 for 
	that trait, since the sum of a set for a given trait must always be evenly
	divisible by 3.
	"""
	return Card(card1.shape if card1.shape == card2.shape else (3 - (card1.shape + card2.shape)), 
		card1.number if card1.number == card2.number else (3 - (card1.number + card2.number)), 
		card1.color if card1.color == card2.color else (3 - (card1.color + card2.color)), 
		card1.shade if card1.shade == card2.shade else (3 - (card1.shade + card2.shade)))

def findSet(cards):
	"""
	Brute force algorithm: 
	Iterate over all possible combinations of three cards and check 
	each combination of three for validity until we find a set.
	"""
	for potentialSet in combinations(cards, 3):
		if validateSet(potentialSet[0], potentialSet[1], potentialSet[2]):
			cards.remove(potentialSet[0])
			cards.remove(potentialSet[1])
			cards.remove(potentialSet[2])
			return (cards, True)

	return (cards, False)

def findSetFast(cards):
	"""
	Better algorithm:
	Iterate over all possible pairs of cards, and for each pair
	construct the card that would complete the set. Check if that card
	exists in cards, if so, we've found a set. 
	"""

	# compare every two cards
	for pair in combinations(cards, 2):
		# construct the card that would make a set
		card3 = completeSet(pair[0], pair[1])

		# check if that card is present
		if card3 in cards:
			cards.remove(pair[0])
			cards.remove(pair[1])
			cards.remove(card3)
			return (cards, True)
	
	return (cards, False)

def findSetFaster(cards):
	"""
	Even better algorithm:
	Check pairs for cards like findSetFast, but don't check every 
	possible pair combination -- skip anything unnecessary or redundant.
	
	1. At the start, sort cards into buckets by trait -- here we sort by number.

	2. Select the two least common variants of the trait, and check all pairs
	between those two variants for possible sets.

	3. If we have not found a set where the cards are all different for our chosen trait,
	check among each trait variant for sets where that trait are the same. 
	Skip redundant comparisons. (e.g. no need to check the last two cards of a givemvariant, since we
	will have already exhausted all possible sets within the variant before we get there.)

	NOTE: Here we arbitrarily use number to sort with every time. In order to more optimally 
	look for sets, at the start sort for EVERY trait and then choose the best trait to continue 
	with. (best trait == trait with the least common variant). However, this would have tradeoffs, 
	because it would require more overhead in time and space.  
	"""

	# sort into buckets by trait
	# TODO: sort for EVERY trait and then choose the best
	numbers = [[], [], []]

	for c in cards:
		numbers[c.number].append(c)

	# sort buckets by size
	numbers.sort(key=lambda x: len(x))

	for card1 in numbers[0]:
		for card2 in numbers[1]:
			# construct the card that would make a set
			card3 = completeSet(card1, card2)

			# check if that card is present
			if card3 in cards:
				cards.remove(card1)
				cards.remove(card2)
				cards.remove(card3)
				return (cards, True)

	for numberSet in numbers:
		for pair in combinations(numberSet, 2):
			# construct the card that would make a set
			card3 = completeSet(pair[0], pair[1])

			# check if that card is present
			if card3 in cards:
				cards.remove(pair[0])
				cards.remove(pair[1])
				cards.remove(card3)
				return (cards, True)

	return (cards, False)

def playSet(findSet):
	d = Deck()

	active = set(d.nextThree() + d.nextThree() + d.nextThree() + d.nextThree())

	while True:
		state = findSet(active)
		active = state[0]
		if not d.empty():
			active = active.union(set(d.nextThree()))
		elif not state[1]:
			# if the deck is empty and there are no more sets, break
			return

def main():

	numIterations = 10

	if (len(sys.argv) == 2):
		numIterations = int(sys.argv[1])

	start = time.time()
	
	for i in range(0, numIterations):
		playSet(findSet)
	
	mid1 = time.time()

	for i in range(0, numIterations):
		playSet(findSetFast)

	mid2 = time.time()

	for i in range(0, numIterations):
		playSet(findSetFaster)

	end = time.time()

	print("***FIND SETS***")
	print("Time: {}".format(mid1 - start))

	print("***FIND SETS FAST***")
	print("Time: {}".format(mid2 - mid1))

	print("***FIND SETS FASTER***")
	print("Time: {}".format(end - mid2))

if __name__ == '__main__':
	main()