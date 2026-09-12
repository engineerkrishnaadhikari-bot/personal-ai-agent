class AppError(Exception):
    """Base exception for expected application errors."""


class OllamaConnectionError(AppError):
    """Raised when Ollama cannot be reached."""


class OllamaRequestError(AppError):
    """Raised when Ollama returns an invalid or unsuccessful response."""


class OllamaResponseError(AppError):
    """Raised when Ollama returns an unexpected response."""
