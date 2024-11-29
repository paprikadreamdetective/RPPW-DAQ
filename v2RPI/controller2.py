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
import serial

app = create_flask_app()

# Configurar el puerto serial
arduino_port = '/dev/ttyACM0'  # Cambia a tu puerto serial
baud_rate = 9600
@app.route('/control_motor', methods=['POST'])
def control_motor():
    try:
        # Obtener datos de la solicitud
        data = request.get_json()
        print(data)
        if not data:
            return jsonify({'success': False, 'message': 'No data provided'}), 400

        # Validar y enviar comando de velocidad
        if 'speed' in data:
            speed = int(data['speed'])
            command = f"SPEED {speed}"
            slave_arduino_mega.write(f"{command}\n".encode())
            arduino_response_speed = slave_arduino_mega.readline().decode().strip()
        else:
            arduino_response_speed = None

        # Validar y enviar comando de revoluciones
        if 'revolutions' in data:
            revolutions = int(data['revolutions'])
            command = f"REV {revolutions}"
            slave_arduino_mega.write(f"{command}\n".encode())
            arduino_response_revolutions = slave_arduino_mega.readline().decode().strip()
        else:
            arduino_response_revolutions = None

        return jsonify({
            'success': True,
            'message': 'Commands sent successfully',
            'responses': {
                'speed': arduino_response_speed,
                'revolutions': arduino_response_revolutions
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500


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
    #print(converted_data)
    #print("TIMER 1: ", time.ctime())
    #print(adc_analog_inputs)
    threading.Timer(0.25, timer_1_callback).start()

'''
def timer_2_callback():
    i2c_inputs = [{'temperature' : i2c_sensor[sensor].temperature, 'humidity' : i2c_sensor[sensor].relative_humidity} for sensor in i2c_sensor] 
    #print("TIMER 2: ", time.ctime())
    #print(i2c_inputs)
    threading.Timer(1, timer_2_callback).start()
'''
def init_timers():
    timer_1_callback()
    # timer_2_callback()


def daq_task():
    global master
    global adc_analog_inputs
    global i2c_sensor
    global slave_arduino_mega
    # i2c = busio.I2C(board.SCL, board.SDA)
    # sensor_aht10 = AHTx0(i2c)
    # i2c_sensor = {'aht10' : sensor_aht10} 
    adc = ADC_MCP3008(busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI), digitalio.DigitalInOut(board.D8))
    master = create_master_daq(adc, [], [])
    master.initOutputs('config.json')  
    # Conectar con el Arduino
    slave_arduino_mega = serial.Serial(arduino_port, baud_rate, timeout=1)
    init_timers()
    
    try:
        while 1:
            master.writeAllOutputPWM(adc_analog_inputs)
            master.showStateOutputPWM()
        
            
    except KeyboardInterrupt:
        print("Programa detenido por el usuario.")
        master.cleanupOutputs()
        #output_ch0.cleanup()
