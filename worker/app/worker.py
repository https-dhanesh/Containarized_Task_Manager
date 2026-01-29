import pika
import time
import json
import os
from sqlalchemy.orm import Session
from . import database, models

rabbitmq_url = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")
params = pika.URLParameters(rabbitmq_url)
while True:
    try:
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        print(" Connected to RabbitMQ successfully!")
        break
    except pika.exceptions.AMQPConnectionError:
        print("RabbitMQ not ready yet. Retrying in 5 seconds...")
        time.sleep(5)
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)

print(" Worker waiting for tasks. To exit press CTRL+C")

def callback(ch, method, properties, body):
    print(f" Received {body}")
    data = json.loads(body)
    task_id = data.get("task_id")

    db = database.SessionLocal()
    
    try:
        task = db.query(models.Task).filter(models.Task.id == task_id).first()
        
        if task:
            print(f" Processing Task ID: {task_id}")
            task.status = "PROCESSING"
            db.commit()

            time.sleep(10)

            task.status = "DONE"
            db.commit()
            print(f" Task {task_id} marked as DONE")
        
    except Exception as e:
        print(f"Error processing task: {e}")
    finally:
        db.close()
        ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)
channel.start_consuming()