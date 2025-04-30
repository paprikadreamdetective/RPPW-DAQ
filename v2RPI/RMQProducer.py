import pika
import json
from datetime import datetime
from bson import ObjectId  # Para simular el formato de _id en MongoDB

import pika
import json
from datetime import datetime
from bson import ObjectId  # Para simular el formato de _id en MongoDB

# Configuración de RabbitMQ desde variables globales
RABBITMQ_HOST = "148.206.162.62"
RABBITMQ_PORT = 5672
RABBITMQ_USERNAME = "admin"
RABBITMQ_PASSWORD = "admin"
RABBITMQ_EXCHANGE = "example_queue"
RABBITMQ_QUEUE = "example_queue"
RABBITMQ_ROUTING_KEY = "routing_key"

class RabbitMQProducer:
    def __init__(self):
        """
        Inicializa el productor de mensajes para RabbitMQ.
        """
        self.connection = None
        self.channel = None
        
    def connect(self):
        """
        Conecta al servidor RabbitMQ y crea un canal de comunicación.
        """
        credentials = pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)
        parameters = pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT, credentials=credentials)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        print("Connected to RabbitMQ")

    def declare_exchange(self):
        """
        Declara el intercambio y la cola en el servidor RabbitMQ.
        """
        self.channel.exchange_declare(exchange=RABBITMQ_EXCHANGE, exchange_type='topic', durable=True)
        self.channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)
        self.channel.queue_bind(exchange=RABBITMQ_EXCHANGE, queue=RABBITMQ_QUEUE, routing_key=RABBITMQ_ROUTING_KEY)
        print(f"Exchange '{RABBITMQ_EXCHANGE}' and Queue '{RABBITMQ_QUEUE}' declared and bound.")

    def publish_message(self, sensor_id, timestamp, value):
        """
        Publica un mensaje en el intercambio especificado usando la clave de enrutamiento.
        """
        metric = {
            "schema": "1.0.0",
            "timestamp": timestamp,
            "sensor_id": sensor_id,
            "configuration": {"sampling_rate": 0.5},
            "metrics": {
                "temperature": {
                    "value": value,
                    "unit": "Celsius"
                }
            }
        }
        try:
            message_json = json.dumps(metric)
            self.channel.basic_publish(
                exchange=RABBITMQ_EXCHANGE,
                routing_key=RABBITMQ_ROUTING_KEY,
                body=message_json,
                properties=pika.BasicProperties(delivery_mode=2)  # Hace que el mensaje sea persistente
            )
            print(f"Sent message: {message_json}")
        except pika.exceptions.UnroutableError:
            print('Message could not be routed to any queue')

    def close_connection(self):
        """
        Cierra la conexión con RabbitMQ.
        """
        if self.connection:
            self.connection.close()
            print("Connection closed")



