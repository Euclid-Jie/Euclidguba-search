import redis
import threading
import configparser

__all__ = ["RedisClient"]


class RedisClient:
    def __init__(self, config: configparser.ConfigParser):
        self.redis_client = redis.StrictRedis(
            host=config.get("Redis", "redis_host"),
            port=config.getint("Redis", "redis_port"),
            db=config.getint("Redis", "redis_db"),
            password=config.get("Redis", "redis_password"),
        )
        self.lock = threading.Lock()
        self.redis_key = config.get("Redis", "redis_key")

    def add_url(self, url) -> None:
        with self.lock:
            self.redis_client.lpush(self.redis_key, url)

    def get_url(self) -> str:
        with self.lock:
            url = self.redis_client.rpop(self.redis_key)
        if url:
            return url.decode("utf-8")
        else:
            return None

    def __len__(self) -> int:
        return self.redis_client.llen(self.redis_key)
