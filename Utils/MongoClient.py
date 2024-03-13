# -*- coding: utf-8 -*-
# @Time    : 2023/2/9 23:26
# @Author  : Euclid-Jie
# @File    : MongoClient.py
import pymongo
import pandas as pd

__all__ = ["MongoClient", "read_mongo"]


def MongoClient(DBName, collectionName):
    # 连接数据库
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient[DBName]  # 数据库名称
    mycol = mydb[collectionName]  # 集合（表）
    return mycol


def read_mongo(DBName, collectionName, query=None, no_id=True):
    """
    Read from Mongo and Store into DataFrame
    :param DBName: mongoDB dataBase's name
    :param collectionName: mongoDB dataBase's collection's name
    :param query: a selection for data, demo: query = {"time": {"$gt": "2021-01-01"}}
    :param no_id: do not write _id column to data
    :return: pd.DataFrame
    """
    # Connect to MongoDB
    if query is None:
        query = {}
    col = MongoClient(DBName, collectionName)
    # Make a query to the specific DB and Collection
    cursor = col.find(query)
    # Expand the cursor and construct the DataFrame
    df = pd.DataFrame(list(cursor))
    # Delete the _id
    if no_id and "_id" in df:
        del df["_id"]
    return df.drop_duplicates()
