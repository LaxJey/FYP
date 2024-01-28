import numpy
import random


class DiceBlackjack:

    def __init__(self):
        # Initialize a matrix of zeros with dimensions 13x4
        self.Z = numpy.zeros((13, 4))
        self.X = numpy.zeros((13, 4))
        self.W = numpy.zeros((13, 4))
        self.win = 0
        self.loss = 0
        self.draw = 0
        self.PT = None
        self.T = None
        self.A = None
        self.Y = None
        self.fix = None

    # Function to calculate absorption matrices
    def matrices(self):
        # Define matrices T and PT with specific values
        # These matrices are used for calculations later

        # Dealer's transition matrix
        self.T = numpy.array([
            [0, 0.25, 0.25, 0.25, 0.25, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0.25, 0.25, 0.25, 0.25, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0.25, 0.25, 0.25, 0.25, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0.25, 0.25, 0.25, 0.25, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0.25, 0.25, 0.25, 0.25, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0.25, 0.25, 0.25, 0.25, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0.25, 0.25, 0.25, 0.25, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0.25, 0.25, 0.25, 0.25, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0.25, 0.25, 0.25, 0.25],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        ])

        # player's transition matrix
        self.PT = numpy.array([
            [0, 0.25, 0.25, 0.25, 0.25, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0.25, 0.25, 0.25, 0.25, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0.25, 0.25, 0.25, 0.25, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0.25, 0.25, 0.25, 0.25, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0.25, 0.25, 0.25, 0.25, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0.25, 0.25, 0.25, 0.25, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0.25, 0.25, 0.25, 0.25, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0.25, 0.25, 0.25, 0.25, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0.25, 0.25, 0.25, 0.25],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.25, 0.25, 0.50],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.25, 0.75],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        ])

        # Perform matrix operations to calculate matrix A
        # A is an absorption matrix
        Q = self.T[:9, :9]
        R = self.T[:9, 9:]
        Identity = numpy.eye(9)
        self.A = numpy.linalg.inv(Identity - Q).dot(R)

    # Function to calculate standing probability
    def stand(self, p, d):
        s = 0
        D = [10, 11, 12, 13]
        # Calculate standing probability 's' using the win function and matrix A
        for x in D:
            s += self.outcome(p, x) * self.A[d - 1][x - 10]
        # If condition to handle player bust
        if p > 12:
            s = -1
        # Update the Z matrix with the calculated probability 's'
        self.Z[p - 1][d - 1] = s

    # Function to determine win/lose/draw
    def outcome(self, p, d):
        self.fix = None
        if p > d or d > 12:
            return 1  # when player's value is higher than the dealers or if the dealer is bust
        elif p < d:
            return -1  # if the dealer's value is higher
        else:
            return 0  # the player and dealer tie

    # Function to iterate through stand() for all possible player hands and dealer's initial value
    def loop(self):
        self.matrices()
        for i in range(1, 5):
            for j in range(13, 0, -1):
                self.stand(j, i)

    # Function to compare and update matrices
    def compare(self):
        self.loop()
        self.Y = self.Z.copy()
        # Perform matrix multiplication and update Z matrix iteratively
        for i in range(1, 13):
            V = self.PT.dot(self.Z)
            self.Z = numpy.maximum(V, self.Z)
        # Print the final updated Z matrix

    # Function to create and run game
    def game(self):
        self.compare()
        d = random.randint(1, 4)
        p = random.randint(1, 4)
        di = d
        P = [p]
        a = 0
        while a == 0:
            if self.Z[p - 1][d - 1] > self.Y[p - 1][d - 1]:
                p += random.randint(1, 4)
                if p > 13:
                    p = 13
                P.append(p)
            else:
                a = 1
        while d < 10:
            d += random.randint(1, 4)
        if p > 12:
            w = -1
            self.loss += 1
        elif d > 12:
            w = 1
            self.win += 1
        elif p > d:
            w = 1
            self.win += 1
        elif d > p:
            w = -1
            self.loss += 1
        else:
            w = 0
            self.draw += 1
        for x in P:
            self.X[x - 1][di - 1] += w
            self.W[x - 1][di - 1] += 1

    # Run simulations for 1000000 times
    def sim(self):
        for i in range(1, 1000001):
            self.game()
        print("Number of wins:", self.win)
        print("Number of losses:", self.loss)
        print("Number of draws:", self.draw)
