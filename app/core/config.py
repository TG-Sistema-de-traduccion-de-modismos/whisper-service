from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = "whisper-service"
    HOST: str = "0.0.0.0"
    PORT: int = 8003

    MODEL_SERVICE_URL: str = "http://whisper-model:8004"  
    REQUEST_TIMEOUT: int = 300

    SAMPLE_RATE: int = 16000
    CHANNELS: int = 1

    class Config:
        env_file = ".env"

settings = Settings()
