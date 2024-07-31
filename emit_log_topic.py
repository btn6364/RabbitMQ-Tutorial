import pika
import sys

# Create a connection with RabbitMQ server. 
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Declare a topic exchange. 
channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

# Get the routing_key for the exchange. 
routing_key = sys.argv[1] if len(sys.argv) > 2 else 'anonymous.info'
message = ' '.join(sys.argv[2:]) or 'Hello World!'

# Publish the message to the exchange. 
channel.basic_publish(exchange='topic_logs', routing_key=routing_key, body=message)
print(f" [x] Sent {routing_key}:{message}")
connection.close()