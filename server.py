import socket
from _thread import *
import sys
import datetime

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = '192.168.1.8'
port = 5555

server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for a connection")

currentId = "0"
data_all = ["0|[]|{}|[]|{}|[]|0001-01-01 00:00:00.000000", "1|[]|{}|[]|{}|[]|0001-01-01 00:00:00.000000"]
def threaded_client(conn):
    global currentId, pos
    conn.send(str.encode(currentId))
    print(f"{conn.getsockname()[0]}: Current ID: {currentId}")
    currentId = "1"
    print(f"{conn.getsockname()[0]}: Current ID: {currentId}")
    reply = ''
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode('utf-8')
            if not data:
                conn.send(str.encode("Goodbye"))
                break
            else:
                arr = reply.split("|")
                id = int(arr[0])
                data_all[id] = reply

                print(f"{conn.getsockname()[0]}: Current ID: {currentId}, ID: {id}" + "Received: " + reply)

                if id == 0: nid = 1
                if id == 1: nid = 0

                reply = data_all[nid][:]
                print(f"{conn.getsockname()[0]}: Current ID: {currentId}, ID: {id}" + "Sending: " + reply)

            conn.sendall(str.encode(reply))
        except:
            break

    print("Connection Closed")
    conn.close()

while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)
    print(f"conn: {conn}")

    start_new_thread(threaded_client, (conn,))