import network
import time

def init_connection(ssid: str, key: str) -> network:
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, key)
    return wlan
    #print(wlan.isconnected())
    #time.sleep(5)