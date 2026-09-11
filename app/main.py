from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.agent.core import PersonalAgent


app = FastAPI(
    title="Personal AI Agent",
    version="0.1.0",
)

agent = PersonalAgent()


class ChatRequest(BaseModel):
    prompt: str


@app.get("/health")
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "version": "0.1.0",
    }


@app.post("/chat")
def chat(request: ChatRequest) -> dict[str, str]:
    try:
        response = agent.ask(request.prompt)
        return {"response": response}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc