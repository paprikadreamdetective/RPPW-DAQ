from utilities import *
from output_buffer import *
from mcp3008 import ADC_MCP3008
from controller import *


import time
import board
import busio
import os
import digitalio
from math import log
import threading

import numpy as np
from adafruit_ahtx0 import AHTx0
import json
'''
app = create_flask_app() 

A = 8.1197e-4
B = 2.65207e-4
C = 1.272206e-7

# PID Configuration
Kp = 30
Ki = 0.5
Kd = 50

output_ch0 = Output(0, 18, "pwm", MANUAL, 0)

adc_analog_inputs = []
i2c_inputs = []

adc = ADC_MCP3008(busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI), digitalio.DigitalInOut(board.D22))
ch0 = adc.get_analog_input(0)

ADC = { 'CH0' : ch0 }

i2c = busio.I2C(board.SCL, board.SDA)
sensor_aht10 = AHTx0(i2c)

i2c_sensor = {'aht10' : sensor_aht10} 

one_second = 1

TIMER_1 = False
samples_per_second_timer_1 = 4
cycle_time_timer_1 = one_second / samples_per_second_timer_1

TIMER_2 = False
samples_per_second_timer_2 = 1
cycle_time_timer_2 = one_second / samples_per_second_timer_2

def convert_adc_to_temperature(adc_value):
    resistance = (65535 / adc_value) - 1
    # resistance = 10000 / resistance
    resistance = 10000 / resistance
    temperature = 1 / (A + B * (np.log(resistance)) + C * (np.log(resistance)) ** 3) - 273.15  # Kelvin to Celsius
    return temperature


        



def pwm_controller(request_data: dict) -> dict:
    """
        MANUAL:     "ADDR 1, 0, OUT_CHANNEL, PWM"
        TIMER:      "ADDR 1, 1, OUT_CHANNEL, TIME_ON, TIME_OFF, PWM"
        PID:        "ADDR 1, 2, OUT_CHANNEL, IN_CHANNEL, SETPOINT"
        ONOFF:      "ADDR 1, 3, OUT_CHANNEL, IN_CHANNEL, LOWER_BOUND, UPPER_BOUND, PWM"
    """
    new_config_data = config_data.copy()
    mode = request_data.json['mode_control']
    if 0 == mode:
        output_ch0.set_manual_output(request_data.json['pwm_value'])
        new_config_data['M0_0']['MODE'] = MANUAL
        new_config_data['M0_0']['PWM_CHANNEL'] = int(request_data.json['pwm_channel'])
        new_config_data['M0_0']['VALUE'] = int(request_data.json['pwm_value'])
        return new_config_data
    elif 1 == mode:
        new_config_data['M0_0']['MODE'] = TIMER
        new_config_data['M0_0']['TIME_ON'] = int(request_data.json['time_on'])
        new_config_data['M0_0']['TIME_OFF'] = int(request_data.json['time_off'])
        new_config_data['M0_0']['VALUE'] = int(request_data.json['pwm_value'])
        new_config_data['M0_0']['PWM_CHANNEL'] = int(request_data.json['pwm_channel'])
        output_ch0.set_timer(int(request_data.json['time_on']), int(request_data.json['time_off']), int(request_data.json['pwm_value']))
        return new_config_data
    elif 2 == mode:
        new_config_data['M0_0']['MODE'] = PID
        new_config_data['M0_0']['PWM_CHANNEL'] = int(request_data.json['pwm_channel'])
        new_config_data['M0_0']['SETPOINT'] = int(request_data.json['setpoint'])
        new_config_data['M0_0']['VALUE'] = int(request_data.json['pwm_value'])
        new_config_data['M0_0']['ADC_CHANNEL'] = int(request_data.json['adc_channel'])
        output_ch0.set_pid(ADC['CH0'].value, int(request_data.json['setpoint']))
        output_ch0.initialize_pid()
        return new_config_data
    elif 3 == mode:
        new_config_data['M0_0']['MODE'] = ONOFF
        new_config_data['M0_0']['VALUE'] = int(request_data.json['pwm_value'])
        new_config_data['M0_0']['PWM_CHANNEL'] = int(request_data.json['pwm_channel'])
        new_config_data['M0_0']['ADC_CHANNEL'] = int(request_data.json['adc_channel'])
        new_config_data['M0_0']['LOWER_BOUND'] = int(request_data.json['lower_bound'])
        new_config_data['M0_0']['UPPER_BOUND'] = int(request_data.json['upper_bound'])
        temp_0 = convert_adc_to_temperature(ADC['CH0'].value)
        output_ch0.set_onoff(temp_0, int(request_data.json['lower_bound']), int(request_data.json['upper_bound']), int(request_data.json['pwm_value']))
        return new_config_data


@app.route('/set_mode_manual', methods=['POST'])
def pwm_set_mode():
        value = request.json['pwm_value']
        mode_control = request.json['mode_control']
        print(str(value)+ ' ' + str(mode_control))
        commands = request
        new_config_data = pwm_controller(commands)
        with open('config.json', 'w') as archivo:
            json.dump(new_config_data, archivo, indent=4)  
        print('Configuracion Actualizada!')
        print(new_config_data)
        return jsonify({'success' : True, 'message' : 'Configuracion Actualizada!'})

def timer_1_callback():
    global TIMER_1
    global adc_analog_inputs
    TIMER_1 = True
    adc_analog_inputs = [{ channel : convert_adc_to_temperature(ADC[channel].value) } for channel in ADC]
    threading.Timer(cycle_time_timer_1, timer_1_callback).start()

def timer_2_callback():
    global TIMER_2
    global i2c_inputs
    TIMER_2 = True
    i2c_inputs = [{'temperature' : i2c_sensor[sensor].temperature, 'humidity' : i2c_sensor[sensor].relative_humidity} for sensor in i2c_sensor] 
    threading.Timer(cycle_time_timer_2, timer_2_callback).start()

def init_timers():
    timer_1_callback()
    timer_2_callback()

def init_outputs():
    output_ch0.set_output_limits(0, 255)
    output_ch0.set_pid_tunings(Kp, Ki, Kd)
    output_ch0.set_sample_time_us(cycle_time_timer_1)
    output_ch0.set_gh_filter(0.7)

def daq_task():
    global TIMER_1
    global TIMER_2
    try:
        init_timers()
        init_outputs()
        adc_inputs = adc_analog_inputs[0]
        while 1:
            if TIMER_1:
                #print("Timer 1 activado")
                print(adc_analog_inputs)
                output_ch0.write_output(adc_analog_inputs[0]['CH0'])
                TIMER_1 = False
            if TIMER_2:
                #print("Timer 2 activado")
                print(i2c_inputs)
                TIMER_2 = False        
    except KeyboardInterrupt:
        print("Programa detenido por el usuario.")
'''
if __name__ == '__main__':
    thread1 = threading.Thread(target=daq_task)
    thread1.start()
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
    
    
        
