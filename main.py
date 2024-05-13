import time
import utime
import machine
import json
from math import log
from config import cfg
import wlanc 
from socketc import Socket 
from mcp3008 import MCP3008
from aht10 import AHT10

CONFIG_THERMISTOR_RESISTOR = 9900

def thermistor_get_resistance(adcval):
    # calculamos la resistencia del NTC a partir del valor del ADC
    return (CONFIG_THERMISTOR_RESISTOR * ((1023.0 / adcval) - 1))

def thermistor_get_temperature(resistance):
    # variable de almacenamiento temporal, evita realizar varias veces el calculo de log
    temp = log(resistance)

    # resolvemos la ecuacion de STEINHART-HART
    # http://en.wikipedia.org/wiki/Steinhart–Hart_equation
    temp = 1 / (0.001129148 + (0.000234125 * temp) + (0.0000000876741 * temp * temp * temp))

    # convertir el resultado de kelvin a centigrados y retornar
    return temp - 273.15

def get_dissolved_oxygen(voltage):
    dissolved_oxygen = 0.4558 * voltage
    return dissolved_oxygen

def main():
  station = wlanc.init_connection(cfg['wlan']['ssid'], cfg['wlan']['pswd'])
  while station.isconnected() == False:
    pass
  print('WiFi Connection is successful')
  print('Connecting to: 224.10.10.10 : 10000')
  socket_sender = Socket('224.10.10.10', 10000)
  led = machine.Pin('LED', machine.Pin.OUT)
  measurements = {}
  ADC = MCP3008(machine.SPI(0, sck=machine.Pin(2), mosi=machine.Pin(3), miso=machine.Pin(4), baudrate=100000), machine.Pin(22, machine.Pin.OUT))
  sensor_aht10 = AHT10(machine.I2C(1, scl=machine.Pin(27), sda=machine.Pin(26)))
  
  while True:
    start_time = utime.ticks_ms()
    led.toggle()
    measurements['Temp'] = thermistor_get_temperature(thermistor_get_resistance(ADC.read(0)))
    measurements['AQ'] = ADC.read(1)
    measurements['Hum'] = sensor_aht10.relative_humidity
    socket_sender.send_msg(json.dumps(measurements))
    print(measurements)
    time.sleep_ms(250)
    end_time = utime.ticks_ms()
    elapsed_time = utime.ticks_diff(end_time, start_time)
    print("Tiempo de ejecucion:", elapsed_time, "ms")

if __name__ == '__main__':
  main()

