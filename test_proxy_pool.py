# 从数据库调用IP
import requests
def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").json()

def get_proxies_count() -> int:
    return requests.get("http://127.0.0.1:5010/count/").json()["count"]


# 删除数据库中IP
def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))


# 使用代理IP发起请求
def getResponse(URL, header):
    retry_count = 5
    proxy = get_proxy().get("proxy")
    while retry_count > 0:
        try:
            response = requests.get(URL, headers=header, timeout=60, proxies={"http": "http://{}".format(proxy)})
            # 使用代理访问
            return response
        except Exception:
            retry_count -= 1
            # 删除代理池中代理
            delete_proxy(proxy)
            return None

if __name__ == "__main__":
    # 测试代理IP
    print(get_proxies_count())
    print(get_proxy().get("proxy"))