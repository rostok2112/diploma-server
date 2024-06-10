from redis.asyncio import Redis 
from environment import settings


redis_conn = Redis(port=settings.REDIS_PORT) #, password=settings.REDIS_PASSWORD
