import itertools
import random
import datetime
import time

from pygame.locals import *

letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
letter_freq = {'A': 13, 'B': 3, 'C': 3, 'D': 6, 'E': 18, 'F': 3, 'G': 4, 'H':3, 'I':12, 'J':2, 'K':2, 'L':5, 'M':3, 'N':8, 'O':11, 'P':3, 'Q':2, 'R':9, 'S':6, 'T':9, 'U': 6, 'V':3, 'W':3, 'X':2, 'Y':3, 'Z':2}
letter_keys = [K_a, K_b, K_c, K_d, K_e, K_d, K_e, K_f, K_g, K_h, K_i, K_j, K_k, K_l, K_m, K_n, K_o, K_p, K_q, K_r, K_s, K_t, K_u, K_t, K_v, K_w, K_x, K_y, K_z]

flip_delay = 1000 # Delay before flip in ms
flip_status = ''

class Banana_server:
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
        self.time_flip = 0

        self.time_last_take = time.time()
        self.p1_last_take = time.time()
        self.p2_last_take = time.time()

        self.current_prev = []
        self.player1words_prev = {}
        self.player1words_list_prev = []
        self.player2words_prev = {}
        self.player2words_list_prev = []

        self.status = ''

        self.gameover = False

    def flip(self):
        self.updated = True

        if not self.tiles:
            self.status = f"No more tiles! Your score: {sum([len(i) for i in self.playerwords_list])}, Opponent's score: {sum([len(i) for i in self.player2words_list])}"
            self.graphics_to_update = self.graphics_to_update + ['status']

            self.gameover = True

            return None

        self.last_update = datetime.datetime.now()

        last = self.tiles.pop()
        self.current.append(last)

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

    def update(self, update_dict, player):
        # If game can be updated according to the update_dict, then update
        # If game cannot be updated, it means that it clashes with a previous update (opponent taking just before)
        # Check to see the take times and if this update_dict's take_time is earlier, then override

        """
        update_dict: {flip_request, candidate, etym_candidate, taken_word, used_tiles, victim, taken_i, taketime}
        """

        if self.flip_waiting and time.time() > self.time_flip:
            self.flip()
            self.flip_waiting = False
            self.last_flip_update = time.time()
        elif not self.gameover and not self.flip_waiting and update_dict['flip_request']:
            self.flip_waiting = True
            self.time_flip = time.time() + 2

        candidate = update_dict['candidate']
        taken_word = update_dict['taken_word']
        victim = update_dict['victim']
        etym_candidate = update_dict['etym_candidate']
        taketime = update_dict['taketime']
        taken_i = update_dict['taken_i']

        # Decide whether to update, not to update or to overwrite
        action = self.__check_new_take(player, taketime, candidate)

        if action == 'update':
            # Save previous versions of game state in case
            self.current_prev = self.current.copy()
            self.player1words_prev = self.player1words.copy()
            self.player1words_list_prev = self.player1words_list.copy()
            self.player2words_prev = self.player2words.copy()
            self.player2words_list_prev = self.player2words_list.copy()


            # Update last take times
            if player == 1:
                self.p1_last_take = taketime
            else:
                self.p2_last_take = taketime

            # Update middle letters
            for letter in update_dict['used_tiles']:
                self.current.remove(letter)

            self.__update_word_lists(player, victim, candidate, etym_candidate, taken_word, taken_i)
            self.last_update = time.time()

            taker = player


        elif action == 'overwrite':
            # Restore previous version of game state
            self.current = self.current_prev.copy()
            self.player1words = self.player1words_prev.copy()
            self.player1words_list = self.player1words_list_prev.copy()
            self.player2words = self.player2words_prev.copy()
            self.player2words_list = self.player2words_list_prev.copy()

            # Update last take times
            if player == 1:
                self.p1_last_take = taketime
            else:
                self.p2_last_take = taketime

            # Update middle letters
            for letter in update_dict['used_tiles']:
                self.current.remove(letter)

            self.__update_word_lists(player, victim, candidate, etym_candidate, taken_word, taken_i)
            self.last_update = time.time()
            taker = player

        else:
            self.status = ''
            taker = ''

        send_dict = {'game_over': self.gameover,
                     'flip_waiting': self.flip_waiting,
                     'current': self.current,
                     'player1words': self.player1words,
                     'player1words_list': self.player1words_list,
                     'player2words': self.player2words,
                     'player2words_list': self.player2words_list,
                     'taker': taker,
                     'candidate': candidate,
                     'etym_candidate': etym_candidate,
                     'taken word': taken_word,
                     'used_tiles': update_dict['used_tiles'],
                     'victim': victim,
                     'taken i': taken_i,
                     'last_update': self.last_update,
                     'last_flip_update': self.last_flip_update,
                     'status': self.status
                     }

        return send_dict





