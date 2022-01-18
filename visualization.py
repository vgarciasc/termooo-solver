import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import database as db
import strategy
import time
import pdb
import json
from game import Game
from itertools import product
from utils import printv, remove_accents

def get_starter_words_data(valid_guesses, valid_solutions):
    possible_responses = list(product([0, 1, 2], repeat=db.WORD_SIZE))
    
    start = time.time()
    data = []

    for i, guess in enumerate(valid_guesses):
        score = 0
        for response in possible_responses:
            solutions = strategy.filter_words_after_guess(
                words=valid_solutions,
                guess=remove_accents(guess),
                response=response)
            score += len(solutions)**2 / len(valid_solutions)
        printv(f"#({i} / {len(valid_guesses)}): \t Word '{guess}' has score {score}")

        data.append((guess, score))
    
    end = time.time()
    print(f"Elapsed time: {'{:.3f}'.format(end - start)} seconds")

    return data

if __name__ == "__main__":
    data = get_starter_words_data(
        db.ACCENTED_VALID_SOLUTIONS,
        db.UNACCENTED_VALID_SOLUTIONS)

    # with open("starter_words_popular.json", 'r', encoding="utf-8") as f: 
    #     data = json.load(f)

    # with open("starter_words_popular.json", 'w', encoding="utf-8") as f:
    #     json.dump(data, f, indent=2, ensure_ascii=False)

    data.sort(key=lambda x : x[1])
    data = data[:25]

    clist = [(0.0, "lightsteelblue"), (1.0, "royalblue")]
    rvb = mcolors.LinearSegmentedColormap.from_list("", clist)

    guesses, scores = zip(*data)
    cmap = rvb((scores - np.min(scores))/(np.max(scores) - np.min(scores)))
    plt.bar(guesses, scores, color=cmap, edgecolor='black')
    plt.xticks(rotation=90)
    plt.title("50 melhores palavras iniciais para o term.ooo (conjunto completo)")
    plt.ylabel("Média de palavras restantes")
    plt.show()

    pdb.set_trace()