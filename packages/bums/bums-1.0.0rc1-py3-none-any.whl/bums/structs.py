from typing import Any

from .const import nil


def firstly(array: list, default: Any = nil):
    """ 优雅的获取列表开头的值
    :param array: 列表对象
    :param default: 无法获取值时的默认值
    """
    return array[0] if array else default


def lastly(array: list, default: Any = nil):
    """ 优雅的获取列表末尾的值
    :param array: 列表对象
    :param default: 无法获取值时的默认值
    """
    return array[-1] if array else default


def gain_idx(array: list, site: int, default: Any = nil):
    """ 优雅的获取列表指定索引的值
    :param array: 列表对象
    :param site: 列表索引
    :param default: 无法获取值时的默认值
    """
    return array[site] if len(array) - 1 >= site else default


def gain(obj, mark, default=nil):
    """ 优雅的获取对象的指定属性，取不到时使用默认值
    :param obj: 对象
    :param mark: 属性标志
    :param default: 无法获取值时的默认值
    """
    if isinstance(obj, dict):
        value = obj.get(mark, default)
    else:
        value = getattr(obj, mark, default)
    return value


def gain_batch(array: list, mark: Any, default: Any = nil, purify_nil=False):
    """ 优雅的获取列表嵌套对象中的对象的属性(当其中嵌套的对象是列表时，mark为int类型的索引).
    :param array: 列表嵌套对象
    :param mark: 属性标志
    :param default: 无法获取值时的默认值
    :param purify_nil: 是否过滤掉nil值，只过滤nil值是因为如果default指定其他值，表示该列表的所有值均有意义
    """
    values = []
    for obj in array:
        if isinstance(obj, list):
            value = gain_idx(obj, mark, default)
        else:
            value = gain(obj, mark, default)
        values.append(value)

    # 过滤掉nil值
    if purify_nil:
        values = purify(values)

    return values


def purify(array: list, value: Any = nil):
    """ 优雅的提纯列表，删除其中的指定值，默认删除列表中的nil值
    :param array: 列表
    :param value: 值
    """
    values = []
    for v in array:
        if v == value:
            continue
        values.append(v)
    return values


def tile(arrays):
    """ 将列表嵌套列表平铺（因为列表嵌套列表的平铺比较常见，但是以下这种写法小部分人不知道，所以使用此函数）
    :param arrays: 列表嵌套列表
    """
    return sum(arrays, [])


def tiles(arrays):
    """ 多层次结构平铺（只拆解嵌套结构中的列表，元组，集合）
    :param arrays: 多层次嵌套结构
    """
    array = []
    for item in arrays:
        if isinstance(item, (list, tuple, set)):
            array.extend(tiles(item))
        else:
            array.append(item)
    return array
