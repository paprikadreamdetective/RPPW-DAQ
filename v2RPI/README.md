# Hardware de recoleccion de datos

Este dispositivo es capaz de tomar mediciones y poderlas mandar mediante la red haciendo uso de un productor de mensajes RabbitMQ, en donde las mediciones que se toman se envian en un cierto formato JSON para posteriormente almacenarlos en una base de datos. 

### Diagrama de contexto: 

![ARCH_LA-Página-6](https://github.com/user-attachments/assets/abeda79b-778c-4bf0-a6b2-c8876a18cb18)


## Peticiones de configuracion

Estas peticiones consisten en configurar las salidas PWM para poder hacer algun cambio a la hora de controlar un actuador. Estos pines abarcan del [18 - 23]

