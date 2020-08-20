import itertools
import random
import datetime
import time
import twl
from collections import Counter
import ast
from itertools import combinations

import api

import pygame, sys
from pygame.locals import *

from take import Take

from pygame.locals import *

letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
letter_freq = {'A': 13, 'B': 3, 'C': 3, 'D': 6, 'E': 18, 'F': 3, 'G': 4, 'H':3, 'I':12, 'J':2, 'K':2, 'L':5, 'M':3, 'N':8, 'O':11, 'P':3, 'Q':2, 'R':9, 'S':6, 'T':9, 'U': 6, 'V':3, 'W':3, 'X':2, 'Y':3, 'Z':2}
letter_keys = [K_a, K_b, K_c, K_d, K_e, K_d, K_e, K_f, K_g, K_h, K_i, K_j, K_k, K_l, K_m, K_n, K_o, K_p, K_q, K_r, K_s, K_t, K_u, K_t, K_v, K_w, K_x, K_y, K_z]

not_allowed_prefixes = ['UN', 'RE']
not_allowed_suffixes = ['S', 'ED', 'D', 'ES', 'ER', 'R', 'OR', 'ING', 'EST', 'IEST', 'LY', 'TION', 'SION']

word_add_twl = ['acai', 'roo', 'tix']

flip_delay = 1000 # Delay before flip in ms
flip_status = ''

no_prefix_suffix = True

time_check = False


def other_player(player):
    if player == 0:
        return 1
    else:
        return 0

class Banana:
    def __init__(self):
        # -------- #
        #  BANANA  #
        # -------- #
        self.tiles = []
        for letter in letters:
            self.tiles = self.tiles + list(itertools.repeat(letter, letter_freq[letter]))

        random.shuffle(self.tiles)

        # Current tiles available
        self.current = []

        self.player1words = {}
        self.player1words_list = []
        self.player2words = {}
        self.player2words_list = []

        self.player1taketime = time.time()
        self.player2taketime = time.time()

        self.fresh_take = False
        self.middle_used = []
        self.taken_word = "\'\'"

        self.game_start_time = datetime.datetime.now()
        self.new_initialization = True

        # Time (do we need??)
        self.last_update = time.time()
        self.last_flip_update = time.time()

        self.flip_status = ''

        self.time_dict = {'loop': 0, 'send_data': 0, 'take': 0, 'update_graphics': 0,
                          'display_graphics': 0, 'send_parse': 0, 'update_players': 0}

        self.taken_i = -1
        self.new_word_i = -1

        self.flip_waiting = False
        self.flip_time = 0

        self.time_last_take = time.time()
        self.p1_last_take = time.time()
        self.p2_last_take = time.time()

        self.current_prev = []
        self.player1words_prev = {}
        self.player1words_list_prev = []
        self.player2words_prev = {}
        self.player2words_list_prev = []

        self.status = {}
        self.last_take = None

        self.last_update = 0
        self.update_event = ''
        self.taker_id = -1
        self.update_number = 0

        self.game_over = False

    def flip(self):
        self.updated = True

        if not self.tiles:
            self.status = f"No more tiles! Your score: {sum([len(i) for i in self.playerwords_list])}, Opponent's score: {sum([len(i) for i in self.player2words_list])}"

            self.gameover = True

            return None

        self.last_update = datetime.datetime.now()

        last = self.tiles.pop()
        self.current.append(last)

    def __superset(self, word1, word2, strict=False):
        # Can word 1 take word 2?
        word1_counter = Counter(word1)
        word2_counter = Counter(word2)

        if strict:
            return (word1_counter - word2_counter and not (word2_counter - word1_counter))
        else:
            return (word1_counter - word2_counter and not (word2_counter - word1_counter)) or (
                        not (word1_counter - word2_counter) and not (word2_counter - word1_counter))

    def __subtract(self, word1, word2):
        # Subtract word2 from word1 (e.g. 'test' - 'tst' = 'e')

        list1 = list(word1)
        for letter in word2:
            list1.remove(letter)

        # Turn list into string
        str = ''
        str = str.join(list1)

        return str

    def __can_take(self, candidate):
        word_list = self.player2words_list

        for word in word_list:
            # First, check if candidate is a superset of the current word
            if self.__superset(candidate, word, strict=True):

                # Then, check if the tiles needed to make candidate are in the middle
                if self.__superset(self.current, self.__subtract(candidate, word)):
                    return True

        word_list = self.playerwords_list

        for word in word_list:
            if self.__superset(candidate, word, strict=True):

                # Then, check if the tiles needed to make candidate are in the middle
                if self.__superset(self.current, self.__subtract(candidate, word)):
                    return True
        if self.__superset(self.current, candidate, strict=False):
            return True
        else:
            return False

    def __check_new_take(self, player, taketime, candidate):
        if player == 1:
            own_last_take = self.p1_last_take
            opp_last_take = self.p2_last_take
        else:
            own_last_take = self.p2_last_take
            opp_last_take = self.p1_last_take

        # If the take time is older than the player's last take, it's not a new take
        if taketime <= own_last_take:
            return 'no update'
        # Otherwise it's a new take for the player. If they can take it, let them
        elif self.__can_take(candidate):
            return 'update'
        # Otherwise a new take for the player but they can't take it. If they're later than the other player, too bad
        elif taketime >= opp_last_take:
            return 'no update'
        # Otherwise they were actually earlier than the other player and we need to rewrite
        else:
            return 'overwrite'

    def __check_steal(self, candidate, etyms_candidate, is_player_2):
        # Check whether a steal happens
        # Input a candidate word (i.e. guess), its merriam stripped version,
        # a dictionary with the words to take from (plus their merriam stripped versions) and
        # a Boolean indicating whether we're checking a steal from the opponent

        # Returns whether stolen, what kind of steal or error, the taken word, and index of taken word

        # Set event_type to 'tiles' arbitrarily
        event_type = 'tiles'

        if is_player_2:
            word_list = self.player2words_list
            word_dict = self.player2words
        else:
            word_list = self.player1words_list
            word_dict = self.player1words


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
        if not is_player_2 and self.__superset(self.current, candidate, strict=False):
            # This is to check middle steals. We have "is_opponent" because we're running this current __check_steal
            # function twice, once for the opponent's words and once for your words, and we don't want it to check
            # for a middle steal twice. So we say that in the first go-through (opponent's words), don't check middle
            event_type = 'middle'
            return True, event_type, None, None
        else:
            return False, event_type, None, None


    def take(self, candidate, player, last_update):
        self.used_tiles = []

        if time_check:
            start_time = time.time()

        self.take_start_time = time.time()

        # First check if has 3 letters
        if len(candidate) < 3:
            self.status = "Word is too short! " + f"({candidate})"
            return 'short', None

        # Then check if a word
        if len(candidate) < 10:
            candidate_lower = candidate.lower()
            is_word = twl.check(candidate_lower) or candidate_lower in word_add_twl
        else:
            is_word = api.get_word_data(candidate)
        if not is_word:
            # self.__display_text("Not a word!", 200, 400)
            self.status = "Not a word! " + f"({candidate})"
            return 'not_word', None

        # If no prefixes and suffixes, check that
        if no_prefix_suffix:
            has_prefix_suffix, prefix, suffix = api.get_prefix_suffix(candidate)
            # print(f"Stuff: {has_prefix_suffix}, {prefix}, {suffix}")
            # print(f"{prefix in not_allowed_prefixes}, {suffix in not_allowed_suffixes}")
            if has_prefix_suffix and (prefix in not_allowed_prefixes or suffix in not_allowed_suffixes):
                self.status = "Prefix / suffix not allowed!"
                return 'prefix_suffix', None


        error_trivial_extension = False
        error_tiles = False

        etyms_candidate = api.get_etym(candidate)

        # Check if can take the player 2's words (not checking middle steal)
        print(f"{candidate}, {etyms_candidate}, {True}")
        is_taken, event_type, taken_word, taken_i = self.__check_steal(candidate, etyms_candidate, True)

        if is_taken:
            # Get time of this steal
            self.last_update = self.take_start_time

            if event_type == 'steal': # in theory, this if statement is unnecessary since there are no middle steals
                # Make the candidate word into a list to remove individual letters.
                candidate_list = list(candidate)

                # Figure out what tiles are used from the middle and remove those from self.current
                for letter in taken_word:
                    candidate_list.remove(letter)

                return 'steal', Take(player, 1, candidate, etyms_candidate, taken_word, taken_i, candidate_list, self.take_start_time - last_update)

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

                    for letter in taken_word:
                        candidate_list.remove(letter)

                    return 'steal', Take(player, 0, candidate, etyms_candidate, taken_word, taken_i,
                                candidate_list, self.take_start_time - last_update)


                elif event_type == 'middle':
                    candidate_list = list(candidate)

                    self.take_end_time = datetime.datetime.now()

                    return 'steal', Take(player, -1, candidate, etyms_candidate, '', taken_i, candidate_list, self.take_start_time - last_update)

            elif error_trivial_extension or event_type == 'trivial':
                self.status = "Same root! " + f"({self.same_root_word} and {candidate} share root {self.root})"
                return 'trivial', None

            elif error_tiles:
                self.status = "Tiles aren't there! " + f"({candidate})"
                return 'tiles', None

            else:
                self.status = "Tiles aren't there! " + f"({candidate})"


    def __update_word_lists(self, player, victim, candidate, etym_candidate, taken_word, taken_i):

        if player == 1:
            if victim == 'self':
                self.player1words_list.remove(taken_word)
                if not taken_word in self.player1words_list:
                    del self.player1words[taken_word]
                self.player1words.update({candidate: etym_candidate})
                self.player1words_list[taken_i](candidate)

            elif victim == 'opp':
                self.player2words_list.remove(taken_word)
                if not taken_word in self.player2words_list:
                    del self.player2words[taken_word]
                self.player1words.update({candidate: etym_candidate})
                self.player1words_list.append(candidate)

            elif victim == 'middle':
                self.player1words.update({candidate: etym_candidate})
                self.player1words_list.append(candidate)

        elif player == 2:
            if victim == 'self':
                self.player2words_list.remove(taken_word)
                if not taken_word in self.player2words_list:
                    del self.player2words[taken_word]
                self.player2words.update({candidate: etym_candidate})
                self.player2words_list[taken_i](candidate)

            elif victim == 'opp':
                self.player1words_list.remove(taken_word)
                if not taken_word in self.player1words_list:
                    del self.player1words[taken_word]
                self.player2words.update({candidate: etym_candidate})
                self.player2words_list.append(candidate)

            elif victim == 'middle':
                self.player2words.update({candidate: etym_candidate})
                self.player2words_list.append(candidate)

    def update(self, take, player):
        # If game can be updated according to the update_dict, then update
        # If game cannot be updated, it means that it clashes with a previous update (opponent taking just before)
        # Check to see the take times and if this update_dict's take_time is earlier, then override

        """
        update_dict: {flip_request, candidate, etym_candidate, taken_word, used_tiles, victim, taken_i, taketime}
        """

        """ FOR GAMEOVER (TODO LATER)
        elif not self.gameover and not self.flip_waiting and update_dict['flip_request']:
            self.flip_waiting = True
            self.time_flip = time.time() + 2
        """

        print(f"taker: {take.taker},  victim: {take.victim}, candidate: {take.candidate}, etym_candidate: {take.etym_candidate}, taken_word: {take.taken_word}, used_tiles: {take.used_tiles}, taken_i: {take.taken_i}")



        # Update middle letters
        for letter in take.used_tiles:
            self.current.remove(letter)

        if take.taker == 0:
            if take.victim == 0:
                if not take.taken_word in self.player1words_list:
                    del self.player1words[take.taken_word]
                self.player1words.update({take.candidate: take.etym_candidate})
                self.player1words_list[take.taken_i] = take.candidate

            elif take.victim == 1:
                self.player2words_list.remove(take.taken_word)
                if not take.taken_word in self.player2words_list:
                    del self.player2words[take.taken_word]
                self.player1words.update({take.candidate: take.etym_candidate})
                self.player1words_list.append(take.candidate)

            elif take.victim == -1:
                self.player1words.update({take.candidate: take.etym_candidate})
                self.player1words_list.append(take.candidate)

        else:
            if take.victim == 1:
                if not take.taken_word in self.player2words_list:
                    del self.player2words[take.taken_word]
                self.player2words.update({take.candidate: take.etym_candidate})
                self.player2words_list[take.taken_i] = take.candidate

            elif take.victim == 0:
                self.player1words_list.remove(take.taken_word)
                if not take.taken_word in self.player1words_list:
                    del self.player1words[take.taken_word]
                self.player2words.update({take.candidate: take.etym_candidate})
                self.player2words_list.append(take.candidate)

            elif take.victim == -1:
                self.player2words.update({take.candidate: take.etym_candidate})
                self.player2words_list.append(take.candidate)

        self.last_update = time.time()






