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
from mcp3008 import ADC_MCP3008

app = create_flask_app()

@app.route('/set_mode_manual', methods=['POST'])
def pwm_set_mode():
    value = request.json['pwm_value']
    mode_control = request.json['mode_control']
    adc_channel = request.json['adc_channel']
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
    global adc_analog_inputs
    adc_analog_inputs = master.getAnalogChannelValues() 
    converted_data = [{key: convert_adc_to_temperature(value)} for item in adc_analog_inputs for key, value in item.items()]
    print(converted_data)
    #print("TIMER 1: ", time.ctime())
    #print(adc_analog_inputs)
    threading.Timer(0.25, timer_1_callback).start()

def timer_2_callback():
    i2c_inputs = [{'temperature' : i2c_sensor[sensor].temperature, 'humidity' : i2c_sensor[sensor].relative_humidity} for sensor in i2c_sensor] 
    #print("TIMER 2: ", time.ctime())
    #print(i2c_inputs)
    threading.Timer(1, timer_2_callback).start()

def init_timers():
    timer_1_callback()
    timer_2_callback()

def daq_task():
    global master
    global adc_analog_inputs
    global i2c_sensor
    i2c = busio.I2C(board.SCL, board.SDA)
    sensor_aht10 = AHTx0(i2c)
    i2c_sensor = {'aht10' : sensor_aht10} 
    adc = ADC_MCP3008(busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI), digitalio.DigitalInOut(board.D8))
    master = create_master_daq(adc, [], [])
    master.initOutputs('config.json')  
     
    init_timers()
    
    try:
        while 1:
            master.writeAllOutputPWM(adc_analog_inputs)
            master.showStateOutputPWM()
        
            time.sleep(3)
    except KeyboardInterrupt:
        print("Programa detenido por el usuario.")
        #output_ch0.cleanup()
