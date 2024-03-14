from TreadCrawler import RedisClient
import configparser


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("setting.ini")
    redis_client = RedisClient(config=config)
    lines = [
        "/news,002611,1407434999.html",
        "/news,002611,1407434732.html",
        "/news,002611,1407434570.html",
        "/news,002611,1407432104.html",
        "/news,002611,1407428529.html",
        "/news,002611,1407428130.html",
        "/news,002611,1407427781.html",
        "/news,002611,1407425977.html",
        "/news,002611,1407424968.html",
        "/news,002611,1407424842.html",
        "/news,002611,1407421621.html",
        "/news,002611,1407420792.html",
        "/news,002611,1407417853.html",
        "/news,002611,1407416059.html",
        "/news,002611,1407415463.html",
        "/news,002229,1407912249.html",
    ]
    for i in lines:
        redis_client.add_url(i)
