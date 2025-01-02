import serial

class SerialCommunicator:
    def __init__(self, port, baud_rate):
        self.port = port
        self.baud_rate = baud_rate
        self.connection = self._initialize_connection()

    def _initialize_connection(self):
        try:
            return serial.Serial(self.port, self.baud_rate, timeout=2)
        except Exception as e:
            raise RuntimeError(f"Failed to connect to Arduino: {str(e)}")

    def send_command(self, command):
        try:
            if self.connection.is_open:
                self.connection.write(f"{command}\n".encode())
                response = self.connection.readline().decode().strip()
                return response
            else:
                raise RuntimeError("Serial connection is not open")
        except Exception as e:
            raise RuntimeError(f"Failed to send command: {str(e)}")
    
    def close_connection(self):
        """Cierra la conexión con el puerto serial."""
        try:
            if self.connection and self.connection.is_open:
                self.connection.close()
                return "Connection closed successfully"
            else:
                return "Connection already closed or not initialized"
        except Exception as e:
            raise RuntimeError(f"Failed to close connection: {str(e)}")

    '''
    def send_data(self, data):
        try:
            self.serial_conn.write(f"{data}\n".encode('utf-8'))
            print(f"Datos enviados: {data}")
        except Exception as e:
            print(f"Error enviando datos: {e}")

    def close(self):
        self.serial_conn.close()
        print("Conexión serial cerrada")
    '''
