"""
Name:    test_decorate
Author:  ReddyFan
Date:    2023/2/11 12:50
Desc:  
"""

# from builtins import function
import function


def decorate(fun):
    print("running decorate()")

    # fun()


# @decorate
# def target():
#     print("running target()")
#
#
# # foo = decrate()
#
#
def deco(func: function):
    def inner():
        print("running inner()")

    return inner


@deco
def target():
    print("running target()")


if __name__ == '__main__':
    # print(type(target))
    target()
