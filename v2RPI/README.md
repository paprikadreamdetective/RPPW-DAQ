# DAQ: Dispositivo de Adquisicion de datos

Raspberry Pi 4: Dispositivo encargado de obtener los datos medidos por los sensores y publicarlos en la fila del agente de mensajes asi como recibir peticiones de cambio de configuracion. Este dispositivo obtiene las mediciones mediante un convertidor analogico-digital (ADC) MCP3008 el cual tiene una resolucion de 10 bits (valores entre 0 - 1023). 

## Peticiones de configuracion

Estas peticiones consisten en configurar las salidas PWM para poder hacer algun cambio a la hora de controlar un actuador. Estos pines abarcan del [18 - 23]

