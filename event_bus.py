from events import StartVideoProcessingEvent
import pika
import pickle
import json


class EventBus(object):
    def __init__(self, event):
        self.event = event

    def publish(self):
        body = json.dumps(self.event.__dict__)

        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        print(type(self.event))
        channel.queue_declare(queue=type(self.event).__name__, durable=True)

        channel.basic_publish(exchange='',
                              routing_key=type(self.event).__name__,
                              body=body)

        connection.close()



