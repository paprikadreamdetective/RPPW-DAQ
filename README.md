# SNMP para el monitoreo de Agentes DAQ usando Raspberry Pi 4 
Cada agente que es monitoreado a traves de el protocolo SNMP (simple network management protocol) contiene el codigo del controlador alojado en este repositorio, mas en concreto en la carpeta v2RPI. 

# Configuracion de un agente SNMP.
Sección 1: Configuración de Información del Sistema
sysLocation: Define la ubicación física del sistema. Al establecerlo en este archivo, el valor de sysLocation.0 será de solo lectura y no podrá modificarse a través de comandos SNMP SET.

Ejemplo: sysLocation Sitting on the Dock of the Bay
sysContact: Proporciona información de contacto para el administrador del sistema.

Ejemplo: sysContact Me <me@example.org>
sysServices: Define los servicios proporcionados por el sistema. En este caso, el valor es 72, que se refiere a servicios de red y aplicaciones disponibles.

Sección 2: Modo de Operación del Agente
master agentx: Configura el agente para operar como agente maestro usando agentx, un protocolo que permite la comunicación entre subagentes y agentes principales.

agentaddress: Especifica las direcciones IP y puertos que el agente escuchará para recibir solicitudes SNMP. El valor por defecto es udp:161, que significa que escuchará en todas las interfaces en el puerto 161 UDP.

Configuración SNMPv3
createUser: Define un usuario SNMPv3 llamado myUser con autenticación MD5 (myAuthPass) y privacidad (encriptación) DES (myPrivPass).

rwuser: Define acceso de lectura-escritura para el usuario myUser, con autenticación y privacidad habilitadas.

Sección 3: Comandos para Extensiones SNMP
Los comandos pass y extend permiten ejecutar scripts personalizados y asociarlos a identificadores de objetos (OIDs) específicos.

pass: Asocia un OID a un script que será ejecutado cuando se consulte ese OID. Ejemplos:

pass .1.3.6.1.2.1.25.1.8.1 ejecuta el script snmpCpuTemp.py para obtener la temperatura de la CPU.
Otros scripts en /usr/local/bin/ están asociados a distintos canales ADC (para sensores conectados).
extend: Ejecuta scripts y devuelve el resultado cuando se consulta el OID asociado.

Ejemplo: extend temp_ch0 ejecuta el script snmpCpuTemp.py para el canal 0.
Sección 4: Configuración de Control de Acceso
view: Define vistas SNMP, que restringen los OIDs que se pueden consultar.

Ejemplo: view systemonly incluye las ramas .1.3.6.1.2.1.1 y .1.3.6.1.2.1.25.1, que contienen información básica del sistema.
rocommunity: Proporciona acceso de solo lectura a comunidades SNMPv1 y SNMPv2c.

Ejemplo: rocommunity public permite acceso de solo lectura a cualquiera que use la comunidad public.
rouser: Para SNMPv3, define el usuario myUser con acceso de solo lectura, autenticación y privacidad habilitadas.

Sección 5: Inclusión de Archivos
includeDir: Permite incluir todos los archivos .conf adicionales en el directorio /etc/snmp/snmpd.conf.d, facilitando una configuración modular del agente SNMP.

# Descripcion del controlador que ejecuta cada Agente DAQ

Cada agente ejecuta el controlador que destaca por:
- Tener un controlador PID el cual puede ser manipulado de manera remota, es decir, no tiene que haber intervencion en el codigo fuente para poder cambiar ciertos parametros.
- El programa acepta peticiones a traves de un servidor Flask, el cual manda peticiones desde el front-end para poder cambiar aspectos de funcionamiento en el controlador PID, habilitar o deshabilitar un canal de salida, tambien brinda la funcionalidad de obtener los datos del agente daq que se esta gestionando.

# 
  






