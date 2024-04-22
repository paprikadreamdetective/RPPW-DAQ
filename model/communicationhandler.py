import abc 
class CommunicationHandler(abc.ABC):
    @abc.abstractmethod
    def request_outputs_info(self):
        pass
    @abc.abstractmethod
    def request_outputs_data(self):
        pass
    @abc.abstractmethod
    def request_inputs_info(self):
        pass
    @abc.abstractmethod
    def request_inputs_data(self):
        pass
    @abc.abstractmethod
    def write_to_master(self):
        pass
    @abc.abstractmethod
    def write_to_slaves(self):
        pass
    @abc.abstractmethod
    def get_outputs_info(self):
        pass
    @abc.abstractmethod
    def get_inputs_info(self):
        pass
    @abc.abstractmethod
    def send_input_data(self):
        pass
    @abc.abstractmethod
    def write_slaves_inputs(self):
        pass
    @abc.abstractmethod
    def update_inputs_buffer(self):
        pass
    @abc.abstractmethod
    def send_output_data(self):
        pass
    @abc.abstractmethod
    def write_slaves_outputs(self):
        pass
    @abc.abstractmethod
    def update_outputs_buffer(self):
        pass