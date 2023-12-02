from pprint import pprint

import elasticsearch

# 连接elasticsearch
es = elasticsearch.Elasticsearch(['http://182.43.196.45:9200/'])

# 定义搜索查询
search_query = {
    "query": {
        "bool": {
            "must": [
                {"match": {"Staff.staff_id": "fanjinwei"}}
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

# 执行搜索查询
search_results = es.search(index="staff_behavior_20230516_1", body=search_query)

# 从搜索结果中提取不同的文件数
distinct_files_count = search_results['aggregations']['distinct_files']['value']
pprint(search_results)
print("张三的账号一共接触过{}个不同的文件".format(distinct_files_count))
