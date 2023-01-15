from pydantic import BaseSettings

# to verify the environmental varriables, if it is configure under system varriable or not and type..
class Settings(BaseSettings):
    database_hostname: str 
    database_port: str ## because it goes in to url so string is required
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"


env_settings = Settings()