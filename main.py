from model.SocketConnector import SocketConnector 
from model.MQ135 import MQ135

import time
import machine
multicast_group = '224.10.10.5' 
port = 10000
print('Connecting to ' + str(multicast_group) + ' : ' + str(port))
led = machine.Pin('LED', machine.Pin.OUT)

temperature = 7.0
humidity = 61.0

mq135 = MQ135(28)

#analog_pin = machine.ADC(28)

web_socket_sender = SocketConnector(multicast_group, port)

while True:
  #message = b'Im Raspberry Pi Pico W, Whats u r name?'

  rzero = mq135.get_rzero()
  corrected_rzero = mq135.get_corrected_rzero(temperature, humidity)
  resistance = mq135.get_resistance()
  ppm = mq135.get_ppm()
  corrected_ppm = mq135.get_corrected_ppm(temperature, humidity)

  print("MQ135 RZero: " + str(rzero) +"\t Corrected RZero: "+ str(corrected_rzero)+
  "\t Resistance: "+ str(resistance) +"\t PPM: "+str(ppm)+
  "\t Corrected PPM: "+str(corrected_ppm)+"ppm")


  #message = str(read_mq135())
  #print('Lectura del sensor MQ-135: ' + message + ' ppm')
  #print('Sending {!r}'.format(message))
  #web_socket_sender.send_msg(message)
  led.off()
  time.sleep_ms(500)
  led.on()
  
