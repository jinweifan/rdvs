"""
Name:    closure
Author:  ReddyFan
Date:    2023/2/11 13:33
Desc:  
"""


def foo(fun):
    def inner( *args, **kwargs):
        if args[0]:
            fun( *args, **kwargs)
            print(args, kwargs)
        else:
            print("NO")

    return inner


@foo
def foo1( *args, **kwargs):
    print(*args)


if __name__ == '__main__':
    foo1(0, 2, a=3, b=4)
    print(repr('RUNOOB'))
    print(repr([0,1]))
    print(repr({"username":"reddy"}))
    print([0, 1])
    print({"username": "reddy"})
    print(str('RUNOOB'))
    print('RUNOOB')
# f = foo()
# f(0, 2, a=3, c=7)
# foo1(1,2)
