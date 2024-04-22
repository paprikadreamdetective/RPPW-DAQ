import abc
class MessageHandler(abc.ABC):
    @abc.abstractmethod
    def parse_serial(self):
        pass
    @abc.abstractmethod
    def parse_serial_master(self):
        pass
    @abc.abstractmethod
    def parse_serial_slave(self):
        pass
    @abc.abstractmethod
    def parse_slave_to_master(self):
        pass