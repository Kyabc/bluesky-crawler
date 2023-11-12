from loguru import logger
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    data_dir: str
    logger_rotation: str

    class Config:
        env_prefix = "BLUESKY_"
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
logger.info(f"The environment variable has been set as {settings}")
