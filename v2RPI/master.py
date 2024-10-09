from utilities import *
from mcp3008 import ADC_MCP3008
import busio
import board
import digitalio
class MasterDAQ:
    def __init__(self, adc, output, i2c_inputs):
        self._adc = adc
        self._output = output
        self._i2c_inputs = i2c_inputs

    
    def getAnalogChannelValues(self):
        return [{ channel : self._adc.get_analog_input(channel).value } for channel in range(0, 8)]


if __name__ == '__main__':
    master = MasterDAQ(ADC_MCP3008(busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI), digitalio.DigitalInOut(board.D8)), [], [])
    print(master.getAnalogChannelValues())