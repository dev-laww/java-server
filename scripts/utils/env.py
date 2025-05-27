from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(BaseSettings):
    docker_path: str

    model_config = SettingsConfigDict(env_file='.env')


environment = Environment()
