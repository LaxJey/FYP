import random
import numpy
from FYP.StateValue import StateValue


class BlackjackSim:

    def __init__(self):
        values = StateValue()
        values.start() # create all required matrices
        self.V = values.getV() # optimal policy
        self.Y = values.getY() # all stand values
        self.S = values.getS() # all split values
        self.D = values.getD() # all double values
        self.dealer_deck = [] # dealer deck
        self.dealer_copy = [] # dealer's initial card
        self.player_deck = [] # player deck
        self.player_deck2 = [] # player split deck
        self.deck = "D:\\Brunel Uni Work\\FYP\\SingleDeck.txt" # single deck
        self.X = numpy.zeros((31, 10)) # games played
        self.W = numpy.zeros((31, 10)) # wins
        self.A = numpy.zeros((11, 10)) # split games wins
        self.B = numpy.zeros((11, 10)) # split games played
        self.P = [] # state values of player's deck
        self.fix = None

    # add a card to a deck
    def assign_card(self):
        DeckFile = open(self.deck, 'r')
        lines = DeckFile.readlines()
        DeckFile.close()
        random_index = random.randint(0, len(lines) - 1)
        random_line = lines[random_index]
        random_line = random_line.replace('\n', '')
        return random_line

    # create the initial hands -> dealer 1 card, player 2 cards
    def initial_hands(self):
        self.dealer_deck.append(self.assign_card())
        self.dealer_copy = self.dealer_deck[:1]
        self.player_deck.append(self.assign_card())
        self.P.append(self.state(self.player_deck))
        self.player_deck.append(self.assign_card())
        self.P.append(self.state(self.player_deck))

    # calculate total hand value
    def hand_value(self, hand):
        self.fix = None
        count = 0
        aces = 0
        for card in hand:
            c = card[0]
            if c in 'JQK':
                count += 10
            elif c == 'A':
                aces += 1
                count += 11
            elif c == '1':
                count += 10
            else:
                count += int(c)
        while count > 21 and aces > 0:
            count -= 10
            aces -= 1
        return count

    # to determine whether to hit or stand
    def action(self, hand):
        p = self.state(hand)
        d = self.hand_value(self.dealer_deck)
        if d == 11:
            d = 1
        if self.V[p][d-1] > self.Y[p][d-1]:
            option = 1
        else:
            option = 2
        return option

    # player chooses to hit according to optimal policy
    def player_hit(self, hand):
        hand.append(self.assign_card())
        self.P.append(self.state(self.player_deck))

    # dealer rules
    def dealer_hit(self):
        while self.hand_value(self.dealer_deck) < 17:
            self.dealer_deck.append(self.assign_card())

    # determine state given hand
    def state(self, hand):
        self.fix = None
        count = 0
        aces = 0
        state = 0
        for card in hand:
            c = card[0]
            if c in 'JQK':
                count += 10
            elif c == 'A':
                aces += 1
                count += 11
            elif c == '1':
                count += 10
            else:
                count += int(c)
        while count > 21 and aces > 0:
            count -= 10
            aces -= 1
        if count > 22:
            count = 22
        if aces == 1 and count < 17:
            state = count - 11
            return state
        elif aces == 1:
            state = count + 4
            return state
        elif count < 17:
            state = count + 4
            return state
        else:
            state = count + 8
            return state

    # to determine win/loss/tie and record the data
    def checkwinner(self):
        w = 0
        if self.hand_value(self.player_deck) > 21:
            w = -1
        elif self.hand_value(self.dealer_deck) > 21:
            w = 1
        elif self.hand_value(self.dealer_deck) > self.hand_value(self.player_deck):
            w = -1
        elif self.hand_value(self.dealer_deck) < self.hand_value(self.player_deck):
            w = 1
        d = self.hand_value(self.dealer_copy)
        if d == 11:
            d = 1
        for p in self.P:
            self.X[p][d-1] += 1
            self.W[p][d-1] += w

    # check if eligible for split
    def checksplit(self):
        card = self.player_deck[0]
        card1 = self.player_deck[1]
        p = self.state(self.player_deck)
        d = self.hand_value(self.dealer_deck)
        if d == 11:
            d = 1
        c = card[0]
        if c in 'JQK':
            a = 10
        elif c == 'A':
            a = 11
        elif c == '1':
            a = 10
        else:
            a = int(c)
        if card == card1:
            if self.V[p][d - 1] < self.S[a - 1][d - 1]:
                self.split()
                return 1
        return 0

    #run the full game
    def game(self):
        self.new_game()
        self.initial_hands()
        check = self.checksplit()
        if check == 1:
            return
        check2 = self.double()
        if check2 == 1:
            return
        option = self.action(self.player_deck)
        while option == 1:
            self.player_hit(self.player_deck)
            option = self.action(self.player_deck)
        if self.hand_value(self.player_deck) < 22:
            self.dealer_hit()
        self.checkwinner()

    # run simulations of blackjack
    def sims(self):
        for i in range(1, 100001):
            self.game()

    # start a new game, resets all the hands
    def new_game(self):
        self.dealer_deck = []
        self.dealer_copy = []
        self.player_deck = []
        self.P = []

    # get simulation results
    def getResult(self):
        self.sims()
        self.getResult2()
        return self.W/self.X

    # get split results
    def getResult2(self):
        z = numpy.divide(self.A, self.B, out=numpy.zeros_like(self.A), where=self.B!=0)
        for row in z:
            print(' '.join([f'{num:.4f}' for num in row]))
        print("\n\n\n")

    # when the player chooses to split according to the optimal policy
    def split(self):
        self.player_deck.pop()
        self.player_deck2 = self.player_deck[:]
        option = self.action(self.player_deck)
        while option == 1:
            self.player_hit(self.player_deck)
            option = self.action(self.player_deck)
        option = self.action(self.player_deck2)
        while option == 1:
            self.player_hit(self.player_deck2)
            option = self.action(self.player_deck2)
        if self.hand_value(self.player_deck) < 22 or self.hand_value(self.player_deck2) < 22:
            self.dealer_hit()
        w = 0
        if self.hand_value(self.player_deck) > 21:
            w += -0.5
        elif self.hand_value(self.dealer_deck) > 21:
            w += 0.5
        elif self.hand_value(self.dealer_deck) > self.hand_value(self.player_deck):
            w += -0.5
        elif self.hand_value(self.dealer_deck) < self.hand_value(self.player_deck):
            w += 0.5
        if self.hand_value(self.player_deck2) > 21:
            w += -0.5
        elif self.hand_value(self.dealer_deck) > 21:
            w += 0.5
        elif self.hand_value(self.dealer_deck) > self.hand_value(self.player_deck2):
            w += -0.5
        elif self.hand_value(self.dealer_deck) < self.hand_value(self.player_deck2):
            w += 0.5
        d = self.hand_value(self.dealer_copy)
        if d == 11:
            d = 1
        self.P = self.P[:2]
        for p in self.P:
            self.X[p][d - 1] += 1
            self.W[p][d - 1] += w
        card = self.player_deck[0]
        c = card[0]
        p = 0
        if c in 'JQK':
            p = 10
        elif c == 'A':
            p = 11
        elif c == '1':
            p = 10
        else:
            p = int(c)
        self.A[p - 1][d - 1] += w
        self.B[p - 1][d - 1] += 1

    # when the player chooses to double according to the optimal policy
    def double(self):
        p = self.state(self.player_deck)
        d = self.hand_value(self.dealer_deck)
        if d == 11:
            d = 1
        if self.D[p][d - 1] > self.V[p][d - 1]:
            self.player_deck.append(self.assign_card())
            self.P.append(self.state(self.player_deck))
            if self.hand_value(self.player_deck) < 22:
                self.dealer_hit()
            w = 0
            if self.hand_value(self.player_deck) > 21:
                w = -2
            elif self.hand_value(self.dealer_deck) > 21:
                w = 2
            elif self.hand_value(self.dealer_deck) > self.hand_value(self.player_deck):
                w = -2
            elif self.hand_value(self.dealer_deck) < self.hand_value(self.player_deck):
                w = 2
            d = self.hand_value(self.dealer_copy)
            if d == 11:
                d = 1
            for a in self.P:
                self.X[a][d - 1] += 1
                self.W[a][d - 1] += w
            return 1
        return 0
