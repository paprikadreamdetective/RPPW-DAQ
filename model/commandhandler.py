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
            input_string += in_char[index]
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

