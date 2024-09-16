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

with open('config.json', 'r') as archivo:
    config_data = json.load(archivo)

A = 8.1197e-4
B = 2.65207e-4
C = 1.272206e-7

# PID Configuration
Kp = 100
Ki = 0.2
Kd = 0.


output_ch0 = Output(0, 18, "pwm", MANUAL, 0)


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

def pwm_controller(config_data: dict, option: int) -> dict:
    new_config_data = config_data
    
    if option == 0:
        output_ch0.set_manual_output(3)
        new_config_data['M0_0']['MODE'] = MANUAL
        new_config_data['M0_0']['VALUE'] = 0.5
        return new_config_data
    elif option == 1:
        new_config_data['M0_0']['MODE'] = TIMER
        new_config_data['M0_0']['TIME_ON'] = 15
        new_config_data['M0_0']['TIME_OFF'] = 30
        new_config_data['M0_0']['VALUE'] = 23.3
        output_ch0.set_timer(15, 30, 23.3)
        return new_config_data
    elif option == 2:
        new_config_data['M0_0']['MODE'] = PID
        new_config_data['M0_0']['SETPOINT'] = 48
        new_config_data['M0_0']['VALUE'] = 0
        output_ch0.set_pid(ADC['CH0'].value, 48)
        output_ch0.initialize_pid()
        return new_config_data
    elif option == 3:
        new_config_data['M0_0']['MODE'] = ONOFF
        new_config_data['M0_0']['VALUE'] = 255
        new_config_data['M0_0']['PWM_CHANNEL'] = 0
        new_config_data['M0_0']['ADC_CHANNEL'] = 0
        new_config_data['M0_0']['LOWER_BOUND'] = 20
        new_config_data['M0_0']['UPPER_BOUND'] = 30
        temp_0 = convert_adc_to_temperature(ADC['CH0'].value)
        output_ch0.set_onoff(temp_0, 20, 30, 255)
        return new_config_data
        
def thread_handle_commands():
    '''
        MANUAL:     "ADDR 1, 0, OUT_CHANNEL, PWM"
        TIMER:      "ADDR 1, 1, OUT_CHANNEL, TIME_ON, TIME_OFF, PWM"
        PID:        "ADDR 1, 2, OUT_CHANNEL, IN_CHANNEL, SETPOINT"
        ONOFF:      "ADDR 1, 3, OUT_CHANNEL, IN_CHANNEL, LOWER_BOUND, UPPER_BOUND, PWM"
    '''
    while 1:
        print('0 -> Obtener informacion del DAQ')
        print('1 -> Obtener datos')
        print('2 -> Cambiar modo de control de salida PWM')
        print('3 -> Ajustar el control PID')
        print('4 -> Ajuste de limites de Apagado/Encendido')
        input_command = int(input('Ingrese un comando: '))
        if input_command == 0:
            print('---------------------- Informacion del DAQ ----------------------')
            print('address: ' + daq_data['address'] + ', ' + 'channels: ' + str(daq_data['inputs']) + ', ' + 'pwm outputs: ' + str(daq_data['outputs']))
        elif input_command == 1:
            print('---------------------- Datos obtenidos ----------------------')
            print('address: ' + daq_data['address'] + ', ' + 'adc inputs: ' + str(adc_analog_inputs) + ', ' + 'i2c inputs: ' + str(i2c_inputs))
        elif input_command == 2:
            print('---------------------- Control de salida PWM ----------------------')
            print('MANUAL: 0')
            print('TIMER: 1')
            print('PID: 2')
            print('ON / OFF: 3')
            print('Configuracion actual: ')
            print(config_data)
            mode_control = int(input('Digite un modo de control: '))
            print('---------------------------------------------------------------')
            new_config_data = pwm_controller(config_data, mode_control)
            with open('config.json', 'w') as archivo:
                json.dump(new_config_data, archivo, indent=4)  
            print('Configuracion Actualizada!')
        '''
        elif input_command == 3:
            print('Configuracion de control PID: ')
            print('Configuracion actual: ')
            print(config_data)
            mode = int(input('Ingrese un modo: '))
            value = int(input('Ingrese el control PID: '))
            pwm_channel = int(input('Ingrese el canal PWM entre [0, 7]: '))
            adc_input = int(input('Ingrese el canal ADC [0, 7]: '))
            set_point = float(input('Ingrese el setpoint: '))
            
            new_config_data = config_data
            
            new_config_data['M0_0']['MODE'] = mode
            new_config_data['M0_0']['VALUE'] = value
            new_config_data['M0_0']['PWM_CHANNEL'] = pwm_channel
            new_config_data['M0_0']['ADC_CHANNEL'] = adc_input
            new_config_data['M0_0']['SETPOINT'] = set_point
            with open('config.json', 'w') as archivo:
                json.dump(new_config_data, archivo, indent=4)
            print('Configuracion Actualizada!')
        elif input_command == 4:
            print('Configuracion actual: ')
            print(config_data)
            mode = int(input('Ingrese un modo: '))
            pwm_channel = int(input('Ingrese el canal PWM entre [0, 7]: '))
            lower_bnd = float(input('Ingrese el limite inferior: '))
            upper_bnd = float(input('Ingrese el limite superior: '))
            value = int(input('Ingrese un valor entre [0, 255]: '))
            
            new_config_data = config_data
            
            new_config_data['M0_0']['MODE'] = mode
            new_config_data['M0_0']['VALUE'] = value
            new_config_data['M0_0']['PWM_CHANNEL'] = pwm_channel
            new_config_data['M0_0']['ADC_CHANNEL'] = adc_input
            new_config_data['M0_0']['LOWER_BOUND'] = lower_bnd
            new_config_data['M0_0']['UPPER_BOUND'] = upper_bnd
            with open('config.json', 'w') as archivo:
                json.dump(new_config_data, archivo, indent=4)  
            print('Configuracion Actualizada!')
        '''

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
    

if __name__ == '__main__':
    #thread_ws = threading.Thread(target=thread_websocket)
    #thread_ws.start()
    thread1 = threading.Thread(target=thread_handle_commands)
    thread1.start()
    try:
        init_timers()
        init_outputs()
        adc_inputs = adc_analog_inputs[0]
        while 1:
            if TIMER_1:
                #print("Timer 1 activado")
                #print(adc_analog_inputs)
                output_ch0.write_output(adc_analog_inputs[0]['CH0'])
                TIMER_1 = False
            if TIMER_2:
                #print("Timer 2 activado")
                #print(i2c_inputs)
                TIMER_2 = False        
    except KeyboardInterrupt:
        print("Programa detenido por el usuario.")
        #thread_ws.join()
        thread1.join()
        
