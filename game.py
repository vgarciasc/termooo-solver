from os import remove
import pdb
import random
from utils import printv, remove_accents, remove_accent
import database as db

from rich import print

class Game:
    def __init__(self, max_tries=6):
        self.max_tries = max_tries
        
        self.reset()
    
    def reset(self): 
        self.history = []
        self.tries = 0
        self.done = False
        self.reward = 0

        self.set_word(random.choice(db.ACCENTED_VALID_SOLUTIONS))

    def set_word(self, word):
        self.word = word
        self.unaccented_word = remove_accents(word)

    def is_legal_guess(self, guess):
        unaccented_guess = remove_accents(guess)

        if len(guess) == db.WORD_SIZE and \
            unaccented_guess in db.UNACCENTED_VALID_SOLUTIONS:
            return True
        
        return False
    
    def guess_word(self, guess, verbose=False):
        unaccented_guess = remove_accents(guess)

        if self.done:
            printv("Game is over!", verbose)
            return None
        
        if not self.is_legal_guess(guess):
            if verbose:
                printv("Illegal guess!", verbose)
            return None

        if self.tries >= self.max_tries:
            printv(f"You're out of tries! Word was '{self.word}'.", verbose)
            self.done = True
            return None
        
        response = [self.guess_letter(letter, i) for (i, letter) in enumerate(guess)]

        self.tries += 1
        self.history.append((guess, response))
        self.print_log(verbose)

        if unaccented_guess == self.unaccented_word:
            printv(f"You're correct! Won after {self.tries} tries.", verbose)
            self.done = True
            self.reward = 1
        
        return response

    def guess_letter(self, letter_guess, pos):
        unaccented_guess_letter = remove_accents(letter_guess)

        if self.unaccented_word[pos] == unaccented_guess_letter:
            return 1
        if unaccented_guess_letter in self.unaccented_word:
            return 2
        return 0
    
    def print_log(self, verbose):
        if not self.history:
            printv("No guesses yet!", verbose)
        
        colors = ["black", "green", "yellow"]
        output = "[bold]"

        for guess, response in self.history:
            for letter, bit in zip(guess, response):
                color = colors[bit]
                output += f"[{color}]{letter}[/{color}]"
            output += "\n"
        
        printv(output, verbose)

if __name__ == "__main__":
    game = Game()
    
    while not game.done:
        random_guess = random.choice(db.UNACCENTED_VALID_SOLUTIONS)
        game.guess_word(random_guess)