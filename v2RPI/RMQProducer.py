import pika
import json
from datetime import datetime
from bson import ObjectId  # Para simular el formato de _id en MongoDB

class RabbitMQProducer:
    def __init__(self, host, port, username, password, exchange_name):
        """
        Inicializa el productor de mensajes para RabbitMQ.

        :param host: Dirección del servidor RabbitMQ.
        :param port: Puerto del servidor RabbitMQ.
        :param username: Nombre de usuario para autenticarse en RabbitMQ.
        :param password: Contraseña para autenticarse en RabbitMQ.
        :param exchange_name: Nombre del intercambio (exchange) de tipo topic.
        """
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.exchange_name = exchange_name
        self.connection = None  # Aquí se almacenará la conexión a RabbitMQ
        self.channel = None  # Aquí se almacenará el canal de comunicación
        
    def connect(self):
        """
        Conecta al servidor RabbitMQ y crea un canal de comunicación.
        """
        credentials = pika.PlainCredentials(self.username, self.password)
        parameters = pika.ConnectionParameters(self.host, self.port, '/', credentials)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        print("Connected to RabbitMQ")

    def declare_exchange(self):
        """
        Declara el intercambio de tipo topic en el servidor RabbitMQ.
        """
        self.channel.exchange_declare(exchange=self.exchange_name, exchange_type=pika.ExchangeType.topic)
        print(f"Exchange '{self.exchange_name}' declared.")

    def publish_message(self, routing_key, configuration=None, metrics=None):
        """
        Publica un mensaje en el intercambio especificado usando la clave de enrutamiento.

        :param routing_key: Clave de enrutamiento para el mensaje.
        :param configuration: Objeto JSON opcional con configuración del sensor.
        :param metrics: Objeto JSON con métricas del sensor.
        """
        # Generar el mensaje en formato measurements
        message = {
              # ID único simulado
            "schema": "1.0.0",
            "timestamp": datetime.utcnow().isoformat(),  # Timestamp en UTC
            "sensor": str(ObjectId()),  # Referencia a un sensor por su _id
            "configuration": configuration if configuration else {},  # Configuración opcional
            "metrics": metrics if metrics else {}
        }

        try:
            # Enviar el mensaje
            self.channel.basic_publish(
                exchange=self.exchange_name,
                routing_key=routing_key,
                body=json.dumps(message),
                mandatory=True  # Activa el manejo de mensajes no enrutables
            )
            print(f"Sent message: {message}")

        except pika.exceptions.UnroutableError:
            print('Message could not be routed to any queue')

    def close_connection(self):
        """
        Cierra la conexión con RabbitMQ.
        """
        if self.connection:
            self.connection.close()
            print("Connection closed")


'''
Ejemplo 1 (deprecated):

producer = RabbitMQProducer(host="ip_address", port=5672, username="admin", password="admin", exchange_name="mytopic")

producer.connect()
producer.declare_exchange()

configuration = {"sampling_rate": "1s"}
metrics = {"temperature": 25.5, "unit": "Celsius"}

producer.publish_message(routing_key="sensor.data.temperature", configuration=configuration, metrics=metrics)

producer.close_connection()

'''

'''
# Ejemplo de uso:
if __name__ == "__main__":
    producer = RabbitMQProducer(
        host="ip_address", 
        port=5672, 
        username="admin", 
        password="admin", 
        exchange_name="mytopic"
    )

    try:
        producer.connect()
        producer.declare_exchange()

        
        configuration = {"sampling_rate": "1s"}
        
        metrics = {
            "temperature": {
                "value": 25.5,
                "unit": "Celsius"
            }
        }

        producer.publish_message(
            routing_key="sensor.data.temperature",
            configuration={},
            metrics=metrics
        )
    finally:
        producer.close_connection()
'''