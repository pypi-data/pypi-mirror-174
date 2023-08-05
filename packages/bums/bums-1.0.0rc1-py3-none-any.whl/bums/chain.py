class ChainFunc:
    """ 链式函数调用
    """

    def __init__(self, func):
        self.func = func

    def __rand__(self, other):
        """ 使用 & 语法连接，根据数据类型的不同，解析不同的入参方式
        """
        if isinstance(other, tuple):
            return self.func(*other)
        elif isinstance(other, dict):
            return self.func(**other)
        return self.func(other)


f = ChainFunc
