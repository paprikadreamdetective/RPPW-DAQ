

class CommandHandler():
    
    def request_outputs_info(self, slave_address):
        pass
    def request_outputs_data(self, slave_address):
        pass
    def request_inputs_info(self, slave_address):
        pass
    def request_inputs_data(self, slave_address):
        pass
    def write_to_master(self, string):
        pass
    def write_to_slaves(self, string):
        pass
    def send_input_data(self, address, slaves, inputs_buffer, pulses_buffer):
        pass
    def write_slaves_inputs(self, slaves):
        pass
    def update_inputs_buffer(self, inputs, inputs_buffer):
        pass
    def send_output_data(self, address, slaves, outputs_buffer):
        pass
    def write_slaves_outputs(self, slaves):
        pass
    def update_outputs_buffer(self, outputs, outputs_buffer):
        pass