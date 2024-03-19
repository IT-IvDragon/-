import datetime
import random
import uuid


def uuid4():
    """
    uuid4

    :return:
    """
    return uuid.uuid4().__str__()


def device_id():
    """
    设备id

    :return:
    """
    chars = "useandom-26T198340PX75pxJACKVERYMINDBUSHWOLF_GQZbfghjklqvwyzrict"
    ce = ""
    le = 21
    while le > 0:
        ce += chars[int(64 * random.random())]
        le -= 1
    return ce


def timestamp_next_day(hour=9, minute=15):
    """
    获取明天指定时间的时间戳

    :param hour:
    :param minute:
    :return:
    """
    # 获取当前时间，并添加一年
    next_year = datetime.datetime.now() + datetime.timedelta(days=1)

    # 设置小时和分钟为指定值
    specific_time_next_year = datetime.datetime(next_year.year, next_year.month, next_year.day, hour, minute)

    # 转换为时间戳（以秒为单位）
    timestamp = int(specific_time_next_year.timestamp())

    return timestamp * 1000


def format_timestamp(timestamp):
    """
    毫秒时间戳转换成 %Y%m%d%H%M%S

    :param timestamp:
    :return:
    """
    # 将时间戳转换为datetime对象
    dt = datetime.datetime.fromtimestamp(timestamp / 1000)

    # 将datetime对象格式化为指定字符串格式
    formatted_time = dt.strftime("%Y%m%d%H%M%S")

    return formatted_time
