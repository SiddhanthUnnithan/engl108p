from utils import exploding_snap_util
from select import select
import random
import cmd
import sys

# Exploding Snap Rules:
# Two cards shown at a time
# Have to type y or n to if they are pairs or not
# If player is right, add 10 points. otherwise subtract one life
# Decrease time cards are shown every time player gets one correct
# Have probabilities for explosion: 3 lives -> 0, 2 lives -> 25%, 1 life -> 33%
# Game ends when explosion OR 0 lives


class ExplodingSnap(cmd.Cmd):
    intro = exploding_snap_util.intro + "Press Enter or type start to Begin Playing\nType help or ? to list commands\n"
    prompt = '(exploding_snap) '
    # Player Initial Values
    lives = 3
    sleep_time = 3

    # String Choices
    success = ["Bravo!", "Splendid!", "Bloody Brilliant!", "Blimey, you're great!", "Correct!"]
    error = ["Galloping Gorgons!", "Horrible!", "Troll.", "Merlin's Pants!", "Like a sack of dragon dung.",
             "Great Sizzling Dragon Bogies!", "Merlin's Beard!", "Dunderhead!", "You snivelling git!"]

    game_started = False

    def emptyline(self):
        if not self.game_started:
            self.game_started = True
            self.start()

    def do_start(self, arg):
        'Start a new game'
        self.start()

    def do_exit(self, arg):
        'Quit the game'
        print("Thanks for playing!")
        return True

    def start(self):
        # Start a new game
        response = raw_input("Enter your name: ")
        self.prompt = "({}) ".format(response)
        self.play_game()

    def play_game(self):
        while self.lives > 0:
            card_1 = exploding_snap_util.get_random_card()
            card_2 = exploding_snap_util.get_second_card(card_1)
            exploding_snap_util.print_two_cards(card_1, card_2)
            self.raw_input_timed(card_1, card_2)

    def raw_input_timed(self, card_1, card_2):
        rlist, _, _ = select([sys.stdin], [], [], self.sleep_time)
        if rlist:
            exploding_snap_util.clear()
            s = sys.stdin.readline()[0]
            if s != 'y' and s != 'n':
                self.lives -= 1
                print "{} You typed in a wrong character. Remember: only \'y\' and \'n\'\n You have {} {} left"\
                    .format(random.choice(self.error), self.lives, "life" if self.lives == 1 else "lives")
            else:
                if (s == 'y' and card_1.val == card_2.val) or (s == 'n' and card_1.val != card_2.val):
                    print "{}".format(random.choice(self.success))
                else:
                    self.lives -= 1
                    print"{} You have {} {} left".format(random.choice(self.error), self.lives, "life" if self.lives == 1 else "lives")
        else:
            exploding_snap_util.clear()
            self.lives -= 1
            print "{} You have {} {} left".format(random.choice(self.error), self.lives, "life" if self.lives == 1 else "lives")

if __name__ == '__main__':
    ExplodingSnap().cmdloop()