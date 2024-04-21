#from serial.tools import list_ports
#from serial.serialutil import SerialException
import serial
import time

# Configuración de la comunicación serial
#puerto_serie = '/dev/ttyACM0'  # Puerto USB donde está conectada la Raspberry Pi Pico
# Definimos el puerto serie de donde queremos obtener la informacion
# en este caso la obtendremos de un arduino conectado al puerto COM4
puerto_serie = 'COM4'
velocidad_serie = 9600  # Velocidad de comunicación en baudios (bps)

# Inicializar la comunicación serial
ser = serial.Serial(puerto_serie, velocidad_serie)


while True:
# Enviar datos a la Raspberry Pi Pico
    getData = ser.read()
    print('Informacion obtenida del puerto COM4: ' + getData)
    #data = str(random.randint(300, 600))
    #print(data)
    #ser.write(data.encode())
    
    time.sleep(1)

    


