# SNMP para el monitoreo de Agentes DAQ usando Raspberry Pi 4 
Cada agente que es monitoreado a traves de el protocolo SNMP (simple network management protocol) contiene el codigo del controlador alojado en este repositorio, mas en concreto en la carpeta v2RPI. 



# Descripcion del controlador que ejecuta cada Agente DAQ

Cada agente ejecuta el controlador que destaca por:
- Tener un controlador PID el cual puede ser manipulado de manera remota, es decir, no tiene que haber intervencion en el codigo fuente para poder cambiar ciertos parametros.
- El programa acepta peticiones a traves de un servidor Flask, el cual manda peticiones desde el front-end para poder cambiar aspectos de funcionamiento en el controlador PID, habilitar o deshabilitar un canal de salida, tambien brinda la funcionalidad de obtener los datos del agente daq que se esta gestionando.

# 
  






