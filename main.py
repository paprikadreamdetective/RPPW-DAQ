from model.SocketConnector import SocketConnector 
import time
import machine
multicast_group = '224.10.10.5' 
port = 10000
print('Connecting to ' + str(multicast_group) + ' : ' + str(port))
led = machine.Pin('LED', machine.Pin.OUT)

analog_pin = machine.ADC(28)

web_socket_sender = SocketConnector(multicast_group, port)

def read_mq135():
  adc_value = analog_pin.read_u16()
  #mq135_ppm = adc_value * (3300 / 65535.0)
  mq135_ppm = adc_value
  return mq135_ppm

while True:
  #message = b'Im Raspberry Pi Pico W, Whats u r name?'
  message = str(read_mq135())
  print('Lectura del sensor MQ-135: ' + message + ' ppm')
  print('Sending {!r}'.format(message))
  web_socket_sender.send_msg(message)
  led.off()
  time.sleep_ms(500)
  led.on()
  
