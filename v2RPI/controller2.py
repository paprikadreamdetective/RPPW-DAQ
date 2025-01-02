from serialhandler import SerialCommunicator
from mcp3008 import ADC_MCP3008
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

# Configurar el puerto serial
arduino_port = '/dev/ttyACM0'  # Cambia a tu puerto serial
baud_rate = 9600

@app.route('/control_motor', methods=['POST'])
def control_motor():
    try:
        # Obtener datos de la solicitud
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'No data provided'}), 400

        arduino_responses = {}

        # Comando de encendido/apagado del motor
        if 'command' in data:
            command = data['command']
            if command in ["POWER ON", "POWER OFF"]:
                response = slave_arduino_mega.send_command(command)
                arduino_responses['power'] = response
            else:
                return jsonify({'success': False, 'message': 'Invalid command'}), 400

        # Validar y enviar comando de velocidad
        if 'speed' in data:
            speed = int(data['speed'])
            command = f"SPEED {speed}"
            arduino_response_speed = slave_arduino_mega.send_command(command)
        else:
            arduino_response_speed = None

        # Validar y enviar comando de revoluciones
        if 'revolutions' in data:
            revolutions = int(data['revolutions'])
            command = f"REV {revolutions}"
            arduino_response_revolutions = slave_arduino_mega.send_command(command)
        else:
            arduino_response_revolutions = None

        return jsonify({
            'success': True,
            'message': 'Commands sent successfully',
            'responses': {
                'power': arduino_responses.get('power'),
                'speed': arduino_response_speed,
                'revolutions': arduino_response_revolutions
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@app.route('/set_mode_manual', methods=['POST'])
def pwm_set_mode():
    '''
    value = request.json['pwm_value']
    mode_control = request.json['mode_control']
    adc_channel = request.json['adc_channel']
    print(str(value)+ ' ' + str(mode_control))
    data = request.get_json()
    master.setControlModeOutputPWM(data)
    '''
    return jsonify({'success' : True, 'message' : 'Configuracion Actualizada!'})

@app.route('/get_daq_info', methods=['GET'])
def get_daq_info():
    if not daq_data:
        return jsonify({'success' : True, 'message' : 'Ha ocurrido un error'})
    return jsonify(daq_data)

def daq_task():
    global master
    #global adc_analog_inputs
    global i2c_sensor
    global slave_arduino_mega
    # i2c = busio.I2C(board.SCL, board.SDA)
    # sensor_aht10 = AHTx0(i2c)
    # i2c_sensor = {'aht10' : sensor_aht10} 
    adc = ADC_MCP3008(busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI), digitalio.DigitalInOut(board.D8))
    master = create_master_daq(adc, [], [])
    # master.initOutputs('config.json')  
    # Conectar con el Arduino
    slave_arduino_mega = SerialCommunicator(arduino_port, baud_rate)
    
    try:
        while 1:
            adc_analog_inputs = master.getAnalogChannelValues() 
            converted_data = [{f'temp{key}': convert_adc_to_temperature(value)} for item in adc_analog_inputs for key, value in item.items()]
            print(converted_data)
            time.sleep(1)
            print("TIME: ", time.ctime())
            
    except KeyboardInterrupt:
        print("Programa detenido por el usuario.")
        slave_arduino_mega.close_connection()