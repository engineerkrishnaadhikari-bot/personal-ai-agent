from app.config import Settings


def test_default_settings() -> None:
    settings = Settings()

    assert settings.app_name == "Personal AI Agent"
    assert settings.app_version == "0.1.0"
    assert settings.environment == "development"
    assert settings.ollama_base_url == "http://127.0.0.1:11434"
    assert settings.ollama_model == "qwen3:1.7b"
    assert settings.ollama_timeout == 120.0

def test_custom_settings() -> None:
    settings = Settings(
        ollama_model="test-model",
        ollama_timeout=30.0,
    )

    assert settings.ollama_model == "test-model"
    assert settings.ollama_timeout == 30.0
