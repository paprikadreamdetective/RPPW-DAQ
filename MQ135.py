#from Sensor import Sensor
#from .Sensor import Sensor
#from Sensor import Sensor
import Sensor 
import machine
import math

class MQ135(Sensor.Sensor):
    def __init__(self, pin):
        self.pin = machine.ADC(pin)
        
    def read(self):
        return self.pin.read_u16()
    