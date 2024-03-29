from random import shuffle, randint
from time import sleep

class Card():
    """An individual playing card"""

    # Each card is worth a static amount of points, besides an Ace
    POINTS_AND_RANKS = {

        # Each card is worth a static amount of points, besides an Ace
        # Format is "'Card type': [value, rank]"
        'Ace' : [11,1], # Ace can either count as a 1 or an 11 in BJ; for Poker is it the highest card unless it's part of a low straight
        '2' : [2,13],
        '3' : [3,12],
        '4' : [4,11],
        '5' : [5,10],
        '6' : [6,9],
        '7' : [7,8],
        '8' : [8,7],
        '9' : [9,6],
        '10' : [10,5],
        'Jack' : [10,4],
        'Queen' : [10,3],
        'King' : [10,2],

    }

    # A standard playing card can have 1 of 4 suits
    SUITS = ['Spades', 'Clubs', 'Diamonds', 'Hearts']

    def __init__(self, value, suit):
        self.value = value
        
        self.points = self.POINTS_AND_RANKS[value][0]
        self.rank = self.POINTS_AND_RANKS[value][1]
        self.suit = suit

    def __repr__(self):
        return f'{self.value} of {self.suit}'

class Deck():

    def __init__(self) -> None:
        self.cards = []
        self.generate_deck()
        self.shuffle_deck()

    def generate_deck(self):
        for value in Card.POINTS_AND_RANKS:
            for suit in Card.SUITS:
                self.cards.append(Card(value, suit))

    def shuffle_deck(self):
        shuffle(self.cards)

# Poker Hand Ranks
# Royal Flush: A straight from Ace to 10, all of the same suit
# Straight Flush: A straight, all of the same suit, that isn't Ace to 10
# Quads: 4 cards of the same type, with a 5th card as the kicker (IE: AAAAK)
# Full House: 3 cards of the same type plus 2 cards of the same type of a different type than the first three (AAAKK)
# Flush: 5 cards of the same suit that are not in sequential order (13579 of spades)
# Straight: 5 cards in sequential order that are not of the same suit (12345 of varying suits)
# Trips: 3 cards of the same type, with the other two being different from the 3 of the same and each other (AAAKQ)
# Pair: 2 cards of the same type, with the other three being different from the 2 of the same and each other (AAKQJ)
# High Card: 5 cards that aren't of the same suit, sequential order and there are no dupes (AKQJ9)


#The portion of the program that is Ultimate Texas Hold Em     
def uth():


# print('This is a test')
# deck = Deck()
# card = deck.cards.pop()
# # print(card.rank)
# print(card, ", and has a rank of ", card.rank, sep='')