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
from graphics_tiles import Graphics

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

letter_keys = [K_a, K_b, K_c, K_d, K_e, K_d, K_e, K_f, K_g, K_h, K_i, K_j, K_k, K_l, K_m, K_n, K_o, K_p, K_q, K_r, K_s, K_t, K_u, K_t, K_v, K_w, K_x, K_y, K_z]

def other_player(player):
    if player == 0:
        return 1
    else:
        return 0

##### MAIN #####

global FPSCLOCK, DISPLAYSURF

pygame.init()

FPSCLOCK = pygame.time.Clock()
# DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

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
taker = None

clock = pygame.time.Clock()

net = Network()

player = net.get_id()

graphics = Graphics()

game = net.send(send_dict)

# DISPLAYSURF.fill(BGCOLOR)
graphics.printstatus(game, player, ['flip', 'status', 'guess'], guess, status, taker)
# pygame.display.update()

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


    # DISPLAYSURF.fill(BGCOLOR)

    #  -------------
    # |  GAME LOOP  |
    #  -------------

    last = None

    for event in pygame.event.get():
        print(f"EVENT: {event}")


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
                if event.key != last:
                    # if letter is typed then add it to the current guess
                    # guess = guess + event.unicode.upper()
                    guess = guess + pygame.key.name(event.key).upper()
                    graphics_to_update = graphics_to_update + ['guess']
                    last_type = time.time()

                    last = event.key

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
                    taker = 'self'
                    taker_text = "You"
                    if game.last_take.victim == player:
                        victim = "yourself"
                    elif game.last_take.victim == other_player(player):
                        victim = "opponent"
                    else:
                        victim = "the middle"
                else:
                    taker = 'opp'
                    taker_text = "Opponent"
                    if game.last_take.victim == player:
                        victim = "you"
                    elif game.last_take.victim == other_player(player):
                        victim = "themselves"
                    else:
                        victim = "the middle"

                if victim == "the middle":
                    status = f"{taker_text} took {game.last_take.candidate} from {victim}!"
                else:
                    status = f"{taker_text} took {game.last_take.candidate} from {victim}! ({game.last_take.taken_word} -> {game.last_take.candidate})"


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

    graphics.printstatus(game, player, graphics_to_update, guess, status, taker)

    if time_check:
        total_printstatus = time.time() - start_printstatus
        start_display = time.time()

    # print(f"Updating the displays: {rects_to_update}")
    # pygame.display.update(rects_to_update)

    if time_check:
        total_display = time.time() - start_display

    if time_check:
        total_loop = time.time() - start_loop
        print(f"Total time: {total_loop}, Take time: {total_take}, Send time: {total_send}, Update time: {total_update}, Printstatus time: {total_printstatus}, Display time: {total_display} ")


