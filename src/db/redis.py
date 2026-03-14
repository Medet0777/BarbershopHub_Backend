import aioredis

from src.config import settings

JTI_EXPIRY = 3600  # 1 hour

token_blocklist = aioredis.StrictRedis(
    host=settings.redis_host,
    port=settings.redis_port,
    db=0,
)


async def add_jti_to_blocklist(jti: str) -> None:
    await token_blocklist.set(name=jti, value="", ex=JTI_EXPIRY)


async def token_in_blocklist(jti: str) -> bool:
    jti_value = await token_blocklist.get(jti)
    return jti_value is not None
