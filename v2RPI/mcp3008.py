import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import time
import numpy as np
import math
'''
A = 8.1197e-4
B = 2.65207e-4
C = 1.272206e-7
'''


class ADC_MCP3008():

    def __init__(self, spi_object, chip_select):
        self._spi_object = spi_object
        self._chip_select = chip_select
        self._mcp = self.init()
    def init(self):
        return MCP.MCP3008(self._spi_object, self._chip_select)
    def get_analog_input(self, channel):
        if channel < 8 and channel >= 0:
            return AnalogIn(self._mcp, getattr(MCP, f'P{channel}'))
        return None
'''
def convert_adc_to_temperature(adc_value):
    resistance = (65535 / adc_value) - 1
    # resistance = 10000 / resistance
    resistance = 10000 / resistance
    temperature = 1 / (A + B * (np.log(resistance)) + C * (np.log(resistance)) ** 3) - 273.15  # Kelvin to Celsius
    return temperature
'''
'''

if __name__ == '__main__':
    adc = ADC_MCP3008(busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI), digitalio.DigitalInOut(board.D22))
    channel0 = adc.get_analog_input(0)
    channel2 = adc.get_analog_input(2)
    while 1:
        print('Temperature: channel 0: {:.2f} °C'.format(convert_adc_to_temperature(channel0.value)))
        print('Temperature: channel 2: {:.2f} °C'.format(convert_adc_to_temperature(channel2.value)))
    #print('Temp OPAMP: {:.2f} '.format(temp_opamp))
        print('Raw ADC 0 Value: ', channel0.value)
        print('Raw ADC 2 Value: ', channel2.value)
        print('ADC 0 Voltage: ' + str(channel0.voltage) + 'V')
        print('ADC 2 Voltage: ' + str(channel2.voltage) + 'V')
        time.sleep(1)
'''

# create the spi bus
#spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
#cs = digitalio.DigitalInOut(board.D22)

# create the mcp object
#mcp = MCP.MCP3008(spi, cs)

# create an analog input channel on pin 0
#chan0 = AnalogIn(mcp, MCP.P0)
#chan2 = AnalogIn(mcp, MCP.P2)



'''


# Coeficientes de Steinhart-Hart para el termistor
# A = 1.009249522e-03
# B = 2.378405444e-04
# C = 9.494028054e-08

A = 8.1197e-4
B = 2.65207e-4
C = 1.272206e-7

REFERENCE_RESISTENCE = 5100
OP_AMP_RESISTORS = [1500, 2000]
RESISTOR_FEEDBACK = 1500
RESISTOR_REFERENCE = 2000
R23 = math.log(RESISTOR_REFERENCE, 2) / (2 * RESISTOR_REFERENCE)
R43 = RESISTOR_FEEDBACK / RESISTOR_REFERENCE
GAIN = (R23 + RESISTOR_FEEDBACK) / R23
RESISTOR_DIVIDER = 5100
def get_resistence_opamp(adc_value):
    return (GAIN * RESISTOR_DIVIDER / ((adc_value / 3.3) + R43)) - RESISTOR_DIVIDER

def get_temp_opamp(adc_value):
    resistance = get_resistence_opamp(adc_value)
    steinhart_eq = 1 / (A + B * (np.log(resistance)) + C * (np.log(resistance)) ** 3)
    return steinhart_eq - 273.15

def convert_adc_to_temperature(adc_value):
    resistance = (65535 / adc_value) - 1
    # resistance = 10000 / resistance
    resistance = 10000 / resistance
    temperature = 1 / (A + B * (np.log(resistance)) + C * (np.log(resistance)) ** 3) - 273.15  # Kelvin to Celsius
    return temperature


# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D22)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create an analog input channel on pin 0
chan0 = AnalogIn(mcp, MCP.P0)
chan2 = AnalogIn(mcp, MCP.P2)

while 1:
    analog_read_ch0 = chan0.value
    analog_read_ch2 = chan2.value
    temperature_0 = convert_adc_to_temperature(analog_read_ch0)
    temperature_2 = convert_adc_to_temperature(analog_read_ch2)
    #temp_opamp = get_temp_opamp(analog_read)
    print('Temperature: channel 0: {:.2f} °C'.format(temperature_0))
    print('Temperature: channel 2: {:.2f} °C'.format(temperature_2))
    
    #print('Temp OPAMP: {:.2f} '.format(temp_opamp))
    print('Raw ADC 0 Value: ', chan0.value)
    print('Raw ADC 2 Value: ', chan2.value)
    print('ADC 0 Voltage: ' + str(chan0.voltage) + 'V')
    print('ADC 2 Voltage: ' + str(chan2.voltage) + 'V')
    time.sleep(1)
'''
