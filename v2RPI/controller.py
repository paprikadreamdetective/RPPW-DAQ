from utilities import *
from output_buffer import *
from mcp3008 import ADC_MCP3008
from app import *
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

app = create_flask_app() 
'''
A = 8.1197e-4
B = 2.65207e-4
C = 1.272206e-7
'''
# PID Configuration



output_ch0 = Output(0, 18, "pwm", MANUAL, 0)

adc_analog_inputs = []
i2c_inputs = []

adc = ADC_MCP3008(busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI), digitalio.DigitalInOut(board.D8))
'''
ch0 = adc.get_analog_input(0)
ch1 = adc.get_analog_input(1)
ch2 = adc.get_analog_input(2)
ch3 = adc.get_analog_input(3)
ch4 = adc.get_analog_input(4)
ch5 = adc.get_analog_input(5)
ch6 = adc.get_analog_input(6)
ch7 = adc.get_analog_input(7)
'''
ch0 = adc.get_analog_input(0)
ch2 = adc.get_analog_input(2)
# ADC = { 'CH0' : ch0, 'CH1' : ch1,  'CH2' : ch2, 'CH3' : ch3, 'CH4' : ch4, 'CH5' : ch5, 'CH6' : ch6, 'CH7' : ch7}
ADC = { 'CH0' : ch0, 'CH2' : ch2}

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
        new_config_data['M0_0']['SETPOINT'] = float(request_data.json['setpoint'])
        new_config_data['M0_0']['VALUE'] = int(request_data.json['pwm_value'])
        new_config_data['M0_0']['ADC_CHANNEL'] = int(request_data.json['adc_channel'])
        new_config_data['M0_0']['OUTPUT_LOWER_LIMIT'] = int(request.json['output_lower_limit'])
        new_config_data['M0_0']['OUTPUT_UPPER_LIMIT'] = int(request.json['output_upper_limit'])
        new_config_data['M0_0']['KP'] = float(request.json['kp_value'])
        new_config_data['M0_0']['KI'] = float(request.json['ki_value'])
        new_config_data['M0_0']['KD'] = float(request.json['kd_value'])
        new_config_data['M0_0']['SAMPLE_TIME_US'] = float(request.json['sample_time_us'])
        new_config_data['M0_0']['GH_FILTER'] = float(request.json['gh_filter'])
        output_ch0.set_pid(ADC['CH0'].value, float(request_data.json['setpoint']))
        output_ch0.set_output_limits(int(request.json['output_lower_limit']), int(request.json['output_upper_limit']))
        output_ch0.set_pid_tunings(float(request.json['kp_value']), float(request.json['ki_value']), float(request.json['kd_value']))
        output_ch0.set_sample_time_us(float(request.json['sample_time_us']))
        output_ch0.set_gh_filter(float(request.json['gh_filter']))
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

@app.route('/get_daq_info', methods=['GET'])
def get_daq_info():
    if not daq_data:
        return jsonify({'success' : True, 'message' : 'Ha ocurrido un error'})
    return jsonify(daq_data)

def timer_1_callback():
    global TIMER_1
    global adc_analog_inputs
    TIMER_1 = True
     
    adc_analog_inputs = [{ channel : convert_adc_to_temperature(ADC[channel].value) } for channel in ADC]
    
    #print(adc_analog_inputs)  
    print("TIMER 1: ", time.ctime())
    #print(f"TIMER 1 PASSED IS: {time_passed} SECS")  ##displaying time passed to 2 decimal places
    threading.Timer(cycle_time_timer_1, timer_1_callback).start()

def timer_2_callback():
    global TIMER_2
    global i2c_inputs
    TIMER_2 = True
    
    i2c_inputs = [{'temperature' : i2c_sensor[sensor].temperature, 'humidity' : i2c_sensor[sensor].relative_humidity} for sensor in i2c_sensor] 
    print("TIMER 2: ", time.ctime())
    #print(i2c_inputs)
    #time_passed = clock - click ##getting the time spent
    #print(f"TIMER2 PASSED IS: {time_passed:0.5f} SECS")  ##displaying time passed to 2 decimal places
    threading.Timer(cycle_time_timer_2, timer_2_callback).start()

def init_timers():
    timer_1_callback()
    timer_2_callback()

def init_outputs():
    Kp = 30
    Ki = 0.5
    Kd = 0.5
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
        while 1:
            #output_ch0.write_output(adc_analog_inputs[0]['CH0'])
            
            if TIMER_1:
                output_ch0.write_output(adc_analog_inputs[0]['CH0'])
                output_ch0.write_output(ADC['CH0'].value)
                TIMER_1 = False
            if TIMER_2:
                TIMER_2 = False    
    except KeyboardInterrupt:
        print("Programa detenido por el usuario.")
        

    