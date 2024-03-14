import WLAN_connection 
import MQTT_connection
import time
from machine import Pin

ssid = 'Totalplay-65A5'
password = '65A52884MYHBTyWx'
station = WLAN_connection.init_connection(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())

led = Pin("LED", Pin.OUT)

client = MQTT_connection.init_connection

#led.on()
#time.sleep(1)
#led.off()