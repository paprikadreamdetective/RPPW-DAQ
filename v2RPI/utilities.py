from math import log

'''
PWM MODES:
'''

A = 8.1197e-4
B = 2.65207e-4
C = 1.272206e-7

def convert_adc_to_temperature(adc_value):
    #print(adc_value)
    if adc_value == 0:
    # Manejo para el caso en que adc_value es cero
        return float('inf')  # O devuelve un valor específico, por ejemplo, `None` o `0`


    resistance = (65535 / adc_value) - 1
    # resistance = 10000 / resistance
    resistance = 10000 / resistance
    temperature = 1 / (A + B * (log(resistance)) + C * (log(resistance)) ** 3) - 273.15  # Kelvin to Celsius
    return temperature

CONFIG_THERMISTOR_RESISTOR = 9900
REF_VOLTAGE = 3.3
thermistor = [8.1197E-4, 2.65207E-4, 1.272206E-7] # 103JT-025 semitec
#thermistor = [0.0008119700000000001, 0.00026520700000000005, 1.2722059999999998e-07]
RESISTOR_DIVIDER = 5100000
op_amp_resistors = [1500, 2200]

a_temp = thermistor[0]
b_temp = thermistor[1]
c_temp = thermistor[2]
# Set opamp resistors
RESISTOR_FEEDBACK = op_amp_resistors[0]
RESISTOR_REFERENCE = op_amp_resistors[1]

R23 = RESISTOR_REFERENCE**2 / (2 * RESISTOR_REFERENCE)
R43 = RESISTOR_FEEDBACK / RESISTOR_REFERENCE
GAIN = (R23 + RESISTOR_FEEDBACK) / R23

def get_resistance(option: int, analog_value: float) -> float:
	if option == 0:
		return RESISTOR_DIVIDER / ((REF_VOLTAGE / analog_value) - 1)
	elif option == 1:
		return (GAIN * RESISTOR_DIVIDER / ((analog_value / REF_VOLTAGE) + R43)) - RESISTOR_DIVIDER
  
def get_steinhart_eq(resistance: float):
	return a_temp + b_temp*log(resistance) + c_temp*log(resistance)**3

def get_temp_voltage_divider(analog_value: float):
	return (1 / get_steinhart_eq(get_resistance(0))) - 273.15


def get_temp_opamp(analog_value: float):
	resistance = get_resistance(1, analog_value)
	return (1 / get_steinhart_eq(resistance)) - 273.15



'''
def thermistor_get_resistance(adcval):
    # calculamos la resistencia del NTC a partir del valor del ADC
    return (CONFIG_THERMISTOR_RESISTOR * ((65535 / adcval) - 1))

def thermistor_get_temperature(resistance):
    # variable de almacenamiento temporal, evita realizar varias veces el calculo de log
    temp = log(resistance)

    # resolvemos la ecuacion de STEINHART-HART
    # http://en.wikipedia.org/wiki/Steinharart_equation
    temp = 1 / (0.001129148 + (0.000234125 * temp) + (0.0000000876741 * temp * temp * temp))

    # convertir el resultado de kelvin a centigrados y retornar
    return temp - 273.15
'''
