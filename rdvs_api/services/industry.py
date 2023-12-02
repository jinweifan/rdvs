"""
Name:    industry
Author:  ReddyFan
Date:    2023/4/4 14:41
Desc:  
"""
from fastapi import APIRouter
from starlette import status

from store.db.industry import query_industry_data

router = APIRouter()


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    tags=["industries"],
    # operation_id="some_specific_id_you_define"
)
def get_industries():
    industries = query_industry_data()
    return {'data': industries}
