"""
Name:    el2
Author:  ReddyFan
Date:    2023/5/23 10:59
Desc:  
"""

import json

import requests

# Elasticsearch服务器地址
url = "http://182.43.196.45:9200"

# 索引名称
index_name = "staff_behavior_20230516_1"

# 查询语句
query = {
    "query": {
        "bool": {
            "must": [
                {
                    "match": {
                        "Staff.staff_id": "zhangsan"
                    }
                }
            ]
        }
    },
    "aggs": {
        "distinct_files": {
            "cardinality": {
                "field": "Data.data_name"
            }
        }
    }
}

# 发送查询请求
response = requests.post(url + "/" + index_name + "/_search", json=query)

# 解析结果
result = json.loads(response.text)
distinct_files = result["aggregations"]["distinct_files"]["value"]

print("张三的账号一共接触过{}个不同的文件".format(distinct_files))
# 张三的账号一共接触过42个不同的文件
