"""
Name:    job
Author:  ReddyFan
Date:    2023/4/2 15:27
Desc:  招聘数据
"""
from typing import Union

from fastapi import APIRouter, Query
from fastapi.params import Path
from starlette import status

from store.db.job import get_job_list, get_job

router = APIRouter()


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    tags=["jobs"],
    # operation_id="some_specific_id_you_define"
)
def get_job_info(
        page: int = Query(1),
        size: int = Query(20),
        industryQuery: str = Query(None),
        cityQuery: Union[str] = Query(None)
):
    skip = page * size - 1
    cityQuery = r'[\s\S]*' if not cityQuery or cityQuery == '全国' else cityQuery
    job_list, total = get_job_list(
        skip,
        size,
        industryQuery,
        cityQuery) if industryQuery else get_job_list(
        skip,
        size,
        cityQuery=cityQuery
    )
    return {"data": job_list, "pagintion": {"page": page, "size": size, "total": total}}


@router.get(
    "/{job_id}",
    status_code=status.HTTP_200_OK,
    tags=["jobs"],
    # operation_id="some_specific_id_you_define"
)
def get_single_job_detail(job_id: str = Path(...)):
    job = get_job(job_id)
    print('job: {}'.format(job))
    return {"data": {'job': job}}
