"""
La clase esclavo define los atributos necesarios para las instancias 
que se emplearan mas adelante, ademas de que brinda permisos para
modificar los atributos de dicha clase y obtener sus valores.
"""
class Slave:
    def __init__(self, name: str, broadcast_address: list[int], input_info: str, output_info: str):
        self._name = name
        self._broadcast_address = broadcast_address
        self._input_info = input_info
        self._output_info = output_info
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = value
    @property
    def broadcast_address(self):
        return self._broadcast_address
    @broadcast_address.setter
    def broadcast_address(self, value):
        self._broadcast_address = value
    @property
    def input_info(self):
        return self._input_info
    @input_info.setter
    def input_info(self, value):
        self._input_info = value
    @property
    def output_info(self):
        return self._output_info
    @output_info.setter
    def output_info(self, value):
        self._output_info = value    