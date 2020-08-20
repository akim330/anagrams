import socket
from _thread import *
import sys
import datetime
import time
import pickle

from banana_server import Banana_server

# from anagrams_network7_new import banana # UPDATE

print_check = True

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = '192.168.1.3'
port = 5555

server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for a connection")

game = Banana_server()

recv_dicts = [{}, {}]


currentId = "0"
def threaded_client(conn, player):
    global currentId, pos

    send_dict_init = {'game_over': False,
                      'flip_waiting': False,
                      'current': [],
                      'player1words': {},
                      'player1words_list': [],
                      'player2words': {},
                      'player2words_list': [],
                      'taker': 0,
                      'candidate': '',
                      'etym_candidate': '',
                      'taken word': '',
                      'used_tiles': [],
                      'victim': '',
                      'taken i': -1,
                      'last_update': time.time(),
                      'last_flip_update': time.time()
                      }

    conn.send(pickle.dumps(send_dict_init))
    print(f"{conn.getsockname()[0]}: Current ID: {currentId}")
    currentId = "1"
    print(f"{conn.getsockname()[0]}: Current ID: {currentId}")
    reply = ''
    while True:
        try:

            data = pickle.loads(conn.recv(2048))
            recv_dicts[player] = data
            if not data:
                conn.send(str.encode("Goodbye"))
                break
            else:
                # Take the received dict and update the game. Returns send_dict
                send_dict = game.update(data, player)

            conn.sendall(pickle.dumps(send_dict))
        except:
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
