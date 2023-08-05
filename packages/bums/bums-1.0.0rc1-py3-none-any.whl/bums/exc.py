import time
from functools import wraps


def try_except(e=Exception, default=None):
    """ 过滤函数异常装饰器
    :param e: 异常或者异常组
    :param default: 异常后函数的返回值
    """
    # 异常外层数据结构调整为元组
    if isinstance(e, (list, tuple, set)):
        e = tuple(e)

    def wrapper(func):

        @wraps(func)
        def inner(*args, **kwargs):
            try:
                res = func(*args, **kwargs)
            except e:
                return default
            return res

        return inner

    return wrapper


def retry_except(e=Exception, retries: int = 0, retry_delay: int = 0, default=None):
    """ 异常重试装饰器
    :param e: 异常组
    :param retries: 重试次数（必传参数，不设置无限重试）
    :param retry_delay: 失败重试间隔时（单位秒）
    :param default: 失败后的默认值
    """

    # 异常外层数据结构调整为元组
    if isinstance(e, (list, tuple, set)):
        e = tuple(e)

    def wrapper(func):

        @wraps(func)
        def inner(*args, **kwargs):
            for retry in range(retries + 1):
                try:
                    res = func(*args, **kwargs)
                except e:
                    if retry == retries:
                        return default
                    else:
                        time.sleep(retry_delay)
                        continue
                return res

        return inner

    return wrapper
