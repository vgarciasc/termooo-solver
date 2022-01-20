from os import remove
import numpy as np
import database as db
import time
import json
import pdb
from game import Game
from itertools import product
from utils import printv, remove_accents

def filter_words_after_guess(words, guess, response):
    for pos, bit in enumerate(response):
        words = filter_words_after_bit(words, guess, response, pos)
    return words

def filter_words_after_bit(words, guess, response, pos):
    bit, letter = response[pos], guess[pos]
    
    if bit == 0:
        return [w for w in words if (letter not in w) or \
            (letter in get_confirmed_letters(w, guess, response))]
    if bit == 1:
        return [w for w in words if w[pos] == letter]
    if bit == 2:
        return [w for w in words if (letter in w) and (w[pos] != letter)]

def get_confirmed_letters(word, guess, response):
    confirmed_letters = [(i, l) for i, l in enumerate(guess) if response[i] == 1]
    return [l for (i, l) in confirmed_letters if word[i] == l]

def get_best_guess(valid_guesses, valid_solutions, verbose=False):
    if len(valid_solutions) == 1:
        return valid_solutions[0]

    # valid_guesses = [remove_accents(w) for w in valid_guesses]
    # valid_solutions = [remove_accents(w) for w in valid_solutions]
    possible_responses = list(product([0, 1, 2], repeat=db.WORD_SIZE))

    best_score = 999999
    best_guess = None

    for i, guess in enumerate(valid_guesses):
        score = 0

        for response in possible_responses:
            if response == (1, 1, 1, 1, 1):
                # So that 'victory now' and 'victory in the next turn' 
                # have different weights
                score += 0
            else:
                solutions = filter_words_after_guess(
                    words=valid_solutions, 
                    guess=guess, 
                    response=response)
                score += len(solutions)**2 / len(valid_solutions)
        
        printv(f"#{i}: Word '{guess}' has score {score}", verbose)
        
        if score < best_score:
            best_score = score
            best_guess = guess
            printv(f"==> New best word '{guess}', with average score {'{:.3f}'.format(score)}!", verbose)
    
    printv(f"Best guess: {best_guess}, score: {best_score}", verbose)

    return best_guess

def run_game(solution=None, starter_word=None, verbose=False):
    starter_word = remove_accents(starter_word)

    game = Game()
    if solution:
        game.set_word(solution)
    printv(f"Starting new game... Word is '{game.word}'.", verbose)

    possible_solutions = db.UNACCENTED_VALID_SOLUTIONS
    start = time.time()

    while not game.done:
        if starter_word and game.tries == 0:
            printv(f"Using starter word '{starter_word}'", verbose)
            guess = starter_word
        else:
            printv("\nSelecting best guess...", verbose)
            guess = get_best_guess(
                valid_guesses=db.UNACCENTED_VALID_SOLUTIONS, 
                valid_solutions=possible_solutions,
                verbose=False)
        
        response = game.guess_word(guess, verbose)

        possible_solutions = filter_words_after_guess(
            words=possible_solutions,
            guess=guess, 
            response=response)
        if len(possible_solutions) < 15:
            print(f"Possible solutions: {possible_solutions}")
        printv(f"Number of possible solutions: {len(possible_solutions)}...")
    
    end = time.time()
    elapsed_time = end - start

    return game.tries, game.reward, elapsed_time

def collect_data():
    data = []
    total_time = 0

    for i, solution in enumerate(db.ACCENTED_VALID_SOLUTIONS):
        tries, reward, elapsed_time = run_game(
            solution=solution,
            starter_word="sério",
            verbose=False)
        printv(f"#({i} / {len(db.ACCENTED_VALID_SOLUTIONS)}) \t '{solution}' \t result {reward} " + \
            f"after {tries} tries. Elapsed time: {elapsed_time} seconds.")
        
        total_time += elapsed_time
        data.append((solution, tries, reward, elapsed_time))
    
    solution, tries, rewards, elapsed_times = zip(*data)
    printv(f"Average number of tries: {np.mean(tries)}")
    printv(f"Average time: {'{:.3f}'.format(np.mean(elapsed_times))} seconds")
    printv(f"Success rate: {np.mean(rewards) * 100 } %")
    printv(f"Total time elapsed: {'{:.3f}'.format(total_time)} seconds")

    with open("overall_solution_data_complete.json", 'w', encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    # collect_data()
    run_game("jatos", "serio", True)