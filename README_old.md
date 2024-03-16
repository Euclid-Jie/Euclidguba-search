# 东方财富股吧数据采集

长期维护，欢迎issue，帮助完善代码

## 程序特性

- [X] 可爬取热帖和全部，在 `def get_data()`中设置 `url`
  - 热帖：https://guba.eastmoney.com/list,600519,99_1.html
  - 全部：https://guba.eastmoney.com/list,600519_1.html
- [X] 需要使用IP代理池，推荐一个简单易用的代理：[快代理](https://www.kuaidaili.com/?ref=mes9ujq5wnrn)
- [X] Excel(csv)和MongoDB两种写入方式
- [X] retry机制，失败直接在之前的page和num上进行重新爬取，注：一个page 有80条帖子[80个num]

## 修改*main*相关参数即可使用

- 股票代码，起始页码，终止页码，如果使用Excel(csv)方式写入，请设置 `“MongoDB=False”`

```python
demo = guba_comments('601985', pages_start=1321, pages_end=1480, MongoDB=True)
```

- 代理服务器域名网址，端口，推荐使用：[快代理](https://www.kuaidaili.com/?ref=mes9ujq5wnrn)，隧道代理按量计费一小时1元钱
  > 如果直接使用[快代理](https://www.kuaidaili.com/?ref=mes9ujq5wnrn)，此链接注册并成功消费，我会收到5%~15%的返现，可以[联系我](Ouweijie123@outlook.com)退还，相当于折扣
  >

```
proxies = {'http': 'http://y889.kdltps.com:15818', 'https': 'http://y889.kdltps.com:15818'}
```

![](https://euclid-picgo.oss-cn-shenzhen.aliyuncs.com/image/202302161115850.png)
