from src.config import settings

broker_url = settings.redis_url
result_backend = settings.redis_url
broker_connection_retry_on_startup = True
