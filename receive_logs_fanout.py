import pika

# Create a connection to the RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Create a fanout exchange
channel.exchange_declare(exchange='logs', exchange_type='fanout')

# Declare a temporary queue
# queue name may look sth like this: amq.gen-JzTY20BRgKO-HjmUJj0wLg
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

# Create a binding between the exchange and the queue.
channel.queue_bind(exchange='logs', queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(f" [x] {body}")

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()