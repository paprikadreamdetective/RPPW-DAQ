import network
import time

def int_to_ascii(list_number: list)-> str:
  string = ''
  for i in range(0, len(list_number)):
      string = string + chr(list_number[i])
  return string

def init_connection(ssid: str, key: str) -> network:
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, key)
    return wlan
    #print(wlan.isconnected())
    #time.sleep(5)