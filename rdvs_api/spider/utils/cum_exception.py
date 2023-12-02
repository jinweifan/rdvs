"""
Name:    cum_exception
Author:  ReddyFan
Date:    2023/2/13 21:37
Desc:  
"""


class NoProxyException(Exception):
    """ 未获取到代理异常 """

    def __init__(self, message):
        super().__init__(self)  # 初始化父类
        self.message = message

    def __str__(self):
        return self.message


class CUMException(Exception):
    """" 自定义异常 """

    def __init__(self, message):
        super().__init__(self)  # 初始化父类
        self.message = message

    def __str__(self):
        return self.message
