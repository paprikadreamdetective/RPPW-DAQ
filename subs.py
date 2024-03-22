import paho.mqtt.client as mqtt

# Dirección IP de la Raspberry Pi Pico W
raspberry_pi_ip = "192.168.100.109"  # ¡Cambia esto por la dirección IP correcta!

# Tema al que quieres suscribirte
topic = "LabHardware"

def on_connect(client, userdata, flags, rc):
    print("Conectado al broker MQTT con resultado: " + mqtt.connack_string(rc))
    client.subscribe(topic)

def on_message(client, userdata, msg):
    print("Mensaje recibido en el tema {}: {}".format(msg.topic, msg.payload.decode()))

# Configurar el cliente MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Conectarse al broker MQTT en la Raspberry Pi Pico W
client.connect(raspberry_pi_ip, 1883, 60)

# Mantener el cliente conectado indefinidamente
client.loop_forever()
