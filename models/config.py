from pydantic_settings import BaseSettings
from pydantic import SecretStr

class GlobalSettings(BaseSettings):
    # Bot token can be obtained via https://t.me/BotFather
    telegram_bot_token: SecretStr

    redis_url: SecretStr = SecretStr("redis://127.0.0.1:6379/0")

    log_json: bool = False
    log_level: str = "INFO"

    # Kafka
    kafka_conf_bootstrap_server: str = "127.0.0.1:9092"
    kafka_conf_auto_offset_reset: str = "earliest"
