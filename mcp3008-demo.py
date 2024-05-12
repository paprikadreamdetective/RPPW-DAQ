from time import sleep
from mcp3008 import MCP3008
from machine import Pin
from math import log
from servo import Servo
import aht10
 
CONFIG_THERMISTOR_RESISTOR = 9900
s1 = Servo(0)       # Servo pin is connected to GP0
chip = MCP3008(machine.SPI(0, sck=Pin(2), mosi=Pin(3), miso=Pin(4), baudrate=100000), machine.Pin(22, machine.Pin.OUT))

i2c = machine.I2C(1, scl=Pin(27), sda=Pin(26))

sensor_aht10 = aht10.AHT10(i2c)
 
def servo_Map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
 
def servo_Angle(angle):
    if angle < 0:
        angle = 0
    if angle > 180:
        angle = 180
    s1.goto(round(servo_Map(angle,0,180,0,1024))) # Convert range value to angle value

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

while True:
    #temperature = round(sensor.temperature, 2)
    #humidity = round(sensor.relative_humidity, 2)
    adc_data_channel0 = chip.read(0)
    adc_data_channel1 = chip.read(1)
    #print("ADC: " + str(lectura_adc))
    resistance = thermistor_get_resistance(adc_data_channel0)
    temperature = thermistor_get_temperature(resistance)
    ppm_co2 = get_dissolved_oxygen(adc_data_channel1)
    print("--------------------------------")
    print("Temperatura: " + str(temperature))
    print("CO2: " + str(ppm_co2))
    print("Humedad: " + str(sensor_aht10.relative_humidity))
    machine.Pin('LED', machine.Pin.OUT).toggle()

    
    #print("Resistance: " + str(resistance))
    sleep(0.25)

