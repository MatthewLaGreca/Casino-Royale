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
    
    # the function to deal an individual card
    def deal(self):
        return self.cards.pop(-1)

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
        
def wager_prompt(bet_name, table_min, table_max, bonus = False):
    if bonus:
        return int(input(f"How much would you like to put on the {bet_name}? $0 to ${table_max} (must be increments of $5): "))
    else:
        return int(input(f"How much would you like to put on the {bet_name}? ${table_min} to ${table_max}: "))  

# Condensed both wager validation functions into one
    
# def valid_wager(bet_name, wager, table_min, table_max):
#     while (wager < table_min) or (wager > table_max):
#         if wager < table_min:
#             print(f'You can not bet less than the table minimum of ${table_min}')
#             wager = wager_prompt(bet_name, table_max, table_max)
#         elif wager > table_max:
#             print(f'You can not bet more than the table maximum of ${table_max}')
#             wager = wager_prompt(bet_name, table_max, table_max)
#     return wager

# def valid_side(bet_name, wager, table_max):
#     while (wager < 0) or (wager > table_max) or (wager % 5 != 0):
#         if wager < 0:
#             print(f'You can not bet less than $0')
#             wager = wager_prompt(bet_name, table_max, True)
#         elif wager > table_max:
#             print(f'You can not bet more than the {bet_name} maximum of ${table_max}')
#             wager = wager_prompt('Trips', 100, 0, True)
#         elif wager % 5 != 0:
#             print(f'Your {bet_name} bet has to be an increment of $5')
#             wager = wager_prompt('Trips', 100, 0, True)
#     return wager
       
def valid_wager(bet_name, wager, table_min, table_max, bonus = False):
    while (wager < table_min) or (wager > table_max) or ((wager % 5 != 0) and (bonus == True)):
        if wager < table_min:
            print(f'You can not bet less than the table minimum of ${table_min}')
            wager = wager_prompt(bet_name, table_min, table_max, bonus)
        elif wager > table_max:
            print(f'You can not bet more than the table maximum of ${table_max}')
            wager = wager_prompt(bet_name, table_min, table_max, bonus)
        elif wager % 5 != 0:
            print(f'Your {bet_name} bet has to be an increment of $5')
            wager = wager_prompt(bet_name, table_max, table_max, bonus)
    return wager

def playing_bonus(bonus_name):
    decision = input(f"Would you like to play {bonus_name}? (Yes/No): ") #Still needs to be programmed for error handling
    if decision:
        bonus_wager = wager_prompt(bonus_name, 0, 100, True)
        confirmed_bonus = valid_wager(bonus_name, bonus_wager, 0, 100, True)
        print(f'You decide to place ${confirmed_bonus} on {bonus_name}')
        return confirmed_bonus
    else:
        print(f'You decide to forego playing {bonus_name}')
        return 0

#The portion of the program that is Ultimate Texas Hold Em     
def uth(table_min):

    deck = Deck()
    main_bet = 'Ante'
    side_bet = 'Trips'
    final_bet = 'Raise'

    #Only want to display this message if changing from another casino game to UTH, or starting up playing UTH
    # if not player.currently_playing:
    #     print('You approach a table of familiar faces, only to be greeted with a table minimum of $', table_min, ' and a table max of $100\n')
    #     print('Debbie: "Hey there, hun!  Stay a while and make your self comfortable!"')

    #Getting the Ante and Blind from the player
    wager = wager_prompt(main_bet, table_min, 100)
    confirmed_wager = valid_wager(main_bet, wager, table_min, 100)
    print("You put $", confirmed_wager, " on the Ante and the Blind, placing a total wager of $", 2*confirmed_wager, sep='')

    #Getting the Trips side bet from the player
    side_wager = playing_bonus(side_bet)

    #Wagers are placed, we now deal the cards
    print('Best of luck to you!')
    


uth(15)
# print('This is a test')
# deck = Deck()
# card = deck.cards.pop()
# # print(card.rank)
# print(card, ", and has a rank of ", card.rank, sep='')