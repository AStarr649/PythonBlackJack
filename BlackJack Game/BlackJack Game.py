#   Alex Starr
#   Black Jack Game
#   7/1/19

import Cards, Games

class BJ_Cards(Cards.Card):
    """ A BlackJack Card """
    ACE_VALUE = 1

    @property
    def value(self):
        if self.is_face_up:
            v = BJ_Cards.RANKS.index(self.rank) + 1
            if v > 10:
                v = 10

        else:
            v = None
        return v

class BJ_Deck(Cards.Deck):
    """ A BlackJack Deck """
    def populate(self):
        for suit in BJ_Cards.SUITS:
            for rank in BJ_Cards.RANKS:
                self.cards.append(BJ_Cards(rank, suit))

class BJ_Hand(Cards.Hand):
    """ A BlackJack Hand """
    def __init__(self, name, bank = 1000):
        super(BJ_Hand, self).__init__()
        self.name = name
        self.bank = bank

    def __str__(self):
        rep = self.name + ":\t" + super(BJ_Hand, self).__str__()
        if self.total:
            rep += "(" + str(self.total) + ")"
        return rep

    def ante(self, num):
        self.bank = self.bank - num
        print(self.name, "has ", self.bank, "remaining.")
    
    @property
    def total(self):
        for card in self.cards:
            if not card.value:
                return None
        t = 0
        for card in self.cards:
            t += card.value

        contains_ace = False
        for card in self.cards:
            if card.value == BJ_Cards.ACE_VALUE:
                contains_ace = True

        if contains_ace and t <= 11:
            t += 10

        return t

    def is_busted(self):
        return self.total > 21

    def is_broke(self):
        return self.bank == 0
    
class BJ_Player(BJ_Hand):
    """ A BlackJack Player """       
    def is_hitting(self):
        response = Games.ask_yes_no("\n" + self.name + ", do you want to hit? (Y/N): ")
        return response == "y"

    def is_betting(self):
        response = Games.ask_yes_no("\n" + self.name + ", will you place bet? (Y/N): ")
        return response == "y"

    def placed_bet(self, player):
        print(self.name, "anties up.")
        self.ante(100)

    def player_bank(self):       
        print(self.name, "has ", self.bank, "available.")

    def won_pot(self, pool):
        self.bank += pool
        
    def bust(self):
        print(self.name, "busts.")
        self.lose()

    def lose(self):
        print(self.name, "loses.")

    def win(self):
        print(self.name, "wins.")

    def push(self):
        print(self.name, "pushes.")
        self.ante(-100) 

        
class BJ_Dealer(BJ_Hand):
    """ A BlackJack Dealer """
    def is_hitting(self):
        return self.total < 17

    def bust(self):
        print(self.name, "busts.")

    def flip_first_card(self):
        first_card = self.cards[0]
        first_card.flip()

class BJ_Game(object):
    """ A BlackJack Game """
    def __init__(self, names):
        self.players = []
        for name in names:
            player = BJ_Player(name)           
            self.players.append(player)

        self.dealer = BJ_Dealer("Dealer")

        self.deck = BJ_Deck()
        self.deck.populate()
        self.deck.shuffle()
        self.pool = 100

    @property
    def still_playing(self):
        sp = []
        for player in self.players:
            if not player.is_busted() and not player.is_broke():
                sp.append(player)
        return sp

    def __additional_cards(self, player):
        while not player.is_busted() and player.is_hitting():
            self.deck.deal([player])
            print(player)
            if player.is_busted():
                player.bust()

    def __increase_bet(self, player):
        if not player.is_busted() and player.is_betting():
            player.placed_bet(100)
            self.pool += 100
            print("New pool total is $", self.pool)

    def reset_pool(self):
        self.pool = 100
            
    def play(self):
        self.deck.deal(self.players + [self.dealer], per_hand = 2)
        self.dealer.flip_first_card()
        for player in self.players:
            print(player)
        print(self.dealer)
        print("Winning pool is $", self.pool)

        for player in self.players:
            self.__additional_cards(player)
            self.__increase_bet(player)

        self.dealer.flip_first_card()

        if not self.still_playing:
            print(self.dealer)
        else:
            print(self.dealer)
            self.__additional_cards(self.dealer)

            if self.dealer.is_busted():
                for player in self.still_playing:
                    player.win()
                    player.won_pot(self.pool)
            else:
                for player in self.still_playing:
                    if player.total > self.dealer.total:
                        player.win()
                    elif player.total < self.dealer.total:
                        player.lose()
                    else:
                        player.push()

        for player in self.players:
            player.clear()
        self.dealer.clear()
        self.reset_pool()

def main():
    print("\t\tWelcome to BlackJack!\n")

    names = []
    number = Games.ask_number("How many players? (1-7): ", low = 1, high = 8)
    for i in range(number):
        name = input("Enter player name: ")
        names.append(name)

    print()

    game = BJ_Game(names)

    again = None
    while again != "n":
        game.play()
        again = Games.ask_yes_no("\nDo you want to play again? ")


#main

main()
input("\n\nPress the enter key to exit.")
