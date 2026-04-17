import redis.asyncio as redis
from app.config import config

redis_client = redis.from_url(config.REDIS_URL, decode_responses=True)

async def get_redis():
    return redis_client