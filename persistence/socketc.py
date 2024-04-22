import socket

class MulticastSocket():
    def __init__(self, multicast_group, port):
        self.multicast_group = multicast_group
        self.port = port
        self.socket = self.init_connection()

    def init_connection(self) -> socket:
        sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return sck

    def send_msg(self, message):
        self.socket.sendto(message, (self.multicast_group, self.port))