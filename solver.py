from distutils.util import strtobool
import database as db
import strategy
import time
from rich import print

if __name__ == "__main__":
    valid_solutions = db.UNACCENTED_VALID_SOLUTIONS

    for turn in range(1, 7):
        print("")
        print(f"Number of valid solutions: {len(valid_solutions)}...")

        start_time = time.time()
        if turn == 1:
            guess = "serio"
        else:
            guess = strategy.get_best_guess(
                valid_guesses=db.UNACCENTED_VALID_SOLUTIONS,
                valid_solutions=valid_solutions)
        end_time = time.time()
        elapsed_time = '{:.3f}'.format(end_time - start_time)
        print(f"Use guess: '{guess}'. (Time elapsed: {elapsed_time} seconds)")

        response = input("Game response: ")
        response = [int(x) for x in response]

        valid_solutions = strategy.filter_words_after_guess(
            words=valid_solutions,
            guess=guess, 
            response=response)
        
        if len(valid_solutions) < 10:
            print(f"Possible solutions: {valid_solutions}")
        
        if len(valid_solutions) == 1:
            solution = valid_solutions[0]
            if response == [1, 1, 1, 1, 1]:
                number_of_tries = turn
            else:
                number_of_tries = turn + 1
            print("")
            print(f"Found solution '{solution}' after {number_of_tries} turns.")
            break
    
    print(f"\nSee you tomorrow!")
