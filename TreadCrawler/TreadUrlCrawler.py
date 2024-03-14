import threading
import requests
import configparser
from TreadCrawler.RedisClient import RedisClient


class ThreadUrlCrawler:
    def __init__(
        self,
    ):
        config = configparser.ConfigParser()
        config.read("setting.ini")
        self.redis_client: RedisClient = RedisClient(config=config)
        self.lock = threading.Lock()
        self.redis_key = config.get("Redis", "redis_key")
        self.num_threads = config.getint("ThreadCrawler", "num_threads")
        self.threads = []
        self.stop_crawling = threading.Event()

    def crawl(self, url) -> bool:
        raise NotImplementedError("Subclasses must implement crawl method")

    def _worker(self):
        while not self.stop_crawling.is_set():
            with self.lock:
                url = self.redis_client.get_url()
            if url:
                if self.crawl(url):
                    pass
                else:
                    with self.lock:
                        self.redis_client.add_url(url)

    def start(self):
        for _ in range(self.num_threads):
            t = threading.Thread(target=self._worker)
            t.daemon = True
            t.start()
            self.threads.append(t)

        for t in self.threads:
            t.join()

        # 打印剩余未爬取URL的数量
        print(f"Remaining URLs: {self.redis_client.__len__()}")

    def stop(self):
        self.stop_crawling.set()


# Example subclass of ThreadUrlCrawler
class MyThreadCrawler(ThreadUrlCrawler):
    def crawl(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(f"Successfully crawled: {url}")
                return True
            else:
                print(f"Failed to crawl: {url}")
                return False
        except Exception as e:
            print(f"Exception while crawling {url}: {e}")
            return False
