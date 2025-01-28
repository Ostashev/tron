from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = "ТРОН"
    database_url: str = ""
    secret: str = "SECRET"
    api_root_path: str = ""
    backend_url: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
