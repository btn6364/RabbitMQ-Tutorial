import pika
import sys

# Create a connection with RabbitMQ server. 
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Create a topic exchange. 
channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

# Create a temporary queue for the consumer. 
result = channel.queue_declare('', exclusive=True)
queue_name = result.method.queue

# Collect the binding keys
binding_keys = sys.argv[1:]
if not binding_keys:
    sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
    sys.exit(1)

for binding_key in binding_keys:
    # Create a binding with the exchange for each queue
    channel.queue_bind(exchange='topic_logs', queue=queue_name, routing_key=binding_key)

print(' [*] Waiting for logs. To exit press CTRL+C')

# Define a callback function. 
def callback(ch, method, properties, body):
    print(f" [x] {method.routing_key}:{body}")

# Consume the message
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()

# "<facility>.<severity>", facility (application, kernel), severity: critical, normal. 
# python receive_logs_topic.py "#"
# python receive_logs_topic.py "kernel.*"
# python receive_logs_topic.py "*.critical"
# python receive_logs_topic.py "kernel.*" "*.critical"
# python emit_log_topic.py "kernel.critical" "A critical kernel error"
# python emit_log_topic.py "application.critical" "A critical application error"
# python emit_log_topic.py "application.normal" "A normal application error"