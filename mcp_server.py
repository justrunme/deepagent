from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()

class Task(BaseModel):
    command: str

@app.get("/capabilities")
def capabilities():
    return {
        "name": "shell-mcp",
        "commands": ["echo", "ls", "translate", "ping"],
        "requires_auth": True
    }

@app.post("/execute")
def execute(task: Task, request: Request):
    if "Authorization" not in request.headers:
        return {"error": "Unauthorized"}, 401
    return {"result": f"Executed: {task.command}"}