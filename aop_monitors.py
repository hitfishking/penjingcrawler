# coding: utf-8
# ------------------------------------------
# AOP wrapper 包裹函数；装饰逻辑，与标准逻辑，处于彼此正交的逻辑空间中；
# timer计时逻辑；
# ------------------------------------------
import datetime

def timer(func):
    def wrapper(*args, **kw):
        t1 = datetime.datetime.now()
        rs = func(*args, **kw)
        t2 = datetime.datetime.now()
        print("函数%s共耗时%d秒." % (func.__name__, (t2 - t1).seconds))
        return rs
    return wrapper

