import time
import machine
import WLAN_connection 
from model.SocketConnector import SocketConnector 
from MQ135 import MQ135

#ssid = 'labred'
#password = 'labred2017'
ssid = [84, 111, 116, 97, 108, 112, 108, 97, 121, 45, 54, 53, 65, 53]
password = [54, 53, 65, 53, 50, 56, 56, 52, 77, 89, 72, 66, 84, 121, 87, 120]
 
def main():
  station = WLAN_connection.init_connection(WLAN_connection.int_to_ascii(ssid), WLAN_connection.int_to_ascii(password))
  while station.isconnected() == False:
    pass
  print('WiFi Connection is successful')
  led = machine.Pin('LED', machine.Pin.OUT)
  mq135 = MQ135(28)
  print('Connecting to: 224.10.10.10 : 10000')
  web_socket_sender = SocketConnector('224.10.10.10', 10000)
  while True:
    ppm_CO2_actual = mq135.read()
    print('Valor actual: ' + str(ppm_CO2_actual) + ' ppm')
    message = str(ppm_CO2_actual) 
    web_socket_sender.send_msg(message)
    led.toggle()
    time.sleep_ms(500)
  
if __name__ == '__main__':
  main()