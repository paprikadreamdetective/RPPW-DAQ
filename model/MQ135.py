import Sensor
class MQ135(Sensor):
    def __init__(self, pin):
        self.pin = pin

    def read(self):
        return 100
    