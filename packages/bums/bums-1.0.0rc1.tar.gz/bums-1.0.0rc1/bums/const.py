class Nil:

    def __str__(self):
        return "nil"

    def __repr__(self):
        return "nil"

    def __bool__(self):
        return False

    def __or__(self, other):
        return other


# 可以理解为作为 None 使用
nil = Nil()
