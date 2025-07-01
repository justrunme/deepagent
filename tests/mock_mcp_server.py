from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()

class Task(BaseModel):
    command: str

@app.get("/capabilities")
def get_capabilities():
    return {
        "name": "mock-mcp",
        "commands": ["echo", "translate"],
        "requires_auth": False
    }

@app.post("/execute")
def execute_task(task: Task, request: Request):
    return {"result": f"Executed: {task.command}"}