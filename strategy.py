from copy import copy
import random
import database as db
import pdb
from game import Game
from itertools import product
from rich import print

def words_with_letter(wordlist, pos, letter, bit):
    if bit == 0:
        return [w for w in wordlist if letter not in w]
    if bit == 1:
        return [w for w in wordlist if w[pos] == letter]
    if bit == 2:
        return [w for w in wordlist if (letter in w) and (w[pos] != letter)]

def get_possible_responses(guess):
    ls = list(product([0, 1, 2], repeat=5))
    for letter in guess:
        if guess.count(letter) > 1:
            repeated_pos = [i for i in range(5) if guess[i] == letter]
            ls = [l for l in ls if not (set([0, 2]) <= set([l[i] for i in repeated_pos]))]
    return ls

if __name__ == "__main__":
    # game = Game()
    wordlist = db.UNACCENTED_VALID_SOLUTIONS
    
    best_score = 999999
    best_word = None

    for i, word in enumerate(wordlist):
        score = 0

        pdb.set_trace()
        for possible_response in get_possible_responses(word):
            valid_words = wordlist
            for pos, bit in enumerate(possible_response):
                valid_words = words_with_letter(valid_words, pos, word[pos], bit)
                # Must eliminate also by number of letters ("trickier": see matt-rickard)
            print(f"\t{possible_response}: {len(valid_words)} words left.")
            score += len(valid_words)

        print(f"#{i}: Word '{word}' has score {score}")
        if score < best_score:
            best_score = score
            best_word = word
            print(f"==> New best word!")