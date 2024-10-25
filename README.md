# SNMP para el monitoreo de Agentes DAQ usando Raspberry Pi 4 

Cada agente que es monitoreado a traves de el protocolo SNMP (simple network management protocol) contiene el codigo del controlador alojado en este repositorio, mas en concreto en la carpeta v2RPI. 

# ¿Que es lo que captan los sensores del DAQ actualmente?

Capturan mediciones como la temperatura, las cuales son captadas a traves de un ADC (convertidor analogico-digital) la cual se usa para los modos de control PID y ON/OFF. 

# Modos de control del DAQ

El DAQ provee una configuracion que nos ayuda a controlar el ancho de pulso (PWM) de los pines que estan configurados como salidas las cuales sirven para poder mandar una señal a un actuador, en este caso valvulas solenoides que se usan para controlar la temperatura de un depósito de agua mediante una resistencia eléctrica externa y se probaron para calentar volúmenes de agua entre 50 ml y 2 l.

Los diferentes modos de control que se ofrecen son:
- MANUAL
- TIMER
- PID
- ON/OFF

Control PID
Este tipo de control automático que se usa para mantener una variable de proceso en un valor deseado (setpoint). El controlador PID tiene parámetros importantes que deben definirse durante la inicialización. 

<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/3/33/PID_Compensation_Animated.gif" alt="Descripción de la imagen" width="300">

</p>
La ecuación general del control PID es:

$$
u(t) = K_p e(t) + K_i \int_{0}^{t} e(\tau) d\tau + K_d \frac{de(t)}{dt}
$$

donde:
- $u(t)$ es la señal de control.
- $e(t)$ es el error, definido como la diferencia entre el valor deseado y el valor real del proceso.
- $K_p$  es el coeficiente proporcional.
- $K_i$  es el coeficiente integral.
- $K_d$  es el coeficiente derivativo.


Estos parámetros tienen valores predeterminados:

Valor mínimo de PWM = 0
Valor máximo de PWM = 255
Tiempo de muestreo en microsegundos = 250000 (0,250 s)
Constantes PID:
Kp = 100, Ki = 0,2, Kd = 0.
El controlador PID utiliza un filtro gh simple para suavizar las señales muy ruidosas. 

```c
filtered_input[k] = alpha * current_input + (1 - alpha) * filtered_input[k - 1]
```
donde alfa [0, 1] controla la intensidad del suavizado. alfa = 1 sin suavizado en absoluto , alfa cerca de 0 suavizado muy fuerte . Por defecto alfa = 0,01.

Los valores predeterminados se ajustaron para controlar la temperatura de un depósito de agua mediante una resistencia eléctrica externa y se probaron para calentar volúmenes de agua entre 50 ml y 2 l.

# Descripcion del controlador que ejecuta cada Agente DAQ

Cada agente ejecuta el controlador que destaca por:
- Tener un controlador PID el cual puede ser manipulado de manera remota, es decir, no tiene que haber intervencion en el codigo fuente para poder cambiar ciertos parametros.
- El programa acepta peticiones a traves de un servidor Flask, el cual manda peticiones desde el front-end para poder cambiar aspectos de funcionamiento en el controlador PID, habilitar o deshabilitar un canal de salida, tambien brinda la funcionalidad de obtener los datos del agente daq que se esta gestionando.

# Paneles de configuracion

## Galería de Imágenes

<table>
  <tr>
    <td align="center"><img src="URL_IMAGEN_1" alt="Imagen 1" width="200"/></td>
    <td align="center"><img src="URL_IMAGEN_2" alt="Imagen 2" width="200"/></td>
  </tr>
  <tr>
    <td align="center"><img src="URL_IMAGEN_3" alt="Imagen 3" width="200"/></td>
    <td align="center"><img src="URL_IMAGEN_4" alt="Imagen 4" width="200"/></td>
  </tr>
</table>


# 
# Sistema actual:
![image](https://github.com/user-attachments/assets/edce40f4-6c06-4552-a72d-6fa72e9e1506)


# Configuracion de un agente SNMP.


```sh
PUEDES EXPLICAR TODA ESTA INFORMACION EN UN READ :
###########################################################################
#
# snmpd.conf
# An example configuration file for configuring the Net-SNMP agent ('snmpd')
# See snmpd.conf(5) man page for details
#
###########################################################################
# SECTION: System Information Setup
#

# syslocation: The [typically physical] location of the system.
#   Note that setting this value here means that when trying to
#   perform an snmp SET operation to the sysLocation.0 variable will make
#   the agent return the "notWritable" error code.  IE, including
#   this token in the snmpd.conf file will disable write access to
#   the variable.
#   arguments:  location_string
sysLocation    Sitting on the Dock of the Bay
sysContact     Me <me@example.org>

# sysservices: The proper value for the sysServices object.
#   arguments:  sysservices_number
sysServices    72



###########################################################################
# SECTION: Agent Operating Mode
#
#   This section defines how the agent will operate when it
#   is running.

# master: Should the agent operate as a master agent or not.
#   Currently, the only supported master agent type for this token
#   is "agentx".
#   
#   arguments: (on|yes|agentx|all|off|no)

master agentx

# agentaddress: The IP address and port number that the agent will listen on.
#   By default the agent listens to any and all traffic from any
#   interface on the default SNMP port (161).  This allows you to
#   specify which address, interface, transport type and port(s) that you
#   want the agent to listen on.  Multiple definitions of this token
#   are concatenated together (using ':'s).
#   arguments: [transport:]port[@interface/address],...

agentaddress udp:161
#agentaddress  udp:161,127.0.0.1,[::1],192.168.100.164
# Config SNMPv3
createUser myUser MD5 myAuthPass DES myPrivPass
rwuser myUser authPriv


pass .1.3.6.1.2.1.25.1.8.1 /usr/bin/python3 /home/equipo10/Desktop/snmpCpuTemp.py -g 
pass .1.3.6.1.2.1.25.1.8.2 /usr/bin/python3 /usr/local/bin/adc_ch1_snmp.py
pass .1.3.6.1.2.1.25.1.8.3 /usr/bin/python3 /usr/local/bin/adc_ch2_snmp.py
pass .1.3.6.1.2.1.25.1.8.4 /usr/bin/python3 /usr/local/bin/adc_ch3_snmp.py
pass .1.3.6.1.2.1.25.1.8.5 /usr/bin/python3 /usr/local/bin/adc_ch4_snmp.py
pass .1.3.6.1.2.1.25.1.8.6 /usr/bin/python3 /usr/local/bin/adc_ch5_snmp.py
pass .1.3.6.1.2.1.25.1.8.7 /usr/bin/python3 /usr/local/bin/adc_ch6_snmp.py
pass .1.3.6.1.2.1.25.1.8.8 /usr/bin/python3 /usr/local/bin/adc_ch7_snmp.py

extend temp_ch0         /usr/bin/sudo /usr/bin/python3 /home/equipo10/Desktop/snmpCpuTemp.py -g  
extend biomass_ch1      /usr/local/bin/adc_ch1_snmp.py
extend temp_ch2         /usr/local/bin/adc_ch2_snmp.py
extend biomass_ch3      /usr/local/bin/adc_ch3_snmp.py
extend temp_ch4         /usr/local/bin/adc_ch4_snmp.py
extend biomass_ch5      /usr/local/bin/adc_ch5_snmp.py
extend temp_ch6         /usr/local/bin/adc_ch6_snmp.py
extend biomass_ch7      /usr/local/bin/adc_ch7_snmp.py




###########################################################################
# SECTION: Access Control Setup
#
#   This section defines who is allowed to talk to your running
#   snmp agent.

# Views 
#   arguments viewname included [oid]

#  system + hrSystem groups only
view   systemonly  included   .1.3.6.1.2.1.1
view   systemonly  included   .1.3.6.1.2.1.25.1


# rocommunity: a SNMPv1/SNMPv2c read-only access community name
#   arguments:  community [default|hostname|network/bits] [oid | -V view]

# Read-only access to everyone to the systemonly view
rocommunity public 
rocommunity  public default -V systemonly
rocommunity6 public default -V systemonly

# SNMPv3 doesn't use communities, but users with (optionally) an
# authentication and encryption string. This user needs to be created
# with what they can view with rouser/rwuser lines in this file.
#
# createUser username (MD5|SHA|SHA-512|SHA-384|SHA-256|SHA-224) authpassphrase [DES|AES] [privpassphrase]
# e.g.
# createuser authPrivUser SHA-512 myauthphrase AES myprivphrase
#
# This should be put into /var/lib/snmp/snmpd.conf 
#
# rouser: a SNMPv3 read-only access username
#    arguments: username [noauth|auth|priv [OID | -V VIEW [CONTEXT]]]
rouser myUser authPriv 

# include a all *.conf files in a directory
includeDir /etc/snmp/snmpd.conf.d
#rouser snmpuser

```


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









