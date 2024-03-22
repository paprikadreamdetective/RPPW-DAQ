class Sensor:
    def get_correction_factor(self, temperature, humidity):
       raise NotImplementedError()

    def get_resistance(self):
       raise NotImplementedError()

    def get_corrected_resistance(self, temperature, humidity):
       raise NotImplementedError()

    def get_ppm(self):
        raise NotImplementedError()

    def get_corrected_ppm(self, temperature, humidity):
        raise NotImplementedError()

    def get_rzero(self):
       raise NotImplementedError()

    def get_corrected_rzero(self, temperature, humidity):
        raise NotImplementedError()