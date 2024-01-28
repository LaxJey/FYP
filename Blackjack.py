import random
import time


class Blackjack:

    def __init__(self):
        self.dealer_deck = []
        self.player_deck = []
        self.player_deck2 = []
        self.dealer_2card = ""
        self.deck = "D:\\Brunel Uni Work\\FYP\\CurrentDeck.txt"
        self.used = "D:\\Brunel Uni Work\\FYP\\UsedCards.txt"
        self.clear = "\n" * 100
        self.fix = None

    def menu(self):
        self.fix = None
        option = '''                    
                                    𝔹 𝕃 𝔸 ℂ 𝕂 𝕁 𝔸 ℂ 𝕂

        𝕄 𝔼 ℕ 𝕌

        𝟙. 𝕡𝕝𝕒𝕪 𝕓𝕝𝕒𝕔𝕜𝕛𝕒𝕔𝕜
        𝟚. 𝕘𝕒𝕞𝕖 𝕚𝕟𝕤𝕥𝕣𝕦𝕔𝕥𝕚𝕠𝕟𝕤
        𝟛. 𝕖𝕩𝕚𝕥 𝕘𝕒𝕞𝕖'''
        print(option)

    def gameinstructions(self):
        self.fix = None
        rules = '''
                                    BLACKJACK GAME INSTRUCTIONS

        1. Goal: Get a hand value close to 21 without going over.
        2. Bet your chips before the game starts.
        3. Receive two cards and decide to hit (take a card) or stand (keep your cards).
        4. You can also:
          - Split: If you have a pair, split them into two separate hands by placing an
          additional bet. Each hand is played individually.
          - Double Down: Double your original bet and receive one more card, committing to
          stand after that card.
        5. The dealer must hit until their hand is worth at least 17.
        6. Try to beat the dealer's hand without busting (exceeding 21).
        7. If you have a Blackjack (21), you win 1.5x.
        8. After the round, decide to play again or quit.
        9. Enjoy the game!
        '''
        print(rules)
        time.sleep(8)

    def assign_card(self):
        DeckFile = open(self.deck, 'r')
        lines = DeckFile.readlines()
        DeckFile.close()
        random_index = random.randint(0, len(lines) - 1)
        random_line = lines[random_index]
        del lines[random_index]
        UsedFile = open(self.used, 'a')
        UsedFile.write(random_line)
        UsedFile.close()
        DeckFile = open(self.deck, 'w')
        DeckFile.writelines(lines)
        DeckFile.close()
        random_line = random_line.replace('\n', '')
        return random_line

    def initial_hands(self):
        self.dealer_deck.append(self.assign_card())
        self.dealer_2card = self.assign_card()
        self.player_deck.append(self.assign_card())
        self.player_deck.append(self.assign_card())
        print('\n')
        print('The dealers hand is:', self.dealer_deck, 'with a value of',
              self.hand_value(self.dealer_deck))
        print('Your hand is:', self.player_deck, 'with a value of',
              self.hand_value(self.player_deck))

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

    def action(self):
        self.fix = None
        option = input('''
        1. Hit
        2. Stand\n
        ''')
        return option

    def player_hit(self, p_deck):
        print('\tYou hit.')
        p_deck.append(self.assign_card())
        print('\tYour hand is: ', p_deck)
        print('\tYour hand value is: ', self.hand_value(p_deck))

    def dealer_hit(self):
        while self.hand_value(self.dealer_deck) < 17:
            self.dealer_deck.append(self.assign_card())
            print('\tThe dealer hits.')
            print('\tThe dealers hand is: ', self.dealer_deck)
            print('\tThe dealers hand value is: ', self.hand_value(self.dealer_deck))

    def checkwinner(self):
        if self.hand_value(self.dealer_deck) > 21:
            print('\nDealer bust, you win!')
        else:
            print('\nYour hand is: ', self.player_deck)
            print('Your hand value is: ', self.hand_value(self.player_deck))
            if self.hand_value(self.player_deck) > self.hand_value(self.dealer_deck):
                print('You win!')
            elif self.hand_value(self.player_deck) == self.hand_value(self.dealer_deck):
                print('You tie!')
            else:
                print('You lose!')

    def split(self):
        self.player_deck2.append(self.player_deck.pop())
        print("For the first hand:")
        self.play(self.player_deck)
        print("For the second hand:")
        self.play(self.player_deck2)

    def double(self):
        self.player_deck.append(self.assign_card())
        print('\tYour hand is: ', self.player_deck)
        print('\tYour hand value is: ', self.hand_value(self.player_deck))
        if self.hand_value(self.player_deck) > 21:
            print('\nYou bust!')
            print('You lose!')
            return
        self.dealer_deck.append(self.dealer_2card)
        print('\n\tThe dealers 2nd card is: ', self.dealer_2card)
        print('\tThe dealers hand value is: ', self.hand_value(self.dealer_deck))
        if self.hand_value(self.dealer_deck) >= 17:
            print('\tThe dealer stands.')
            print('\tThe dealers hand is: ', self.dealer_deck)
            print('\tThe dealers hand value is: ', self.hand_value(self.dealer_deck))
        else:
            self.dealer_hit()
            self.checkwinner()

    def play(self, p_deck):
        player_action = 0
        while player_action != '2':
            player_action = self.action()
            if player_action == '2':
                print('\tYou stand.')
                self.dealer_deck.append(self.dealer_2card)
                print('\tThe dealers 2nd card is: ', self.dealer_2card)
                print('\tThe dealers hand value is: ', self.hand_value(self.dealer_deck))
                if self.hand_value(self.dealer_deck) >= 17:
                    print('\tThe dealer stands.')
                    print('\tThe dealers hand is: ', self.dealer_deck)
                    print('\tThe dealers hand value is: ', self.hand_value(self.dealer_deck))
                else:
                    self.dealer_hit()
                self.checkwinner()
            elif player_action == '1':
                self.player_hit(p_deck)
                if self.hand_value(p_deck) > 21:
                    print('\nYou bust!')
                    print('You lose!')
                    break
            else:
                print('Invalid option.')

    def game(self):
        self.initial_hands()
        if self.hand_value(self.player_deck) == 21:
            self.dealer_deck.append(self.dealer_2card)
            print('\tThe dealers 2nd card is: ', self.dealer_2card)
            print('\tThe dealers hand value is: ', self.hand_value(self.dealer_deck))
            if self.hand_value(self.dealer_deck) == 21:
                print('\nYou tie!')
                return
            else:
                print('\nYou have a Blackjack!')
                print('You win 1.5x!')
                return
        c = []
        for card in self.player_deck:
            c.append(card[0])
        if c[0] == c[1]:
            psplit = 'a'
            while psplit != 'n':
                psplit = input("\nDo you want to split? (y/n)\n")
                if psplit == 'y':
                    self.split()
                    return
                else:
                    print('Invalid input.')
        pdouble = 'a'
        while pdouble != 'n':
            pdouble = input("\nDo you want to double down? (y/n)\n")
            if pdouble == 'y':
                self.double()
                return
            elif pdouble != 'n':
                print('Invalid input.')
        self.play(self.player_deck)

    def new_game(self):
        self.dealer_deck.clear()
        self.player_deck.clear()

    def shuffle(self):
        DeckFile = open(self.deck, 'r')
        Deck = DeckFile.readlines()
        DeckFile.close()
        if len(Deck) < 234:
            print("asd")
            UsedFile = open(self.used, 'r')
            cards = UsedFile.readlines()
            UsedFile.close()
            UsedFile = open(self.deck, 'w')
            UsedFile.truncate(0)
            UsedFile.close()
            DeckFile = open(self.deck, 'a')
            DeckFile.writelines(cards)
            DeckFile.close()

    def start_game(self):
        while True:
            time.sleep(3)
            print(self.clear)
            self.menu()
            option = input('\nInput Your Menu Option: ')
            if option == '3':
                print('\nGoodbye')
                break
            elif option == '2':
                self.gameinstructions()
            elif option == '1':
                self.shuffle()
                self.new_game()
                self.game()
            else:
                print('Invalid menu option\n')
