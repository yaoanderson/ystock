#!/usr/bin/env python
# coding=utf-8

import tushare as ts
import datetime
import time
import json
import os


# code：股票代码，即6位数字代码，或者指数代码（sh=上证指数 sz=深圳成指 hs300=沪深300指数 sz50=上证50 zxb=中小板 cyb=创业板）
# start：开始日期，格式YYYY-MM-DD
# end：结束日期，格式YYYY-MM-DD
# ktype：数据类型，D=日k线 W=周 M=月 5=5分钟 15=15分钟 30=30分钟 60=60分钟，默认为D


def get_info(code):
    print stock_dict[code] + ":"

    data_day = ts.get_hist_data(code, ktype="D", start=start, end=end)

    _close_list = list(reversed(data_day["close"].tolist()))
    _last = _close_list[-1]
    _max = max(_close_list)
    _min = min(_close_list)
    _gap = _last - _max
    _gap_percent = round(_gap / _max, 4) * 100
    stock_statistics_list.append((stock_dict[code], _gap, _gap_percent))
    print "当前价：" + str(_last), "上涨：" + str(_gap) if _gap > 0 else "下跌：" + str(_gap), \
        "涨幅：" + str(_gap_percent) + "%" if _gap_percent > 0 else "跌幅：" + str(_gap_percent) + "%"

    ma20_list = list(reversed(data_day["ma20"].tolist()))
    _last_day_ma20 = ma20_list[-1]

    time.sleep(3)

    data_week = ts.get_hist_data(code, ktype="W", start=start, end=end)

    ma20_list = list(reversed(data_week["ma20"].tolist()))
    _last_week_ma20 = ma20_list[-1]

    time.sleep(3)

    data_month = ts.get_hist_data(code, ktype="M", start=start, end=end)

    ma20_list = list(reversed(data_month["ma20"].tolist()))
    _last_month_ma20 = ma20_list[-1]

    _ma_dict = {
        _last_day_ma20: "日均线",
        _last_week_ma20: "周均线",
        _last_month_ma20: "月均线"
    }

    _gap_list = [_last - _last_day_ma20, _last - _last_week_ma20, _last - _last_month_ma20]
    _gap_filter_list = list()
    for g in _gap_list:
        if g > 0:
            _gap_filter_list.append(g)
        else:
            _gap_filter_list.append(100000)
    _gap_index = _gap_filter_list.index(min(_gap_filter_list))
    if _gap_index == 0:
        print "在日均线附近\n"
    elif _gap_index == 1:
        print "在周均线附近\n"
    elif _gap_index == 2:
        print "在月均线附近\n"


stock_dict = dict()
with open(os.path.join(os.path.dirname(__file__), "..", "conf", "stocks.json"), "r") as rf:
    stock_dict = json.loads(rf.read())

stock_statistics_list = list()

today = datetime.datetime.now()
offset = datetime.timedelta(weeks=-4*3)
start = (today + offset).strftime('%Y-%m-%d')
end = today.strftime("%Y-%m-%d")

for cd in stock_dict.keys():
    time.sleep(5)

    get_info(cd)

_output = u"跌值排行榜如下：\n"
for name, gap, percent in sorted(stock_statistics_list, key=lambda x: x[1]):
    _output += str(gap) + "," + name + "\n"

_output += u"\n跌幅排行榜如下：\n"
for name, gap, percent in sorted(stock_statistics_list, key=lambda x: x[2]):
    _output += str(percent) + "%," + name + "\n"

print _output
with open(os.path.join(os.path.dirname(__file__), "..", "output", "%s.csv" % today.strftime("%Y_%m_%d_%H_%M")), "w") as wf:
    wf.write(_output.encode("utf-8"))
