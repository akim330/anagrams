import itertools
import random
import twl
from collections import Counter
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import root
import time

print_check = False

letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
letter_freq = {'A': 13, 'B': 3, 'C': 3, 'D': 6, 'E': 18, 'F': 3, 'G': 4, 'H':3, 'I':12, 'J':2, 'K':2, 'L':5, 'M':3, 'N':8, 'O':11, 'P':3, 'Q':2, 'R':9, 'S':6, 'T':9, 'U': 6, 'V':3, 'W':3, 'X':2, 'Y':3, 'Z':2}

def listToString(s):
    str = ''
    return(str.join(s))

def output_html(url):
    raw_html = simple_get(url)
    html = BeautifulSoup(raw_html, 'html.parser')
    return html

def merriam_word_check(word):
    start_merriam_word_check = time.time()
    url_merriam = 'https://www.merriam-webster.com/dictionary/' + word
    raw_html = simple_get(url_merriam)
    html = BeautifulSoup(raw_html, 'html.parser')
    titles = html.find_all('title')

    titles_list = []
    for title in titles:
        titles_list.append(title.text.strip().split(' | ')[0])

    is_proper_noun = [not word.islower() for word in titles_list]
    end_merriam_word_check = time.time()
    if print_check:
        print(f"Merriam word check time: {end_merriam_word_check - start_merriam_word_check} seconds")
    return not all(is_proper_noun)

class banana(object):
    def __init__(self):

        # -------- #
        #  BANANA  #
        # -------- #
        self.tiles = []
        for letter in letters:
            self.tiles = self.tiles + list(itertools.repeat(letter, letter_freq[letter]))

        random.shuffle(self.tiles)

        self.current = []

        self.playerwords = {}


    def flip(self):
        if not self.tiles:
            print("Banana is empty!")
            return None

        last = self.tiles.pop()
        self.current.append(last)

    def current(self):
        print(self.current)

    def __superset(self, word1, word2, strict = False):
        # Can word 1 take word 2?
        word1_counter = Counter(word1)
        word2_counter = Counter(word2)

        if strict:
            return (word1_counter - word2_counter and not (word2_counter - word1_counter))
        else:
            return (word1_counter - word2_counter and not(word2_counter - word1_counter)) or (not (word1_counter - word2_counter) and not (word2_counter - word1_counter))

    def __subtract(self, word1, word2):
        # Subtract word2 from word1 (e.g. 'test' - 'tst' = 'e')

        list1 = list(word1)
        for letter in word2:
            list1.remove(letter)

        return listToString(list1)

    def __root(self,word):
        root = word
        at_least_four = len(root) > 3

        last = word[-1]
        last_two = word[-2:]
        last_three = word[-3:]
        if at_least_four:
            last_four = word[-4:]

        one_letter_suffixes = ['I','S','Y']
        two_letter_suffixes = ['ED','ER','LY']
        three_letter_suffixes = ['ING','EST','IST']
        four_letter_suffixes = ['ABLE','TION','SION']

        if at_least_four and (last_four in four_letter_suffixes):
            root = root[:-4]
        elif last_three in three_letter_suffixes:
            root = root[:-3]
        elif last_two in two_letter_suffixes:
            root = root[:-2]
        elif last in one_letter_suffixes:
            root = root[:-1]

        at_least_one = len(root) > 0
        at_least_two = len(root) > 1
        at_least_three = len(root) > 2
        at_least_four = len(root) > 3

        if at_least_one:
            first = root[:1]
        if at_least_two:
            first_two = root[:2]
        if at_least_three:
            first_three = root[:3]
        if at_least_four:
            first_four = root[:4]

        one_letter_prefixes = ['A','E']
        two_letter_prefixes = ['UN','RE','DE','IN']
        three_letter_prefixes = ['OUT']
        four_letter_prefixes = ['ANTI','OVER']

        if at_least_four and (first_four in four_letter_prefixes):
            root = root[4:]
        elif at_least_three and (first_three in three_letter_prefixes):
            root = root[3:]
        elif at_least_two and (first_two in two_letter_prefixes):
            root = root[2:]
        elif at_least_one and (first in one_letter_prefixes):
            root = root[1:]

        return root


    def take(self, candidate):

        # First check if has 3 letters
        if len(candidate) < 3:
            print("Word is too short!")
            return None

        # First check if a word
        if len(candidate) < 10:
            is_word = twl.check(candidate.lower())
        else:
            is_word = merriam_word_check(candidate)
        if not is_word:
            print("Not a word!")
            return None

        error_trivial_extension = False
        error_tiles = False

        steal_type = None

        merriam_candidate = root.merriam_strip(candidate)

        for i, word in enumerate(self.playerwords):
            # First, check if candidate is a superset of the current word
            if self.__superset(candidate, word, strict=True):
                # root_candidate = self.__root(candidate)
                # root_word = self.__root(word)

                # Then, check if the tiles needed to make candidate are in the middle
                if not self.__superset(self.current, self.__subtract(candidate, word)):
                    error_tiles = True
                else:
                    merriam_word = self.playerwords[word]

                    root_candidate = root.lookup(merriam_candidate)
                    root_word = root.lookup(merriam_word)
                    # merriam_root_check = root.merriam_root_check(candidate, word)

                    try:
                        root_overlap = any(x in root_candidate for x in root_word)
                    except TypeError:
                        root_overlap = False

                    if (root_candidate is None or root_word is None) and (merriam_candidate == merriam_word):
                        error_trivial_extension = True
                    elif root_overlap or (merriam_candidate == merriam_word):
                        error_trivial_extension = True
                    else:
                        steal_type = 'steal'
                        taken_word = word

                # elif word in candidate and any(x in root.lookup(candidate) for x in root.lookup(word)):
                     # error_trivial_extension = True

                # If all of those check out, then it's a steal and record which word is being stolen

        if steal_type is None:
            if self.__superset(self.current, candidate, strict=False):
                steal_type = 'middle'

        if steal_type == 'steal':
            candidate_list = list(candidate)

            del self.playerwords[taken_word]
            self.playerwords.update({candidate: merriam_candidate})

            for letter in taken_word:
                candidate_list.remove(letter)
            for letter in candidate_list:
                self.current.remove(letter)
            self.printstatus()
        elif steal_type == 'middle':
            candidate_list = list(candidate)
            for letter in candidate_list:
                self.current.remove(letter)
            self.playerwords.update({candidate: merriam_candidate})
            self.printstatus()
        elif error_trivial_extension:
            print("Same root!")
        elif error_tiles:
            print("Tiles aren't there!")
        else:
            print("Tiles aren't there!")

    def printstatus(self):
        print("\nCurrent tiles: ")
        for i, tile in enumerate(self.current):
            print(tile, end ='  ')
            if i % 10 == 9:
                print("\n")
        print('\n')
        print("Your words: ")
        for i, word in enumerate(self.playerwords):
            print(word, end= '   ')
            if i % 5 == 4:
                print("\n")
        print('\n')

def main():
    print("Welcome to Anagrams")
    print("Press Enter to start the game")
    input()

    game = banana()

    while True:
        quit = False
        game.printstatus()
        while True:
            key = input("Enter a word or press \'Return\' to flip:\n")
            if key == '':
                game.flip()
                break
            elif key == 'quit':
                quit = True
                break
            else:
                game.take(key.upper())

        if quit:
            print("Quitting game...")
            break

if __name__ == "__main__":
    # execute only if run as a script
    main()

