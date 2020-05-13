import itertools
import random
import twl
from collections import Counter
import root
import time

import pygame, sys
from pygame.locals import *

FPS = 30
WINDOWWIDTH = 640
WINDOWHEIGHT = 640

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
NAVYBLUE = (60, 60, 100)

BGCOLOR = WHITE
TEXTCOLOR = BLACK

print_check = False

letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
letter_freq = {'A': 13, 'B': 3, 'C': 3, 'D': 6, 'E': 18, 'F': 3, 'G': 4, 'H':3, 'I':12, 'J':2, 'K':2, 'L':5, 'M':3, 'N':8, 'O':11, 'P':3, 'Q':2, 'R':9, 'S':6, 'T':9, 'U': 6, 'V':3, 'W':3, 'X':2, 'Y':3, 'Z':2}
letter_keys = [K_a, K_b, K_c, K_d, K_e, K_d, K_e, K_f, K_g, K_h, K_i, K_j, K_k, K_l, K_m, K_n, K_o, K_p, K_q, K_r, K_s, K_t, K_u, K_t, K_v, K_w, K_x, K_y, K_z]

#  ________
# | LAYOUT |
#  --------

# 'Current'
font_current = 'freesansbold.ttf'
size_current = 32
color_current = BLACK
x_current = 10
y_current = 20

# Tiles
font_tile = 'freesansbold.ttf'
size_tile = 32
color_tile = BLACK
x_tile_0 = 150
y_tile_0 = 20
x_gap_tile = 30
y_gap_tile = 50

# 'Your Words'
font_your = 'freesansbold.ttf'
size_your = 32
color_your = BLACK
x_your = 10
y_your = 100
y_gap_your = 50

# Words
font_words = 'freesansbold.ttf'
size_words = 32
color_words = BLACK
x_words = 10
y_words = y_your + y_gap_your
x_gap_words = 100
y_gap_words = 50

# Guess
font_guess = 'freesansbold.ttf'
size_guess = 32
color_guess = BLACK
x_guess = 10
y_guess = 400

# Status
font_status = 'freesansbold.ttf'
size_status = 32
color_status = BLACK
x_status = 10
y_status = 500


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
        self.playerwords_list = []

        self.fontObj_current = pygame.font.Font(font_current, size_current)
        self.fontObj_tile = pygame.font.Font(font_tile, size_tile)
        self.fontObj_your = pygame.font.Font(font_your, size_your)
        self.fontObj_words = pygame.font.Font(font_words, size_words)
        self.fontObj_guess = pygame.font.Font(font_guess, size_guess)
        self.fontObj_status = pygame.font.Font(font_status, size_status)

        self.guess = ''
        self.previous_guess = ''

        self.status = ''

    def flip(self):
        if not self.tiles:
            self.status = 'Banana is empty!'
            self.__display_text(self.status, x_status, y_status, self.fontObj_status, color_status)
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

        # Turn list into string
        str = ''
        str = str.join(list1)

        return str



    def __display_text(self, text, x, y, fontObj, color):
        textSurfaceObj = fontObj.render(text, True, color)
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.topleft = (x, y)
        DISPLAYSURF.blit(textSurfaceObj, textRectObj)


    def take(self, candidate):

        # First check if has 3 letters
        if len(candidate) < 3:
            self.previous_guess = self.guess
            self.status = "Word is too short! " + f"({self.previous_guess})"
            self.guess = ''
            return None

        # First check if a word
        if len(candidate) < 10:
            is_word = twl.check(candidate.lower())
        else:
            is_word = root.merriam_word_check(candidate)
        if not is_word:
            # self.__display_text("Not a word!", 200, 400)
            self.previous_guess = self.guess
            self.status = "Not a word! " + f"({self.previous_guess})"
            self.guess = ''
            return None

        error_trivial_extension = False
        error_tiles = False

        steal_type = None

        merriam_candidate = root.merriam_strip(candidate)

        for i, word in enumerate(self.playerwords):
            # First, check if candidate is a superset of the current word
            if self.__superset(candidate, word, strict=True):

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
                        taken_i = i

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

            self.playerwords_list[taken_i] = candidate

            for letter in taken_word:
                candidate_list.remove(letter)
            for letter in candidate_list:
                self.current.remove(letter)
            self.previous_guess = self.guess
            self.status = "Success! " + f"({self.previous_guess})"

        elif steal_type == 'middle':
            candidate_list = list(candidate)
            for letter in candidate_list:
                self.current.remove(letter)
            self.playerwords.update({candidate: merriam_candidate})
            self.playerwords_list.append(candidate)

            self.previous_guess = self.guess
            self.status = "Success! " + f"({self.previous_guess})"
        elif error_trivial_extension:
            self.previous_guess = self.guess
            self.status = "Same root! " + f"({self.previous_guess})"
        elif error_tiles:
            self.previous_guess = self.guess
            self.status = "Tiles aren't there! " + f"({self.previous_guess})"
        else:
            self.previous_guess = self.guess
            self.status = "Tiles aren't there! " + f"({self.previous_guess})"
        self.guess = ''


    def __display_status(self):
        self.__display_text(self.status, x_status, y_status, self.fontObj_status, color_status)

    def printstatus(self):

        y_tile = y_tile_0
        x_tile = x_tile_0

        self.__display_text('Current: ', x_current, y_current, self.fontObj_current, color_current)

        """
        currentSurfaceObj = self.fontObj.render('Current:', True, BLACK)
        currentRectObj = currentSurfaceObj.get_rect()
        currentRectObj.topleft = (x_current, y_current)
        DISPLAYSURF.blit(currentSurfaceObj, currentRectObj)
        """

        for i, tile in enumerate(self.current):
            x_tile = x_tile + x_gap_tile

            self.__display_text(tile, x_tile, y_tile, self.fontObj_tile, color_tile)

            """
            tileSurfaceObj = self.fontObj.render(tile, True, BLACK)
            tileRectObj = tileSurfaceObj.get_rect()
            tileRectObj.topleft = (x_tile, y_tile)
            DISPLAYSURF.blit(tileSurfaceObj, tileRectObj)
            """

            if i % 10 == 9:
                y_tile = y_tile + y_gap_tile
                x_tile = x_tile_0



        self.__display_text('Your Words: ', x_your, y_your, self.fontObj_your, color_your)

        """
        wordsSurfaceObj = self.fontObj.render('Your Words:', True, BLACK)
        wordsRectObj = wordsSurfaceObj.get_rect()
        wordsRectObj.topleft = (x_words, y_words)
        DISPLAYSURF.blit(wordsSurfaceObj, wordsRectObj)
        """

        x_words_local = x_words
        y_words_local = y_words

        for i, word in enumerate(self.playerwords_list):

            self.__display_text(word, x_words_local, y_words_local, self.fontObj_words, color_words)


            """
            wordSurfaceObj = self.fontObj.render(word, True, BLACK)
            wordRectObj = wordSurfaceObj.get_rect()
            wordRectObj.topleft = (x_words, y_words)
            DISPLAYSURF.blit(wordSurfaceObj, wordRectObj)
            """

            if i % 10 == 9:
                x_words_local = x_words_local + x_gap_words

            y_words_local = y_words_local + y_gap_words


        self.__display_text('Guess: ' + self.guess, x_guess, y_guess, self.fontObj_guess, color_guess)

        """
        guessSurfaceObj = self.fontObj.render('Guess: ' + self.guess, True, BLACK)
        guessRectObj = guessSurfaceObj.get_rect()
        guessRectObj.topleft = (x_guess, y_guess)
        DISPLAYSURF.blit(guessSurfaceObj, guessRectObj)
        """

        self.__display_status()

def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    pygame.display.set_caption('Anagrams')

    game = banana()

    while True: # main game loop
        DISPLAYSURF.fill(BGCOLOR)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    if game.guess == '':
                        pass
                    else:
                        game.guess = game.guess[:-1]

                elif event.key == K_SPACE:
                    pass



                elif event.key == K_RETURN:
                    # if Return and no guess is present, then flip next tile
                    if game.guess == '':
                        game.flip()
                    else:
                        game.take(game.guess.upper())

                elif event.key in letter_keys:
                    game.guess = game.guess + event.unicode.upper()



        game.printstatus()
        pygame.display.update()


if __name__ == "__main__":
    # execute only if run as a script
    main()

