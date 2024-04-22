import machine
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
            pass

