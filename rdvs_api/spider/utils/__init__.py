"""
Name:    __init__.py
Author:  ReddyFan
Date:    2023/2/13 14:19
Desc:  
"""
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
print(BASE_DIR)
sys.path.append(BASE_DIR)


