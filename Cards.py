import itertools
import random
import copy

# Cards
class Card(object):

    name2rank = {
        '3': 1,
        '4': 2,
        '5': 3,
        '6': 4,
        '7': 5,
        '8': 6,
        '9': 7,
        '10': 8,
        'J': 9,
        'Q': 10,
        'K': 11,
        'A': 12,
        '2': 13,
        'Joker': 14
        }
    def __init__(self, card):
        self.card = card
        self.name, self.color = self.card

    @property
    def rank(self):
        return Card.name2rank[self.name]


class Cards(object):
    def __init__(self, n_deck=1):
        self.names = ['3', '4', '5', '6', '7', '8', '9', '10',
                      'J', 'Q', 'K', 'A', '2']
        self.colors = ['SPADE', 'HEART', 'CLUB', 'DIAMOND']
        self.cards = list(itertools.product(self.names, self.colors))
        self.cards.extend([('Joker', 'BLACK'), ('Joker', 'RED')])
        self.cards = self.cards * n_deck

    def get_cards(self, shuffle=True):
        cards = copy.deepcopy(self.cards)
        if shuffle:
            random.shuffle(cards)
        return cards


# Player
class Player(object):
    def __init__(self, name):
        self.name = str(name)
        self.cards_remain = None
        self.score = 0

    def get_cards(self, cards):
        self.cards_remain = [Card(card) for card in cards]
        self.cards_remain.sort(key=lambda x:x.rank)

    def show_remain_cards(self):
        for card in self.cards_remain:
            print(card.card)

    def get_move(self):
        return [self.cards_remain[0]]


# Game
class RBCard(object):
    def __init__(self):
        self.player1 = Player('p1')
        self.player2 = Player('p2')
        self.player3 = Player('p3')
        self.player4 = Player('p4')
        self.players = [self.player1, self.player2, self.player3, self.player4]

        # Initialize game
        print("RB Card game begins! Dealing Cards!")
        self.deal()
        print("Cards Dealed!")
        self.show_player_cards()

        self.team1 = [self.player1, self.player2]   # random
        self.team2 = [self.player3, self.player4]
        print("Team 1: {} + {}".format(self.team1[0].name, self.team1[1].name))
        print("Team 2: {} + {}".format(self.team2[0].name, self.team2[1].name))

        self.winner = None
        self.game_end = False
        self.next_player = -1
        self.round = 0

    def deal(self):
        cards = Cards(n_deck=2).get_cards()
        self.player1.get_cards(cards[:27])
        self.player2.get_cards(cards[27:54])
        self.player3.get_cards(cards[54:81])
        self.player4.get_cards(cards[81:])

    def start(self):
        while not self.game_end:
            self.round += 1
            print("Round {} begins!".format(self.round))

            self.play_round()
            break
                
    def play_round(self):
        round_end = False
        score = 0
        no_afford = 0
        while not round_end:
            
            self.next_player = (self.next_player + 1) % 4

            move = None
            while not self.is_valid(move):
                if move is not None:
                    print("Invalid Move: ", move)
                move = self.players[self.next_player].get_move()

            score += self.make_move(move)
            
            if len(move) == 0:
                no_afford += 1
            else:
                no_afford = 0

            if no_afford == 3:
                round_end = True
                self.next_player = (self.next_player + 1) % 4
                print("Round ends! {} scores {} + {}!".format(
                    self.next_player.name, self.next_player.score, score))
                self.next_player.score += score


        self.check_win()
            
    
    def is_valid(self, move):
        if move is None:
            return False
        return True

    def make_move(self, move):
        score = 0
        if len(move) == 0:
            pass
        else:
            for m in move:
                self.players[self.next_player].cards_remain.remove(m)
                if m.name == '5':
                    score += 5
                elif m.name == '10' or m.name == 'K':
                    score += 10
        
        print("{}: {}".format(self.players[self.next_player].name, [m.card for m in move]))
        return score

    def check_win(self):
        pass

    
    def show_player_cards(self):
        for player in self.players:
            print(player.name)
            player.show_remain_cards()


if __name__ == '__main__':
    game = RBCard()
    game.start()
