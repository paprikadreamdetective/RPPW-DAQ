import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

class ADC_MCP3008:
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