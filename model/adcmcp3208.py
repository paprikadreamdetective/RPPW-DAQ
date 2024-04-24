import machine

class adcMCP3208:
    def __init__(self, input_data: int, output_data: int, clock: int, chip_select: int): 
        self._input_data = input_data
        self._output_data = output_data
        self._clock = clock
        self._chip_select = chip_select
        self._channels = 8
        self._max_value = 4095
        self._spi_speed = 1000000
        self._reference_voltage = 3.3
        """
        Se definen los pines como atributos del ADC, se especifica si seran entradas o salidas
        """
        self._chip_select_pin = machine.Pin(self._chip_select, machine.Pin.OUT)
        self._input_data_pin = machine.Pin(self._input_data, machine.Pin.IN)
        self._output_data_pin = machine.Pin(self._output_data, machine.Pin.OUT)
        self._clock_pin = machine.Pin(self._clock, machine.Pin.OUT)
        
        self._output_data_pin.off()
        self._clock_pin.off()
        
        self._spi_settings = self.begin()


        def begin(self):
            self._chip_select_pin.on()
            self._chip_select_pin.off()
            self._chip_select_pin.on()
            return machine.SPI(0).init(baudrate=self._spi_speed, polarity=0, phase=0)

        def set_reference_voltage(self, reference_voltage: float):
            self._reference_voltage = reference_voltage

        def set_spi_speed(self, speed: int):
            self._spi_speed = speed
            self._spi_settings = machine.SPI(0).init(baudreate=self._spi_speed, polarity=0, phase=0)
            
        def build_request_MCP3208(self, channel: int, data: int) -> int:
            data[0] = 0x04
            data[0] |= 0x2
            if channel > 3: data[0] |= 0x01
            if channel: data[1] |= (channel << 6)
            return 3

        def software_spi_transfer(self, data: int) -> int:
            clk = self._clock
            out_data = self._output_data
            in_data = self._input_data
            ref_volt = 0
            mask = 0x80
            while mask:
                if data & mask:
                    self._output_data_pin.on()
                else:
                    self._output_data_pin.off()
                self._clock_pin.on()
                if self._input_data_pin.on() == 1:
                    ref_volt |= mask
                self._clock_pin.off()
                mask >>= 1
            return ref_volt
        
        def read_adc(self, channel: int):
            if channel >= self._channels: return 0
            data = [0, 0, 0]
            bytes = self.build_request_MCP3208(channel, data)
            self._chip_select_pin.off()
            for byte in range(0, bytes):
                data[byte] = self.software_spi_transfer(data[byte])
            self._chip_select_pin.on()
            return 
