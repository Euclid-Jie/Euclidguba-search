# 东方财富股吧数据采集

[![wakatime](https://wakatime.com/badge/user/b638b33f-0c9e-4408-b427-258fe0b24ad0/project/018e0f79-4bee-4fd1-8d86-55a20bee6528.svg)](https://wakatime.com/badge/user/b638b33f-0c9e-4408-b427-258fe0b24ad0/project/018e0f79-4bee-4fd1-8d86-55a20bee6528)

长期维护，欢迎issue，帮助完善代码

由于近期无免费代理可用，本项目恢复到使用付费代理池，推荐使用[*快代理*](https://www.kuaidaili.com/?ref=mes9ujq5wnrn)

在启动本项目前，希望你已经安装了`MongoDB`、`redis`，这两个数据库会使得本项目更易于使用，展开来说：

1. 如果你没有安装`redis`，你仍可以使用本项目，但是无法获取帖子的详情，只能获取标题
2. 如果你没有安装`MongoDB`，你仍可以使用本项目，因为本项目支持写入csv文件
3. 很遗憾，尽管你安装了`redis`，但是没有安装`MongoDB`，那你依旧无无法获取帖子的详情，只能获取标题
4. 很遗憾，尽管你安装了`MongoDB`，但是没有安装`redis`，那你依旧无无法获取帖子的详情，只能获取标题
5. 幸运的是，如果你两个都没有，你仍可以使用本项目，因为你仍旧可以获得仅有标题的csv文件，心软的我为你特别准备了`simple_main.py`

## 程序特性

- [X] 可爬取热帖和全部，在 `main_class.get_data()`中设置 `url`
  - 热帖：https://guba.eastmoney.com/list,600519,99_1.html
  - 全部：https://guba.eastmoney.com/list,600519_1.html
- ~~使用免费代理，亲测可以完成爬取任务~~ (24年由于免费代理库的作者不更新，本项目也只能转向付费代理，sorry)
- [X] 仅爬取帖子 `title`时，速度极快
- [x] `redis`异步多线程获取完整贴子内容
- [ ] 指定时间区间的爬取
- [ ] docker部署（暂时还不会，等我搞完这个，你们就不需要学`redis`和`mongoDB`了)
- [ ] UI界面（多半不会有，希望有大佬帮我一把）

## 启动步骤

### 1. 获取代码

1. 第一种方式，如果你会使用 `git`, 请直接 `clone`
2. 第二种方式，下载源码，详见下图，点击 `Download ZIP` 既可下载，随即解压既可

   ![image-20240315122017995](https://euclid-picgo.oss-cn-shenzhen.aliyuncs.com/image/image-20240315122017995.png)

### 2. 配置环境

前置条件是安转并启动了 `redis`,`mongo`,并将 `redis`密码设置为123456，后续会添加这部分的操作说明

建议使用虚拟环境，并安装依赖

```cmd
pip install -r requirements.txt
```

### 3.编写配置

本项目非常人性化地设置了配置文件，`setting.ini`

- `Redis`部分为用于评论详情爬取的后台程序`FullTextCrawler`
- `proxies`是使用[*快代理*](*https://www.kuaidaili.com/?ref=mes9ujq5wnrn*)获取的代理tunnel
- `ThreadCrawler`部分是用于评论详情爬取的后台程序`FullTextCrawler`的线程池数量设置
- `mainClass`是主程序的参数

```ini
[Redis]
redis_host = localhost
redis_port = 6379
redis_password = 
redis_db = 0
redis_key = urls

[proxies]
tunnel = d476.kdltps.com:15818

[ThreadCrawler]
num_threads = 32

[mainClass]
pages_start = 0
pages_end = 100
```

### 4.启动程序

1. 启动 `FullTextCrawler`，如果没有`redis`, 跳过次步骤

   新开终端，运行

   ```cmd
   python -m full_text_Crawler
   ```
2. 启动主程序

   在 `main_class.py`中设置好参数，新开终端，运行

   ```
   python -m main_class
   ```

爬取成功的数据会在，`MongoDB.guba` 中，如有问题，请 [issue](https://github.com/Euclid-Jie/Euclidguba-search/issues/new)

## 附录

1. 爬取成功的数据截图

   ![image-20240315123641440](https://euclid-picgo.oss-cn-shenzhen.aliyuncs.com/image/image-20240315123641440.png)
2. 股吧页面截图

   ![](https://euclid-picgo.oss-cn-shenzhen.aliyuncs.com/image/202302161115850.png)
