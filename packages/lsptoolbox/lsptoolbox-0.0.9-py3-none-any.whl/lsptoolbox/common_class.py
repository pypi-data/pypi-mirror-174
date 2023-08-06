
'''
json.dumps 参数说明
skipkeys	是否跳过无法被JSON序列化的key（包括str, int, float, bool, None）	False
sort_keys	是否对数据按照key进行排序	False
ensure_ascii	输出保证将所有输入的非 ASCII 字符转义	True
allow_nan	是否允许JSON规范外的float数据(nan, inf, -inf)	True
default	是一个函数, 当某个value无法被序列化时, 对其调用该函数	None
indent	是一个正整数,  代表序列化后的缩进	None
separator	是一个格式为 (item_separator, key_separator) 的元组, 默认取值为 (', ', ': ')	None
check_circular	是否检查循环引用	True
'''

import json
import datetime
import decimal
class DefaultJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        elif isinstance(obj, datetime.time):
            return obj.strftime("%H:%M:%S")
        elif isinstance(obj, datetime.timedelta):
            return (datetime.datetime.min + obj).time().strftime("%H:%M:%S")
        elif isinstance(obj, bytes):
            return obj.decode('utf-8')
        elif isinstance(obj, decimal.Decimal):
            return str(decimal.Decimal(obj).quantize(decimal.Decimal('0.0000')))
        elif isinstance(obj, list):
            return json.dumps(obj, cls=DefaultJSONEncoder, ensure_ascii=False)
        elif isinstance(obj, dict):
            return json.dumps(obj, cls=DefaultJSONEncoder, ensure_ascii=False)
        else:
            return json.JSONEncoder.default(self, obj)