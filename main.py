from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import asyncio
import uuid
import time
import os
import edge_tts

from dotenv import load_dotenv
from openai import OpenAI

# =====================================
# LOAD ENV
# =====================================

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# =====================================
# FASTAPI
# =====================================

app = FastAPI()

task_queue = asyncio.Queue()

task_store = {}

# =====================================
# TASK MODEL
# =====================================

class Task:

    def __init__(self, task_type, payload):

        self.id = str(uuid.uuid4())

        self.task_type = task_type

        self.payload = payload

        self.status = "PENDING"

        self.result = None

        self.created_at = time.time()

    def to_dict(self):

        return {
            "id": self.id,
            "task_type": self.task_type,
            "payload": self.payload,
            "status": self.status,
            "result": self.result,
            "created_at": self.created_at
        }

# =====================================
# REQUEST MODEL
# =====================================

class ScriptRequest(BaseModel):

    topic: str

    platform: str = "tiktok"

    duration: int = 30

# =====================================
# AI SCRIPT GENERATOR
# =====================================

async def generate_script(topic, platform, duration):

    prompt = f"""
Create a viral short-form video script.

Topic:
{topic}

Platform:
{platform}

Duration:
{duration} seconds

Return:
- Hook
- 3 short scenes
- CTA
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content

# =====================================
# VOICE GENERATOR
# =====================================

async def generate_voice(text, task_id):

    os.makedirs("outputs", exist_ok=True)

    filename = f"outputs/{task_id}.mp3"

    communicate = edge_tts.Communicate(
        text,
        voice="en-US-AriaNeural"
    )

    await communicate.save(filename)

    return filename

# =====================================
# WORKER
# =====================================

async def worker():

    while True:

        task = await task_queue.get()

        print(f"[WORKER] processing {task.id}")

        task.status = "RUNNING"

        try:

            if task.task_type == "generate_script":

                script_result = await generate_script(
                    task.payload["topic"],
                    task.payload["platform"],
                    task.payload["duration"]
                )

                voice_file = await generate_voice(
                    script_result,
                    task.id
                )

                task.result = {
                    "script": script_result,
                    "voice_file": voice_file
                }

            task.status = "COMPLETED"

        except Exception as e:

            task.status = "FAILED"

            task.result = str(e)

        print(f"[WORKER] completed {task.id}")

        task_queue.task_done()

# =====================================
# STARTUP
# =====================================

@app.on_event("startup")
async def startup():

    print("=== AI CONTENT AUTOMATION RUNTIME ===")

    asyncio.create_task(worker())

# =====================================
# ROOT
# =====================================

@app.get("/")
def root():

    return {
        "status": "alive"
    }

# =====================================
# HEALTH
# =====================================

@app.get("/health")
def health():

    return {
        "kernel": "running",
        "queue_size": task_queue.qsize(),
        "tasks": len(task_store)
    }

# =====================================
# GENERATE SCRIPT
# =====================================

@app.post("/generate-script")
async def create_script(req: ScriptRequest):

    task = Task(
        "generate_script",
        req.dict()
    )

    task_store[task.id] = task

    await task_queue.put(task)

    return {
        "queued": True,
        "task": task.to_dict()
    }

# =====================================
# TASK STATUS
# =====================================

@app.get("/task/{task_id}")
def task_status(task_id: str):

    task = task_store.get(task_id)

    if not task:

        return {
            "error": "task not found"
        }

    return task.to_dict()

# =====================================
# LIST TASKS
# =====================================

@app.get("/tasks")
def tasks():

    return {
        "tasks": [
            task.to_dict()
            for task in task_store.values()
        ]
    }

# =====================================
# MAIN
# =====================================

if __name__ == "__main__":

    print("=== AI_OS_CONTENT_RUNTIME STARTING ===")

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8010,
        reload=False
    )