import redis
from config import RedisConfig


class RedisConnection:
    def __init__(self):
        self.redis_client = redis.StrictRedis(
            host=RedisConfig.HOST, port=RedisConfig.PORT,
            password=RedisConfig.PASSWORD, db=RedisConfig.DB)

        if not self.redis_client.exists('gallery'):
            self.redis_client.lpush('gallery', 'initial_value')

    def get_client(self):
        return self.redis_client
