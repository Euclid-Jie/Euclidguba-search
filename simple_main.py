# -*- coding: utf-8 -*-
# @Time    : 2023/2/11 21:27
# @Author  : Euclid-Jie
# @File    : main_class.py
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import logging
from retrying import retry
from typing import Optional, Union
from concurrent.futures import ThreadPoolExecutor, as_completed
from Utils.EuclidDataTools import CsvClient
import configparser


class guba_comments:
    """
    this class is designed for get hot comments for guba, have two method which can be set at def get_data()
    1、all: https://guba.eastmoney.com/list,600519_1.html, secCode: 600519, page: 1
    2、hot: https://guba.eastmoney.com/list,600519,99_1.html secCode: 600519, page: 1

    because to the ip control, this need to set proxies pools
    by using proxies https://www.kuaidaili.com/usercenter/overview/, can solve this problem

    Program characteristics:
        1、default write data to mongoDB, by init "MogoDB=False", can switch to write data to csv file
        2、Use retry mechanism, once rise error, the program will restart at the least page and num (each page has 80 num)

    """

    failed_proxies = {}
    proxy_fail_times_treshold = 3

    def __init__(
        self,
        config: configparser.ConfigParser,
        secCode: Union[str, int],
        pages_start: int = 0,
        pages_end: int = 100,
        num_start: int = 0,
        collectionName: Optional[str] = None,
    ):
        # param init
        if isinstance(secCode, int):
            # 补齐6位数
            self.secCode = str(secCode).zfill(6)
        elif isinstance(secCode, str):
            self.secCode = secCode
        self.pages_start = pages_start
        self.pages_end = pages_end
        self.num_start = num_start
        self._year = pd.Timestamp.now().year

        # rewrite the secCode setting
        if config.has_option("mainClass", "secCode"):
            self.secCode = config.get("mainClass", "secCode")
            print(
                f"secCode has been overridden by {self.secCode} in the configuration file."
            )
        if config.has_option("mainClass", "pages_start"):
            self.pages_start = int(config.get("mainClass", "pages_start"))
            print(
                f"pages_start has been overridden by {self.pages_start} in the configuration file."
            )
        if config.has_option("mainClass", "pages_end"):
            self.pages_end = int(config.get("mainClass", "pages_end"))
            print(
                f"pages_end has been overridden by {self.pages_end} in the configuration file."
            )
        if config.has_option("mainClass", "collectionName"):
            collectionName = config.get("mainClass", "collectionName")
            print(
                f"collectionName has been overridden by {collectionName} in the configuration file."
            )

        collectionName = collectionName if collectionName else self.secCode
        self.col = CsvClient("guba", collectionName)

        # log setting
        log_format = "%(levelname)s %(asctime)s %(filename)s %(lineno)d %(message)s"
        logging.basicConfig(filename="test.log", format=log_format, level=logging.INFO)

    @staticmethod
    def clear_str(str_raw):
        for pat in ["\n", " ", " ", "\r", "\xa0", "\n\r\n"]:
            str_raw.strip(pat).replace(pat, "")
        return str_raw

    @staticmethod
    def run_thread_pool_sub(target, args, max_work_count):
        with ThreadPoolExecutor(max_workers=max_work_count) as t:
            res = [t.submit(target, i) for i in args]
            return res

    @retry(stop_max_attempt_number=5)  # 最多尝试5次
    def get_soup_form_url(self, url: str) -> BeautifulSoup:
        """
        get the html content used by requests.get
        :param url:
        :return: BeautifulSoup
        """
        response = requests.get(
            url, headers=self.header, timeout=10, proxies=self.proxies
        )  # 使用request获取网页
        html = response.content.decode("utf-8", "ignore")
        soup = BeautifulSoup(html, features="lxml")
        return soup

    def get_data_json(self, item):
        """
        get the special keys from item, in this the project,
        the keys con be "阅读"、"评论"、……

        by use the get_full_text, the return json data will contain full_text
        :param item:
        :return: json data contains full_text
        """

        tds = item.find_all("td")
        data_json = {
            "阅读": tds[0].text,
            "评论": tds[1].text,
            "标题": tds[2].a.text,
            "href": tds[2].a["href"],
            "作者": tds[3].a.text,
            "最后更新": tds[4].text,
        }
        if "caifuhao" in data_json["href"]:
            self._year = int(data_json["href"].split("/")[-1][0:4])
        dt = pd.to_datetime(str(self._year) + "-" + data_json["最后更新"])
        if dt > pd.Timestamp.now():
            self._year -= 1
            dt = pd.to_datetime(str(self._year) + "-" + data_json["最后更新"])
        data_json["最后更新"] = dt
        return data_json

    def get_data(self, page):
        """
        process to deal the single page's data
        :param page: the page needed to be processed
        :return:
        """
        # Url = "http://guba.eastmoney.com/list,{},99_{}.html".format(self.secCode, page)
        Url = "http://guba.eastmoney.com/list,{},f_{}.html".format(self.secCode, page)
        soup = self.get_soup_form_url(Url)
        data_list = soup.find_all("tr", "listitem")

        # 开启并行获取data_json
        res = self.run_thread_pool_sub(self.get_data_json, data_list, max_work_count=12)
        for future in as_completed(res):
            data_json = future.result()
            self.col.insert_one(data_json)
            self.t.set_postfix(
                {
                    "状态": "已写num:{}".format(self.num_start),
                }
            )  # 进度条右边显示信息
            self.num_start += 1

    def main(self):
        with tqdm(range(self.pages_start, self.pages_end)) as self.t:
            for page in self.t:
                self.t.set_description("page:{}".format(page))  # 进度条左边显示信息
                self.get_data(page)
                self.num_start = 0
                self.pages_start += 1


if __name__ == "__main__":
    # config
    config = configparser.ConfigParser()
    config.read("setting.ini", encoding="utf-8")
    # init
    demo = guba_comments(
        config=config,
        secCode="002611",
        collectionName="东方精工",
    )

    # setting
    header = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/61.0",
    }
    demo.header = header
    tunnel = config.get("proxies", "tunnel")
    demo.proxies = {
        "http": "http://%(proxy)s/" % {"proxy": tunnel},
        "https": "http://%(proxy)s/" % {"proxy": tunnel},
    }
    # run and get data
    demo.main()
