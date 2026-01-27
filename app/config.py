from pydantic_settings import BaseSettings
from pydantic import computed_field
import os


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    # DB_URL: str

    class Config:
        env_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")

    @computed_field
    @property
    def DB_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

stgs = Settings()
print(stgs.DB_URL)