import itertools
import random
import twl
from collections import Counter
import time
from network import Network
import ast
import datetime

import api

import pygame, sys
from pygame.locals import *

print_check = True
time_check = False

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
x_gap_words = 100
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
x_gap_opp_words = 100
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
        self.fontObj_flip = pygame.font.Font(font_flip, size_flip)

        self.fontObj_opp = pygame.font.Font(font_your, size_your)
        self.fontObj_opp_words = pygame.font.Font(font_words, size_words)

        self.guess = ''
        self.previous_guess = ''
        self.fresh_take = False
        self.middle_used = []
        self.taken_word = "\'\'"

        self.status = ''
        self.last_update = datetime.datetime(1,1,1)

        self.game_start_time = datetime.datetime.now()
        self.new_initialization = True

        self.net = Network()
        self.player2current = []
        self.player2words = {}
        self.player2words_list = []
        self.player2tiles = []
        self.player2_last_update = datetime.datetime(1,1,1)

        self.graphics_to_update = []

        self.flip_status = ''

        self.currentSurfObj = self.fontObj_current.render('Current: ', True, color_current)
        self.tilesSurfObj_list = []
        self.yourSurfObj = self.fontObj_your.render('Your Words: ', True, color_your)
        self.playerwordsSurfObj_list = []
        self.oppSurfObj = self.fontObj_opp.render('Opponent\'s Words: ', True, color_opp)
        self.player2wordsSurfObj_list = []
        self.guessSurfObj = self.fontObj_guess.render('Take: ' + self.guess, True, color_guess)
        self.statusSurfObj = self.fontObj_status.render(self.status, True, color_status)
        self.flipSurfObj = self.fontObj_flip.render(self.flip_status, True, color_flip)

        self.y_gap_words = y_gap_words
        self.y_gap_opp_words = y_gap_opp_words
        self.x_gap_tile = x_gap_tile
        self.y_gap_tile = y_gap_tile

        self.time_dict = {'loop': 0, 'send_data': 0, 'take': 0, 'update_graphics': 0,
                          'display_graphics': 0, 'send_parse': 0, 'update_players': 0}

        self.last_type = time.time() - 1

        self.same_root_word = ''

        self.take_start_time = datetime.datetime(1,1,1)
        self.take_end_time = datetime.datetime(1,1,1)
        self.used_tiles = []

        self.mode = 'waiting'
        self.host = False
        self.seed_set = False
        self.seed = 0
        self.frozen = False

        self.who_took = ''
        self.taken_i = -1
        self.new_word_i = -1

        self.flip_waiting = False
        self.time_flip = pygame.time.get_ticks()

    def send_data(self):
        if time_check:
            start_time = time.time()
        # print(f"NET ID: {self.net.id}")
        data = str(self.net.id) + "|" + str(self.seed) + "|" + str(self.current) + "|" + str(self.playerwords) + "|" + str(self.playerwords_list) + "|" + str(self.player2words) + "|" + str(self.player2words_list) + "|" + str(self.last_update) + "|" + str(self.used_tiles) + "|" + str(self.new_word_i) + "|" + self.taken_word + "|" + str(self.flip_waiting)
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
            current = ast.literal_eval(split[2])
            player2words = ast.literal_eval(split[3])
            player2words_list = ast.literal_eval(split[4])
            playerwords = ast.literal_eval(split[5])
            playerwords_list = ast.literal_eval(split[6])
            last_update = try_parsing_date(split[7])
            used_tiles_recv = ast.literal_eval(split[8])
            new_word_i_recv = ast.literal_eval(split[9])
            taken_word_recv = split[10]
            flip_waiting_recv = ast.literal_eval(split[11])

            return net_id, seed_recv, current, player2words, player2words_list, playerwords, playerwords_list, last_update, used_tiles_recv, new_word_i_recv, taken_word_recv, flip_waiting_recv
        except:
            return -1, 0, None, {}, [], None, None, datetime.datetime(1, 1, 1, 0, 0), [], -1, '', False



    def flip(self):
        self.updated = True

        if not self.tiles:
            self.status = f"No more tiles! Your score: {sum([len(i) for i in self.playerwords_list])}, Opponent's score: {sum([len(i) for i in self.player2words_list])}"
            self.graphics_to_update = self.graphics_to_update + ['status']

            return None

        self.last_update = datetime.datetime.now()

        last = self.tiles.pop()
        self.current.append(last)

        self.graphics_to_update = self.graphics_to_update + ['tiles']

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


    def __check_steal(self, candidate, etyms_candidate, is_opponent):
        # Check whether a steal happens
        # Input a candidate word (i.e. guess), its merriam stripped version,
        # a dictionary with the words to take from (plus their merriam stripped versions) and
        # a Boolean indicating whether we're checking a steal from the opponent

        # Returns whether stolen, what kind of steal or error, the taken word, and index of taken word

        # Set event_type to 'tiles' arbitrarily
        event_type = 'tiles'

        if is_opponent:
            word_list = self.player2words_list
            word_dict = self.player2words
        else:
            word_list = self.playerwords_list
            word_dict = self.playerwords


        for i, word in enumerate(word_list):
            # First, check if candidate is a superset of the current word
            if self.__superset(candidate, word, strict=True):

                # Then, check if the tiles needed to make candidate are in the middle
                if not self.__superset(self.current, self.__subtract(candidate, word)):
                    event_type = 'tiles'
                else:
                    etyms_word = word_dict[word]

                    try:
                        # Check for any common roots. If etymonline returns nothing, then assume there are no
                        # common roots
                        root_overlap = any(x in etyms_candidate for x in etyms_word)
                    except TypeError:
                        root_overlap = False

                    if root_overlap:
                        self.same_root_word = word
                        self.root = set(etyms_candidate).intersection(etyms_word).pop()
                        event_type = 'trivial'
                    else:
                        event_type = 'steal'
                        taken_word = word
                        taken_i = i
                        return True, event_type, taken_word, taken_i
        if not is_opponent and self.__superset(self.current, candidate, strict=False):
            # This is to check middle steals. We have "is_opponent" because we're running this current __check_steal
            # function twice, once for the opponent's words and once for your words, and we don't want it to check
            # for a middle steal twice. So we say that in the first go-through (opponent's words), don't check middle
            event_type = 'middle'
            return True, event_type, None, None
        else:
            return False, event_type, None, None

                # elif word in candidate and any(x in root.lookup(candidate) for x in root.lookup(word)):
                     # error_trivial_extension = True

                # If all of those check out, then it's a steal and record which word is being stolen


    def take(self, candidate):
        self.used_tiles = []

        if time_check:
            start_time = time.time()

        self.take_start_time = datetime.datetime.now()

        # First check if has 3 letters
        if len(candidate) < 3:
            self.previous_guess = self.guess
            self.status = "Word is too short! " + f"({self.previous_guess})"
            self.guess = ''
            self.graphics_to_update = self.graphics_to_update + ['status', 'guess']
            return None

        # Then check if a word
        if len(candidate) < 10:
            is_word = twl.check(candidate.lower())
        else:
            is_word = api.get_word_data(candidate)
        if not is_word:
            # self.__display_text("Not a word!", 200, 400)
            self.previous_guess = self.guess
            self.status = "Not a word! " + f"({self.previous_guess})"
            self.guess = ''
            self.graphics_to_update = self.graphics_to_update + ['status', 'guess']
            return None

        error_trivial_extension = False
        error_tiles = False

        etyms_candidate = api.get_etym(candidate)

        # Check if can take the other player's words (not checking middle steal)
        is_taken, event_type, taken_word, taken_i = self.__check_steal(candidate, etyms_candidate, True)

        if is_taken:
            # Get time of this steal
            self.last_update = self.take_start_time

            if event_type == 'steal': # in theory, this if statement is unnecessary since there are no middle steals
                # Make the candidate word into a list to remove individual letters.
                candidate_list = list(candidate)

                # Delete the taken word from opponent's list, add it to your own dictionary and corresponding list (list for ordering purposes)
                self.player2words_list.remove(taken_word)
                if not taken_word in self.player2words_list:
                    del self.player2words[taken_word]

                self.playerwords.update({candidate: etyms_candidate})
                self.playerwords_list.append(candidate)

                # Figure out what tiles are used from the middle and remove those from self.current
                for letter in taken_word:
                    candidate_list.remove(letter)

                for letter in candidate_list:
                    self.used_tiles.append(letter)
                    self.current.remove(letter)
                self.previous_guess = self.guess
                self.status = "Success! " + f"({taken_word} -> {self.previous_guess})"
                self.fresh_take = True
                self.taken_word = taken_word
                self.middle_used = candidate_list
                self.who_took = 'self'
                self.taken_i = taken_i
                self.my_word_taken = False
                self.new_word_i = len(self.playerwords_list) - 1

            self.graphics_to_update = self.graphics_to_update + ['tiles', 'playerwords', 'player2words', 'status', 'guess']
            self.take_end_time = datetime.datetime.now()

        else:
            # If no steal was triggered above, then couldn't steal opponent's words for one of the reasons below
            # (wait until you check whether you can take one of your own words to see if it was a failure overall)
            if event_type == 'trivial':
                error_trivial_extension = True
            elif event_type == 'tiles':
                error_tiles = True

        # if could not take the other player's words, check if can take one's own
        if not is_taken:
            self_is_taken, event_type, taken_word, taken_i = self.__check_steal(candidate, etyms_candidate, False)

            if self_is_taken:
                self.last_update = self.take_start_time
                self.updated = True
                if event_type == 'steal':
                    candidate_list = list(candidate)

                    self.playerwords.update({candidate: etyms_candidate})

                    self.playerwords_list[taken_i] = candidate
                    if not taken_word in self.playerwords_list:
                        del self.playerwords[taken_word]

                    for letter in taken_word:
                        candidate_list.remove(letter)
                    for letter in candidate_list:
                        self.used_tiles.append(letter)
                        self.current.remove(letter)
                    self.previous_guess = self.guess
                    self.status = "Success! " + f"({taken_word} -> {self.previous_guess})"
                    self.fresh_take = True
                    self.taken_word = taken_word
                    self.middle_used = candidate_list
                    self.who_took = 'self'
                    self.taken_i = taken_i
                    self.my_word_taken = True
                    self.new_word_i = taken_i

                    self.graphics_to_update = self.graphics_to_update + ['tiles', 'playerwords', 'player2words',
                                                                         'status', 'guess']
                    self.take_end_time = datetime.datetime.now()

                elif event_type == 'middle':
                    candidate_list = list(candidate)

                    for letter in candidate_list:
                        self.used_tiles.append(letter)
                        self.current.remove(letter)
                    self.playerwords.update({candidate: etyms_candidate})
                    self.playerwords_list.append(candidate)

                    self.previous_guess = self.guess
                    self.status = "Success! " + f"({self.previous_guess} from the middle)"
                    self.fresh_take = True
                    self.taken_word = '0'
                    self.middle_used = candidate_list
                    self.who_took = 'self'
                    self.taken_i = len(self.playerwords_list) - 1
                    self.my_word_taken = False
                    self.new_word_i = len(self.playerwords_list) - 1

                    self.graphics_to_update = self.graphics_to_update + ['tiles', 'playerwords', 'player2words',
                                                                         'status', 'guess']
                    self.take_end_time = datetime.datetime.now()

            elif error_trivial_extension or event_type == 'trivial':
                self.previous_guess = self.guess
                self.status = "Same root! " + f"({self.same_root_word} and {self.previous_guess} share root {self.root})"
                self.graphics_to_update = self.graphics_to_update + ['status', 'guess']
            elif error_tiles:
                self.previous_guess = self.guess
                self.status = "Tiles aren't there! " + f"({self.previous_guess})"
                self.graphics_to_update = self.graphics_to_update + ['status', 'guess']
            else:
                self.previous_guess = self.guess
                self.status = "Tiles aren't there! " + f"({self.previous_guess})"
                self.graphics_to_update = self.graphics_to_update + ['status', 'guess']
        self.guess = ''
        if time_check:
            end_time = time.time()
            self.time_dict['take'] = end_time - start_time

    def __update_graphics(self):
        if time_check:
            start_time = time.time()

        if 'flip' in self.graphics_to_update:
            self.flipSurfObj = self.fontObj_flip.render(self.flip_status, True, color_flip)


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
                for i, word in enumerate(self.playerwords_list):
                    if i == self.new_word_i:
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
                for i, word in enumerate(self.player2words_list):
                    if i == self.new_word_i:
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

    def printstatus(self):

        if time_check:
            start_time = time.time()

        # Send network stuff, outputs of this function are the stuff you receive from the other player
        if self.mode != 'solo':
            if self.host and not self.seed_set:
                # print(f"I AM THE HOST!!!")
                self.seed = random.randint(1, 100000)
                self.seed_set = True

            if time.time() - self.last_type > 0.5:
                net_id_recv, seed_recv, self.player2current, player2words_recv, player2words_list_recv, playerwords_recv, playerwords_list_recv, self.player2_last_update, used_tiles_recv, new_word_i_recv, taken_word_recv, flip_waiting_recv = self.parse_data(self.send_data())
                # print(f"Net ID received: {net_id_recv}")
                if seed_recv < 1:
                    print("No data...")
                    # self.player2tiles, self.player2current, player2words_recv, player2words_list_recv, playerwords_recv, playerwords_list_recv, self.player2_last_update, used_tiles_recv = return [], None, {}, [], None, None, datetime.datetime(1, 1, 1, 0, 0), []
                    if not self.seed_set:
                        self.host = True
                    elif self.mode == 'multiplayer':
                        self.frozen = True


                elif self.mode == 'waiting':
                    self.mode = 'multiplayer'
                    self.status = 'Player 2 joined. Starting multiplayer'
                    self.graphics_to_update = self.graphics_to_update + ['status']
                    if not self.host and not self.seed_set:
                        self.seed = seed_recv
                        self.seed_set = True
                else:
                    self.frozen = False


        if time_check:
            end_time = time.time()
            self.time_dict['send_parse'] = end_time - start_time

        # If just initialized and other player has tiles, make them your own tiles
        if self.new_initialization:
            if self.player2tiles:
                self.tiles = self.player2tiles
                self.new_initialization = False
            else:
                self.new_initialization = False


        # If it's a fresh take, check to see if the opponent's taken it first
        """
        if self.fresh_take:
            # Check if center tiles and taken word are still there:
            if not self.__superset(self.player2current, self.middle_used, strict=False) or (not self.pre_take_word in player2words_list_recv and not self.pre_take_word in playerwords_list_recv):
                print("OVERWRITING!!!!")
                self.current = self.player2current
                self.playerwords = playerwords_recv
                self.playerwords_list = playerwords_list_recv
                self.last_update = self.player2_last_update
                self.player2words = player2words_recv
                self.player2words_list = player2words_list_recv
        # Reset self.fresh_take
        self.fresh_take = False
        """

        if time_check:
            start_time = time.time()

        # Check if other player has made a more recent update, meaning you would need to update your lists

        if self.player2_last_update > self.last_update:
            # print(f"take_start_time: {self.take_start_time}, player 2 last update: {self.player2_last_update}, take end time: {self.take_end_time}, current: {self.current}, used_tiles_recv: {used_tiles_recv}")
            if not (self.take_start_time < self.player2_last_update < (self.take_end_time + datetime.timedelta(0,0.2)) and not self.__superset(self.current, used_tiles_recv)):
                # print("UPDATING")
                if not self.flip_waiting and flip_waiting_recv:
                    self.flip_waiting = True
                    self.flip_status = 'Ready...'
                    self.graphics_to_update = self.graphics_to_update + ['flip']

                elif self.player2words_list == player2words_list_recv and self.playerwords_list == playerwords_list_recv:
                    # print("JUST A FLIP")
                    self.current = self.player2current
                    self.last_update = self.player2_last_update
                    self.flip_status = 'Flipped!'

                    self.graphics_to_update = self.graphics_to_update + ['tiles', 'guess', 'flip']

                    last = self.tiles.pop()
                    self.flip_waiting = False
                else:
                    # print("A TAKE!")
                    self.current = self.player2current
                    self.playerwords = playerwords_recv
                    self.playerwords_list = playerwords_list_recv
                    self.last_update = self.player2_last_update
                    self.player2words = player2words_recv
                    self.player2words_list = player2words_list_recv

                    self.who_took = 'opp'
                    self.new_word_i = new_word_i_recv

                    if taken_word_recv == '0':
                        self.status = f'Opponent took {self.player2words_list[new_word_i_recv]} from the middle!'
                    else:
                        self.status = f'Opponent took {taken_word_recv} with {self.player2words_list[new_word_i_recv]}!'

                    self.graphics_to_update = self.graphics_to_update + ['tiles', 'playerwords', 'player2words', 'status', 'guess']
            else:
                self.last_update = datetime.datetime.now()

        if time_check:
            end_time = time.time()
            self.time_dict['update_players'] = end_time - start_time

        self.__update_graphics()

        if time_check:
            start_time = time.time()

        y_tile = y_tile_0
        x_tile = x_tile_0

        """
        def __display_text(self, text, x, y, fontObj, color):
            textSurfaceObj = fontObj.render(text, True, color)
            textRectObj = textSurfaceObj.get_rect()
            textRectObj.topleft = (x, y)
            DISPLAYSURF.blit(textSurfaceObj, textRectObj)
        """


        self.__display_text(self.currentSurfObj, x_current, y_current)

        """
        currentSurfaceObj = self.fontObj.render('Current:', True, BLACK)
        currentRectObj = currentSurfaceObj.get_rect()
        currentRectObj.topleft = (x_current, y_current)
        DISPLAYSURF.blit(currentSurfaceObj, currentRectObj)
        """

        for i, tile in enumerate(self.tilesSurfObj_list):
            x_tile = x_tile + self.x_gap_tile

            self.__display_text_tiles(tile, x_tile, y_tile)

            """
            tileSurfaceObj = self.fontObj.render(tile, True, BLACK)
            tileRectObj = tileSurfaceObj.get_rect()
            tileRectObj.topleft = (x_tile, y_tile)
            DISPLAYSURF.blit(tileSurfaceObj, tileRectObj)
            """

            if i % 20 == 19:
                y_tile = y_tile + self.y_gap_tile
                x_tile = x_tile_0



        self.__display_text(self.yourSurfObj, x_your, y_your)

        """
        wordsSurfaceObj = self.fontObj.render('Your Words:', True, BLACK)
        wordsRectObj = wordsSurfaceObj.get_rect()
        wordsRectObj.topleft = (x_words, y_words)
        DISPLAYSURF.blit(wordsSurfaceObj, wordsRectObj)
        """

        x_words_local = x_words
        y_words_local = y_words

        for i, word in enumerate(self.playerwordsSurfObj_list):


            self.__display_text(word, x_words_local, y_words_local)


            """
            wordSurfaceObj = self.fontObj.render(word, True, BLACK)
            wordRectObj = wordSurfaceObj.get_rect()
            wordRectObj.topleft = (x_words, y_words)
            DISPLAYSURF.blit(wordSurfaceObj, wordRectObj)
            """

            if i % 10 == 9:
                x_words_local = x_words_local + x_gap_words
                y_words_local = y_words - self.y_gap_words

            y_words_local = y_words_local + self.y_gap_words


        self.__display_text(self.guessSurfObj, x_guess, y_guess)

        """
        guessSurfaceObj = self.fontObj.render('Guess: ' + self.guess, True, BLACK)
        guessRectObj = guessSurfaceObj.get_rect()
        guessRectObj.topleft = (x_guess, y_guess)
        DISPLAYSURF.blit(guessSurfaceObj, guessRectObj)
        """

        self.__display_text(self.oppSurfObj, x_opp, y_opp)

        """
        wordsSurfaceObj = self.fontObj.render('Your Words:', True, BLACK)
        wordsRectObj = wordsSurfaceObj.get_rect()
        wordsRectObj.topleft = (x_words, y_words)
        DISPLAYSURF.blit(wordsSurfaceObj, wordsRectObj)
        """

        x_opp_words_local = x_opp_words
        y_opp_words_local = y_opp_words

        for i, word in enumerate(self.player2wordsSurfObj_list):

            self.__display_text(word, x_opp_words_local, y_opp_words_local)


            """
            wordSurfaceObj = self.fontObj.render(word, True, BLACK)
            wordRectObj = wordSurfaceObj.get_rect()
            wordRectObj.topleft = (x_words, y_words)
            DISPLAYSURF.blit(wordSurfaceObj, wordRectObj)
            """

            if i % 10 == 9:
                x_opp_words_local = x_opp_words_local + x_gap_opp_words
                y_opp_words_local = y_opp_words - self.y_gap_opp_words

            y_opp_words_local = y_opp_words_local + self.y_gap_opp_words

        self.__display_text(self.flipSurfObj, x_flip, y_flip)

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

    backspace_hold = False

    while True: # main game loop
        FPSCLOCK.tick(60)

        if time_check:
            start_loop = time.time()

        DISPLAYSURF.fill(BGCOLOR)

        if game.flip_waiting:
            print("Check if time to flip!")
            if pygame.time.get_ticks() - game.time_flip > 1000:
                game.flip()
                game.flip_status = 'Flipped!'
                game.graphics_to_update = game.graphics_to_update + ['flip']
                game.flip_waiting = False

        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if game.frozen:
                game.status = 'Oops! Connection problem! Reconnecting...'
                game.graphics_to_update = game.graphics_to_update + ['status']

            elif not game.tiles and datetime.datetime.now() - game.last_update > datetime.timedelta(seconds=3):
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
                        game.flip_waiting = True
                        game.flip_status = 'Ready...'
                        game.graphics_to_update = game.graphics_to_update + ['flip']
                        game.time_flip = pygame.time.get_ticks()

                    else:
                        game.take(game.guess.upper())

                elif event.key in letter_keys:
                    # if letter is typed then add it to the current guess
                    game.guess = game.guess + event.unicode.upper()
                    game.graphics_to_update = game.graphics_to_update + ['guess']
                    game.last_type = time.time()



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
