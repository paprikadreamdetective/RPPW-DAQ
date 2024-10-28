from utilities import *
from mcp3008 import ADC_MCP3008
import busio
import board
import digitalio
import json
from output_buffer import *

class MasterDAQ:
    
    def __init__(self, adc, pwm_outputs: list, i2c_inputs):
        self._adc = adc
        self._pwm_outputs = pwm_outputs
        self._i2c_inputs = i2c_inputs
        self._config_file = {} 
        self._MAX_SIZE_OUTPUT_PWM = 8    

    def getAnalogChannelValues(self):
        return [{ channel : self._adc.get_analog_input(channel).value } for channel in range(0, 8)]

    def enableOutputPWM(self, output_channel, pin, output_type, control_mode, value):
        if len(self._pwm_outputs) >= 8:
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
        channel = int(request_data['pwm_channel'])
        new_config_data = self._config_file.copy()
        #gpio_output = request_data['gpio_output']
        # Verificar si el canal ya existe, si no, agregarlo con la plantilla predeterminada
        if f'M0_{channel}' not in new_config_data:
            new_config_data[f'M0_{channel}'] = {
                "GPIO_OUTPUT": gpio_output,  # Puedes personalizar este valor o dejar uno por defecto
                "MODE": None,
                "PWM_CHANNEL": None,
                "TIME_ON": 0,
                "TIME_OFF": 0,
                "SETPOINT": 0.1,
                "VALUE": 0,
                "ADC_CHANNEL": 0,
                "OUTPUT_LOWER_LIMIT": 1,
                "OUTPUT_UPPER_LIMIT": 1,
                "KP": 0.1,
                "KI": 0.1,
                "KD": 0.1,
                "SAMPLE_TIME_US": 0.1,
                "GH_FILTER": 0.1,
                "LOWER_BOUND": 1,
                "UPPER_BOUND": 1
            }
            self.enableOutputPWM(output_channel=channel, pin=gpio_output, output_type="PWM", control_mode=mode_control, value=255)

        print(self._pwm_outputs[channel].channel)
        output = self._pwm_outputs[channel]
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
            # output.set_pid(25.25, float(request_data['setpoint']))
            output.set_pid(0, float(request_data['setpoint']))
            output.set_adc_input_channel(int(request_data['adc_channel']))
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
            output.set_adc_input_channel(int(request_data['adc_channel']))
            output.set_onoff(0, int(request_data['lower_bound']), int(request_data['upper_bound']), int(request_data['pwm_value']))
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
                print(f"Canal {pwm.channel} - Pin GPIO {pwm.pin} - Valor: {pwm.manual_value} - ADC Channel: {pwm._adc_input}")

    def writeAllOutputPWM(self, adc_inputs):
        for output in self._pwm_outputs:
            print(output)
            #print("PWM CH: " + str(output.channel) + " ADC CH: " + str(output._adc_input))
            input_value = adc_inputs[output._adc_input][output._adc_input]
            #print("INPUT_VALUE: ", input_value)
            output.write_output(input_value)
        #print("-----------------")

    def initOutputs(self, json_file):
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
                #variable = config['VARIABLE']
                setpoint = config['SETPOINT']
                lower_bound = config['LOWER_BOUND']
                upper_bound = config['UPPER_BOUND']
                pwm_value = config['VALUE']
                pwm_channel = config['PWM_CHANNEL']
                adc_channel = config['ADC_CHANNEL']
                output_lower_limit = config['OUTPUT_LOWER_LIMIT']
                output_upper_limit = config['OUTPUT_UPPER_LIMIT']
                kp = config['KP']
                ki = config['KI']
                kd = config['KD']
                sample_time_us = config['SAMPLE_TIME_US']
                gh_filter = config['GH_FILTER']
                pin = gpio_output
                
                self.enableOutputPWM(output_channel=key, pin=pin, output_type="PWM", control_mode=mode, value=pwm_value)
                
                self._pwm_outputs[-1].set_adc_input_channel(adc_channel)
                self._pwm_outputs[-1].set_manual_output(pwm_value)  # Último PWM agregado
                self._pwm_outputs[-1].set_timer(time_on, time_off, pwm_value)
                self._pwm_outputs[-1].set_pid(25.25, setpoint)
                self._pwm_outputs[-1].set_output_limits(output_lower_limit, output_upper_limit)
                self._pwm_outputs[-1].set_pid_tunings(kp, ki, kd)
                self._pwm_outputs[-1].set_sample_time_us(sample_time_us)
                self._pwm_outputs[-1].set_gh_filter(gh_filter)
                self._pwm_outputs[-1].initialize_pid()
                self._pwm_outputs[-1].set_onoff(25.25, lower_bound, upper_bound, pwm_value)
                print(f"Canal {key} configurado: {config}")
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo {json_file}")
        except json.JSONDecodeError:
            print(f"Error: No se pudo leer el archivo {json_file}, formato JSON inválido.")