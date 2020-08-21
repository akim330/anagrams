import socket
from _thread import *
import sys
import datetime
import time
import pickle

from banana import Banana
from take import Take


print_check = False

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = ''
port = 5555

server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for a connection")

game = Banana()

recv_dicts = [{}, {}]

flip_delay = 1.5

pending_take = None

def other_player(player):
    if player == 0:
        return 1
    else:
        return 0

currentId = "0"
def threaded_client(conn, player):
    global currentId, pos, pending_take

    conn.send(str.encode(str(player)))

    print(f"{conn.getsockname()[0]}: Current ID: {currentId}")
    currentId = "1"
    print(f"{conn.getsockname()[0]}: Current ID: {currentId}")
    reply = ''
    while True:

        if not game.tiles:
            game.game_over = True


        if print_check:
            print(f"Flip_waiting: {game.flip_waiting}; Flip time: {game.flip_time}; Current time: {time.time()}")

        if game.flip_waiting and time.time() > game.flip_time:
            game.flip()
            game.flip_waiting = False
            game.flip_status = 'Flipped!'

            game.update_event = 'flip'
            game.update_number += 1


        try:

            data = pickle.loads(conn.recv(2048))

            if not data:
                conn.send(str.encode("Goodbye"))
                break
            else:
                if data['event'] == 'steal':
                    if pending_take:
                        if pending_take.taker != player:
                            if game.both_can_take(pending_take, data['take']):
                                game.update(pending_take, pending_take.taker)
                                game.update(data['take'], player)

                            elif data['take'].take_time < pending_take.take_time:
                                # TAKE
                                game.last_take = data['take']
                                game.update(game.last_take, player)
                                pending_take = None
                            else:
                                # TAKE
                                game.last_take = pending_take
                                game.update(game.last_take, pending_take.taker)
                                pending_take = None

                            game.update_event = 'take'
                            game.update_number += 1

                        else:
                            print('Submitting the same take')

                    else:
                        # No pending take, so this take becomes the pending take if you can still take it
                        if game.can_take(data['take']):
                            pending_take = data['take']

                else:
                    if pending_take and pending_take.taker != player and data['time_since_update'] > pending_take.take_time:
                        # TAKE
                        game.last_take = pending_take
                        game.update(game.last_take, other_player(player))
                        pending_take = None

                        game.update_event = 'take'
                        game.update_number += 1



                    elif data['event'] == 'flip_request':
                        if not game.flip_waiting:
                            game.flip_waiting = True
                            game.flip_time = time.time() + flip_delay
                            game.flip_status = 'Ready...'

                            game.update_event = 'flip_request'
                            game.update_number += 1

            conn.sendall(pickle.dumps(game))
        except socket.error as e:
            print(str(e))
            break

    print("Connection Closed")
    conn.close()


currentplayer = 0

while True:
    conn, addr = s.accept() # this gets the client socket object
    print("Connected to: ", addr)
    print(f"conn: {conn}")

    start_new_thread(threaded_client, (conn, currentplayer))

    currentplayer += 1
