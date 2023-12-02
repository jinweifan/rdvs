"""
Name:    action_scope
Author:  ReddyFan
Date:    2023/2/11 13:19
Desc:  
"""
from dis import dis

b = 3


def foo(a):
    print(a)
    global b
    print(b)
    # nonlocal b
    b = 7
    print(b)


if __name__ == '__main__':
    foo(2)
    print(b)
    dis(foo)
