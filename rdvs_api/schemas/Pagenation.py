"""
Name:    Pagenation
Author:  ReddyFan
Date:    2023/4/2 16:33
Desc:  
"""
from models import BaseModel


class Pagenation(BaseModel):
    page: int
    size: int
    # // pageSizes: number[]
    total: int
