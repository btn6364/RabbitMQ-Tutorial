import pika
import sys

# Create a connection to RabbitMQ server. 
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Create a direct exchange
channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

# Declare a temporary queue
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

severities = sys.argv[1:]
if not severities:
    sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
    sys.exit(1)

for severity in severities:
    # Create a binding for each severity
    channel.queue_bind(exchange='direct_logs', queue=queue_name, routing_key=severity)

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(f" [x] {method.routing_key}:{body}")


channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()

# python receive_logs_direct.py warning error
# python receive_logs_direct.py info warning error
# python emit_log_direct.py error "Run. Run. Or it will explode."
# python emit_log_direct.py info "This is some information."