import random
import database as db
import utils

from rich import print

class Game:
    def __init__(self, max_tries=6):
        self.max_tries = max_tries
        
        self.reset()
    
    def reset(self): 
        self.history = []
        self.tries = 0
        self.word = random.choice(db.ACCENTED_VALID_SOLUTIONS)
        self.done = False

    def is_legal_guess(self, guess):
        unaccented_guess = utils.remove_accents(guess)

        if len(guess) == db.WORD_SIZE and \
            unaccented_guess in db.UNACCENTED_VALID_SOLUTIONS:
            return True
        
        return False
    
    def guess_word(self, guess):
        if self.done:
            print("Game is over!")
            return -1
        
        if not self.is_legal_guess(guess):
            print("Illegal guess!")
            return None
        
        response = [self.guess_letter(letter, i) for (i, letter) in enumerate(guess)]

        self.tries += 1
        self.history.append((guess, response))
        self.print_log()

        if guess == self.word:
            print("You're correct!")
            return 1
        
        if self.tries == self.max_tries:
            print("You're out of tries!")
            self.done = True
            return -1

        return 0

    def guess_letter(self, guess, pos):
        if self.word[pos] == guess:
            return 1
        if guess in self.word:
            return 2
        return 0
    
    def print_log(self):
        colors = ["black", "green", "yellow"]
        output = "[bold]"

        for guess, response in self.history:
            for letter, bit in zip(guess, response):
                color = colors[bit]
                output += f"[{color}]{letter}[/{color}]"
            output += "\n"
        
        print(output)

if __name__ == "__main__":
    game = Game()
    while not game.done:
        random_guess = random.choice(db.UNACCENTED_VALID_SOLUTIONS)
        game.guess_word(random_guess)