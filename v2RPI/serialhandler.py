import serial

class SerialCommunicator:
    def __init__(self, port="/dev/ttyUSB0", baudrate=9600):
        self.serial_conn = serial.Serial(port, baudrate, timeout=1)
        if self.serial_conn.is_open:
            print("Conexión serial establecida")

    def send_data(self, data):
        try:
            self.serial_conn.write(f"{data}\n".encode('utf-8'))
            print(f"Datos enviados: {data}")
        except Exception as e:
            print(f"Error enviando datos: {e}")

    def close(self):
        self.serial_conn.close()
        print("Conexión serial cerrada")
