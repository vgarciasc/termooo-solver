from rich import print

def remove_accent(letter):
    accent_map = {
        "á": "a", "â": "a", "ã": "a", "à": "a", "é": "e", "ê": "e", "è": "e", 
        "í": "i", "ì": "i", "ï": "i", "ó": "o", "ò": "o", "ô": "o", "õ": "o",
        "a": "a", "b": "b", "c": "c", "d": "d", "e": "e", "f": "f", "g": "g",
        "h": "h", "i": "i", "j": "j", "k": "k", "l": "l", "m": "m", "n": "n",
        "o": "o", "p": "p", "q": "q", "r": "r", "s": "s", "t": "t", "u": "u",
        "v": "v", "w": "w", "x": "x", "y": "y", "z": "z", "ç": "c", "ú": "u",
        "û": "u", "ü": "u" }
    return accent_map[letter]

def remove_accents(input_str):
    return "".join([remove_accent(c) for c in input_str])

def printv(str, verbose=True):
    if verbose:
        print(str)