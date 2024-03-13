# -*- coding: utf-8 -*-
# @Time    : 2023/3/11 10:45
# @Author  : Euclid-Jie
# @File    : EuclidDataTools.py
import pandas as pd
from pathlib import Path
from typing import Optional, Union

__all__ = ["EuclidCsvTools", "CsvClient"]


class EuclidCsvTools:
    """
    this class include tools used to precess csv file
    """

    def __init__(
        self,
        subFolder: Optional[Union[str, Path]] = None,
        FileName: str = "DemoOut.csv",
    ):
        # para init
        if subFolder:
            self.subFolder = Path(subFolder)

        assert FileName.endswith(".csv"), "file name must end with .csv"
        self.FileName = FileName
        self.path_clear()

    def path_clear(self):
        """
        get the full folder path and full file path
        :return:
        """
        if self.subFolder:
            self.FullFolderPath = Path.cwd().joinpath(self.subFolder)
            self.FullFolderPath.mkdir(parents=True, exist_ok=True)
            self.FullFilePath = (
                Path.cwd().joinpath(self.subFolder).joinpath(self.FileName)
            )
        else:
            self.FullFolderPath = Path.cwd()
            self.FullFolderPath.mkdir(parents=True, exist_ok=True)
            self.FullFilePath = Path.cwd().joinpath(self.FileName)
        print("文件将存储在: {}".format(self.FullFilePath))

    def saveCsvFile(self, df, append=False):
        """
        save data to csv
        :param df: pd.DataFrame
        :param append: True(append save) or False(overwrite)
        :return:
        """
        if append and self.FullFilePath.exists():
            self.writeDf2Csv(df, self.FullFilePath)
        else:
            df.to_csv(self.FullFilePath, encoding="utf_8_sig", index=False)

    @classmethod
    def writeDf2Csv(cls, df: pd.DataFrame, FullFilePath):
        if FullFilePath.exists():
            # write after a exist file without header
            df.to_csv(
                FullFilePath, mode="a", encoding="utf_8_sig", header=False, index=False
            )
        else:
            # write out a new file with header
            df.to_csv(
                FullFilePath, mode="w", encoding="utf_8_sig", header=True, index=False
            )


class CsvClient(EuclidCsvTools):
    def __init__(
        self,
        subFolder: Optional[Union[str, Path]] = None,
        FileName: str = "DemoOut.csv",
    ):
        """
        :param subFolder:
        :param FileName:
        """
        if ~FileName.endswith(".csv") and "." not in FileName:
            FileName = FileName + ".csv"
        else:
            raise ValueError("FileName must end with .csv or not contain '.'")
        super().__init__(subFolder=subFolder, FileName=FileName)

    def insert_one(self, data: Union[dict, pd.DataFrame]):
        if isinstance(data, dict):
            data = pd.DataFrame([data])
        elif isinstance(data, pd.DataFrame):
            pass
        else:
            raise TypeError("传入参数仅支出dict和pd.DataFrame")
        self.saveCsvFile(df=data, append=True)
