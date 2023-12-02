"""
Name:    company
Author:  ReddyFan
Date:    2023/4/2 09:45
Desc:  公司、企业业务处理
"""

from fastapi import APIRouter, Query
from starlette import status

from store.db.company import query_company_info, query_total_demand, query_company_info_list

router = APIRouter()


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    tags=["companies"],
)
def get_company_simple_info(
        page: int = Query(1),
        size: int = Query(20),
        searchInput: str = Query(None),
):
    """ 获取公司列表 """

    skip = 0 if page == 1 else page * size - 1
    print('search：', searchInput, skip)
    company_list, total = query_company_info_list(
        skip,
        size,
        searchInput if searchInput else r'[\s\S]*'
    )

    return {"data": company_list, "pagintion": {"page": page, "size": size, "total": total}}


@router.get(
    "/{company_id}",
    status_code=status.HTTP_200_OK,
    tags=["companies"],
)
def get_company_info(company_id: str):
    cp: dict = query_company_info(company_id)
    return {"data": {
        "company": cp
    }}


@router.get(
    "/{company_id}/totalDemand",
    status_code=status.HTTP_200_OK,
    tags=["companies"],
)
def get_total_demand(company_id: str):
    totalDemand = query_total_demand(company_id)
    return {"data": {
        "totalDemand": totalDemand
    }}
