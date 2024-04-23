import machine
import utime
from .messagehandler import MessageHandler
from .communicationhandler import CommunicationHandler
class CommandHandler(MessageHandler, CommunicationHandler):
    def parse_serial(self, in_char: list[chr], new_command: bool) -> str:
        """
        Lectura serial del buffer
        """
        input_string = ''
        index = 0
        while index < 255:
            input_string += in_char[index ]
            if in_char[index] == '!':
                new_command = True
                break
            index += 1
        return input_string
    
    def parse_serial_master(self, new_command: bool) -> str:
        """
        Lectura serial del buffer
        """
        input_string = ''
        while machine.uart.any():
            in_char = chr(machine.uart.read(1)[0])
            input_string += in_char
            if in_char == '!':
                new_command = True
                break
        return input_string
    
    def parse_serial_slave(new_command: bool) -> str:
        """
        Lectura serial del buffer
        """
        input_string = ''
        while machine.uart.any():
            in_char = chr(machine.uart.read(1)[0])
            input_string += in_char
            if in_char == '!':
                new_command = True
                break
        return input_string
    
    def parse_slave_to_master(self) -> str:
        """
        Esta es una funcion que bloquea.

        Espera 90ms la entrada del buffer serial de los esclavos (Serial2)
        Esta lectura se hace cuando el buffer de informacion Serial2 esta disponible
        """
        wait_for = 500
        waiting = True
        slave_string = ''
        started_waiting = utime.ticks_ms()
        while waiting and (utime.ticks_diff(utime.ticks_ms(), started_waiting) <= wait_for):
            while uart.any():
                in_char = uart.read(1)[0]
                if in_char != '!':
                    slave_string += in_char
                if in_char == '!':
                    waiting = False
                    break
        return slave_string
    
    def request_inputs_info(self):
        # Definir comando y cadena de comando
        GET_INPUTS_INFO = 2  # Debes definir GET_INPUTS_INFO según tu aplicación
        command = str(GET_INPUTS_INFO)
        command_string = "{} {}{}!".format(slave_address, command, ",")

        # Enviar comando a los esclavos
        self.write_to_slaves(command_string, transmit_pin)

        # Leer y devolver la información de entradas
        input_info = self.parse_slave_to_master()
        return input_info
    
    def request_inputs_data(self, slave_address: str, transmit_pin: int):
        """
        Envia las peticiones a la entrada de los esclavos y espera 
        una respuesta.
        """
        GET_INPUTS_DATA = 1
        command = str(GET_INPUTS_DATA)
        command_string = slave_address + " " + command + ",!"
        self.write_to_slaves(command_string, transmit_pin)
        input_data = self.parse_slave_to_master()
        return input_data
    
    # Función para enviar una solicitud de información de salidas a los esclavos y esperar una respuesta
    def request_outputs_info(slave_address, transmit_pin):
        # Definir comando y cadena de comando
        GET_OUTPUTS_INFO = 4  # Debes definir GET_OUTPUTS_INFO según tu aplicación
        command = str(GET_OUTPUTS_INFO)
        command_string = "{} {}{}!".format(slave_address, command, ",")

        # Enviar comando a los esclavos
        self.write_to_slaves(command_string, transmit_pin)

        # Leer y devolver la información de salidas
        output_info = self.parse_slave_to_master()
        return output_info

    # Función para enviar una solicitud de datos de salidas a los esclavos y esperar una respuesta
    def request_outputs_data(slave_address, transmit_pin):
        # Definir comando y cadena de comando
        GET_OUTPUTS_DATA = 3  # Debes definir GET_OUTPUTS_DATA según tu aplicación
        command = str(GET_OUTPUTS_DATA)
        command_string = "{} {}{}!".format(slave_address, command, ",")

        # Enviar comando a los esclavos
        self.write_to_slaves(command_string, transmit_pin)

        # Leer y devolver los datos de salidas
        output_data = self.parse_slave_to_master()
        return output_data
        
    # Función para escribir en el maestro
    def write_to_master(string, transmit_pin):
        # Configurar el pin de transmisión como salida y ponerlo en alto
        transmit_pin_obj = machine.Pin(transmit_pin, machine.Pin.OUT)
        transmit_pin_obj.value(1)
        utime.sleep_ms(10)  # Esperar 10 milisegundos

        # Enviar la cadena a través de Serial2
        uart = machine.UART(1, baudrate=9600, tx=transmit_pin)
        uart.write(string.encode('utf-8'))  # Convertir la cadena a bytes y enviarla

        utime.sleep_ms(120)  # Esperar 120 milisegundos

        # Poner el pin de transmisión en bajo
        transmit_pin_obj.value(0)

    # Función para escribir en los esclavos
    def write_to_slaves(string, transmit_pin):
        # Configurar el pin de transmisión como salida y ponerlo en alto
        transmit_pin_obj = machine.Pin(transmit_pin, machine.Pin.OUT)
        transmit_pin_obj.value(1)

        # Enviar la cadena a través de Serial2
        uart = machine.UART(1, baudrate=9600, tx=transmit_pin)
        uart.write(string.encode('utf-8'))  # Convertir la cadena a bytes y enviarla

        utime.sleep_ms(20)  # Esperar 20 milisegundos

        # Poner el pin de transmisión en bajo
        transmit_pin_obj.value(0)

    # Función para obtener información de entradas y generar una cadena de texto con el formato deseado
    def get_inputs_info(inputs, number_of_inputs):
        # Inicializar la cadena de texto
        inputs_string = ""

        # Recorrer cada entrada en la lista de entradas
        for i in range(number_of_inputs):
            # Agregar información de cada entrada al formato de cadena deseado
            inputs_string += "('" + inputs[i]['type'] + "'," + str(inputs[i]['channel']) + "," + "'" + inputs[i]['variable'] + "'),"

        return inputs_string
    
    # Función para obtener información de salidas y generar una cadena de texto con el formato deseado
    def get_outputs_info(outputs, number_of_outputs):
        # Inicializar la cadena de texto
        outputs_string = ""

        # Recorrer cada salida en la lista de salidas
        for i in range(number_of_outputs):
            # Agregar información de cada salida al formato de cadena deseado
            outputs_string += "('" + outputs[i]['type'] + "'," + str(outputs[i]['channel']) + "),"
        return outputs_string   
    
    # Función para enviar datos de entrada a través de UART a los esclavos y al maestro
    def send_input_data(address, slaves, number_of_slaves, transmit_pin, inputs_buffer, pulses_buffer):
        # Construir la cadena de datos de entrada para el maestro
        inputs_string = "{'" + address + "':[" + inputs_buffer + pulses_buffer + "],"

        # Llamar a la función para enviar datos de entrada a los esclavos y agregar sus datos a la cadena
        inputs_string += write_slaves_inputs(slaves, number_of_slaves, transmit_pin) + "}115,!"

        # Imprimir la cadena de datos de entrada
        print(inputs_string)

        # Limpiar los buffers para mantener solo las lecturas más recientes
        inputs_buffer = ""
        pulses_buffer = ""

    # Función para enviar datos de salida a través de UART a los esclavos y al maestro
    def send_output_data(address, slaves, number_of_slaves, transmit_pin, outputs_buffer):
        # Construir la cadena de datos de salida para el maestro
        outputs_string = "{'" + address + "':[" + outputs_buffer + "],"

        # Llamar a la función para enviar datos de salida a los esclavos y agregar sus datos a la cadena
        outputs_string += write_slaves_outputs(slaves, number_of_slaves, transmit_pin) + "}115,!"

        # Imprimir la cadena de datos de salida
        print(outputs_string)

        # Limpiar el buffer para mantener solo los valores más recientes
        outputs_buffer = ""

    # Función para solicitar datos de entrada a los esclavos
    def write_slaves_inputs(slaves, number_of_slaves, transmit_pin):
        # Inicializar la cadena de datos de entrada de los esclavos
        slaves_input_data = ""

        # Recorrer cada esclavo en la lista de esclavos
        for i in range(number_of_slaves):
            # Agregar la entrada de datos de cada esclavo al formato de cadena deseado
            slaves_input_data += "'" + slaves[i] + "':["
            slaves_input_data += request_inputs_data(slaves[i], transmit_pin)
            slaves_input_data += "],"

        return slaves_input_data

    # Función para solicitar datos de salida a los esclavos
    def write_slaves_outputs(slaves, number_of_slaves, transmit_pin):
        # Inicializar la cadena de datos de salida de los esclavos
        slaves_output_data = ""

        # Recorrer cada esclavo en la lista de esclavos
        for i in range(number_of_slaves):
            # Agregar la salida de datos de cada esclavo al formato de cadena deseado
            slaves_output_data += "'" + slaves[i] + "':["
            slaves_output_data += request_outputs_data(slaves[i], transmit_pin)
            slaves_output_data += "],"

        return slaves_output_data

    # Función para actualizar el buffer de entradas
    def update_inputs_buffer(inputs, number_of_inputs, inputs_buffer):
        # Limpiar el buffer para mantener solo las lecturas más recientes
        inputs_buffer = ""

        # Recorrer cada entrada en la lista de entradas
        for i in range(number_of_inputs):
            # Agregar la entrada al formato de cadena deseado en el buffer de entradas
            inputs_buffer += "(" + str(inputs[i]['channel']) + "," + str(inputs[i]['value']) + "),"

        return inputs_buffer
    
    # Función para actualizar el buffer de salidas
    def update_outputs_buffer(outputs, number_of_outputs, outputs_buffer):
        # Limpiar el buffer para mantener solo las lecturas más recientes
        outputs_buffer = ""

        # Recorrer cada salida en la lista de salidas
        for i in range(number_of_outputs):
            # Agregar la salida al formato de cadena deseado en el buffer de salidas
            outputs_buffer += "(" + str(outputs[i]['channel']) + "," + str(outputs[i]['value']) + "),"

        return outputs_buffer


