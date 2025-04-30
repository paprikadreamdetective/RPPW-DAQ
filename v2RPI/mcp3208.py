import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

class ADC_MCP3208:  # Mantenemos este nombre aunque sea un MCP3008
    def __init__(self, spi_object, chip_select):
        """Inicializa el MCP3008 con SPI y Chip Select (CS)."""
        self.spi = spi_object
        self.cs = chip_select
        self.mcp = MCP.MCP3008(self.spi, self.cs)

    def get_analog_input(self, channel):
        """Lee el valor analógico de un canal (0-7) y devuelve un valor entre 0 y 65535."""
        if 0 <= channel < 8:
            return AnalogIn(self.mcp, getattr(MCP, f'P{channel}'))
        else:
            raise ValueError("Canal fuera de rango (0-7)")


'''
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

class ADC_MCP3208:
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


'''
import spidev

class ADC_MCP3208:
    def __init__(self, bus=0, device=0):
        self.spi = spidev.SpiDev()  # Crear objeto SPI
        self.spi.open(bus, device)  # Abrir SPI en el bus y dispositivo especificado
        self.spi.max_speed_hz = 1350000  # Velocidad de comunicación SPI
        self.spi.mode = 0b00  # Modo SPI (CPOL=0, CPHA=0)

    def read_channel(self, channel):
        if not (0 <= channel <= 7):
            raise ValueError("El canal debe estar entre 0 y 7")

        # Comando para MCP3208 (inicio, modo, canal)
        cmd = [0b00000110 | (channel >> 2),  # Byte 1: 0x06 para single-ended + 2 bits MSB del canal
               (channel & 0b11) << 6,        # Byte 2: 2 bits LSB del canal + 6 bits vacíos
               0x00]                         # Byte 3: 8 bits vacíos para recibir datos

        # Enviar comando y recibir respuesta
        result = self.spi.xfer2(cmd)

        # Combinar los bits recibidos en un valor de 12 bits
        adc_value = ((result[1] & 0x0F) << 8) | result[2]

        return adc_value

    def close(self):
        self.spi.close()
'''