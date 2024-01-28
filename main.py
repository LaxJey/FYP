from FYP.Blackjack import Blackjack
from FYP.BlackjackSim import BlackjackSim
from FYP.DiceBlackjack import DiceBlackjack
from FYP.StateValue import StateValue
import time

start_time = time.time()


def old():
    values = StateValue()
    V = values.getV()
    for row in V:
        print(' '.join([f'{num:.4f}' for num in row]))

    game = Blackjack()
    game.start_game()

    dice = DiceBlackjack()
    dice.sim()

    game = BlackjackSim()
    A = game.getResult()
    for row in A:
        print(' '.join([f'{num:.4f}' for num in row]))
    print("\n\n\n")
    values = StateValue()
    C = values.getS()
    for row in C:
        print(' '.join([f'{num:.4f}' for num in row]))
    print("\n\n\n")
    B = values.getV()
    for row in B:
        print(' '.join([f'{num:.4f}' for num in row]))
    print("\n\n\n")


game = BlackjackSim()
A = game.getResult()
for row in A:
    print(' '.join([f'{num:.4f}' for num in row]))
print("\n\n\n")
values = StateValue()
values.start()
B = values.getS()
for row in B:
    print(' '.join([f'{num:.4f}' for num in row]))
print("\n\n\n")
B = values.getV()
for row in B:
    print(' '.join([f'{num:.4f}' for num in row]))
print("\n\n\n")

end_time = time.time()
print(f"\nRuntime = {end_time - start_time}")
