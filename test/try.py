# -*- coding: utf-8 -*-
# @Time    : 2023/2/10 19:53
# @Author  : Euclid-Jie
# @File    : try.py
import os
import pandas as pd
import pymongo
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def MongoClient(DBName, collectionName):
    # 连接数据库
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient[DBName]  # 数据库名称
    mycol = mydb[collectionName]  # 集合（表）
    return mycol


def get_data(page, fileFullName):
    header = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/61.0"
    }
    Url = "http://guba.eastmoney.com/list,600519,99_{}.html".format(page)
    response = requests.get(Url, headers=header, timeout=60)  # 使用request获取网页
    html = response.content.decode("utf-8", "ignore")  # 将网页源码转换格式为html
    soup = BeautifulSoup(html, features="lxml")  # 构建soup对象，"lxml"为设置的解析器
    data_list = soup.find_all("div", "articleh")
    num = len(data_list)
    out_df = pd.DataFrame()
    for item in data_list:
        try:
            data_json = get_data_json(item)
            # col.insert_one(data_json)
        except:
            num -= 1
            pass
    save_data(out_df, os.getcwd(), fileFullName)
    return num


def clear_str(str_raw):
    for pat in ["\n", " ", " ", "\r", "\xa0", "\n\r\n"]:
        str_raw = str_raw.replace(pat, "")
    return str_raw


def get_full_text(data_json):
    header = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/61.0"
    }
    if "caifuhao" in data_json["href"]:
        url = "https:" + data_json["href"]
        response = requests.get(url, headers=header, timeout=60)
        html = response.content.decode("utf-8", "ignore")  # 将网页源码转换格式为html
        soup = BeautifulSoup(html, features="lxml")  # 构建soup对象，"lxml"为设置的解析器
        try:
            data_json["full_text"] = soup.find("div", "article-body").get_text()
            return data_json
        except:
            return data_json

    elif "/new" in data_json["href"]:
        url = "http://guba.eastmoney.com" + data_json["href"]
        response = requests.get(url, headers=header, timeout=60)
        html = response.content.decode("utf-8", "ignore")  # 将网页源码转换格式为html
        soup = BeautifulSoup(html, features="lxml")  # 构建soup对象，"lxml"为设置的解析器
        data_json["full_text"] = clear_str(
            soup.find("div", {"id": "post_content"}).text
        )
        return data_json
    else:
        return data_json


def get_data_json(item):
    spans = item.find_all("span")
    data_json = {
        "阅读": spans[0].text,
        "评论": spans[1].text,
        "标题": spans[2].a["title"],
        "href": spans[2].a["href"],
        "作者": spans[3].a.text,
        "最后更新": spans[4].text,
    }

    return get_full_text(data_json)


def save_data(data_df, FileFullPath, FilePath):
    """
    轮子函数，用于存储数据，可实现对已存在文件的追加写入
    :param data_df: 目标数据
    :param FileFullPath: 全路径，包括文件名和后缀
    :param FilePath: 文件名，包括后缀
    :return:
    """
    FileFullPath = os.path.join(FileFullPath, FilePath)
    if os.path.isfile(FileFullPath):
        data_df.to_csv(
            FilePath, mode="a", header=False, index=False, encoding="utf_8_sig"
        )
    else:
        data_df.to_csv(
            FilePath, mode="w", header=True, index=False, encoding="utf_8_sig"
        )


if __name__ == "__main__":

    fileFullName = "茅台.csv"
    with tqdm(range(1, 60)) as t:
        for page in t:
            t.set_description("page:{}".format(page))  # 进度条左边显示信息
            writed_len = get_data(page, fileFullName)
            t.set_postfix({"状态": "已成功写入{}条".format(writed_len)})  # 进度条右边显示信息
