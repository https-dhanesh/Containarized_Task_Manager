from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, database
import pika
import json
import os

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

def get_rabbitmq_channel():
    url = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")
    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True)
    return connection, channel


@app.post("/tasks", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(database.get_db)):
    db_task = models.Task(content=task.content, status="PENDING")
    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    try:
        connection, channel = get_rabbitmq_channel()
        message = json.dumps({"task_id": db_task.id})
        
        channel.basic_publish(
            exchange='',
            routing_key='task_queue',
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2, 
            ))
        connection.close()
    except Exception as e:
        print(f"Error connecting to RabbitMQ: {e}")

    return db_task

@app.get("/tasks", response_model=list[schemas.Task])
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    tasks = db.query(models.Task).offset(skip).limit(limit).all()
    return tasks