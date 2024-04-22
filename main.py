import sys
import time
import select
import machine
from config import cfg
import wlanc 
from client.persistence.socketc import MulticastSocket 
from MQ135 import MQ135

# Set up the poll object
poll_obj = select.poll()
poll_obj.register(sys.stdin, select.POLLIN)

def main():
  station = wlanc.init_connection(cfg['wlan']['ssid'], cfg['wlan']['pswd'])
  while station.isconnected() == False:
    pass
  print('WiFi Connection is successful')
  led = machine.Pin('LED', machine.Pin.OUT)
  sensor_mq135 = MQ135(28)
  print('Connecting to: 224.10.10.10 : 10000')
  socket_sender = MulticastSocket('224.10.10.10', 10000)
  while True:
    ppm_CO2_actual = sensor_mq135.read()
    print('Valor actual: ' + str(ppm_CO2_actual) + ' ppm')
    message = str(ppm_CO2_actual) 
    socket_sender.send_msg(message)
    led.toggle()
    time.sleep_ms(500)     

  
    # Wait for input on stdin
    #poll_results = poll_obj.poll(1) # the '1' is how long it will wait for message before looping again (in microseconds)
    #if poll_results:
        # Read the data from stdin (read data coming from PC)
        #data = sys.stdin.readline().strip()
        # Write the data to the input file
        #sys.stdout.write("received data: " + data + "\r")
        ###################
        #ppm_CO2_actual = sensor_mq135.read()
        #print('Valor actual: ' + str(ppm_CO2_actual) + ' ppm')
        #print('Informacion:')
        #print(data)
        #message = str(ppm_CO2_actual) 
        #message = data.decode()
        
  
if __name__ == '__main__':
  main()