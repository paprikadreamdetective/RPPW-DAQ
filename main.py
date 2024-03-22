from model.SocketConnector import SocketConnector 
import time
import machine
multicast_group = '224.10.10.5' 
port = 10000
print('Connecting to ' + str(multicast_group) + ' : ' + str(port))
led = machine.Pin('LED', machine.Pin.OUT)
web_socket_sender = SocketConnector(multicast_group, port)

while True:
  message = b'Im Raspberry Pi Pico W, Whats u r name?'
  print('Sending {!r}'.format(message))
  web_socket_sender.send_msg(message)
  led.off()
  time.sleep_ms(500)
  led.on()
  
