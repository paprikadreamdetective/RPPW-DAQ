import socket

class Socket:
    def __init__(self, multicast_group, port):
        self.multicast_group = multicast_group
        self.port = port
        self.socket = self.init_connection()

    def init_connection(self) -> socket:
        sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sck.bind(('', self.port))  # Bind to port to receive messages
        mreq = socket.inet_aton(self.multicast_group) + socket.inet_aton('0.0.0.0')
        sck.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        return sck

    def send_msg(self, message):
        self.socket.sendto(message, (self.multicast_group, self.port))

    def receive_msg(self):
        data, address = self.socket.recvfrom(1024)  # Buffer size 1024 bytes
        print(f"Received message from {address}: {data.decode()}")