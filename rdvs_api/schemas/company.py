"""
Name:    company
Author:  ReddyFan
Date:    2023/4/2 11:30
Desc:  
"""
from pydantic import BaseModel


class CompanySimpleInfoResponse(BaseModel):
    _id: str
    enterprise_name: str
    legal_person: str
    registered_capital: str
