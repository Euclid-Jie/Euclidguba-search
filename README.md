# 东方财富股吧数据采集
[![wakatime](https://wakatime.com/badge/user/b638b33f-0c9e-4408-b427-258fe0b24ad0/project/018e0f79-4bee-4fd1-8d86-55a20bee6528.svg)](https://wakatime.com/badge/user/b638b33f-0c9e-4408-b427-258fe0b24ad0/project/018e0f79-4bee-4fd1-8d86-55a20bee6528)

长期维护，欢迎issue，帮助完善代码

现有新旧两个版本，新版本要求高但是免费，旧版本要求不高，但是要使用付费代理(约1 `rmb`/小时)

1. 如果你仅会使用简答的python，对数据库并不了解，请使用老版本，程序下载[地址](https://github.com/Euclid-Jie/Euclidguba-search/releases/tag/archive)，详见[介绍](README_old.md)
2. 如果你有数据库基础（需要用到`redis`,`MongoDB`)，请使用新版本，直接往下读

## 程序特性

- [X] 可爬取热帖和全部，在 `main_class.get_data()`中设置 `url`
  - 热帖：https://guba.eastmoney.com/list,600519,99_1.html
  - 全部：https://guba.eastmoney.com/list,600519_1.html
- [x] 使用免费代理，亲测可以完成爬取任务
- [x] 仅爬取帖子`title`时，速度极快
- [x] `redis`异步多线程获取完整贴子内容

## 启动步骤

### 1. 获取代码

1. 第一种方式，如果你会使用`git`, 请直接`clone`

2. 第二种方式，下载源码，详见下图，点击 `Download ZIP` 既可下载，随即解压既可

   ![image-20240315122017995](https://euclid-picgo.oss-cn-shenzhen.aliyuncs.com/image/image-20240315122017995.png)

### 2. 配置环境

前置条件是安转并启动了`redis`,`mongo`,并将`redis`密码设置为123456，后续会添加这部分的操作说明

1. 安转代理池模块，再次感谢[作者](https://github.com/jhao104/proxy_pool)

   ```cmd
   git submodule update --init
   ```

2. 建议使用虚拟环境，并安装依赖

   ```cmd
   pip install -r requirements.txt
   ```

### 3. 启动程序

1. 启动代理池

    新开两个终端，第一个运行

    ```cmd
    cd .\proxy_pool\
    python proxyPool.py schedule 
    ```

    第二个运行

    ```cmd
    cd .\proxy_pool\
    python proxyPool.py server 
    ```

2. 启动`FullTextCrawler`

   新开终端，运行

   ```cmd
   python -m full_text_Crawler
   ```

3. 启动主程序

    在`main_class.py`中设置好参数，新开终端，运行

    ```
    python -m main_class
    ```

爬取成功的数据会在，`MongoDB.guba` 中，如有问题，请 [issue](https://github.com/Euclid-Jie/Euclidguba-search/issues/new)

## 附录

1. 爬取成功的数据截图

   ![image-20240315123641440](https://euclid-picgo.oss-cn-shenzhen.aliyuncs.com/image/image-20240315123641440.png)

2. 股吧页面截图

    ![](https://euclid-picgo.oss-cn-shenzhen.aliyuncs.com/image/202302161115850.png)
