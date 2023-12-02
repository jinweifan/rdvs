"""
Name:    common
Author:  ReddyFan
Date:    2023/4/20 17:37
Desc:  
"""
from fastapi import APIRouter, Query
from starlette import status

from store.db.common import query_city, query_relation_content

router = APIRouter()


@router.get(
    "/allCity",
    status_code=status.HTTP_200_OK,
    tags=["common"],
)
def get_all_city():
    """ 获取公司列表 """
    city = query_city()
    return {'city': city}


@router.get(
    "/searchRelationContent",
    status_code=status.HTTP_200_OK,
    tags=["common"],
)
def search_relation_content(searchString: str = Query(...)):
    """ 获取搜索内容 """
    search_content = query_relation_content(searchString)
    print(search_content)
    search_content = [{'value': i.get('company_name')} for i in search_content]
    return {'data': search_content}
