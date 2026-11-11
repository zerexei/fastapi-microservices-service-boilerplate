from config import settings
from redis.asyncio import Redis

# Initialize the async Redis client
redis_client = Redis.from_url(
    str(settings.REDIS_URL),
    encoding="utf-8",
    decode_responses=True,
    protocol=2,
    socket_timeout=5.0,
    socket_connect_timeout=3.0,
    health_check_interval=30,
)