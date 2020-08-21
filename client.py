import pygame
import datetime
import time
from collections import Counter
import twl
import api
import sys
from network import Network
import pickle

from banana import Banana
from take import Take

import pygame, sys
from pygame.locals import *

time_check = True
print_check = True
no_prefix_suffix = True

# Need to display pygame

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

letter_keys = [K_a, K_b, K_c, K_d, K_e, K_d, K_e, K_f, K_g, K_h, K_i, K_j, K_k, K_l, K_m, K_n, K_o, K_p, K_q, K_r, K_s, K_t, K_u, K_t, K_v, K_w, K_x, K_y, K_z]


class Graphics:
    def __init__(self):
        #  ________
        # | LAYOUT |
        #  --------

        # 'Current'
        ''''
        font_current = 'freesansbold.ttf'
        size_current = 32
        color_current = BLACK
        x_current = 10
        y_current = 20
        '''

        self.current = {'font': 'freesansbold.ttf',
                        'size': 32,
                        'color': BLACK,
                        'x': 10,
                        'y': 20}

        # Ready Flip
        """
        font_flip = 'freesansbold.ttf'
        size_flip = 20
        color_flip = BLACK
        x_flip = 20
        y_flip = 60
        """

        self.flip = {'font': 'freesansbold.ttf',
                     'size': 20,
                     'color': BLACK,
                     'x': 20,
                     'y': 60}

        # Tiles
        """
        font_tile = 'freesansbold.ttf'
        size_tile = 32
        color_tile = BLACK
        x_tile_0 = 150
        y_tile_0 = 38
        x_gap_tile = 30
        y_gap_tile = 50
        """

        self.tile = {'font': 'freesansbold.ttf',
                     'size': 32,
                     'color': BLACK,
                     'x_0': 150,
                     'y_0': 38,
                     'x_gap': 30,
                     'y_gap': 50}

        # 'Your Words'
        '''
        font_your = 'freesansbold.ttf'
        size_your = 32
        color_your = BLACK
        x_your = 10
        y_your = 100
        y_gap_your = 50
        '''

        self.your = {'font': 'freesansbold.ttf',
                     'size': 32,
                     'color': BLACK,
                     'x': 10,
                     'y': 100,
                     'y_gap': 50}

        # Your Words

        '''
        font_words = 'freesansbold.ttf'
        size_words = 32
        color_words = BLACK
        x_words = 10
        y_words = y_your + y_gap_your
        x_gap_words = 150
        y_gap_words = 50
        '''

        self.self_words = {'font': 'freesansbold.ttf',
                     'size': 32,
                     'color': BLACK,
                     'x': 10,
                     'y': self.your['y'] + self.your['y_gap'],
                     'x_gap': 150,
                     'y_gap': 50}

        # 'Opponent's Words'
        '''
        font_opp = 'freesansbold.ttf'
        size_opp = 32
        color_opp = BLACK
        x_opp = 300
        y_opp = 100
        y_gap_opp = 50
        '''
        self.opp = {'font': 'freesansbold.ttf',
                    'size': 32,
                    'color': BLACK,
                    'x': 300,
                    'y': 100,
                    'y_gap': 50}


        # Opponent's Words
        '''
        font_opp_words = 'freesansbold.ttf'
        size_opp_words = 32
        color_opp_words = BLACK
        x_opp_words = 300
        y_opp_words = y_opp + y_gap_opp
        x_gap_opp_words = 150
        y_gap_opp_words = 50
        '''

        self.opp_words = {'font': 'freesansbold.ttf',
                          'size': 32,
                          'color': BLACK,
                          'x': 300,
                          'y': self.opp['y'] + self.opp['y_gap'],
                          'x_gap': 150,
                          'y_gap': 50}

        self.color_taken = BLUE

        # Guess
        '''
        font_guess = 'freesansbold.ttf'
        size_guess = 32
        color_guess = BLACK
        x_guess = 10
        y_guess = 500
        '''

        self.guess = {'font': 'freesansbold.ttf',
                      'size': 32,
                      'color': BLACK,
                      'x': 10,
                      'y': 500}

        # Status
        """
        font_status = 'freesansbold.ttf'
        size_status = 24
        color_status = BLACK
        x_status = 10
        y_status = 550
        """

        self.status = {'font': 'freesansbold.ttf',
                       'size': 24,
                       'color': BLACK,
                       'x': 10,
                       'y': 550}

        self.fontObjs = {'current': pygame.font.Font(self.current['font'], self.current['size']),
                         'tile': pygame.font.Font(self.tile['font'], self.tile['size']),
                         'your': pygame.font.Font(self.your['font'], self.your['size']),
                         'self_words': pygame.font.Font(self.self_words['font'], self.self_words['size']),
                         'guess': pygame.font.Font(self.guess['font'], self.guess['size']),
                         'status': pygame.font.Font(self.status['font'], self.status['size']),
                         'flip': pygame.font.Font(self.flip['font'], self.flip['size']),
                         'opp': pygame.font.Font(self.your['font'], self.your['size']),
                         'opp_words': pygame.font.Font(self.self_words['font'], self.self_words['size']),
                         }

        self.SurfObjs = {'current': self.fontObjs['current'].render('Current: ', True, self.current['color']),
                         'tiles_list': [],
                         'your': self.fontObjs['your'].render('Your Words: ', True, self.your['color']),
                         'self_words_list': [],
                         'opp': self.fontObjs['opp'].render('Opponent\'s Words: ', True, self.opp['color']),
                         'opp_words_list': [],
                         'guess': self.fontObjs['guess'].render('Take: ', True, self.guess['color']),
                         'status': self.fontObjs['status'].render('', True, self.status['color']),
                         'flip': self.fontObjs['flip'].render('', True, self.flip['color'])
                         }

    def __numwords_to_fontsize(self, numwords):
        if numwords <= 6:
            return int(self.self_words['size'] / 1.25), int(self.self_words['y_gap'] / 1.25)
        elif 6 < numwords <= 10:
            return int(self.self_words['size'] / 1.75), int(self.self_words['y_gap'] / 1.75)
        elif 10 < numwords <= 20:
            return int(self.self_words['size'] / 2), int(self.self_words['y_gap'] / 2)
        elif 20 < numwords <= 50:
            return int(self.self_words['size'] / 3), int(self.self_words['y_gap'] / 3)

    def __numtiles_to_fontsize(self, numtiles):
        if numtiles <= 10:
            return self.tile['size'], self.tile['y_gap'], self.tile['x_gap']
        elif 10 < numtiles <= 40:
            return int(self.tile['size'] / 1.5), int(self.tile['y_gap'] / 1.5), int(self.tile['x_gap'] / 1.5)
        elif 40 < numtiles <= 60:
            return int(self.tile['size'] / 2), int(self.tile['y_gap'] / 2), int(self.tile['x_gap'] / 2)
        elif 60 < numtiles <= 144:
            return int(self.tile['size'] / 4), int(self.tile['y_gap'] / 4), int(self.tile['x_gap'] / 4)

    def display_text(self, SurfaceObj, x, y):
        textRectObj = SurfaceObj.get_rect()
        textRectObj.topleft = (x, y)
        DISPLAYSURF.blit(SurfaceObj, textRectObj)
        return textRectObj

    def display_text_tiles(self, SurfaceObj, x, y):
        textRectObj = SurfaceObj.get_rect()
        textRectObj.center = (x, y)
        DISPLAYSURF.blit(SurfaceObj, textRectObj)
        return textRectObj

    def printstatus(self, game, player, graphics_to_update, guess, status):

        rects_to_update = []

        if player == 0:
            self_words_list = game.player1words_list
            self_words = game.player1words
            opp_words_list = game.player2words_list
            opp_words = game.player2words
        else:
            self_words_list = game.player2words_list
            self_words = game.player2words
            opp_words_list = game.player1words_list
            opp_words = game.player1words

        # Make the surface objects (or lists of surface objects)

        size_tiles, y_gap_tile, x_gap_tile = self.__numtiles_to_fontsize(len(game.current))

        if 'flip' in graphics_to_update or 'flip_status' in graphics_to_update:
            print(f"Updating flip status to {game.flip_status}!")
            self.SurfObjs['flip'] = self.fontObjs['flip'].render(game.flip_status, True, self.flip['color'])


        if 'tiles' in graphics_to_update:
            print("UPDATING TILES")
            self.SurfObjs['tiles_list'] = []

            self.fontObjs['tile'] = pygame.font.Font(self.self_words['font'], size_tiles)

            for tile in game.current:
                self.SurfObjs['tiles_list'].append(self.fontObjs['tile'].render(tile, True, self.tile['color']))

        if 'self_words' in graphics_to_update:
            self.SurfObjs['self_words_list'] = []

            size_words, y_gap_words = self.__numwords_to_fontsize(len(self_words_list))
            self.fontObjs['self_words'] = pygame.font.Font(self.self_words['font'], size_words)

            if who_took == 'self':
                for i, word in enumerate(self_words_list):
                    if i == game.new_word_i:
                        self.SurfObjs['self_words_list'].append(self.fontObjs['self_words'].render(word, True, self.color_taken))
                    else:
                        self.SurfObjs['self_words_list'].append(self.fontObjs['self_words'].render(word, True, self.self_words['color']))
            else:
                for word in self_words_list:
                    self.SurfObjs['self_words_list'].append(self.fontObjs['self_words'].render(word, True, self.self_words['color']))

        if 'opp_words' in graphics_to_update:
            self.SurfObjs['opp_words_list'] = []

            size_opp_words, y_gap_opp_words = self.__numwords_to_fontsize(len(opp_words_list))
            self.fontObjs['opp_words'] = pygame.font.Font(self.opp_words['font'], size_opp_words)

            if who_took == 'opp':
                for i, word in enumerate(opp_words_list):
                    if i == game.new_word_i:
                        self.SurfObjs['opp_words_list'].append(self.fontObjs['opp_words'].render(word, True, self.color_taken))
                    else:
                        self.SurfObjs['opp_words_list'].append(self.fontObjs['opp_words'].render(word, True, self.opp_words['color']))
            else:
                for word in opp_words_list:
                    self.SurfObjs['opp_words_list'].append(self.fontObjs['opp_words'].render(word, True, self.opp_words['color']))

        if 'guess' in graphics_to_update:
            self.SurfObjs['guess'] = self.fontObjs['guess'].render('Take: ' + guess, True, self.guess['color'])

        if 'status' in graphics_to_update:
            print(f"UPDATING STATUS: {status}")
            self.SurfObjs['status'] = self.fontObjs['status'].render(status, True, self.status['color'])

        # Display all the surface objects created above

        y_tile = self.tile['y_0']
        x_tile = self.tile['x_0']

        rect_tiles = self.display_text(self.SurfObjs['current'], self.current['x'], self.current['y'])

        for i, tile in enumerate(self.SurfObjs['tiles_list']):
            x_tile = x_tile + self.tile['x_gap']

            self.display_text_tiles(tile, x_tile, y_tile)

            if i % 20 == 19:
                y_tile = y_tile + y_gap_tile
                x_tile = self.tile['x_0']

        _ = self.display_text(self.SurfObjs['your'], self.your['x'], self.your['y'])


        x_words_local = self.self_words['x']
        y_words_local = self.self_words['y']

        rect_self_list = []

        for i, word in enumerate(self.SurfObjs['self_words_list']):

            rect_self_list.append(self.display_text(word, x_words_local, y_words_local))

            if i % 10 == 9:
                x_words_local = x_words_local + self.self_words['x_gap']
                y_words_local = self.self_words['y'] - self.self_words['y_gap']

            y_words_local = y_words_local + self.self_words['y_gap']

        rect_guess = self.display_text(self.SurfObjs['guess'], self.guess['x'], self.guess['y'])


        _ = self.display_text(self.SurfObjs['opp'], self.opp['x'], self.opp['y'])


        x_opp_words_local = self.opp_words['x']
        y_opp_words_local = self.opp_words['y']

        rect_opp_list = []

        for i, word in enumerate(self.SurfObjs['opp_words_list']):

            rect_opp_list.append(self.display_text(word, x_opp_words_local, y_opp_words_local))

            if i % 10 == 9:
                x_opp_words_local = x_opp_words_local + self.opp_words['x_gap']
                y_opp_words_local = self.opp_words['y'] - self.opp_words['y_gap']

            y_opp_words_local = y_opp_words_local + self.opp_words['y_gap']

        rect_flip = self.display_text(self.SurfObjs['flip'], self.flip['x'], self.flip['y'])

        rect_status = self.display_text(self.SurfObjs['status'], self.status['x'], self.status['y'])

        if 'flip' in graphics_to_update or 'flip_status' in graphics_to_update:
            rects_to_update.append(rect_flip)
        if 'tiles' in graphics_to_update:
            rects_to_update.append(rect_tiles)
        if 'self_words' in graphics_to_update:
            rects_to_update = rects_to_update + rect_self_list
        if 'opp_words' in graphics_to_update:
            rects_to_update = rects_to_update + rect_opp_list
        if 'guess' in graphics_to_update:
            rects_to_update.append(rect_guess)
        if 'status' in graphics_to_update:
            rects_to_update.append(rect_status)

        # Reset graphics_to_update
        graphics_to_update = []

        return rects_to_update


def other_player(player):
    if player == 0:
        return 1
    else:
        return 0

##### MAIN #####

global FPSCLOCK, DISPLAYSURF

pygame.init()

FPSCLOCK = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

pygame.display.set_caption('Anagrams')

# dict to send to server
send_dict = {'event': 'none',
             'take': None,
             'time_since_update': None,
             }

# get the initial game state

guess = ''
status = ''
last_update = 0
last_type = 0

clock = pygame.time.Clock()

net = Network()

player = net.get_id()

graphics = Graphics()

game = net.send(send_dict)

DISPLAYSURF.fill(BGCOLOR)
rects_to_update = graphics.printstatus(game, player, ['flip', 'status', 'guess'], guess, status)
pygame.display.update()

# Time check variables

while True:


    FPSCLOCK.tick(60)

    graphics_to_update = []

    if time_check:
        start_loop = time.time()
        total_take = 0
        total_send = 0
        total_update = 0
        total_display = 0


    DISPLAYSURF.fill(BGCOLOR)

    #  -------------
    # |  GAME LOOP  |
    #  -------------

    for event in pygame.event.get():

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if game.game_over and time.time() - last_update > 3.0:
            if player == 0:
                status = f"No more tiles! Your score: {sum([len(i) for i in game.player1words_list])}, Opponent's score: {sum([len(i) for i in game.player2words_list])}"
            else:
                status = f"No more tiles! Your score: {sum([len(i) for i in game.player2words_list])}, Opponent's score: {sum([len(i) for i in game.player1words_list])}"

            graphics_to_update = graphics_to_update + ['status']


        if event.type == KEYDOWN:
            if event.key == K_BACKSPACE:
                if guess == '':
                    pass
                else:
                    # Delete one letter from the guess
                    guess = guess[:-1]
                    graphics_to_update = graphics_to_update + ['guess']
                    last_type = time.time()

            elif event.key == K_SPACE:
                # Don't do anything if input is a space
                pass

            elif event.key == K_RETURN:
                # if Return and no guess is present, then flip next tile. If guess is present, see if it's a take
                if guess == '':
                    if not game.game_over:
                        send_dict['event'] = 'flip_request'
                        graphics_to_update = graphics_to_update + ['flip_status']

                else:
                    take_start_time = time.time()

                    if time_check:
                        start_take = take_start_time

                    guess_upper = guess.upper()
                    result, take_obj = game.take(guess_upper, player, last_update)

                    guess = ''
                    graphics_to_update = graphics_to_update + ['guess', 'status']

                    if result == 'steal':
                        send_dict['event'] = 'steal'
                        send_dict['take'] = take_obj
                    else:
                        send_dict['event'] = 'none'

                        if result == 'tiles':
                            status = f"Tiles aren't there! ({guess_upper})"
                        elif result == 'trivial':
                            status = f"Same root! ({game.same_root_word} and {guess_upper} share root {game.root})"
                        elif result == 'prefix_suffix':
                            status = f"Prefix or suffix not allowed! ({guess_upper})"
                        elif result == 'not_word':
                            status = f'Not a word! ({guess_upper})'
                        elif result == 'short':
                            status = f'Too short! ({guess_upper})'
                        else:
                            print("Error! Result is none of the options!")

                    if time_check:
                        end_take = time.time()
                        total_take = end_take - start_take


            elif event.key in letter_keys:
                print(f"TYPED {event.unicode.upper()}")
                # if letter is typed then add it to the current guess
                guess = guess + event.unicode.upper()
                graphics_to_update = graphics_to_update + ['guess']
                last_type = time.time()

    #  ----------
    # |  UPDATE  |
    #  ----------

    current_time = time.time()
    print(f"CURRENT TIME: {current_time}, LAST TYPE: {last_type}, UPDATE? {time.time() - last_type > 0.2}")

    if send_dict['event'] != 'none' or time.time() - last_type > 0.2:
        # Send our send_dict, receive a Banana
        send_dict['time_since_update'] = time.time() - last_update
        # print(send_dict)

        if time_check:
            start_send = time.time()

        recv_game = net.send(send_dict)

        if time_check:
            end_send = time.time()
            total_send = end_send - start_send

        send_dict['event'] = 'none'

        if recv_game and recv_game.update_number > game.update_number:

            if time_check:
                start_update = time.time()

            game = recv_game

            print(f"My ID: {player}")
            print(f"Recv Game current: {recv_game.current}")
            print(f"Game current: {game.current}")
            print(f"Update event: {game.update_event}")
            print(f"Recv flip status: {recv_game.flip_status}")
            print(f"Flip status: {game.flip_status}")
            print(f"Recv Player 1 words: {recv_game.player1words_list}")
            print(f"Recv Player 2 words: {recv_game.player2words_list}")
            print(f"Player 1 words: {game.player1words_list}")
            print(f"Player 2 words: {game.player2words_list}")

            if game.update_event == 'take':
                last_update = time.time()
                graphics_to_update = graphics_to_update + ['tiles', 'self_words', 'opp_words', 'status']

                if game.last_take.taker == player:
                    taker = "You"
                    if game.last_take.victim == player:
                        victim = "yourself"
                    elif game.last_take.victim == other_player(player):
                        victim = "opponent"
                    else:
                        victim = "the middle"
                else:
                    taker = "Opponent"
                    if game.last_take.victim == player:
                        victim = "you"
                    elif game.last_take.victim == other_player(player):
                        victim = "themselves"
                    else:
                        victim = "the middle"

                if victim == "the middle":
                    status = f"{taker} took {game.last_take.candidate} from {victim}!"
                else:
                    status = f"{taker} took {game.last_take.candidate} from {victim}! ({game.last_take.taken_word} -> {game.last_take.candidate})"

                if game.taker_id == id:
                    who_took = 'self'
                else:
                    who_took = 'opp'

            elif game.update_event == 'flip_request':
                graphics_to_update = graphics_to_update + ['flip_status']
            elif game.update_event == 'flip':
                graphics_to_update = graphics_to_update + ['flip_status', 'tiles']
                last_update = time.time()

            if time_check:
                end_update = time.time()
                total_update = end_update - start_update

    if time_check:
        start_printstatus = time.time()

    rects_to_update = graphics.printstatus(game, player, graphics_to_update, guess, status)

    if time_check:
        total_printstatus = time.time() - start_printstatus
        start_display = time.time()

    print(f"Updating the displays: {rects_to_update}")
    pygame.display.update(rects_to_update)

    if time_check:
        total_display = time.time() - start_display

    if time_check:
        total_loop = time.time() - start_loop
        print(f"Total time: {total_loop}, Take time: {total_take}, Send time: {total_send}, Update time: {total_update}, Printstatus time: {total_printstatus}, Display time: {total_display} ")


