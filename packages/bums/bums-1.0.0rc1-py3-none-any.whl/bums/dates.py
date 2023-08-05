from typing import Union
from datetime import datetime, date, timedelta


def automatic_fmt(d) -> str:
    """ 自动根据参数识别fmt格式
    """
    if isinstance(d, (int, float)):
        fmt = '%Y%m%d'
    else:
        if '/' in d:
            fmt = '%Y/%m/%d'
        elif '-' in d:
            fmt = '%Y-%m-%d'
        else:
            fmt = '%Y%m%d'
    return fmt


def to_date(d: Union[int, float, str], fmt=None):
    """ 转为date类型
    :param d: 字符串或者数字的日期
    :param fmt: d的格式
    """
    fmt = fmt or automatic_fmt(d)
    return datetime.strptime(d, fmt).date()


def date_to_dtime(d: date):
    """ date类型转datetime类型
    :param d: datetime类型日期
    """
    return datetime.combine(d, datetime.min.time())


def second_of_day(d: datetime = None) -> int:
    """ 一天的第几秒
    :param d: 日期类型数据
    """
    d = d or datetime.now()
    return d.hour * 60 * 60 + d.minute * 60 + d.second


def minute_of_day(d: datetime = None) -> int:
    """ 一天的第几分钟
    :param d: 日期类型数据
    """
    d = d or datetime.now()
    return d.hour * 60 + d.minute


def hour_of_day(d: datetime = None) -> int:
    """ 一天的第几小时
    :param d: 日期类型数据
    """
    d = d or datetime.now()
    return d.hour


def day_of_week(d: Union[date, datetime] = None) -> int:
    """ 一周的第几天
    :param d: 日期类型数据
    """
    d = d or datetime.now()
    return d.weekday()


def week_of_year(d: Union[date, datetime] = None) -> int:
    """ 一年的第几周
    :param d: 日期类型数据
    """
    d = d or datetime.now()
    return d.isocalendar()[1]


def week_first(d: Union[date, datetime] = None) -> datetime:
    """ 一周的第一天
    :param d: 日期类型数据
    """
    d = d or datetime.now()
    d = d.date()
    d = d - timedelta(day_of_week())
    return date_to_dtime(d)


def week_end(d: Union[date, datetime] = None) -> datetime:
    """ 一周的最后一天
    :param d: 日期类型数据
    """
    d = d or datetime.now()
    return week_first(d) + timedelta(6)


def week_office(d: Union[date, datetime] = None, office: int = 0) -> datetime:
    """ 一周的第几天的日期
    :param d: 日期类型数据
    :param office: 指定第几天
    """
    # 对日期校验
    if office not in tuple(range(0, 7)):
        raise ValueError("office must be between 0 and 6")

    # 获取时间
    d = d or datetime.now()

    return week_first(d) + timedelta(office)


def month_first(d: Union[date, datetime] = None) -> datetime:
    """ 一个月的第一天
    :param d: 日期类型数据
    """
    d = d or datetime.now()
    return datetime(d.year, d.month, 1)


def month_end(d: Union[date, datetime] = None) -> datetime:
    """ 一个月的最后一天
    :param d: 日期类型数据
    """
    d = d or datetime.now()
    _month = d.month
    _year = d.year
    if _month == 12:
        _year += 1
        _month = 1
    else:
        _month += 1

    return datetime(_year, _month, 1) - timedelta(1)


def quarter_of_year(d: Union[date, datetime] = None) -> int:
    """ 一年的第几个季度
    :param d: 日期类型数据
    """
    d = d or datetime.now()
    return (d.month - 1) // 3 + 1


def quarter_to_month(q: int) -> int:
    """ 季度对应的月份
    """
    return [1, 4, 7, 10][q - 1]


def day_of_quarter(d: Union[date, datetime] = None) -> int:
    """ 一个季度的第几天
    :param d: 日期类型数据
    """
    if isinstance(d, datetime):
        d = d.date()
    else:
        d = d or date.today()

    # 季度对应月份
    _month = quarter_to_month(quarter_of_year(d))

    # 所在季度中的天数
    return (d - date(d.year, _month, 1)).days


def quarter_first(d: Union[date, datetime] = None) -> datetime:
    """ 一个季度的第一天
    :param d: 日期类型数据
    """
    d = d or datetime.now()
    _month = quarter_to_month(quarter_of_year(d))
    return datetime(d.year, _month, 1)


def quarter_end(d: Union[date, datetime] = None) -> datetime:
    """ 一个季度的最后一天
    :param d: 日期类型数据
    """
    d = d or datetime.now()
    _month = quarter_to_month(quarter_of_year(d)) + 3
    _year = d.year
    if _month == 13:
        _month = 1
        _year += 1
    return datetime(_year, _month, 1) - timedelta(1)


def day_of_year(d: Union[date, datetime] = None) -> int:
    """ 一年的第几天
    :param d: 日期类型数据
    """
    if isinstance(d, datetime):
        d = d.date()
    else:
        d = d or date.today()
    return (d - date(d.year, 1, 1)).days


def year_fist(d: Union[date, datetime] = None) -> datetime:
    """ 一年的第一天
    :param d: 日期类型数据
    """
    d = d or datetime.now()
    return datetime(d.year, 1, 1)


def year_end(d: Union[date, datetime] = None) -> datetime:
    """ 一年的最后一天
    :param d: 日期类型数据
    """
    d = d or datetime.now()
    return datetime(d.year + 1, 1, 1) - timedelta(1)
