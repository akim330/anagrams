import socket
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = '50.116.53.35'
        # self.host = "192.168.1.3" # For this to work on your machine this must be equal to the ipv4 address of the machine running the server
                                    # You can find this address by typing ipconfig in CMD and copying the ipv4 address. Again this must be the servers
                                    # ipv4 address. This feild will be the same for all your clients.
        self.port = 5555
        self.addr = (self.host, self.port)
        print("Network: gonna connect")
        self.id = int(self.connect())
        print("Network: finished!")

    def connect(self):
        self.client.connect(self.addr)
        print("Network: connected!")
        return self.client.recv(2048).decode()

    def get_id(self):
        return self.id


    def send(self, data):
        """
        :param data: str
        :return: str
        """
        #try:
        print("Sending data")
        self.client.send(pickle.dumps(data))
        print("Gonna receive data")
        data = []
        while True:
            packet = self.client.recv(4096)
            if not packet: break
            data.append(packet)
        return pickle.loads(b"".join(data))

        # return pickle.loads(self.client.recv(4096))
        """
        except:
            print("Error!")
            return None
        """