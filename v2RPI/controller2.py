from utilities import *
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

one_second = 1

TIMER_1 = False
samples_per_second_timer_1 = 4
cycle_time_timer_1 = one_second / samples_per_second_timer_1

TIMER_2 = False
samples_per_second_timer_2 = 1
cycle_time_timer_2 = one_second / samples_per_second_timer_2

@app.route('/set_mode_manual', methods=['POST'])
def pwm_set_mode():
    value = request.json['pwm_value']
    mode_control = request.json['mode_control']
    print(str(value)+ ' ' + str(mode_control))
    data = request.get_json()
    master.setControlModeOutputPWM(data)
    return jsonify({'success' : True, 'message' : 'Configuracion Actualizada!'})

@app.route('/get_daq_info', methods=['GET'])
def get_daq_info():
    if not daq_data:
        return jsonify({'success' : True, 'message' : 'Ha ocurrido un error'})
    return jsonify(daq_data)

def timer_1_callback():
    adc_analog_inputs = master.getAnalogChannelValues() 
    print("TIMER 1: ", time.ctime())
    print(adc_analog_inputs)
    threading.Timer(cycle_time_timer_1, timer_1_callback).start()

def timer_2_callback():
    i2c_inputs = [{'temperature' : i2c_sensor[sensor].temperature, 'humidity' : i2c_sensor[sensor].relative_humidity} for sensor in i2c_sensor] 
    print("TIMER 2: ", time.ctime())
    print(i2c_inputs)
    threading.Timer(cycle_time_timer_2, timer_2_callback).start()

def init_timers():
    timer_1_callback()
    timer_2_callback()

def daq_task():
    #global TIMER_1
    #global TIMER_2
    global master
    global i2c_sensor
    i2c = busio.I2C(board.SCL, board.SDA)
    sensor_aht10 = AHTx0(i2c)
    i2c_sensor = {'aht10' : sensor_aht10} 
    adc = ADC_MCP3008(busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI), digitalio.DigitalInOut(board.D8))
    master = create_master_daq(adc, [], [])
    master.initOutputs('config.json')  
    time.sleep(3)
    try:
        init_timers()
        #init_outputs()
        while 1:
            #output_ch0.write_output(adc_analog_inputs[0]['CH0'])
            master.writeAllOutputPWM()
            # if TIMER_1:
                
                # output_ch0.write_output(adc_analog_inputs[0]['CH0'])
                # output_ch0.write_output(ADC['CH0'].value)
                # TIMER_1 = False
            #if TIMER_2:
            #    TIMER_2 = False    
    except KeyboardInterrupt:
        print("Programa detenido por el usuario.")
        #output_ch0.cleanup()
