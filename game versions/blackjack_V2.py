import random


class Card:
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
    def __str__(self):
        return f"{self.rank['rank']} of {self.suit}"

class Deck:
    def __init__(self):
        self.cards = []
        suits = ["spades","clubs","hearts","diamonds"]
        ranks = [
                {"rank":"A","value":11},
                {"rank":"2","value":2},
                {"rank":"3","value":3},
                {"rank":"4","value":4},
                {"rank":"5","value":5},
                {"rank":"6","value":6},
                {"rank":"7","value":7},
                {"rank":"8","value":8},
                {"rank":"9","value":9},
                {"rank":"10","value":10},
                {"rank":"J","value":10},
                {"rank":"Q","value":10},
                {"rank":"K","value":10}
                ]

        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit,rank))

    def shuffle(self):
        if len(self.cards) > 1:
            random.shuffle(self.cards)

    def deal(self,number):
        cards_delt = []
        for x in range(number):
            if len(self.cards) > 0:
                card = self.cards.pop()
                cards_delt.append(card)
        return cards_delt
    

class Hand:
    def __init__(self,dealer=False):
        self.cards = []
        self.value = 0
        self.dealer = dealer

    def add_card(self,card_list):
        self.cards.extend(card_list)

    def calc_value(self):
        self.value = 0
        has_ace = False

        for card in self.cards:
            card_value = int(card.rank["value"])
            self.value += card_value
            if card.rank["rank"] == "A":
                has_ace = True
        if has_ace and self.value > 21:
            self.value -= 10

    def get_value(self):
        self.calc_value()
        return self.value

    def is_blackjack(self):
        return self.get_value() == 21
    
    def display(self,show_all_dealer_cards=False):
        print(f'''{"Dealer's" if self.dealer else "Your"} hand:''')
        for index, card in enumerate(self.cards):
            if index == 0 and self.dealer and not show_all_dealer_cards and not self.is_blackjack():
                print ("hidden")
            else:
                print(card)
            
        if not self.dealer:
            print("Value:", self.get_value())

class Game:
    def play(self):
        keep_playing = True
        game_number = 0

        while keep_playing:
            game_number += 1
            deck = Deck()
            deck.shuffle()

            player_hand = Hand()
            dealer_hand = Hand(dealer=True)

            for i in range(2):
                player_hand.add_card(deck.deal(1))
                dealer_hand.add_card(deck.deal(1))
            
            print()
            print("*"*10+ f"Game Number "+str(game_number)+"*"*10)
            player_hand.display()
            print()
            dealer_hand.display()
            print("*"*33)
            print()

            if self.check_winner(player_hand,dealer_hand):
                continue
            
            choice = "meep"
            while player_hand.get_value() < 21 and choice not in ["stand","s"]:
                choice = input("Please choose 'Hit' or 'Stand': ").lower()
                print()
                while choice not in ["h","s","hit","stand",""]:
                    choice = input("Please enter 'Hit' or 'Stand' (or H/S): ").lower()
                    print()
                if choice in ["hit","h",""]:
                    player_hand.add_card(deck.deal(1))
                    player_hand.display()
                    print()
                    dealer_hand.display()
            
            if self.check_winner(player_hand,dealer_hand):
                continue

            player_hand_value = player_hand.get_value()
            dealer_hand_value = dealer_hand.get_value()

            while dealer_hand_value < 17:
                dealer_hand.add_card(deck.deal(1))
                dealer_hand_value = dealer_hand.get_value()
            
            dealer_hand.display(show_all_dealer_cards=True)
            
            if self.check_winner(player_hand,dealer_hand):
                continue

            print("\nFinal Results")
            print("Your hand: ",player_hand_value)
            print("Dealer's hand: ",dealer_hand_value)

            self.check_winner(player_hand,dealer_hand,True)
            self.keep_playing()

    def keep_playing(self):    
        keep_playing_input = "meep"
        game_number = 1
        while keep_playing_input not in ['yes','y','No','n',""]:
            keep_playing_input = input("\nWould you like to keep playing? ").lower()
            if keep_playing_input in ["yes","y",""]:
                keep_playing = True
            elif keep_playing_input in ["no",'n']:
                keep_playing = False
                print("\nThanks for playing!")
            else:
                keep_playing_input = input("Please enter 'Yes' or 'No' (or Y/N): ").lower()
                print()

       
    def check_winner(self,player_hand,dealer_hand,game_over=False):
        if not game_over:
            if player_hand.get_value() > 21:
                print("You busted. Dealer wins!")
                self.keep_playing()
                return True
            elif dealer_hand.get_value() > 21:
                print("Dealer busted. You win!")
                self.keep_playing()
                return True
            elif dealer_hand.is_blackjack() and player_hand.is_blackjack():
                print("Both players have blackjack. Push!")
                self.keep_playing()
                return True
            elif player_hand.is_blackjack():
                print("You have blackjack. You win!")
                self.keep_playing()
                return True
            elif dealer_hand.is_blackjack():
                print("Dealer has blackjack. Dealer wins!")
                self.keep_playing()
                return True
        else:
            if player_hand.get_value() > dealer_hand.get_value():
                print("\nYou win!")
                return True
            elif player_hand.get_value() == dealer_hand.get_value():
                print("\nTie!")
                return True
            else:
                print("\nDealer wins!")
                return True
        return False


g = Game()
g.play()