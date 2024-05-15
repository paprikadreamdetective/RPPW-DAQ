import time
import utime
import machine
import json
import wlanc 
import sensorutils
from config import cfg  
from socketc import Socket 
from mcp3008 import MCP3008
from aht10 import AHT10

def read_adc_ch0_handler(timer):
  measurements['Temp'] = sensorutils.thermistor_get_temperature(sensorutils.thermistor_get_resistance(ADC.read(0)))

def read_adc_ch1_handler(timer):
  measurements['AQ'] = ADC.read(1)

def read_i2c_1_2726_handler(timer):
  measurements['Hum'] = sensor_aht10.relative_humidity

def main():
  global measurements
  global ADC
  global sensor_aht10

  measurements = {}
  ADC = MCP3008(machine.SPI(0, sck=machine.Pin(2), mosi=machine.Pin(3), miso=machine.Pin(4), baudrate=100000), machine.Pin(22, machine.Pin.OUT))
  sensor_aht10 = AHT10(machine.I2C(1, scl=machine.Pin(27), sda=machine.Pin(26)))
  
  station = wlanc.init_connection(cfg['wlan']['ssid'], cfg['wlan']['pswd'])
  while station.isconnected() == False:
    pass
  print('WiFi Connection is successful')
  print('Connecting to: 224.10.10.10 : 10000')
  socket_sender = Socket('224.10.10.10', 10000)

  led = machine.Pin('LED', machine.Pin.OUT)

  read_adc_ch0_timer = machine.Timer()
  read_adc_ch0_timer.init(period=250, mode=machine.Timer.PERIODIC, callback=read_adc_ch0_handler)
  
  read_adc_ch1_timer = machine.Timer()
  read_adc_ch1_timer.init(period=250, mode=machine.Timer.PERIODIC, callback=read_adc_ch1_handler)
  
  read_i2c_1_2726_timer = machine.Timer()
  read_i2c_1_2726_timer.init(period=250, mode=machine.Timer.PERIODIC, callback=read_i2c_1_2726_handler)

  while True:
    start_time = utime.ticks_ms()
    led.toggle()
    socket_sender.send_msg(json.dumps(measurements))
    print(measurements)
    time.sleep_ms(248)
    end_time = utime.ticks_ms()
    elapsed_time = utime.ticks_diff(end_time, start_time)
    print("Tiempo de ejecucion:", elapsed_time, "ms")

if __name__ == '__main__':
  main()