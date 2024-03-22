import WLAN_connection 
#from model.WLAN_connection import init_connection
#from model.MQTT_connection import init_connection_mqtt

from machine import Pin
topic = b'HelloMQTT/temp'
PUBLISH_TOPIC = b"temp"
ssid = 'Totalplay-65A5'
password = '65A52884MYHBTyWx'
msg = 'Im In'
station = WLAN_connection.init_connection(ssid, password)
last_publish = time.time()
publish_interval = 5

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())

led = Pin("LED", Pin.OUT)

def sub_cb(topic, msg):
  print((topic, msg))
  if msg.decode() == "ON":
    led.value(1)
  else:
    led.value(0)

try:
  client = MQTT_connection.init_connection()
  client.set_callback(sub_cb)
  client.connect()
  client.subscribe(topic)
  print(f"Connected to MQTT  Broker :: {topic}, and waiting for callback function to be called!")
except OSError as e:
  print('Failed to connect to the MQTT Broker. Reconnecting...')
  time.sleep(5)
  #machine.reset()

while True:
  client.check_msg()
  
 
  if (time.time() - last_publish) >= publish_interval:
    random_temp = "Hi"
    client.publish(topic, str(random_temp).encode())
    last_publish = time.time()
    time.sleep(1)