"""
Name:    token
Author:  ReddyFan
Date:    2023/1/19 08:36
Desc:  
"""
from typing import Union

from pydantic import BaseModel


class TokenData(BaseModel):
    username: Union[str, None] = None


class Token(BaseModel):
    access_token: str
    token_type: str
