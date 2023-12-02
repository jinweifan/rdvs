"""
Name:    __init__
Author:  ReddyFan
Date:    2023/2/17 22:35
Desc:  
"""
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
print(BASE_DIR)
sys.path.append(BASE_DIR)