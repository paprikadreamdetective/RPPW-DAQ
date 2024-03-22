
#import socket
from SocketConnector import SocketConnector 
import time
multicast_group = ('224.10.10.5', 10000)

#sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#server_address = ('192.168.100.136', 999)

print('Connecting to {} port {}'.format(*multicast_group))

web_socket_sender = SocketConnector('224.10.10.5', 10000)


#sck.connect(server_address)

while True:
#try:
  message = b'Im Raspberry Pi Pico W, Whats u r name?'
  print('sending {!r}'.format(message))
  web_socket_sender.send_msg(message)
  time.sleep(1)
    #sent = sck.sendto(message, multicast_group)
    #sck.sendall(message)
    
    #amount_received = 0
    #amount_expected = len(message)
    #while amount_received < amount_expected:
    #    data = sck.recv(32)
    #    amount_received += len(data)
    #    print('received {!r}'.format(data))
#finally:
#    print('closing socket')
#    sck.close()
  

'''
import socket
import time
sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('192.168.100.136', 999)

print('connecting to {} port {}'.format(*server_address))
sck.connect(server_address)

while True:
  #try:
  message = b'It is very long message but will only be transmitted in chunks of 16 at a time'
  print('sending {!r}'.format(message))
  sck.sendall(message)
  amount_received = 0
  amount_expected = len(message)
    #while amount_received < amount_expected:
    #    data = sck.recv(32)
    #    amount_received += len(data)
    #    print('received {!r}'.format(data))
  #finally:
    #print('closing socket')
    #sck.close()
  time.sleep(10)
'''