import time
import utime
import machine
import gc
from math import log
from config import cfg
import wlanc 
from socketc import WebSocket 
from mcp3008 import MCP3008
from aht10 import AHT10
CONFIG_THERMISTOR_RESISTOR = 9900

'''
def handle_read_adc(pin):
  global ADC
  global ADC_values
  ADC_values['CH0'] = ADC.read(0)
  ADC_values['CH1'] = ADC.read(1)
  #for channel in range(8):
  #  ADC_values[f'CH{channel}'] = {ADC.read(channel)}
'''


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
  #print('Connecting to: 224.10.10.10 : 10000')
  led = machine.Pin('LED', machine.Pin.OUT)
  ADC_values = {}
  ADC = MCP3008(machine.SPI(0, sck=machine.Pin(2), mosi=machine.Pin(3), miso=machine.Pin(4), baudrate=100000), machine.Pin(22, machine.Pin.OUT))
  sensor_aht10 = AHT10(machine.I2C(1, scl=machine.Pin(27), sda=machine.Pin(26)))
  #ADC_int_pin = machine.Pin(22, machine.Pin.IN)
  #ADC_int_pin.irq(trigger=machine.Pin.IRQ_FALLING, handler=handle_read_adc)
  
  while True:
    start_time = utime.ticks_ms()
    led.toggle()
    ADC_values['CH0'] = thermistor_get_temperature(thermistor_get_resistance(ADC.read(0)))
    ADC_values['CH1'] = get_dissolved_oxygen(ADC.read(1))
    print(ADC_values)
    print("Humedad: " + str(sensor_aht10.relative_humidity))
    #free_memory = gc.mem_free()
    #allocated_memory = gc.mem_alloc()
    #print("Memoria libre:", free_memory, "bytes")
    #print("Memoria asignada:", allocated_memory, "bytes")
    time.sleep_ms(1000)
    end_time = utime.ticks_ms()
    elapsed_time = utime.ticks_diff(end_time, start_time)
    print("Tiempo de ejecucion:", elapsed_time, "ms")
if __name__ == '__main__':
  main()

'''
  import time
import machine
from config import cfg
import wlanc 
from socketc import WebSocket 
from MQ135 import MQ135

def main():
  station = wlanc.init_connection(cfg['wlan']['ssid'], cfg['wlan']['pswd'])
  while station.isconnected() == False:
    pass
  print('WiFi Connection is successful')
  led = machine.Pin('LED', machine.Pin.OUT)
  sensor_mq135 = MQ135(28)
  print('Connecting to: 224.10.10.10 : 10000')
  web_socket_sender = WebSocket('224.10.10.10', 10000)
  while True:
    ppm_CO2_actual = sensor_mq135.read()
    print('Valor actual: ' + str(ppm_CO2_actual) + ' ppm')
    message = str(ppm_CO2_actual) 
    web_socket_sender.send_msg(message)
    led.toggle()
    time.sleep_ms(500)
  
if __name__ == '__main__':
  main()
'''