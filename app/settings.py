from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    use_local_ollama: str
    ollama_llm_model: str
    google_api_key: str
    google_llm_model: str
    use_aws_bedrock: str
    aws_region: str
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_session_token: str
    dynamodb_table: str


    class Config:
        model_config = SettingsConfigDict(env_file=".env")