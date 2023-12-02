"""
Name:    schemes
Author:  ReddyFan
Date:    2023/2/12 17:51
Desc:  
"""
from typing import List, Union

from pydantic import BaseModel


class Job(BaseModel):
    job_name: str
    job_area: str
    salary: str
    job_experience: str
    job_degree: str
    skill_list: Union[List[str], None]
    welfare_list: Union[List[str], None]

    boss_name: str
    boss_title: str
    brand_logo: str
    brand_name: str
    brand_scale_name: str
    brand_stage_name_obj: str
    brand_stage_name: Union[str, None]

    detail_url: str
    company_detail_url: str

