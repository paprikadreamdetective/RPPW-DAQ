import WLAN_connection 
from machine import Pin
ssid = 'Totalplay-65A5'
password = '65A52884MYHBTyWx'

#station = network.WLAN(network.STA_IF)
station = WLAN_connection.init_connection(ssid, password)
#station.active(True)
#station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())

led = Pin("LED", Pin.OUT)
led.on()