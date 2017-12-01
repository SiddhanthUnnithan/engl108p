from utils import exploding_snap_util
from select import select
import time
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
    sleep_time = 2

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
            self.raw_input_timed()

    def raw_input_timed(self):
        rlist, _, _ = select([sys.stdin], [], [], self.sleep_time)
        if rlist:
            s = sys.stdin.readline()
            print s
        else:
            exploding_snap_util.clear()
            self.lives -= 1
            print "Not Fast Enough! You have {} {} left".format(self.lives, "life" if self.lives == 1 else "lives")

if __name__ == '__main__':
    ExplodingSnap().cmdloop()