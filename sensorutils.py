from math import log

CONFIG_THERMISTOR_RESISTOR = 9900

def thermistor_get_resistance(adcval):
    # calculamos la resistencia del NTC a partir del valor del ADC
    return (CONFIG_THERMISTOR_RESISTOR * ((1023.0 / adcval) - 1))

def thermistor_get_temperature(resistance):
    # variable de almacenamiento temporal, evita realizar varias veces el calculo de log
    temp = log(resistance)

    # resolvemos la ecuacion de STEINHART-HART
    # http://en.wikipedia.org/wiki/Steinhart–Hart_equation
    temp = 1 / (0.001129148 + (0.000234125 * temp) + (0.0000000876741 * temp * temp * temp))

    # convertir el resultado de kelvin a centigrados y retornar
    return temp - 273.15

def get_dissolved_oxygen(voltage):
    dissolved_oxygen = 0.4558 * voltage
    return dissolved_oxygen