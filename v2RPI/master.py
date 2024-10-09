from utilities import *
from mcp3008 import ADC_MCP3008
import busio
import board
import digitalio
from output_buffer import *

class MasterDAQ:
    def __init__(self, adc, pwm_outputs: list, i2c_inputs):
        self._adc = adc
        self._pwm_outputs = pwm_outputs
        self._i2c_inputs = i2c_inputs

    def getAnalogChannelValues(self):
        return [{ channel : self._adc.get_analog_input(channel).value } for channel in range(0, 8)]

    def enableOutputPWM(self, output_channel, pin, output_type, control_mode, value):
        if len(self._pwm_outputs) >= 6:
            print("No se pueden agregar más de 6 canales PWM.")
            return 
        channel = len(self._pwm_outputs) 

        '''
        pin = int(input("Introduce el número de pin GPIO: "))
        output_type = "PWM"
        control_mode = "manual"
        value = int(input("Introduce el valor inicial de PWM (0-100): "))
        '''

        new_pwm_output = Output(channel, pin, output_type, control_mode, value)
        self._pwm_outputs.append(new_pwm_output)
        print(f"Canal PWM {channel} agregado en el pin GPIO {pin} con valor inicial {value}%.")

    def updateOutputPWM(self):
        pass
    
    def showStateOutputPWM(self):
        if len(self._pwm_outputs) == 0:
            print("No hay canales PWM activos.")
        else:
            print("Canales PWM activos:")
            for pwm in self._pwm_outputs:
                print(f"Canal {pwm.channel} - Pin GPIO {pwm.pin} - Valor: {pwm.manual_value}%")


    def writeAllOutputPWM(self, value):
        for output in self._pwm_outputs:
            output.write_output(25.25, value)


if __name__ == '__main__':
    adc = ADC_MCP3008(busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI), digitalio.DigitalInOut(board.D8))
    master = MasterDAQ(adc, [], [])
    
    adc_channel_inputs = master.getAnalogChannelValues()
    
    master.enableOutputPWM(0, 18, "pwm", MANUAL, 0)
    while 1:
        print(master.getAnalogChannelValues())
        master.writeAllOutputPWM(255)
        master.writeAllOutputPWM(0)
        master.showStateOutputPWM()
        
    # master.enableOutputPWM(1, 19, "pwm", MANUAL, 0)