import serial.tools.list_ports

def escanear_puertos_com():
    # Obtener una lista de los puertos COM disponibles y utilizados
    puertos = serial.tools.list_ports.comports()
    
    print("Puertos COM disponibles y utilizados:")
    for puerto in puertos:
        print(f"- {puerto.device}: {puerto.description}")

if __name__ == "__main__":
    escanear_puertos_com()