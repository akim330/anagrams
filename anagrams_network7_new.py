import itertools
import random
import twl
from collections import Counter
import time
from network_new import Network  # UPDATE
import ast
import datetime
from itertools import combinations

import api

import pygame, sys
from pygame.locals import *

print_check = True
time_check = False
no_prefix_suffix = True

not_allowed_prefixes = ['UN', 'RE']
not_allowed_suffixes = ['S', 'ED', 'D', 'ES', 'ER', 'R', 'OR', 'ING', 'EST', 'IEST', 'LY', 'TION', 'SION']

word_add_twl = ['acai', 'roo', 'tix']

FPS = 30
WINDOWWIDTH = 640
WINDOWHEIGHT = 640

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
NAVYBLUE = (60, 60, 100)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

BGCOLOR = WHITE
TEXTCOLOR = BLACK

flip_delay = 1000 # Delay before flip in ms
flip_status = ''

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


# Ready Flip
font_flip = 'freesansbold.ttf'
size_flip = 20
color_flip = BLACK
x_flip = 20
y_flip = 60

# Tiles
font_tile = 'freesansbold.ttf'
size_tile = 32
color_tile = BLACK
x_tile_0 = 150
y_tile_0 = 38
x_gap_tile = 30
y_gap_tile = 50

# 'Your Words'
font_your = 'freesansbold.ttf'
size_your = 32
color_your = BLACK
x_your = 10
y_your = 100
y_gap_your = 50

# Your Words
font_words = 'freesansbold.ttf'
size_words = 32
color_words = BLACK
x_words = 10
y_words = y_your + y_gap_your
x_gap_words = 150
y_gap_words = 50

# 'Opponent's Words'
font_opp = 'freesansbold.ttf'
size_opp = 32
color_opp = BLACK
x_opp = 300
y_opp = 100
y_gap_opp = 50

# Opponent's Words
font_opp_words = 'freesansbold.ttf'
size_opp_words = 32
color_opp_words = BLACK
x_opp_words = 300
y_opp_words = y_opp + y_gap_opp
x_gap_opp_words = 150
y_gap_opp_words = 50

color_taken = BLUE

# Guess
font_guess = 'freesansbold.ttf'
size_guess = 32
color_guess = BLACK
x_guess = 10
y_guess = 500

# Status
font_status = 'freesansbold.ttf'
size_status = 24
color_status = BLACK
x_status = 10
y_status = 550

def numwords_to_fontsize(numwords):
    if numwords <= 6:
        return int(size_words/1.25), int(y_gap_words/1.25)
    elif 6 < numwords <= 10:
        return int(size_words / 1.75), int(y_gap_words / 1.75)
    elif 10 < numwords <= 20:
        return int(size_words / 2), int(y_gap_words / 2)
    elif 20 < numwords <= 50:
        return int(size_words / 3), int(y_gap_words / 3)

def numtiles_to_fontsize(numtiles):
    if numtiles <= 10:
        return size_tile, y_gap_tile, x_gap_tile
    elif 10 < numtiles <= 40:
        return int(size_tile / 1.5), int(y_gap_tile / 1.5), int(x_gap_tile / 1.5)
    elif 40 < numtiles <= 60:
        return int(size_tile / 2), int(y_gap_tile / 2), int(x_gap_tile / 2)
    elif 60 < numtiles <= 144:
        return int(size_tile / 4), int(y_gap_tile / 4), int(x_gap_tile / 4)

def try_parsing_date(text):
    for fmt in ('%Y-%m-%d %H:%M:%S.%f', '%Y-%m-%d %H:%M:%S'):
        try:
            return datetime.datetime.strptime(text, fmt)
        except ValueError:
            pass
    raise ValueError('no valid date format found')

class banana(object):
    def __init__(self):

        # -------- #
        #  BANANA  #
        # -------- #


        self.take_dict = {'new_word': '', 'etyms_new_word': '', 'take_time': 0,
                          'used_tiles': [], 'self_taken_words': [], 'opp_taken_words': [],
                          'self_taken_is':[], 'opp_taken_is':[]}

        self.take_dict_past = {'new_word': '', 'etyms_new_word': '', 'take_time': 0,
                          'used_tiles': [], 'self_taken_words': [], 'opp_taken_words': [],
                          'self_taken_is':[], 'opp_taken_is':[]}

        self.flip_dict = {'flip_status': '', 'flip_waiting': False,
                                'scheduled_flip': 0}


        # Game state
        self.tiles = []
        self.current = []
        self.playerwords = {}
        self.playerwords_list = []
        self.player2words = {}
        self.player2words_list = []
        self.guess = ''
        self.previous_guess = ''
        self.status = ''
        self.last_update = 0
        self.player2_last_update = 0
        self.mode = 'waiting'
        self.frozen = False
        self.take_waiting = False
        self.i_flipped = False

        # Previous game state
        self.tiles_past = []
        self.current_past = []
        self.playerwords_past = {}
        self.playerwords_list_past = []
        self.player2words_past = {}
        self.player2words_list_past = []

        # Things in flip timer dict
        """
        self.flip_waiting = False
        self.time_flip = pygame.time.get_ticks()
        """

        # things in the take dict
        """
        self.middle_used = []
        self.taken_word = "\'\'"
        self.take_start_time = 0
        self.used_tiles = []
        """

        # not added to a dict
        self.player2current = []
        self.player2tiles = []
        self.take_end_time = 0

        self.who_took = ''
        self.taken_i = -1
        self.new_word_i = -1
        self.new_word = ''

        # Graphics
        self.fontObj_current = pygame.font.Font(font_current, size_current)
        self.fontObj_tile = pygame.font.Font(font_tile, size_tile)
        self.fontObj_your = pygame.font.Font(font_your, size_your)
        self.fontObj_words = pygame.font.Font(font_words, size_words)
        self.fontObj_guess = pygame.font.Font(font_guess, size_guess)
        self.fontObj_status = pygame.font.Font(font_status, size_status)
        self.fontObj_flip = pygame.font.Font(font_flip, size_flip)
        self.fontObj_opp = pygame.font.Font(font_your, size_your)
        self.fontObj_opp_words = pygame.font.Font(font_words, size_words)

        self.currentSurfObj = self.fontObj_current.render('Current: ', True, color_current)
        self.tilesSurfObj_list = []
        self.yourSurfObj = self.fontObj_your.render('Your Words: ', True, color_your)
        self.playerwordsSurfObj_list = []
        self.oppSurfObj = self.fontObj_opp.render('Opponent\'s Words: ', True, color_opp)
        self.player2wordsSurfObj_list = []
        self.guessSurfObj = self.fontObj_guess.render('Take: ' + self.guess, True, color_guess)
        self.statusSurfObj = self.fontObj_status.render(self.status, True, color_status)
        self.flipSurfObj = self.fontObj_flip.render(self.flip_dict['flip_status'], True, color_flip)

        self.graphics_to_update = []

        self.y_gap_words = y_gap_words
        self.y_gap_opp_words = y_gap_opp_words
        self.x_gap_tile = x_gap_tile
        self.y_gap_tile = y_gap_tile


        # Initialization variables
        self.game_start_time = 0
        self.host = False
        self.seed_set = False
        self.seed = 0

        print("Initializing network")
        # Network
        self.net = Network()

        print("Finished initializing network")

        # For time checks
        self.time_dict = {'loop': 0, 'send_data': 0, 'take': 0, 'update_graphics': 0,
                          'display_graphics': 0, 'send_parse': 0, 'update_players': 0}

        self.last_type = time.time() - 1

        self.same_root_word = ''

        print("gonna do first server update")
        # Perform an initial server update
        self.get_server_update()
        print("finished first server update")

        # If you receive a invalid seed, there's no opponent and you should set the seed yourself
        # If you do receive a valid seed, there's already an opponent and take their seed
        if self.seed_recv < 1:
            self.seed = random.randint(1, 100000)
            self.seed_set = True
        else:
            self.seed = self.seed_recv

        # Set the tiles and shuffle them
        for letter in letters:
            self.tiles = self.tiles + list(itertools.repeat(letter, letter_freq[letter]))
        random.shuffle(self.tiles)

    def send_data(self):
        if time_check:
            start_time = time.time()
        # print(f"NET ID: {self.net.id}")
        data = str(self.net.id) + "|" + str(self.seed) + "|" + str(self.last_update) + "|" + str(self.take_dict) + "|" + str(self.flip_dict)
        # print(f"DATA TO SEND: {data}")
        reply = self.net.send(data)
        # print(f"DATA RECEIVED: {reply}")

        if time_check:
            end_time = time.time()
            self.time_dict['send_data'] = end_time - start_time

        return reply

    @staticmethod
    def parse_data(data):
        try:
            # print(f"DATA TO PARSE: {data}")
            split = data.split('|')
            net_id = ast.literal_eval(split[0])
            seed_recv = ast.literal_eval(split[1])
            last_update_recv = ast.literal_eval(split[2])
            take_dict_recv = ast.literal_eval(split[3])
            flip_timer_dict_recv = ast.literal_eval(split[4])

            return net_id, seed_recv, last_update_recv, take_dict_recv, flip_timer_dict_recv
        except:
            return -1, 0, {}, {}, {}

    def flip(self):
        if not self.tiles:
            self.status = f"No more tiles! Your score: {sum([len(i) for i in self.playerwords_list])}, Opponent's score: {sum([len(i) for i in self.player2words_list])}"
            self.graphics_to_update = self.graphics_to_update + ['status']
            return None

        # self.last_update = time.time()
        last = self.tiles.pop()
        self.current.append(last)
        self.flip_dict['flip_status'] = ''
        self.flip_dict['flip_waiting'] = False

        self.graphics_to_update = self.graphics_to_update + ['tiles', 'flip']

    def __cleared_take_dict(self):
        cleared_dict = ({'new_word': '', 'etyms_new_word': '', 'take_time': 0,
                          'used_tiles': [], 'self_taken_words': [], 'opp_taken_words': [],
                          'self_taken_is': [], 'opp_taken_is': []}).copy()

        return cleared_dict

    def __is_cleared(self, dict):
        return dict['take_time'] == 0

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

    def __check_steal(self, candidate, etyms_candidate):
        # Check whether a steal happens
        # Input a candidate word (i.e. guess), its merriam stripped version,
        # a dictionary with the words to take from (plus their merriam stripped versions) and
        # a Boolean indicating whether we're checking a steal from the opponent

        # Returns whether stolen, what kind of steal or error, the taken word, and index of taken word

        # Set event_type to 'tiles' arbitrarily
        error_type = 'tiles'

        # Dictionary with all the words that need middle tiles, to check if multi-word steal is possible
        # Each value is a tuple (index, bool indicating if self not opp, word_etym)
        lacks_middle_tiles = {}

        # First check if can steal opponent's word
        for i, word in enumerate(self.player2words_list):
            # First, check if candidate is a superset of the current word
            if self.__superset(candidate, word, strict=True):

                # Then, check if the tiles needed to make candidate are in the middle
                used_tiles = self.__subtract(candidate, word)
                if not self.__superset(self.current, used_tiles):
                    if error_type != 'trivial':
                        error_type = 'tiles'
                    lacks_middle_tiles[word] = (i, False, self.player2words[word])
                else:
                    etyms_word = self.player2words[word]

                    try:
                        # Check for any common roots. If etymonline returns nothing, then assume there are no
                        # common roots
                        root_overlap = any(x in etyms_candidate for x in etyms_word)
                    except TypeError:
                        root_overlap = False

                    if root_overlap:
                        self.same_root_word = word
                        self.root = set(etyms_candidate).intersection(etyms_word).pop()
                        error_type = 'trivial'
                    else:
                        taken_word = word
                        taken_i = i
                        return True, used_tiles, [], [taken_word], [], [taken_i]

        # Check if can steal own word
        for i, word in enumerate(self.playerwords_list):
            # First, check if candidate is a superset of the current word
            if self.__superset(candidate, word, strict=True):

                # Then, check if the tiles needed to make candidate are in the middle
                used_tiles = self.__subtract(candidate, word)
                if not self.__superset(self.current, used_tiles):
                    if error_type != 'trivial':
                        error_type = 'tiles'
                    lacks_middle_tiles[word] = (i, True, self.playerwords[word])
                else:
                    etyms_word = self.playerwords[word]

                    try:
                        # Check for any common roots. If etymonline returns nothing, then assume there are no
                        # common roots
                        root_overlap = any(x in etyms_candidate for x in etyms_word)
                    except TypeError:
                        root_overlap = False

                    if root_overlap:
                        self.same_root_word = word
                        self.root = set(etyms_candidate).intersection(etyms_word).pop()
                        error_type = 'trivial'
                    else:
                        taken_word = word
                        taken_i = i
                        return True, used_tiles, [taken_word], [], [taken_i], []

        # Check if can steal middle word
        if self.__superset(self.current, candidate, strict=False):
            return True, list(candidate), [], [], [], []

        # Check for multi-word steals
        if len(lacks_middle_tiles) >= 2:
            for word1, word2 in combinations(lacks_middle_tiles, 2):
                if self.__superset(candidate, word1 + word2, strict=False):

                    # Then, check if the tiles needed to make candidate are in the middle
                    used_tiles = self.__subtract(candidate, word1 + word2)
                    if self.__superset(self.current, used_tiles):
                        etyms_word1 = lacks_middle_tiles[word1][2]
                        etyms_word2 = lacks_middle_tiles[word2][2]

                        try:
                            # Check for any common roots. If etymonline returns nothing, then assume there are no
                            # common roots
                            root_overlap1 = any(x in etyms_candidate for x in etyms_word1)
                        except TypeError:
                            root_overlap1 = False
                        try:
                            root_overlap2 = any(x in etyms_candidate for x in etyms_word2)
                        except TypeError:
                            root_overlap2 = False

                        if root_overlap1:
                            self.same_root_word = word1
                            self.root = set(etyms_candidate).intersection(etyms_word1).pop()
                            error_type = 'trivial'
                        elif root_overlap2:
                            self.same_root_word = word2
                            self.root = set(etyms_candidate).intersection(etyms_word2).pop()
                            error_type = 'trivial'

                        else:
                            self_taken_words = [word for word in [word1, word2] if lacks_middle_tiles[word][1]]
                            opp_taken_words = [word for word in [word1, word2] if not lacks_middle_tiles[word][1]]

                            self_taken_is = [lacks_middle_tiles[word][0] for word in self_taken_words]
                            opp_taken_is = [lacks_middle_tiles[word][0] for word in opp_taken_words]

                            return True, used_tiles, self_taken_words, opp_taken_words, self_taken_is, opp_taken_is

        if error_type == 'trivial':
            self.status = "Same root! " + f"({self.same_root_word} and {candidate} share root {self.root})"
            self.graphics_to_update = self.graphics_to_update + ['status', 'guess']
            return False, [], [], [], []
        elif error_type == 'tiles':
            self.status = "Tiles aren't there! " + f"({candidate})"
            self.graphics_to_update = self.graphics_to_update + ['status', 'guess']
            return False, [], [], [], []

    def take(self, candidate):
        self.take_dict['used_tiles'] = []

        if time_check:
            start_time = time.time()

        self.take_dict['take_time'] = time.time()

        # First check if has 3 letters
        if len(candidate) < 3:
            self.status = "Word is too short! " + f"({candidate})"
            self.guess = ''
            self.graphics_to_update = self.graphics_to_update + ['status', 'guess']
            return None

        # Then check if a word
        if len(candidate) < 10:
            candidate_lower = candidate.lower()
            is_word = twl.check(candidate_lower) or candidate_lower in word_add_twl
        else:
            is_word = api.get_word_data(candidate)
        if not is_word:
            # self.__display_text("Not a word!", 200, 400)
            self.status = "Not a word! " + f"({candidate})"
            self.guess = ''
            self.graphics_to_update = self.graphics_to_update + ['status', 'guess']
            return None

        # If no prefixes and suffixes rule, check that
        if no_prefix_suffix:
            has_prefix_suffix, prefix, suffix = api.get_prefix_suffix(candidate)
            # print(f"Stuff: {has_prefix_suffix}, {prefix}, {suffix}")
            # print(f"{prefix in not_allowed_prefixes}, {suffix in not_allowed_suffixes}")
            if has_prefix_suffix and (prefix in not_allowed_prefixes or suffix in not_allowed_suffixes):
                self.status = "Prefix / suffix not allowed!"
                self.guess = ''
                self.graphics_to_update = self.graphics_to_update + ['status', 'guess']
                return None

        etyms_candidate = api.get_etym(candidate)

        is_taken, used_tiles, self_taken_words, opp_taken_words, self_taken_is, opp_taken_is = self.__check_steal(candidate, etyms_candidate)

        if is_taken:
            self.take_dict['new_word'] = candidate
            self.take_dict['etyms_new_word'] = etyms_candidate
            self.take_dict['take_time'] = self.take_dict['take_time']
            self.take_dict['used_tiles'] = used_tiles
            self.take_dict['self_taken_words'] = self_taken_words
            self.take_dict['opp_taken_words'] = opp_taken_words
            self.take_dict['self_taken_is'] = self_taken_is
            self.take_dict['opp_taken_is'] = opp_taken_is

            self.take_waiting = True
            self.take_waiting_time = time.time()

            # Make a copy of current game state in case we need to backtrack
            self.tiles_past = self.tiles.copy()
            self.current_past = self.current.copy()
            self.playerwords_past = self.playerwords.copy()
            self.playerwords_list_past = self.playerwords_list.copy()
            self.player2words_past = self.player2words.copy()
            self.player2words_list_past = self.player2words_list.copy()

        if self.mode == 'solo':
            self.update_take('self', self.take_dict)


        self.guess = ''
        if time_check:
            end_time = time.time()
            self.time_dict['take'] = end_time - start_time

    def update_take(self, robber, take_dict):
        for letter in take_dict['used_tiles']:
            self.current.remove(letter)

        if robber == 'self':
            self.last_update = take_dict['take_time']

            self.playerwords.update({take_dict['new_word']: take_dict['etyms_new_word']})
            if take_dict['self_taken_is']:
                self.playerwords_list[take_dict['self_taken_is'][0]] = take_dict['new_word']
            else:
                self.playerwords_list.append(take_dict['new_word'])

            # Delete any taken words from own dictionary and list
            for j in range(1, len(take_dict['self_taken_is'])):
                del self.playerwords_list[take_dict['self_taken_is'][j]]

            for word in take_dict['self_taken_words']:
                if word not in self.playerwords_list:
                    del self.playerwords[word]

            # Delete any taken words from opp's dictionary and list
            for j in range(len(take_dict['opp_taken_is'])):
                del self.player2words_list[take_dict['opp_taken_is'][j]]

            for word in take_dict['opp_taken_words']:
                if word not in self.player2words_list:
                    del self.player2words[word]

            if take_dict['self_taken_words'] or take_dict['opp_taken_words']:
                taken_words_string = ' '.join(
                    str(take_dict['self_taken_words'] + take_dict['opp_taken_words']).split("'")[1:-1])
                self.status = "Success! " + f"({taken_words_string} -> {take_dict['new_word']})"
            else:
                self.status = "Success! " + f"({take_dict['new_word']} from the middle)"

        else:
            self.last_update = self.take_dict['take_time']

            self.player2words.update({take_dict['new_word']: take_dict['etyms_new_word']})
            if take_dict['opp_taken_is']:
                self.player2words_list[take_dict['opp_taken_is'][0]] = take_dict['new_word']
            else:
                self.player2words_list.append(take_dict['new_word'])

            # Delete any taken words from own dictionary and list
            for j in range(0, len(take_dict['self_taken_is'])):
                del self.playerwords_list[take_dict['self_taken_is'][j]]

            for word in take_dict['self_taken_words']:
                if word not in self.playerwords_list:
                    del self.playerwords[word]

            # Delete any taken words from opp's dictionary and list
            for j in range(1, len(take_dict['opp_taken_is'])):
                del self.player2words_list[take_dict['opp_taken_is'][j]]

            for word in take_dict['opp_taken_words']:
                if word not in self.player2words_list:
                    del self.player2words[word]

            if take_dict['self_taken_words'] or take_dict['opp_taken_words']:
                taken_words_string = ' '.join(
                    str(take_dict['self_taken_words'] + take_dict['opp_taken_words']).split("'")[1:-1])
                self.status = f"Opponent took {taken_words_string} with {take_dict['new_word']}!"
            else:
                self.status = f"Opponent took {take_dict['new_word']} from the middle!"

        self.graphics_to_update = self.graphics_to_update + ['tiles', 'playerwords', 'player2words',
                                                             'status', 'guess']

        self.graphics_to_update = self.graphics_to_update + ['tiles', 'playerwords', 'player2words',
                                                                     'status', 'guess']

        self.who_took = robber
        self.new_word = take_dict['new_word']

    def update_graphics(self):
        if time_check:
            start_time = time.time()

        if 'flip' in self.graphics_to_update:
            self.flipSurfObj = self.fontObj_flip.render(self.flip_dict['flip_status'], True, color_flip)


        if 'tiles' in self.graphics_to_update:
            self.tilesSurfObj_list = []

            size_tiles, self.y_gap_tile, self.x_gap_tile = numtiles_to_fontsize(len(self.current))
            self.fontObj_tile = pygame.font.Font(font_words, size_tiles)

            for tile in self.current:
                self.tilesSurfObj_list.append(self.fontObj_tile.render(tile, True, color_tile))

        if 'playerwords' in self.graphics_to_update:
            self.playerwordsSurfObj_list = []

            size_words, self.y_gap_words = numwords_to_fontsize(len(self.playerwords_list))
            self.fontObj_words = pygame.font.Font(font_words, size_words)

            if self.who_took == 'self':
                new_word_i = self.playerwords_list.index(self.new_word)
                for i, word in enumerate(self.playerwords_list):
                    if i == new_word_i:
                        self.playerwordsSurfObj_list.append(self.fontObj_words.render(word, True, color_taken))
                    else:
                        self.playerwordsSurfObj_list.append(self.fontObj_words.render(word, True, color_words))
            else:
                for word in self.playerwords_list:
                    self.playerwordsSurfObj_list.append(self.fontObj_words.render(word, True, color_words))

        if 'player2words' in self.graphics_to_update:
            self.player2wordsSurfObj_list = []

            size_opp_words, self.y_gap_opp_words = numwords_to_fontsize(len(self.player2words_list))
            self.fontObj_words = pygame.font.Font(font_words, size_opp_words)

            if self.who_took == 'opp':
                new_word_i = self.player2words_list.index(self.new_word)
                for i, word in enumerate(self.player2words_list):
                    if i == new_word_i:
                        self.player2wordsSurfObj_list.append(self.fontObj_words.render(word, True, color_taken))
                    else:
                        self.player2wordsSurfObj_list.append(self.fontObj_words.render(word, True, color_words))
            else:
                for word in self.player2words_list:
                    self.player2wordsSurfObj_list.append(self.fontObj_words.render(word, True, color_words))

        if 'guess' in self.graphics_to_update:
            self.guessSurfObj = self.fontObj_guess.render('Take: ' + self.guess, True, color_guess)

        if 'status' in self.graphics_to_update:
            self.statusSurfObj = self.fontObj_status.render(self.status, True, color_status)

        self.graphics_to_update = []

        if time_check:
            end_time = time.time()
            self.time_dict['update_graphics'] = end_time - start_time

    def __display_text(self, SurfaceObj, x, y):
        textRectObj = SurfaceObj.get_rect()
        textRectObj.topleft = (x, y)
        DISPLAYSURF.blit(SurfaceObj, textRectObj)

    def __display_text_tiles(self, SurfaceObj, x, y):
        textRectObj = SurfaceObj.get_rect()
        textRectObj.center = (x, y)
        DISPLAYSURF.blit(SurfaceObj, textRectObj)

    def __can_take(self, take_dict):
        if not self.__superset(self.current, take_dict['used_tiles'], strict=False):
            return False
        elif not self.__superset(self.playerwords, take_dict['self_taken_words'], strict=False):
            return False
        elif not self.__superset(self.player2words, take_dict['opp_taken_words'], strict=False):
            return False
        else:
            return True

    def __reconcile_takes(self, dict1, dict2):
        combined_dict = {}
        for key in dict1:
            combined_dict[key] = dict1[key] + dict2[key]

        if not self.__superset(self.current, combined_dict['used_tiles'], strict=False):
            return False
        elif not self.__superset(self.playerwords, combined_dict['self_taken_words'], strict=False):
            return False
        elif not self.__superset(self.player2words, combined_dict['opp_taken_words'], strict=False):
            return False
        else:
            return True

    def __dict_supersedes(self, dict1, dict2):
        if not (dict1['self_taken_words'] == dict2['self_taken_words'] and dict1['opp_taken_words'] == dict2['opp_taken_words']):
            return None
        else:
            if self.__superset(dict1['new_word'], dict2['new_word'], strict=True):
                return 'one'
            elif self.__superset(dict2['new_word'], dict1['new_word'], strict=True):
                return 'two'
            else:
                return None

    def get_server_update(self):
        flip_waiting_recv = False

        if time_check:
            start_time =  time.time()

        if time.time() - self.last_type > 0.2:
            # Get player 2 update
            print("Getting player 2 update!")
            net_id_recv, self.seed_recv, self.last_update_recv, self.take_dict_recv, self.flip_dict_recv = self.parse_data(self.send_data())
            print(f"Flip dict: {self.flip_dict_recv}")

            if self.seed_recv < 1:
                print("No data...")
                if self.mode == 'multiplayer':
                    self.frozen = True

            # If 'waiting' mode and get a valid seed, player 2 has joined and you're ready to start multiplayer
            elif self.mode == 'waiting':
                self.mode = 'multiplayer'
                self.status = 'Player 2 joined. Starting multiplayer'
                self.graphics_to_update = self.graphics_to_update + ['status']
            else:
                self.frozen = False

        take_dict_recv = self.take_dict_recv

        if time_check:
            end_time = time.time()
            self.time_dict['send_parse'] = end_time - start_time

        if time_check:
            start_time = time.time()

        if not self.i_flipped and not self.flip_dict['flip_waiting'] and self.flip_dict_recv['flip_waiting']:
            self.flip_dict['flip_waiting'] = True
            self.flip_dict['flip_status'] = 'Ready...'
            self.flip_dict['scheduled_flip'] = self.flip_dict_recv['scheduled_flip']
            # if the scheduled flip time has already passed, there's a snafu, so flip
            print("Secondhand flip")
            print(f"Current time is {time.time()}")
            print(f"Gonna flip at {self.flip_dict['scheduled_flip']}")
            if time.time() > self.flip_dict['scheduled_flip']:
                print("OOPS! Already flipped!!!")
                self.flip()
                self.flip_dict['flip_waiting'] = False

            self.graphics_to_update = self.graphics_to_update + ['flip']
            self.last_update = self.last_update_recv

        if self.take_waiting and time.time() - self.take_waiting_time > 0.5:
            self.update_take('self', self.take_dict)
            self.take_waiting = False
            self.take_dict = self.__cleared_take_dict()
            self.last_update = time.time()

        # Check if other player has made a more recent update, meaning you would need to update your lists
        # Don't check for flips (because they are timed and independently done). Only check for takes
        # So in theory, the following should be triggered only if there's a take or a counter-update!
        if self.last_update_recv > self.last_update and not self.__is_cleared(self.take_dict_recv):
            if print_check:
                """
                print(f"Opponent's last update: {self.player2_last_update}")
                print(f"My last update: {self.last_update}")
                print(f"My take start time: {self.take_start_time}")
                print(f"Current: {self.current}")
                print(f"Tiles used from opponent: {used_tiles_recv}")
                print(f"Tiles used by me: {self.take_dict['used_tiles']}")
                """

            """
            If opp last update more recent, get opp take dict
                - if not waiting, check if can take
                    - if yes, great!
                    - if no, earlier take wins, update_take that one
                            - if i win, set last update to my time
                            - if i lose, SNAFU: apologize and backtrack
                - if waiting, reconcile take dicts
                    - if compatible, update_take both
                    - if one supersedes the other, take that one
                    - else earlier take wins, update_take that one
                        - if i win, set last update to my time
                    - no matter what, self.take_waiting = False
            """

            if not self.take_waiting:
                if self.__can_take(take_dict_recv):
                    self.update_take('opp', take_dict_recv)
                elif self.__dict_supersedes(self.take_dict_past, take_dict_recv) == 'two':
                    new_dict = {}
                    new_dict['new_word'] = take_dict_recv['new_word']
                    new_dict['etyms_new_word'] = take_dict_recv['etyms_new_word']
                    new_dict['take_time'] = take_dict_recv['take_time']
                    new_dict['used_tiles'] = self.__subtract(take_dict_recv['used_tiles'] , self.take_dict_past['used_tiles'])
                    new_dict['self_taken_words'] = self.take_dict_past['new_word']
                    new_dict['opp_taken_words'] = []
                    new_dict['self_taken_is'] = [self.playerwords.index(self.take_dict_past['new_word'])]
                    new_dict['opp_taken_is'] = []

                    self.update_take('opp', new_dict)
                elif self.take_dict_past['take_time'] < take_dict_recv['take_time']:
                    self.last_update = time.time()
                else:
                    print('SNAFU')
                    self.status = 'SNAFU'
                    self.graphics_to_update = self.graphics_to_update + ['status']

                    # BACKTRACK

                    self.tiles = self.tiles_past.copy()
                    self.current = self.current_past.copy()
                    self.playerwords = self.playerwords_past.copy()
                    self.playerwords_list = self.playerwords_list_past.copy()
                    self.player2words = self.player2words_past.copy()
                    self.player2words_list = self.player2words_list_past.copy()

                    self.update_take('opp', take_dict_recv)
            else:
                who_supersedes = self.__dict_supersedes(self.take_dict, take_dict_recv)
                if self.__reconcile_takes(self.take_dict, take_dict_recv):
                    self.update_take('opp', take_dict_recv)
                    self.update_take('self', self.take_dict)

                    self.last_update = time.time()
                    self.take_dict = self.__cleared_take_dict()
                elif who_supersedes == 'one':
                    self.update_take('self', self.take_dict)
                    self.last_update = time.time()
                    self.take_dict = self.__cleared_take_dict()
                elif who_supersedes == 'two':
                    self.update_take('opp', take_dict_recv)
                    self.take_dict = self.__cleared_take_dict()
                elif self.take_dict['take_time'] <= take_dict_recv['take_time']:
                    self.update_take('self', self.take_dict)
                    self.last_update = time.time()
                    self.take_dict = self.__cleared_take_dict()
                else:
                    self.update_take('opp', take_dict_recv)
                    self.take_dict = self.__cleared_take_dict()

                self.take_waiting = False

        if time_check:
            end_time = time.time()
            self.time_dict['update_players'] = end_time - start_time

    def printstatus(self):
        if time_check:
            start_time = time.time()

        # 'CURRENT'

        self.__display_text(self.currentSurfObj, x_current, y_current)

        # CURRENT TILES

        y_tile = y_tile_0
        x_tile = x_tile_0

        for i, tile in enumerate(self.tilesSurfObj_list):
            x_tile = x_tile + self.x_gap_tile

            self.__display_text_tiles(tile, x_tile, y_tile)

            if i % 20 == 19:
                y_tile = y_tile + self.y_gap_tile
                x_tile = x_tile_0

        # 'YOUR'

        self.__display_text(self.yourSurfObj, x_your, y_your)

        # YOUR WORDS

        x_words_local = x_words
        y_words_local = y_words

        for i, word in enumerate(self.playerwordsSurfObj_list):
            self.__display_text(word, x_words_local, y_words_local)

            if i % 10 == 9:
                x_words_local = x_words_local + x_gap_words
                y_words_local = y_words - self.y_gap_words

            y_words_local = y_words_local + self.y_gap_words

        # GUESS
        self.__display_text(self.guessSurfObj, x_guess, y_guess)

        if self.mode != 'solo':
            # 'OPPONENT'S'
            self.__display_text(self.oppSurfObj, x_opp, y_opp)

            # OPPONENT'S WORDS

            x_opp_words_local = x_opp_words
            y_opp_words_local = y_opp_words

            for i, word in enumerate(self.player2wordsSurfObj_list):
                self.__display_text(word, x_opp_words_local, y_opp_words_local)

                if i % 10 == 9:
                    x_opp_words_local = x_opp_words_local + x_gap_opp_words
                    y_opp_words_local = y_opp_words - self.y_gap_opp_words

                y_opp_words_local = y_opp_words_local + self.y_gap_opp_words

        # FLIP STATUS
        self.__display_text(self.flipSurfObj, x_flip, y_flip)

        # STATUS
        self.__display_text(self.statusSurfObj, x_status, y_status)

        if time_check:
            end_time = time.time()
            self.time_dict['display_graphics'] = end_time - start_time

def main():
    # Main game loop
    global FPSCLOCK, DISPLAYSURF
    pygame.init()

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    pygame.display.set_caption('Anagrams')

    game = banana()

    while True: # main game loop
        FPSCLOCK.tick(60)

        if time_check:
            start_loop = time.time()

        DISPLAYSURF.fill(BGCOLOR)

        if game.flip_dict['flip_waiting']:
            if time.time() >= game.flip_dict['scheduled_flip']:
                # print("Firsthand flip")
                game.flip()
                game.flip_dict['flip_waiting'] = False

        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if game.frozen:
                game.status = 'Oops! Connection problem! Reconnecting...'
                game.graphics_to_update = game.graphics_to_update + ['status']

            elif not game.tiles and time.time() - game.last_update > 3:
                game.status = f"No more tiles! Your score: {sum([len(i) for i in game.playerwords_list])}, Opponent's score: {sum([len(i) for i in game.player2words_list])}"
                game.graphics_to_update = game.graphics_to_update + ['status']

            elif game.mode == 'waiting':
                if event.type == KEYDOWN and event.key == K_RETURN:
                    game.mode = 'solo'
                    game.status = 'Now playing solo'
                    game.graphics_to_update = game.graphics_to_update + ['status']
                else:
                    game.status = 'Waiting for other player... Press Enter to play solo'
                    game.graphics_to_update = game.graphics_to_update + ['status']

            elif event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    if game.guess == '':
                        pass
                    else:
                        # Delete one letter from the guess
                        game.guess = game.guess[:-1]
                        game.graphics_to_update = game.graphics_to_update + ['guess']
                        game.last_type = time.time()

                elif event.key == K_SPACE:
                    # Don't do anything if input is a space
                    pass

                elif event.key == K_RETURN:
                    # if Return and no guess is present, then flip next tile. If guess is present, see if it's a take
                    if game.guess == '':
                        if game.mode != 'solo':
                            game.flip_dict['flip_waiting'] = True
                            game.flip_dict['flip_status'] = 'Ready...'
                            game.graphics_to_update = game.graphics_to_update + ['flip']
                            game.last_update = time.time()
                            game.flip_dict['scheduled_flip'] = time.time() + 1
                            game.i_flipped = True

                            print("Firsthand flip")
                            print(f"Current time is {time.time()}")
                            print(f"Gonna flip at {game.flip_dict['scheduled_flip']}")
                        else:
                            game.flip()

                    else:
                        game.take(game.guess.upper())

                elif event.key in letter_keys:
                    # if letter is typed then add it to the current guess
                    game.guess = game.guess + event.unicode.upper()
                    game.graphics_to_update = game.graphics_to_update + ['guess']
                    game.last_type = time.time()

        if game.mode != 'solo':
            game.get_server_update()

        if game.i_flipped and game.flip_dict['flip_waiting']:
            game.flip_dict['flip_waiting'] = False
            game.i_flipped = False

        game.update_graphics()
        game.printstatus()
        pygame.display.update()

        if time_check:
            end_loop = time.time()
            loop_time = end_loop - start_loop
            game.time_dict['loop'] = loop_time

            if loop_time > 0.1:
                print(f"Delay: {game.time_dict}")


if __name__ == "__main__":
    # execute only if run as a script
    main()
