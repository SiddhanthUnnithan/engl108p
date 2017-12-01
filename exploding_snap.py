from utils import exploding_snap_util
from select import select
import random
import cmd
import sys
import operator

# Exploding Snap Rules:
# Two cards shown at a time
# Have to type y or n to if they are pairs or not
# If player is right, add 10 points. otherwise subtract one life
# Decrease time cards are shown every time player gets one correct
# Have probabilities for explosion: 3 lives -> 0, 2 lives -> 25%, 1 life -> 33%
# Game ends when explosion OR 0 lives

explosion = """
                        . . .
                         \|/
                       `--+--'
                         /|\\
                        ' | '
                          |
                          |
                      ,--'#`--.
                      |#######|
                   _.-'#######`-._
                ,-'###############`-.
              ,'#####################`,
             /#########################\\
            |###########################|
           |#############################|
           |#############################|
           |#############################|
           |#############################|
            |###########################|
             \#########################/
              `.#####################,'
                `._###############_,'
                   `--..#####..--'      \n"""


class ExplodingSnap(cmd.Cmd):
    intro = exploding_snap_util.intro + "Press Enter or type start to Begin Playing\nType help or ? to list commands\n"
    prompt = '(exploding_snap) '
    # Player Initial Values
    lives = 3
    sleep_time = 3
    score = 0
    explosion_chance = [0, 0.15, 0.05, 0.00]
    name = ""

    # String Choices
    success = ["Bravo!", "Splendid!", "Bloody Brilliant!", "Blimey, you're great!", "Correct!"]
    error = ["Galloping Gorgons!", "Horrible!", "Troll.", "Merlin's Pants!", "Like a sack of dragon dung.",
             "Great Sizzling Dragon Bogies!", "Merlin's Beard!", "Dunderhead!", "You snivelling git!"]

    scores = []

    game_started = False

    def emptyline(self):
        if not self.game_started:
            self.game_started = True
            self.start()

    def do_start(self, arg):
        'Start a new game'
        self.reset()
        self.start()

    def do_scores(self, arg):
        'Show top ten high scores'
        for i in range(len(self.scores) - 1, 0, -1):
            print "{} {}".format(self.scores[i][0], self.scores[i][1])

    def do_exit(self, arg):
        'Quit the game'
        print("Thanks for playing!")
        return True

    def reset(self):
        self.lives = 3
        self.sleep_time = 3
        self.score = 0
        self.name = ""

    def start(self):
        # Start a new game
        self.name = raw_input("Enter your name: ")
        self.prompt = "({}) ".format(self.name)
        self.play_game()

    def play_game(self):
        exploded = False
        while self.lives > 0:
            card_1 = exploding_snap_util.get_random_card()
            card_2 = exploding_snap_util.get_second_card(card_1)
            exploding_snap_util.print_two_cards(card_1, card_2)

            if random.random() < self.explosion_chance[self.lives]:
                exploding_snap_util.clear()
                exploded = True
                # Cards explode
                print explosion
                break
            self.raw_input_timed(card_1, card_2)
        if not exploded:
            exploding_snap_util.clear()

        self.insert_score()
        print "You're out of lives! That is, unless you've got some horcruxes."
        print "Your score: {}\nType start to play again. Type scores to see high scores!".format(self.score)

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
                    self.sleep_time *= 0.97
                    self.score += 1
                else:
                    self.lives -= 1
                    print"{} You have {} {} left".format(random.choice(self.error), self.lives, "life" if self.lives == 1 else "lives")
        else:
            exploding_snap_util.clear()
            self.lives -= 1
            print "{} You have {} {} left".format(random.choice(self.error), self.lives, "life" if self.lives == 1 else "lives")

    def insert_score(self):
        new_score = (self.name, self.score)
        self.scores.append(new_score)
        self.scores = sorted(self.scores, key=operator.itemgetter(1))
        if len(self.scores) > 10:
            self.scores.pop(0)

if __name__ == '__main__':
    ExplodingSnap().cmdloop()