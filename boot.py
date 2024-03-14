import model.WLAN_connection 
import model.MQTT_connection
import time
from machine import Pin

ssid = 'Totalplay-65A5'
password = '65A52884MYHBTyWx'
station = model.WLAN_connection.init_connection(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())

led = Pin("LED", Pin.OUT)



try:
  client = model.MQTT_connection.init_connection()
except OSError as e:
  print('Failed to connect to the MQTT Broker. Reconnecting...')
  time.sleep(5)
  machine.reset()

while True:
  
  client.publish("LabHardware", "led on")
  led.on()
  time.sleep(5)
  client.publish("LabHardware", "led off")
  led.off() 