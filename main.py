import time
import machine
from config import cfg
import wlanc 
from socketc import MulticastSocket 
from MQ135 import MQ135

def main():
  station = wlanc.init_connection(cfg['wlan']['ssid'], cfg['wlan']['pswd'])
  while station.isconnected() == False:
    pass
  print('WiFi Connection is successful')
  led = machine.Pin('LED', machine.Pin.OUT)
  sensor_mq135 = MQ135(28)
  print('Connecting to: 224.10.10.10 : 10000')
  web_socket_sender = MulticastSocket('224.10.10.10', 10000)
  while True:
    ppm_CO2_actual = sensor_mq135.read()
    print('Valor actual: ' + str(ppm_CO2_actual) + ' ppm')
    message = str(ppm_CO2_actual) 
    web_socket_sender.send_msg(message)
    led.toggle()
    time.sleep_ms(500)
  
if __name__ == '__main__':
  main()