import redis
from config import RedisConfig


class RedisConnection:
    def __init__(self):
        self.redis_client = redis.StrictRedis(
            host=RedisConfig.HOST, port=RedisConfig.PORT,
            password=RedisConfig.PASSWORD, db=RedisConfig.DB)

    def get_client(self):
        return self.redis_client
