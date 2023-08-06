#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2022/10/29 19:00
Desc: 申万宏源研究-指数系列
https://www.swhyresearch.com/institute_sw/allIndex/releasedIndex
"""
import math

import pandas as pd
import requests
from tqdm import tqdm


def index_realtime_sw(symbol: str = "二级行业"):
    """
    申万宏源研究-指数系列
    https://www.swhyresearch.com/institute_sw/allIndex/releasedIndex
    :param symbol: choice of {"市场表征", "一级行业", "二级行业", "风格指数"}
    :type symbol: str
    :return: 指数系列实时行情数据
    :rtype: pandas.DataFrame
    """
    url = "https://www.swhyresearch.com/institute-sw/api/index_publish/current/"
    params = {"page": "1", "page_size": "50", "indextype": symbol}
    r = requests.get(url, params=params)
    data_json = r.json()
    total_num = data_json["data"]["count"]
    total_page = math.ceil(total_num / 50)
    big_df = pd.DataFrame()
    for page in tqdm(range(1, total_page + 1), leave=False):
        params.update({"page": page})
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["data"]["results"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)
    big_df.columns = [
        "指数代码",
        "指数名称",
        "昨收盘",
        "今开盘",
        "成交额",
        "最高价",
        "最低价",
        "最新价",
        "成交量",
    ]
    big_df = big_df[
        [
            "指数代码",
            "指数名称",
            "昨收盘",
            "今开盘",
            "最新价",
            "成交额",
            "成交量",
            "最高价",
            "最低价",
        ]
    ]
    big_df["昨收盘"] = pd.to_numeric(big_df["昨收盘"])
    big_df["今开盘"] = pd.to_numeric(big_df["今开盘"])
    big_df["最新价"] = pd.to_numeric(big_df["最新价"])
    big_df["成交额"] = pd.to_numeric(big_df["成交额"])
    big_df["成交量"] = pd.to_numeric(big_df["成交量"])
    big_df["最高价"] = pd.to_numeric(big_df["最高价"])
    big_df["最低价"] = pd.to_numeric(big_df["最低价"])
    return big_df


if __name__ == "__main__":
    index_realtime_sw_df = index_realtime_sw(symbol="市场表征")
    print(index_realtime_sw_df)
