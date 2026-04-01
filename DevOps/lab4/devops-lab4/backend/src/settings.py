from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERVER_ADDR: str = "0.0.0.0"
    SERVER_PORT: int = 8080

    DB_ADDR: str
    DB_USER: str
    DB_PASSWORD: str
    DB_PORT: int = 5432
    DB_NAME: str
    
settings = Settings()