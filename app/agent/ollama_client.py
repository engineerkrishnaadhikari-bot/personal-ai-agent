import logging
from typing import Any

import httpx

from app.config import get_settings
from app.exceptions import (
    OllamaConnectionError,
    OllamaRequestError,
    OllamaResponseError,
)

logger = logging.getLogger(__name__)


class OllamaClient:
    """Client for communicating with a local Ollama server."""

    def __init__(
        self,
        base_url: str | None = None,
        model: str | None = None,
        timeout: float | None = None,
    ) -> None:
        settings = get_settings()

        self.base_url = (
            base_url or settings.ollama_base_url
        ).rstrip("/")
        self.model = model or settings.ollama_model
        self.timeout = timeout or settings.ollama_timeout

    def chat(self, prompt: str) -> str:
        """Send a prompt to Ollama and return the assistant response."""

        if not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        payload: dict[str, Any] = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            "stream": False,
        }

        logger.info("Sending request to Ollama model=%s", self.model)

        try:
            response = httpx.post(
                f"{self.base_url}/api/chat",
                json=payload,
                timeout=self.timeout,
            )
        except httpx.ConnectError as exc:
            logger.error("Unable to connect to Ollama: %s", exc)
            raise OllamaConnectionError(
                "Unable to connect to Ollama."
            ) from exc
        except httpx.TimeoutException as exc:
            logger.error("Ollama request timed out: %s", exc)
            raise OllamaConnectionError(
                "Ollama request timed out."
            ) from exc
        except httpx.HTTPError as exc:
            logger.error("Ollama HTTP error: %s", exc)
            raise OllamaRequestError(
                "Ollama request failed."
            ) from exc

        if response.is_error:
            logger.error(
                "Ollama returned HTTP %s",
                response.status_code,
            )
            raise OllamaRequestError(
                f"Ollama returned HTTP {response.status_code}."
            )

        try:
            data = response.json()
        except ValueError as exc:
            logger.error("Ollama returned invalid JSON")
            raise OllamaResponseError(
                "Ollama returned invalid JSON."
            ) from exc

        try:
            content = data["message"]["content"]
        except (KeyError, TypeError) as exc:
            logger.error("Unexpected Ollama response format")
            raise OllamaResponseError(
                "Unexpected response from Ollama."
            ) from exc

        if not isinstance(content, str) or not content.strip():
            logger.error("Ollama returned an empty response")
            raise OllamaResponseError(
                "Ollama returned an empty response."
            )

        logger.info("Ollama response received successfully")

        return content