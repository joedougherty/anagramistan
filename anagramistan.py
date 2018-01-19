from copy import deepcopy
from collections import OrderedDict
from itertools import combinations
import random


LETTERS = {'a': 9,
           'b': 2,
           'c': 2,
           'd': 4,
           'e': 12,
           'f': 2,
           'g': 3,
           'h': 2,
           'i': 9,
           'j': 1,
           'k': 1,
           'l': 4,
           'm': 2,
           'n': 6,
           'o': 8,
           'p': 2,
           'q': 1,
           'r': 6,
           's': 4,
           't': 6,
           'u': 4,
           'v': 2,
           'x': 1,
           'y': 2,
           'z': 1}


def probability_mass_fn(freq_dict):
    pmf_as_dict = {}
    total_occurrences = sum(freq_dict.values())

    for k, v in freq_dict.items():  
        pmf_as_dict[k] = freq_dict[k]/total_occurrences

    return OrderedDict(sorted(pmf_as_dict.items(), key=lambda x: x[1]))


def weighted_choice(prob_dict):
    random_value = random.random()
    total = 0

    for k, v in prob_dict.items():
        total += v
        if random_value <= total:
            return k

    raise Exception("Something is awry in `weighted_choice`")


def draw_letters(num=7):
    bag_of_letters = deepcopy(LETTERS)

    random_letters = []
    for i in range(0, num):
        new_letter = weighted_choice(probability_mass_fn(bag_of_letters))
        random_letters.append(new_letter)
        bag_of_letters[new_letter] -= 1

    return random_letters


def lexical_hash(word):
    letters = [i for i in word]
    letters.sort()
    return ''.join(letters)


def normalize_words(path_to_dict_file):
    def clean(word):
        if "'" in word:
            return False

        word = word.strip()
        word = word.lower()
        return word

    with open(path_to_dict_file, 'r') as word_file:
        words = [clean(word) for word in word_file.readlines()]
            
    return [w for w in words if w != False]


KNOWN_WORDS = normalize_words('/usr/share/dict/words')

WORDS_BY_LEN = {}
for i in range(3, 7):
    WORDS_BY_LEN[i] = [w for w in KNOWN_WORDS if len(w) == i]


def find_n_letter_anagrams(letters, n):
    anagrams = set()
    for i in combinations(letters, n):
        for word in WORDS_BY_LEN[n]:
            if lexical_hash(i) == lexical_hash(word):
                anagrams.add(word)
    return anagrams


def find_anagrams(letters):
    found = []
    for n in range(3, 7):
        n_letter_anagrams = list(find_n_letter_anagrams(letters, n))
        n_letter_anagrams.sort()
        found = found + n_letter_anagrams
    return found
