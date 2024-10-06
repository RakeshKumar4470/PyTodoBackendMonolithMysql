import mysql.connector
import uvicorn
import os
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Update connection string format for MySQL
connection_config = {
    'user': "dbadmin",
    'password': "Test@1234",
    'host': "172.17.0.2",
    'database': "todoapp",
}

app = FastAPI()

# Configure CORSMiddleware to allow all origins (disable CORS for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # This allows all origins (use '*' for development only)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the Task model
class Task(BaseModel):
    title: str
    description: str

# Create a table for tasks (You can run this once outside of the app)
@app.get("/api")
def create_tasks_table():
    try:
        conn = mysql.connector.connect(**connection_config)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Tasks (
                ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                Title VARCHAR(255),
                Description TEXT
            );
        """)
        conn.commit()        
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
    return "Table Created... Tasks API Ready"

# List all tasks
@app.get("/api/tasks")
def get_tasks():
    tasks = []
    try:
        conn = mysql.connector.connect(**connection_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Tasks")
        tasks = cursor.fetchall()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
    return tasks

# Retrieve a single task by ID
@app.get("/api/tasks/{task_id}")
def get_task(task_id: int):
    try:
        conn = mysql.connector.connect(**connection_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Tasks WHERE ID = %s", (task_id,))
        task = cursor.fetchone()
        if task:
            return task
        return {"message": "Task not found"}
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

# Create a new task
@app.post("/api/tasks")
def create_task(task: Task):
    try:
        conn = mysql.connector.connect(**connection_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Tasks (Title, Description) VALUES (%s, %s)", (task.title, task.description))
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
    return task

# Update an existing task by ID
@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: Task):
    try:
        conn = mysql.connector.connect(**connection_config)
        cursor = conn.cursor()
        cursor.execute("UPDATE Tasks SET Title = %s, Description = %s WHERE ID = %s", 
                       (updated_task.title, updated_task.description, task_id))
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
    return {"message": "Task updated"}

# Delete a task by ID
@app.delete("/api/tasks/{task_id}")
def delete_task(task_id: int):
    try:
        conn = mysql.connector.connect(**connection_config)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Tasks WHERE ID = %s", (task_id,))
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
    return {"message": "Task deleted"}

if __name__ == "__main__":
    create_tasks_table()
    uvicorn.run(app, host="0.0.0.0", port=8000)

