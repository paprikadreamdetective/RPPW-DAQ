'''
En el bloque try-except se intenta importar la libreria usocket
bajo el alias socket. Esto se hace pues usocket es una
version simplificada de socket, que a menudo se usa
en sistemas embebidos. 
'''
try:
    import usocket as socket 
except:
    import socket
'''
machine es un módulo en MicroPython que proporciona acceso 
a características específicas de hardware, como pines 
GPIO (General Purpose Input/Output).
'''
from machine import Pin
import network
'''
gc es un módulo que proporciona funciones para controlar la recolección de basura, 
útil para gestionar la memoria en sistemas con recursos limitados como 
los microcontroladores.
'''
import gc

gc.collect()


ssid = 'Totalplay-65A5'
password = '65A52884MYHBTyWx'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())

led = Pin("LED", Pin.OUT)
led.on()