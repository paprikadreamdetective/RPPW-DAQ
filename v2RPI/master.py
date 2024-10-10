from utilities import *
from mcp3008 import ADC_MCP3008
import busio
import board
import digitalio
import json
from output_buffer import *


PWM_OUTPUT_GPIO = [18, 19, 20, 21, 22, 23]

with open('config.json', 'w') as archivo:
    json.dump(config_data, archivo, indent=4)  


class MasterDAQ:
    
    def __init__(self, adc, pwm_outputs: list, i2c_inputs):
        self._adc = adc
        self._pwm_outputs = pwm_outputs
        self._i2c_inputs = i2c_inputs
        self._config_file = {} 
        self._MAX_SIZE_OUTPUT_PWM = 6    

    def getAnalogChannelValues(self):
        return [{ channel : self._adc.get_analog_input(channel).value } for channel in range(0, 8)]

    def enableOutputPWM(self, output_channel, pin, output_type, control_mode, value):
        if len(self._pwm_outputs) >= 6:
            print("No se pueden agregar más de 6 canales PWM.")
            return 
        channel = len(self._pwm_outputs) 
        new_pwm_output = Output(channel, pin, output_type, control_mode, value)
        self._pwm_outputs.append(new_pwm_output)
        print(f"Canal PWM {channel} agregado en el pin GPIO {pin} con valor inicial {value}%.")

    def setControlModeOutputPWM(self, request_data: dict):
        """
            MANUAL:     "ADDR 1, 0, OUT_CHANNEL, PWM"
            TIMER:      "ADDR 1, 1, OUT_CHANNEL, TIME_ON, TIME_OFF, PWM"
            PID:        "ADDR 1, 2, OUT_CHANNEL, IN_CHANNEL, SETPOINT"
            ONOFF:      "ADDR 1, 3, OUT_CHANNEL, IN_CHANNEL, LOWER_BOUND, UPPER_BOUND, PWM"
        """
        mode_control = request_data['mode_control']
        channel = request_data['pwm_channel']
        output = self._pwm_outputs[channel]
        new_config_data = config_data.copy()
        if 0 == mode_control:
            output.set_manual_output(request_data['pwm_value'])
            new_config_data[f'M0_{channel}']['MODE'] = MANUAL
            new_config_data[f'M0_{channel}']['PWM_CHANNEL'] = int(request_data['pwm_channel'])
            new_config_data[f'M0_{channel}']['VALUE'] = int(request_data['pwm_value'])
        elif 1 == mode_control:
            output.set_timer(int(request_data['time_on']), int(request_data['time_off']), int(request_data['pwm_value']))
            new_config_data[f'M0_{channel}']['MODE'] = TIMER
            new_config_data[f'M0_{channel}']['TIME_ON'] = int(request_data['time_on'])
            new_config_data[f'M0_{channel}']['TIME_OFF'] = int(request_data['time_off'])
            new_config_data[f'M0_{channel}']['VALUE'] = int(request_data['pwm_value'])
            new_config_data[f'M0_{channel}']['PWM_CHANNEL'] = int(request_data['pwm_channel'])
        elif 2 == mode_control:
            output.set_pid(25.25, float(request_data['setpoint']))
            output.set_output_limits(int(request_data['output_lower_limit']), int(request_data['output_upper_limit']))
            output.set_pid_tunings(float(request_data['kp_value']), float(request_data['ki_value']), float(request_data['kd_value']))
            output.set_sample_time_us(float(request_data['sample_time_us']))
            output.set_gh_filter(float(request_data['gh_filter']))
            output.initialize_pid()
            new_config_data[f'M0_{channel}']['MODE'] = PID
            new_config_data[f'M0_{channel}']['PWM_CHANNEL'] = int(request_data['pwm_channel'])
            new_config_data[f'M0_{channel}']['SETPOINT'] = float(request_data['setpoint'])
            new_config_data[f'M0_{channel}']['VALUE'] = int(request_data['pwm_value'])
            new_config_data[f'M0_{channel}']['ADC_CHANNEL'] = int(request_data['adc_channel'])
            new_config_data[f'M0_{channel}']['OUTPUT_LOWER_LIMIT'] = int(request_data['output_lower_limit'])
            new_config_data[f'M0_{channel}']['OUTPUT_UPPER_LIMIT'] = int(request_data['output_upper_limit'])
            new_config_data[f'M0_{channel}']['KP'] = float(request_data['kp_value'])
            new_config_data[f'M0_{channel}']['KI'] = float(request_data['ki_value'])
            new_config_data[f'M0_{channel}']['KD'] = float(request_data['kd_value'])
            new_config_data[f'M0_{channel}']['SAMPLE_TIME_US'] = float(request_data['sample_time_us'])
            new_config_data[f'M0_{channel}']['GH_FILTER'] = float(request_data['gh_filter'])
        elif 3 == mode_control:
            temp_0 = 25.25
            output.set_onoff(temp_0, int(request_data['lower_bound']), int(request_data['upper_bound']), int(request_data['pwm_value']))
            new_config_data[f'M0_{channel}']['MODE'] = ONOFF
            new_config_data[f'M0_{channel}']['VALUE'] = int(request_data['pwm_value'])
            new_config_data[f'M0_{channel}']['PWM_CHANNEL'] = int(request_data['pwm_channel'])
            new_config_data[f'M0_{channel}']['ADC_CHANNEL'] = int(request_data['adc_channel'])
            new_config_data[f'M0_{channel}']['LOWER_BOUND'] = int(request_data['lower_bound'])
            new_config_data[f'M0_{channel}']['UPPER_BOUND'] = int(request_data['upper_bound'])
        with open('config.json', 'w') as archivo:
            json.dump(new_config_data, archivo, indent=4)  
        print('Configuracion Actualizada!')
        print(new_config_data)
    
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

    # Método para leer el archivo JSON y crear los objetos Output
    def loadConfig(self, json_file):
        try:
            with open(json_file, 'r') as file:
                self._config_file = json.load(file)  # Cargar la configuración JSON
                print(f"Configuración leída desde {json_file}:")
                
                for key, config in self._config_file.items():
                    if len(self._pwm_outputs) >= self._MAX_SIZE_OUTPUT_PWM:
                        print("Se alcanzó el número máximo de canales PWM.")
                        break

                    gpio_output = config['GPIO_OUTPUT']
                    mode = config['MODE']
                    time_on = config['TIME_ON']
                    time_off = config['TIME_OFF']
                    variable = config['VARIABLE']
                    setpoint = config['SETPOINT']
                    lower_bound = config['LOWER_BOUND']
                    upper_bound = config['UPPER_BOUND']
                    value = config['VALUE']
                    pwm_channel = config['PWM_CHANNEL']
                    adc_channel = config['ADC_CHANNEL']
                    output_lower_limit = config['OUTPUT_LOWER_LIMIT']
                    output_upper_limit = config['OUTPUT_UPPER_LIMIT']
                    kp = config['KP']
                    ki = config['KI']
                    kd = config['KD']
                    sample_time_us = config['SAMPLE_TIME_US']
                    gh_filter = config['GH_FILTER']
                    
                    # Definir el canal PWM y el pin (puedes personalizar esto)
                    pin = gpio_output  # Usamos GPIO 17+ como ejemplo de pin
                    

                    # Crear el objeto Output con la configuración
                    self.enableOutputPWM(output_channel=key, pin=pin, output_type="PWM", control_mode=mode, value=value)
                    
                    # Asignar configuraciones adicionales
                    pwm_output = self._pwm_outputs[-1]  # Último PWM agregado
                    '''
                    pwm_output._time_on = time_on if time_on is not None else pwm_output._time_on
                    pwm_output._time_off = time_off if time_off is not None else pwm_output._time_off
                    pwm_output._input_value_lb = lower_bound if lower_bound is not None else pwm_output._input_value_lb
                    pwm_output._input_value_ub = upper_bound if upper_bound is not None else pwm_output._input_value_ub
                    pwm_output._setpoint = setpoint if setpoint is not None else pwm_output._setpoint
                    '''
                    print(f"Canal {key} configurado: {config}")
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo {json_file}")
        except json.JSONDecodeError:
            print(f"Error: No se pudo leer el archivo {json_file}, formato JSON inválido.")


if __name__ == '__main__':
    num_channels_pwm = 6
    modes = [0,1,2,3]
    adc = ADC_MCP3008(busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI), digitalio.DigitalInOut(board.D8))
    master = MasterDAQ(adc, [], [])
    
    adc_channel_inputs = master.getAnalogChannelValues()
    
    master.enableOutputPWM(0, 18, "pwm", MANUAL, 25)
    master.enableOutputPWM(1, 19, "pwm", MANUAL, 50)
    master.enableOutputPWM(2, 20, "pwm", MANUAL, 75)

    values = {  
        "mode_control" : 3, 
        "pwm_channel" : 1, 
        "pwm_value" : 23 ,
        'time_on' : 0,
        'time_off' : 23,
        'setpoint': 20,
        'adc_channel' : 0,
        'output_lower_limit' : 0,
        'output_upper_limit' : 1,
        'kp_value' : 30,
        'ki_value' : 0.5,
        'kd_value' : 0.1,
        'sample_time_us' : 0.25,
        'gh_filter' : 0.7,
        'lower_bound' : 0,
        'upper_bound' : 23 }

    master.setControlModeOutputPWM(values)

    while 1:
        print(master.getAnalogChannelValues())
        master.writeAllOutputPWM(255)
        master.writeAllOutputPWM(0)
        master.showStateOutputPWM()
        
    # master.enableOutputPWM(1, 19, "pwm", MANUAL, 0)