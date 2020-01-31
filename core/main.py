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


def get_info(num, code):
    print str(num) + ". " + stock_dict[code] + ":"
    _domain = "SH" if code.startswith("6") else "SZ"

    # this program is focus on data from 20191115
    try:
        data_day = ts.pro_bar(ts_code=code + "." + _domain, freq='D', adj='qfq', start_date="20191115", end_date=end)
    except Exception as e:
        if u"TOKEN无效" in e.args[1]:
            raise Exception("请在auth.txt文件中填入有效的token")
        raise e

    _close_list = list(reversed(data_day["close"].tolist()))

    _last = _close_list[-1]
    _max = max(_close_list)
    _min = min(_close_list[: -1])
    _gap = _last - _max
    _gap_percent = round(_gap / _max, 4) * 100

    _last2 = _close_list[-2]
    _last2_gap_percent = round((_last - _last2) / _max, 4) * 100

    _last3 = _close_list[-3]
    _last3_gap_percent = round((_last2 - _last3) / _max, 4) * 100

    _latest = u"加速下跌" if _last3_gap_percent > _last2_gap_percent else (u"开始反弹" if _last2_gap_percent > 0 else u"减速下跌")

    # last 30 days sample
    _last_30_days_max = max(_close_list[-30:])
    _lower = u"继续再创新低" if _last == min(_close_list[_close_list.index(_last_30_days_max):]) else (u"没有创新低了" if _last2 == min(_close_list[_close_list.index(_last_30_days_max):]) else u"已经连续2天没有创新低了")

    print "当前价：" + str(_last), "总上涨：" + str(_gap) if _gap > 0 else "总下跌：" + str(_gap), \
        "总涨幅：" + str(_gap_percent) + "%" if _gap_percent > 0 else "总跌幅：" + str(_gap_percent) + "%", \
        "最近涨幅：" + str(_last2_gap_percent) + "%" if _last2_gap_percent > 0 else "最近跌幅：" + str(_last2_gap_percent) + "%", \
        "比前一日" + str(_last3_gap_percent) + "% " + _latest.encode("utf-8")

    time.sleep(3)

    data_day_half_year = ts.pro_bar(ts_code=code + "." + _domain, freq='D', adj='qfq', start_date="20190801", end_date=end)

    _close_half_year_list = list(reversed(data_day_half_year["close"].tolist()))

    _min_half_year = min(_close_half_year_list[: -15])

    time.sleep(3)

    data_day_3_4_year = ts.pro_bar(ts_code=code + "." + _domain, freq='D', adj='qfq', start_date="20190501", end_date=end)

    _close_3_4_year_list = list(reversed(data_day_3_4_year["close"].tolist()))

    _min_3_4_year = min(_close_3_4_year_list[: -30])
    _max_3_4_year = max(_close_3_4_year_list)

    time.sleep(3)

    data_day = ts.pro_bar(ts_code=code + "." + _domain, ma=[5, 10, 20], freq='D', adj='qfq', start_date=start, end_date=end)

    _close_list = list(reversed(data_day["close"].tolist()))

    ma20_list = list(reversed(data_day["ma20"].tolist()))
    _last_day_ma20 = ma20_list[-1]

    # _day_ma60 = list(reversed(data_day["ma60"].tolist()))
    # _last_day_ma60 = _day_ma60[-1]
    #
    # _day_ma120 = list(reversed(data_day["ma120"].tolist()))
    # _last_day_ma120 = _day_ma120[-1]

    _day_ma60 = _close_list[-60:]
    _last_day_ma60 = round(sum(_day_ma60) / len(_day_ma60), 2)
    _day_ma120 = _close_list[-120:]
    _last_day_ma120 = round(sum(_day_ma120) / len(_day_ma120), 2)
    # print "日线：60均线：%s, 120均线：%s" % (_last_day_ma60, _last_day_ma120)

    time.sleep(3)

    data_week = ts.pro_bar(ts_code=code + "." + _domain, ma=[5, 10, 20], freq='W', adj='qfq', start_date=start, end_date=end)
    _close_list = list(reversed(data_week["close"].tolist()))

    ma20_list = list(reversed(data_week["ma20"].tolist()))
    _last_week_ma20 = ma20_list[-1]

    # _week_ma60 = list(reversed(data_week["ma60"].tolist()))
    # _last_week_ma60 = _week_ma60[-1]
    #
    # _week_ma120 = list(reversed(data_week["ma120"].tolist()))
    # _last_week_ma120 = _week_ma120[-1]

    _week_ma60 = _close_list[-60:]
    _last_week_ma60 = round(sum(_week_ma60) / len(_week_ma60), 2)
    _week_ma120 = _close_list[-120:]
    _last_week_ma120 = round(sum(_week_ma120) / len(_week_ma120), 2)
    # print "周线：60均线：%s, 120均线：%s" % (_last_week_ma60, _last_week_ma120)

    time.sleep(3)

    data_month = ts.pro_bar(ts_code=code + "." + _domain, ma=[5, 10, 20], freq='M', adj='qfq', start_date=start, end_date=end)
    _close_list = list(reversed(data_month["close"].tolist()))

    ma20_list = list(reversed(data_month["ma20"].tolist()))
    _last_month_ma20 = ma20_list[-1]

    # _month_ma60 = list(reversed(data_month["ma60"].tolist()))
    # _last_month_ma60 = _month_ma60[-1]
    #
    # _month_ma120 = list(reversed(data_week["ma120"].tolist()))
    # _last_month_ma120 = _month_ma120[-1]

    _month_ma60 = _close_list[-60:]
    _last_month_ma60 = round(sum(_month_ma60) / len(_month_ma60), 2)
    _month_ma120 = _close_list[-120:]
    _last_month_ma120 = round(sum(_month_ma120) / len(_month_ma120), 2)
    # print "月线：60均线：%s, 120均线：%s" % (_last_month_ma60, _last_month_ma120)

    # last one
    _gap_list = [_last - _last_day_ma20, _last - _last_day_ma60, _last - _last_day_ma120,
                 _last - _last_week_ma20, _last - _last_week_ma60, _last - _last_week_ma120,
                 _last - _last_month_ma20, _last - _last_month_ma60, _last - _last_month_ma120,
                 _last - _min, _last - _min_half_year, _last - _min_3_4_year]
    _gap_filter_list = list()
    for g in _gap_list:
        if g > 0:
            _gap_filter_list.append(g)
        else:
            _gap_filter_list.append(100000)

    _position_last = ""
    _gap_index = _gap_filter_list.index(min(_gap_filter_list))
    if _gap_index == 0:
        _position_last = u"在日20日均线附近"
    elif _gap_index == 1:
        _position_last = u"在日60日均线附近"
    elif _gap_index == 2:
        _position_last = u"在日120日均线附近"
    elif _gap_index == 3:
        _position_last = u"在周20日均线附近"
    elif _gap_index == 4:
        _position_last = u"在周60日均线附近"
    elif _gap_index == 5:
        _position_last = u"在周120日均线附近"
    elif _gap_index == 6:
        _position_last = u"在月20日均线附近"
    elif _gap_index == 7:
        _position_last = u"在月60日均线附近"
    elif _gap_index == 8:
        _position_last = u"在月120日均线附近"
    elif _gap_index == 9:
        _position_last = u"在前期低点附近"
    elif _gap_index == 10:
        _position_last = u"在前期大低点附近"
    elif _gap_index == 11:
        _position_last = u"在前期大大低点附近"
    print _position_last.encode("utf-8") + "\n"

    # last 2nd
    _gap_last2_list = [_last2 - _last_day_ma20, _last2 - _last_day_ma60, _last2 - _last_day_ma120,
                       _last2 - _last_week_ma20, _last2 - _last_week_ma60, _last2 - _last_week_ma120,
                       _last2 - _last_month_ma20, _last2 - _last_month_ma60, _last2 - _last_month_ma120,
                       _last2 - _min, _last - _min_half_year, _last - _min_3_4_year]
    _gap_last2_filter_list = list()
    for g in _gap_last2_list:
        if g > 0:
            _gap_last2_filter_list.append(g)
        else:
            _gap_last2_filter_list.append(100000)

    _position_last2 = ""
    _gap_last2_index = _gap_last2_filter_list.index(min(_gap_last2_filter_list))
    if _gap_last2_index == 0:
        _position_last2 = u"在日20日均线附近"
    elif _gap_last2_index == 1:
        _position_last2 = u"在日60日均线附近"
    elif _gap_last2_index == 2:
        _position_last2 = u"在日120日均线附近"
    elif _gap_last2_index == 3:
        _position_last2 = u"在周20日均线附近"
    elif _gap_last2_index == 4:
        _position_last2 = u"在周60日均线附近"
    elif _gap_last2_index == 5:
        _position_last2 = u"在周120日均线附近"
    elif _gap_last2_index == 6:
        _position_last2 = u"在月20日均线附近"
    elif _gap_last2_index == 7:
        _position_last2 = u"在月60日均线附近"
    elif _gap_last2_index == 8:
        _position_last2 = u"在月120日均线附近"
    elif _gap_last2_index == 9:
        _position_last2 = u"在前期低点附近"
    elif _gap_last2_index == 10:
        _position_last2 = u"在前期大低点附近"
    elif _gap_last2_index == 11:
        _position_last2 = u"在前期大大低点附近"

    # last 3rd
    _gap_last3_list = [_last3 - _last_day_ma20, _last3 - _last_day_ma60, _last3 - _last_day_ma120,
                       _last3 - _last_week_ma20, _last3 - _last_week_ma60, _last3 - _last_week_ma120,
                       _last3 - _last_month_ma20, _last3 - _last_month_ma60, _last3 - _last_month_ma120,
                       _last3 - _min, _last - _min_half_year, _last - _min_3_4_year]
    _gap_last3_filter_list = list()
    for g in _gap_last3_list:
        if g > 0:
            _gap_last3_filter_list.append(g)
        else:
            _gap_last3_filter_list.append(100000)

    _position_last3 = ""
    _gap_last3_index = _gap_last3_filter_list.index(min(_gap_last3_filter_list))
    if _gap_last3_index == 0:
        _position_last3 = u"在日20日均线附近"
    elif _gap_last3_index == 1:
        _position_last3 = u"在日60日均线附近"
    elif _gap_last3_index == 2:
        _position_last3 = u"在日120日均线附近"
    elif _gap_last3_index == 3:
        _position_last3 = u"在周20日均线附近"
    elif _gap_last3_index == 4:
        _position_last3 = u"在周60日均线附近"
    elif _gap_last3_index == 5:
        _position_last3 = u"在周120日均线附近"
    elif _gap_last3_index == 6:
        _position_last3 = u"在月20日均线附近"
    elif _gap_last3_index == 7:
        _position_last3 = u"在月60日均线附近"
    elif _gap_last3_index == 8:
        _position_last3 = u"在月120日均线附近"
    elif _gap_last3_index == 9:
        _position_last3 = u"在前期低点附近"
    elif _gap_last3_index == 10:
        _position_last3 = u"在前期大低点附近"
    elif _gap_last3_index == 11:
        _position_last3 = u"在前期大大低点附近"

    _support_list = [_last_day_ma20, _last_day_ma60, _last_day_ma120, _last_week_ma20, _last_week_ma60, _last_week_ma120, _last_month_ma20, _last_month_ma60, _last_month_ma120, _last]
    _support_list.sort(reverse=True)

    stock_statistics_list.append((stock_dict[code], _gap, _gap_percent, _latest, _position_last,
                                  (u"持续3天处于该位置" if _position_last2 == _position_last3 else u"已经2天处于该位置")
                                  if _position_last2 == _position_last else u"第一次进入该位置", _lower,
                                  _support_list.index(_last), _last - _min, _last - _min_half_year,
                                  _last - _min_3_4_year, round((_max_3_4_year - _last) / (_max_3_4_year - _min_3_4_year) * 100, 2)))


with open(os.path.join(os.path.dirname(__file__), "..", "conf", "auth.txt"), "r") as rf:
    token = rf.read()
    if token:
        ts.set_token(token)

stock_dict = dict()
with open(os.path.join(os.path.dirname(__file__), "..", "conf", "stocks.json"), "r") as rf:
    stock_dict = json.loads(rf.read())

stock_statistics_list = list()

today = datetime.datetime.now()
offset = datetime.timedelta(weeks=-1000)
start = (today + offset).strftime('%Y%m%d')
end = today.strftime("%Y%m%d")

for i, cd in enumerate(stock_dict.keys()):
    time.sleep(5)

    get_info(i+1, cd)

_output = u"涨跌值排行榜如下：\n排名,  涨跌值,  股票\n"
for i, (name, gap, _, _, _, _, _, _, _, _, _, _) in enumerate(sorted(stock_statistics_list, key=lambda x: x[1])):
    _output += str(i+1) + ", " + str(gap) + ", " + name + "\n"

_output += u"\n涨跌幅排行榜如下：\n排名,  涨跌幅,  股票,  最近动态,  当前位置\n"
for i, (name, gap, percent, latest, position, status, lower, support, min_gap, min_half_year_gap, min_3_4_year_gap, percent_3_4_year) in enumerate(sorted(stock_statistics_list, key=lambda x: x[2])):
    _output += str(i+1) + ", " + str(percent) + "%, " + name + ", " + latest + ", " + position + " [%s, %s, %s, %s, %s, %s, %s]\n" % \
               (status, lower, u"已跌破%s个支撑/共9个" % support, u"距离近期低点距离%s" % min_gap, u"距离前期大低点距离%s" % min_half_year_gap, u"距离前期大大低点距离%s" % min_3_4_year_gap, u"后半年最大回调幅度%s" % percent_3_4_year + u"%")

print _output
with open(os.path.join(os.path.dirname(__file__), "..", "output", "%s.csv" % today.strftime("%Y_%m_%d_%H_%M")), "w") as wf:
    wf.write(_output.encode("utf-8"))
