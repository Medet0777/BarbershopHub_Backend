from slowapi import Limiter
from slowapi.util import get_remote_address


limiter = Limiter(key_func=get_remote_address)

DEFAULT_RATE_LIMIT = "30/minute"
HOURLY_RATE_LIMIT = "500/hour"
WRITE_RATE_LIMIT = "20/hour"
