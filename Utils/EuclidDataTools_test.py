# -*- coding: utf-8 -*-
# @Time    : 2023/3/11 11:16
# @Author  : Euclid-Jie
# @File    : EuclidDataTools_test.py
import pandas as pd

from EuclidDataTools import *

if __name__ == "__main__":
    data = {"id": 123, "sex": "male", "age": "12", "job": "student"}
    # 1、CsvClient.insert_one
    myCol = CsvClient(subFolder="demoOut", FileName="demo1")
    myCol.insert_one(data)

    # 2、EuclidCsvTools.saveCsvFile
    df = pd.DataFrame([data])
    EuclidCsvTools(subFolder="demoOut", FileName="demo2.csv").saveCsvFile(
        df, append=False
    )
