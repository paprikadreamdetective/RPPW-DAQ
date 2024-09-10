from utilities import *
from output_buffer import *

import time
import board
import busio
import os
import digitalio
from math import log
import threading
from mcp3008 import ADC_MCP3008
import numpy as np
from adafruit_ahtx0 import AHTx0
import json

with open('daq_info.json', 'r') as archivo:
    daq_data = json.load(archivo)


A = 8.1197e-4
B = 2.65207e-4
C = 1.272206e-7

adc_analog_inputs = []
i2c_inputs = []

adc = ADC_MCP3008(busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI), digitalio.DigitalInOut(board.D22))
ch0 = adc.get_analog_input(0)
ch2 = adc.get_analog_input(2)  

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

'''
def thread_websocket():
    ws.connect('ws://192.168.100.164:1880/ws/example')
    while 1:    
        print("Enviando medicion") 
        if i2c_inputs:
            data_to_send = {'temperature': i2c_inputs[0]['temperature']}
            message = json.dumps(data_to_send)
            ws.send(message)
        else:
            print("No hay datos para enviar.")
        time.sleep(3)
'''
def thread_handle_commands():
    while 1:
        print('0 -> Obtener informacion del DAQ')
        print('1 -> Obtener datos')
        print('2 -> Cambiar modo de control de salida PWM')
        print('3 -> ')
        input_command = int(input('Ingrese un comando: '))
        if input_command == 0:
            print('address: ' + daq_data['address'] + ', ' + 'channels: ' + str(daq_data['inputs']) + ', ' + 'pwm outputs: ' + str(daq_data['outputs']))
        elif input_command == 1:
            print('address: ' + daq_data['address'] + ', ' + 'adc inputs: ' + str(adc_analog_inputs) + ', ' + 'i2c inputs: ' + str(i2c_inputs))
        elif input_command == 2:
            print()
        elif input_command == 3:
            print()
            


def timer_1_callback():
    global TIMER_1
    global adc_analog_inputs
    TIMER_1 = True
    adc_analog_inputs = [(channel, convert_adc_to_temperature(ADC[channel].value), ADC[channel].voltage) for channel in ADC]
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

if __name__ == '__main__':
    #thread_ws = threading.Thread(target=thread_websocket)
    #thread_ws.start()
    
    thread1 = threading.Thread(target=thread_handle_commands)
    thread1.start()
    
    
    try:
        init_timers()
        while 1:
            if TIMER_1:
                #print("Timer 1 activado")
                #print(adc_analog_inputs)
                TIMER_1 = False
            if TIMER_2:
                #print("Timer 2 activado")
                #print(i2c_inputs)
                TIMER_2 = False        
    except KeyboardInterrupt:
        print("Programa detenido por el usuario.")
        #thread_ws.join()
        thread1.join()
        
