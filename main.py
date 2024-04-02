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

    # A standard playing card can have 1 of 4 suits, using a numerical representation to make it easy for sorting
    SUITS = {
        'Hearts': 1,
        'Clubs': 2,
        'Diamonds': 3,
        'Spades': 4,
    }

    def __init__(self, value, suit):
        self.value = value
        
        self.points = self.POINTS_AND_RANKS[value][0]
        self.rank = self.POINTS_AND_RANKS[value][1]
        self.suit = [suit, self.SUITS[suit]]

    def __repr__(self):
        return f'{self.value} of {self.suit[0]}'

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

# class Player(bankroll):
#     def __init__(self):
#         bankroll = int(bankroll)
#         hands = [[],[],[],[]]
#         status = 'Ready'

class Hand():
    def __init__(self):
        cards = []

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

    def evaluate(hand, hand2 = [], hand3 = []):

        #We need to dictate the base hand ranks
        RANKS = {
            'rf': [['s', 'f', 'has A-10'], 1], # conditions for a royal flush
            'sf': [['s','f'], 2],  #conditions for a str8 flush
            'q': [['x','x','x','x']],
            'fh': 4,
            'f': 5,
            's': 6,
            'tok': 7,
            'tp': 8,
            'p': 9,
            'hc': 10
        }

        #Creating a temp hand for evaulation purposes
        to_evaluate = []
        #To eventually return what kind of hand the player has
        status = ''
        #We make sure to add all cards to the eval hand
        for hand in (hand, hand2, hand3):
            for card in hand:
                if card:
                    to_evaluate.append(card)
        to_evaluate.sort(key=card.rank)

        #initializing variables
        resulting_hand = []
        card_counts = {}
        suit_counts = {}
        straight_potential = False
        flush = False
        trips_count = 0
        trips = False
        quads = False
        quads_card = ''
        pair_count = 0
        two_pair = False
        full_house = False
        pair = False
        l,r,start,end = 0,4,0,4
        suit = 0
        straight_flush = False

        #getting preliminary data about the hand being evaluated
        for i in range(len(to_evaluate)):
            
            #getting ranks and positions
            if to_evaluate[i].rank in card_counts:
                card_counts[to_evaluate[i].rank][0] +=1
                card_counts[to_evaluate[i].rank][1].append(i)
            else:
                card_counts[to_evaluate[i].rank] = [1, [i]]
            
            #getting suits and positions
            if to_evaluate[i].suit[0] in suit_counts:
                suit_counts[to_evaluate[i].suit[0]][0] +=1
                suit_counts[to_evaluate[i].suit[0]][1].append(i)
            else:
                suit_counts[to_evaluate[i].suit[0]] = [1, [i]]
            
            if to_evaluate[i].rank == 10 or to_evaluate[i].rank == 5:
                straight_potential = True

        #checking to see if there's a flush in the hand
        for suit,number in suit_counts:
            if number > 4:
                flush = True

        #checking to see what hands are possible based on card counts
        for card,value in card_counts:
            if value == 4:
                quads = True
                quads_card = card
                break
            elif value == 3:
                trips = True
                trips_count +=1
            elif value == 2:
                pair = True
                pair_count +=1
            
        if (trips and pair) or trips_count > 1:
            full_house = True
        elif pair_count > 1:
            two_pair = True
        
        if quads:
            if quads_card == to_evaluate[0].rank:
                resulting_hand = to_evaluate[0:4]
            else:
                resulting_hand = to_evaluate[card_counts[quads_card][1][0]:card_counts[quads_card][1][3]] + to_evaluate[0]
            return resulting_hand
        
        if full_house:
            if trips_count > 1:
                for card,value in card_counts:
                    if value[0] == 3 and resulting_hand == []:
                        resulting_hand = to_evaluate[card_counts[card][1][0]:card_counts[card][1][2]]
                    elif value[0] == 3:
                        resulting_hand += to_evaluate[card_counts[card][1][0]:card_counts[card][1][1]]
            else:
                temp_hand = []
                for card,value in card_counts:
                    if value[0] == 3:
                        resulting_hand = to_evaluate[card_counts[card][1][0]:card_counts[card][1][2]]
                    if value[0] == 2 and temp_hand == []:
                        temp_hand = to_evaluate[card_counts[card][1][0]:card_counts[card][1][1]]
                resulting_hand += temp_hand
            return resulting_hand


        #check 1: checking for a straight flush (not worrying about 5-1 just yet):
        while (resulting_hand != [] and flush and straight_potential):

            #this loop doesn't need to complete if the current hand being evaluated is just the player's hole cards
            #or if the sliding window makes the resulting hand less than 5 cards
            #reset the pointers and break out of the loop
            if (len(to_evaluate) == 2) or (l == 3):
                l,r,start,end = 0,4,0,4
                break

            #based on the current iteration of the sliding window, we check the endpoints 
            #to see if they are 4 ranks apart and the same suit
            if (to_evaluate[start].rank == to_evaluate[end].rank - 4) and (to_evaluate[start].suit[1] == to_evaluate[end].suit[1]):
                suit = to_evaluate[start].suit[1]
                start += 1
                end -=1
                if (to_evaluate[start].rank == to_evaluate[end].rank - 2) and (to_evaluate[start].suit[1] == to_evaluate[end].suit[1]) and (suit == to_evaluate[start].suit[1]):
                    if (to_evaluate[start].rank == to_evaluate[start+1].rank - 1) and (to_evaluate[start].suit[1] == to_evaluate[start+1].suit[1]) and (suit == to_evaluate[start+1].suit[1]):
                        resulting_hand = to_evaluate[l:r]
                        straight_flush = True
                        return resulting_hand

                    #at this point, we know that there can't be a straight flush due to the 3rd card in the 7 card hand either being of a different suit or the isn't a connector the card after it
                    #we can exit this while loop
                    else:
                        l,r,start,end = 0,4,0,4
                        break
                else:
                    l += 1
                    start = l
                    r += 1
                    end = r
            #move the sliding and reset the pointers
            else:
                l += 1
                start = l
                r += 1
                end = r
        
        #At this point, if there isn't a straight flush, but there is a flush that is the best hand
        if flush:
            for suit, number in suit_counts:
                if number[0] > 4:
                    resulting_hand = to_evaluate[suit_counts[suit][1][0]] + to_evaluate[suit_counts[suit][1][1]] + to_evaluate[suit_counts[suit][1][2]] + to_evaluate[suit_counts[suit][1][3]] + to_evaluate[suit_counts[suit][1][4]]
            return resulting_hand


        # OLD QUADS CODE
        # l,r,start,end = 0,4,0,1
        # quads_flag = False
        # #check 2: quads
        # while (resulting_hand != []):

        #     #this loop doesn't need to complete if the current hand being evaluated is just the player's hole cards
        #     #or if the sliding window makes the resulting hand can't have quads because it's only 3 cards left
        #     #reset the pointers and break out of the loop
        #     if (len(to_evaluate) == 2) or (l == 4):
        #         l,r,start,end = 0,4,0,4
        #         break

        #     if to_evaluate[start].rank == to_evaluate[end].rank:
        #         end += 1
        #         if to_evaluate[start].rank == to_evaluate[end].rank:
        #             end += 1
        #             if to_evaluate[start].rank == to_evaluate[end].rank:
        #                 if l == 0: #if the quads are the highest cards in the hand
        #                     resulting_hand = to_evaluate[l,r]
        #                     quads_flag = True
        #                 else: #if not, we need to include the highest card as the kicker
        #                     resulting_hand = to_evaluate[start,end] + to_evaluate[0]
        #                     quads_flag = True
        #                 break
        #     else:
        #         l +=1
        #         start = l
        #         end = l+1
        #         if (r < 6):
        #             r +=1
        #         else:
        #             r = 6

        # l,r,start,end = 0,4,0,1
        
            


                        

            
                

        
            

            
            

            
            

        return status

    flop = Hand()
    river = Hand()

    #function from the deck class, 
    #that is going to deal to X cards to Y hand
    deck.deal(3, flop) #hidden
    deck.deal(2, river)
    deck.deal(2, player.hand) #shown
    deck.deal(2, dealer.hand) #hidden

    #stage one
    display(player.hand)
    evaluate(player.hand)
    check_or_bet(3, 4, player.bankroll) #function will be (min, max, bankroll)

    #stage two
    display(flop)
    display(player.hand)
    evaluate(player.hand, flop)
    check_or_bet(2, 2, player.bankroll)

    #stage three
    display(flop, river)
    display(player.hand)
    evaluate(player.hand, flop, river) 
    check_or_bet(1, 1, player.bankroll, player.status) #here, we evaulate if the player folds or not

    #stage four
    display(dealer.hand)
    display(flop, river)
    if(player.status == 'ready'):
        evaluate(dealer.hand, flop, river)

        #player wins
        if (compare_hands(player.hand, dealer.hand) == 'player'):
            #pay player appropriately
            pass

        #dealer wins
        elif (compare_hands(player.hand, dealer.hand) == 'dealer'):
            #take money appropriately
            pass
        
        #push
        else:
            #take trips if need be
            pass

    #This means that the player folded during stage 3
    #Take bets and subtract from bankroll
    else:
        pass

    player.display_hand()
    

    

player = Player(1500)
    


uth(15)
# print('This is a test')
# deck = Deck()
# card = deck.cards.pop()
# # print(card.rank)
# print(card, ", and has a rank of ", card.rank, sep='')