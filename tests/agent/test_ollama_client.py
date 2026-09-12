from unittest.mock import Mock, patch

import httpx
import pytest

from app.agent.ollama_client import OllamaClient
from app.exceptions import (
    OllamaConnectionError,
    OllamaRequestError,
    OllamaResponseError,
)


def test_empty_prompt_is_rejected() -> None:
    client = OllamaClient()

    with pytest.raises(ValueError, match="Prompt cannot be empty"):
        client.chat("   ")


@patch("app.agent.ollama_client.httpx.post")
def test_connection_error(mock_post: Mock) -> None:
    mock_post.side_effect = httpx.ConnectError("connection failed")

    client = OllamaClient()

    with pytest.raises(
        OllamaConnectionError,
        match="Unable to connect to Ollama",
    ):
        client.chat("Hello")


@patch("app.agent.ollama_client.httpx.post")
def test_timeout_error(mock_post: Mock) -> None:
    mock_post.side_effect = httpx.TimeoutException("timeout")

    client = OllamaClient()

    with pytest.raises(
        OllamaConnectionError,
        match="timed out",
    ):
        client.chat("Hello")


@patch("app.agent.ollama_client.httpx.post")
def test_http_error(mock_post: Mock) -> None:
    response = Mock()
    response.is_error = True
    response.status_code = 500
    mock_post.return_value = response

    client = OllamaClient()

    with pytest.raises(
        OllamaRequestError,
        match="HTTP 500",
    ):
        client.chat("Hello")


@patch("app.agent.ollama_client.httpx.post")
def test_invalid_json(mock_post: Mock) -> None:
    response = Mock()
    response.is_error = False
    response.json.side_effect = ValueError("invalid json")
    mock_post.return_value = response

    client = OllamaClient()

    with pytest.raises(
        OllamaResponseError,
        match="invalid JSON",
    ):
        client.chat("Hello")


@patch("app.agent.ollama_client.httpx.post")
def test_invalid_response_structure(mock_post: Mock) -> None:
    response = Mock()
    response.is_error = False
    response.json.return_value = {"unexpected": "data"}
    mock_post.return_value = response

    client = OllamaClient()

    with pytest.raises(
        OllamaResponseError,
        match="Unexpected response",
    ):
        client.chat("Hello")
