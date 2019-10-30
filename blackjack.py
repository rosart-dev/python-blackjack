import random
import functools

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')

ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven',
 		'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')

values ={'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6,
		 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

playing = True

# Card Class 

class Card(): 
	
	def __init__(self, suit, rank):
		self.suit = suit
		self.rank = rank

	def __str__(self):
		return (f'{self.rank} of {self.suit} \n')

# Deck Class

class Deck(): 

	def __init__(self):
		self.deck = []
		for suit in suits:
			for rank in ranks:
				self.deck.append(Card(suit, rank))

	def __str__(self):
		deck_str = ""
		for card in self.deck:
			deck_str += card.__str__
		return deck_str

	def shuffle(self):
		random.shuffle(self.deck)

	def deal(self):
		return self.deck.pop()

# Hand Class

class Hand():
	def __init__(self):
		self.cards = [] #empty list
		self.value = 0 # zero value
		self.aces = 0 # keep track of aces

	def add_card(self, card):
		self.cards.append(card)
		self.value += values[card.rank]
		if card.rank == 'Ace':
			self.aces += 1

	def adjust_for_ace(self):
		#Only adjust when value is greater than 21
		#and there is atleast one ace 
		#0 is a falsey value
		while self.value > 21 and self.aces:
			self.value -= 10
			self.aces -= 1


# Chips Class

class Chips():
	def __init__(self, total = 100):
		self.total = total
		self.bet = 0

	def win_bet(self):
		self.total += self.bet

	def lose_bet(self):
		self.total -= self.bet

# Functions 

def take_bet(chips):
	while True:
		try:
			chips.bet = int(input("How many chips do you want to bet?"))
		except:
			print("Please provide a number")
		else:
			if chips.bet > chips.total:
				print(f'Sorry, you do not have enough chips! You have {chips.total} chips')
			else:
				break

def hit(deck, hand):
	card = deck.deal()
	hand.add_card(card)
	hand.adjust_for_ace()

def hit_or_stand(deck, hand):
	global playing

	while True: 
		choice = input("Hit Or Stand?").lower()

		if choice == 'hit':
			hit(deck,hand)

		elif choice == 'stand':
			print("Player Stands Dealer's Turn")
			playing = False

		else:
			print('Sorry, I did not understand that')
			continue

		break

def show_some(player, dealer):
	print("Dealer's hand:")
	print(dealer.cards[1])
	print('\n')

	print("Player's hand:")
	for card in player.cards:
		print(card)

def show_all(player, dealer):
	print("Dealer's hand:")
	for card in dealer.cards:
		print(card)
	print('\n')
	print("Player's hand:")
	for card in player.cards:
		print(card)


def player_busts(chips):
	print('Player busted!')
	chips.lose_bet()

def player_wins(chips):
    print('Player won!')
    chips.win_bet()

def dealer_busts(chips):
    print('Dealer busted! Player won!')
    chips.win_bet()
    
def dealer_wins(chips):
    print('Dealer wins!')
    chips.lose_bet()
    
def push():
    print('Dealer and player tie! PUSH')

if __name__ == '__main__':
	print('Welcome To BlackJack')

	#Create and shuffle deck
	deck = Deck()
	deck.shuffle()

	#deal two cards to each player
	player_hand = Hand()
	player_hand.add_card(deck.deal())
	player_hand.add_card(deck.deal())

	dealer_hand = Hand()
	dealer_hand.add_card(deck.deal())
	dealer_hand.add_card(deck.deal())

	#Set up player's chips
	player_chips = Chips()

	#Prompt the player for their bet 
	take_bet(player_chips)

	#Show some cards
	show_some(player_hand, dealer_hand)

	while playing:

		#Prompt for player to hit or stand
		hit_or_stand(deck, player_hand)

		#Show some cards
		show_some(player_hand, dealer_hand)

		#If player's hand exceeds 21
		if player_hand.value > 21:
			player_busts(player_chips)

			#Ask to play again
			new_game = input('Would you like to play again? y/n').lower()

			if new_game == 'y':
				playing = True
				continue
			else:
				print('Thank you for playing')
				playing = False
			

		#If player has not busted - it is the dealer's turn
		if player_hand.value <= 21:
			while dealer_hand.value < player_hand.value:
				hit(deck, dealer_hand)

			#Show all cards
			show_all(player_hand, dealer_hand)

			#Different scenarios
			if dealer_hand.value > 21:
				dealer_busts(player_chips)
			elif (dealer_hand.value > player_hand.value):
				dealer_wins(player_chips)
			elif(dealer_hand.value > player_hand.value):
				player_wins(player_chips)
			else:
				push()

			#Inform player of their remaining chips
			print(f"\n Player's total chips are: {player_chips.total}")

			#Ask to play again
			new_game = input('Would you like to play again? y/n').lower()

			if new_game == 'y':
				playing = True
				continue
			else:
				print('Thank you for playing')
				playing = False