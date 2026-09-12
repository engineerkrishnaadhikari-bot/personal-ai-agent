import logging

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.agent.core import PersonalAgent
from app.exceptions import (
    OllamaConnectionError,
    OllamaRequestError,
    OllamaResponseError,
)
from app.logging.setup import configure_logging

configure_logging()

logger = logging.getLogger(__name__)

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
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except OllamaConnectionError as exc:
        logger.warning("Ollama connection problem: %s", exc)
        raise HTTPException(
            status_code=503,
            detail="Local AI service is unavailable.",
        ) from exc

    except OllamaRequestError as exc:
        logger.error("Ollama request problem: %s", exc)
        raise HTTPException(
            status_code=502,
            detail="Local AI service request failed.",
        ) from exc

    except OllamaResponseError as exc:
        logger.error("Ollama response problem: %s", exc)
        raise HTTPException(
            status_code=502,
            detail="Local AI service returned an invalid response.",
        ) from exc