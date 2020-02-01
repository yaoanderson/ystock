#!/usr/bin/env python
# coding=utf-8

import tushare as ts
import datetime
import time
import json
import os


def get_info(num, code):
    _domain = "SH" if code.startswith("6") else "SZ"

    # the latest data is from 20191115
    try:
        data_day_latest = ts.pro_bar(ts_code=code + "." + _domain, freq='D', adj='qfq', start_date="20191115", end_date=end)
    except Exception as e:
        if u"TOKEN无效" in e.args[1]:
            raise Exception("请在auth.txt文件中填入有效的token")
        raise e

    _close_latest_list = list(reversed(data_day_latest["close"].tolist()))

    _last = _close_latest_list[-1]
    _last2 = _close_latest_list[-2]
    _last3 = _close_latest_list[-3]
    _max_latest = max(_close_latest_list[: -1])
    _min_latest = min(_close_latest_list[: -1])
    _rebound_latest = _last - _max_latest
    _rise_latest = _max_latest - _min_latest
    _rebound_percent_latest = round(_rebound_latest / _rise_latest, 4) * 100

    time.sleep(3)

    data_day_half_year_2_latest = ts.pro_bar(ts_code=code + "." + _domain, freq='D', adj='qfq', start_date="20190801",
                                             end_date="20191115")

    _close_half_year_2_latest_list = list(reversed(data_day_half_year_2_latest["close"].tolist()))

    _max_half_year_2_latest = max(_close_half_year_2_latest_list)
    _min_half_year_2_latest = min(_close_half_year_2_latest_list)

    time.sleep(3)

    data_day_3_4_year_2_half_year = ts.pro_bar(ts_code=code + "." + _domain, freq='D', adj='qfq', start_date="20190501",
                                               end_date="20190801")

    _close_3_4_year_2_half_year_list = list(reversed(data_day_3_4_year_2_half_year["close"].tolist()))

    _max_3_4_year_2_half_year = max(_close_3_4_year_2_half_year_list)
    _min_3_4_year_2_half_year = min(_close_3_4_year_2_half_year_list)

    _max_list = sorted([_max_latest, _max_half_year_2_latest, _max_3_4_year_2_half_year])
    _min_list = sorted([_min_latest, _min_half_year_2_latest, _min_3_4_year_2_half_year])

    _rebound_3_4_year = _last - _max_list[-1]
    _rise_3_4_year = _max_list[-1] - _min_list[0]
    _rebound_3_4_year_percent = round(_rebound_3_4_year / _rise_3_4_year, 4) * 100

    _gap_to_low1 = _last - _min_list[-1]
    _gap_to_low2 = _last - _min_list[-2]
    _gap_to_low3 = _last - _min_list[-3]
    _break_low = 0
    if _gap_to_low1 < 0:
        _break_low = 1
    if _gap_to_low2 < 0:
        _break_low = 2
    if _gap_to_low3 < 0:
        _break_low = 3

    time.sleep(3)

    data_all_day = ts.pro_bar(ts_code=code + "." + _domain, freq='D', adj='qfq', start_date=start, end_date=end)

    _close_all_day_list = list(reversed(data_all_day["close"].tolist()))

    _all_day_ma20 = _close_all_day_list[-20:]
    _last_all_day_ma20 = round(sum(_all_day_ma20) / len(_all_day_ma20), 2)
    _all_day_ma60 = _close_all_day_list[-60:]
    _last_all_day_ma60 = round(sum(_all_day_ma60) / len(_all_day_ma60), 2)
    _all_day_ma120 = _close_all_day_list[-120:]
    _last_all_day_ma120 = round(sum(_all_day_ma120) / len(_all_day_ma120), 2)
    # print "日线：20均线：%s, 60均线：%s, 120均线：%s" % (_last_all_day_ma20, _last_all_day_ma60, _last_all_day_ma120)

    time.sleep(3)

    data_all_week = ts.pro_bar(ts_code=code + "." + _domain, freq='W', adj='qfq', start_date=start, end_date=end)

    _close_all_week_list = list(reversed(data_all_week["close"].tolist()))

    _all_week_ma20 = _close_all_week_list[-20:]
    _last_all_week_ma20 = round(sum(_all_week_ma20) / len(_all_week_ma20), 2)
    _all_week_ma60 = _close_all_week_list[-60:]
    _last_all_week_ma60 = round(sum(_all_week_ma60) / len(_all_week_ma60), 2)
    _all_week_ma120 = _close_all_week_list[-120:]
    _last_all_week_ma120 = round(sum(_all_week_ma120) / len(_all_week_ma120), 2)
    # print "周线：20均线：%s, 60均线：%s, 120均线：%s" % (_last_all_week_ma20, _last_all_week_ma60, _last_all_week_ma120)

    time.sleep(3)

    data_all_month = ts.pro_bar(ts_code=code + "." + _domain, freq='M', adj='qfq', start_date=start, end_date=end)

    _close_all_month_list = list(reversed(data_all_month["close"].tolist()))

    _all_month_ma20 = _close_all_month_list[-20:]
    _last_all_month_ma20 = round(sum(_all_month_ma20) / len(_all_month_ma20), 2)
    _all_month_ma60 = _close_all_month_list[-60:]
    _last_all_month_ma60 = round(sum(_all_month_ma60) / len(_all_month_ma60), 2)
    _all_month_ma120 = _close_all_month_list[-120:]
    _last_all_month_ma120 = round(sum(_all_month_ma120) / len(_all_month_ma120), 2)
    # print "月线：20均线：%s, 60均线：%s, 120均线：%s" % (_last_all_month_ma20, _last_all_month_ma60, _last_all_month_ma120)

    _support_list = [_last_all_day_ma20, _last_all_day_ma60, _last_all_day_ma120,
                     _last_all_week_ma20, _last_all_week_ma60, _last_all_week_ma120,
                     _last_all_month_ma20, _last_all_month_ma60, _last_all_month_ma120]
    _support_list += _max_list
    _support_list += _min_list
    _support_sort_list = sorted(_support_list, reverse=True)
    _break_count = 0
    _break_keep_days = 1

    _last_before_support = -1
    _last_after_support = -1
    for i in range(len(_support_sort_list)):
        if _last >= _support_sort_list[i]:
            if i > 0:
                _last_before_support = _support_sort_list[i - 1]
            if i < len(_support_sort_list):
                _last_after_support = _support_sort_list[i]
            break
        else:
            _last_before_support = _support_sort_list[i]
        _break_count += 1

    _last2_before_support = -1
    _last2_after_support = -1
    for i in range(len(_support_sort_list)):
        if _last2 >= _support_sort_list[i]:
            if i > 0:
                _last2_before_support = _support_sort_list[i - 1]
            if i < len(_support_sort_list):
                _last2_after_support = _support_sort_list[i]
            break
        else:
            _last2_before_support = _support_sort_list[i]

    if _last2_before_support == _last_before_support and _last2_after_support == _last_after_support:
        _break_keep_days += 1

    _last3_before_support = -1
    _last3_after_support = -1
    for i in range(len(_support_sort_list)):
        if _last3 >= _support_sort_list[i]:
            if i > 0:
                _last3_before_support = _support_sort_list[i - 1]
            if i < len(_support_sort_list):
                _last3_after_support = _support_sort_list[i]
            break
        else:
            _last3_before_support = _support_sort_list[i]

    if _break_keep_days == 2 and _last3_before_support == _last_before_support and _last3_after_support == _last_after_support:
        _break_keep_days += 1

    _position_last = u""
    if _last_after_support != -1:
        _index = _support_list.index(_last_after_support)
        if _index == 0:
            _position_last = u"在日20日均线附近"
        elif _index == 1:
            _position_last = u"在日60日均线附近"
        elif _index == 2:
            _position_last = u"在日120日均线附近"
        elif _index == 3:
            _position_last = u"在周20日均线附近"
        elif _index == 4:
            _position_last = u"在周60日均线附近"
        elif _index == 5:
            _position_last = u"在周120日均线附近"
        elif _index == 6:
            _position_last = u"在月20日均线附近"
        elif _index == 7:
            _position_last = u"在月60日均线附近"
        elif _index == 8:
            _position_last = u"在月120日均线附近"
        elif _index == 9:
            _position_last = u"在前期第3高点附近"
        elif _index == 10:
            _position_last = u"在前期第2高点附近"
        elif _index == 11:
            _position_last = u"在前期第1高点附近"
        elif _index == 12:
            _position_last = u"在前期第1低点附近"
        elif _index == 13:
            _position_last = u"在前期第2低点附近"
        elif _index == 14:
            _position_last = u"在前期第3低点附近"

    _new_low = _last < _min_latest
    _last2_gap_percent = round((_last - _last2) / _last2, 4) * 100
    _last3_gap_percent = round((_last2 - _last3) / _last3, 4) * 100
    _latest_up_down_status = u"加速下跌" if _last3_gap_percent > _last2_gap_percent else (u"开始反弹" if _last2_gap_percent > 0 else u"减速下跌")

    stock_statistics_list.append((stock_dict[code],
                                  _rebound_latest, _rebound_percent_latest,
                                  _rebound_3_4_year, _rebound_3_4_year_percent,
                                  _gap_to_low1, _gap_to_low2, _gap_to_low3, _break_low,
                                  _break_count, _position_last, _break_keep_days,
                                  _new_low, _last2_gap_percent, _last3_gap_percent, _latest_up_down_status))

    print str(num) + ". " + stock_dict[code], "done"


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

_output = u"\n关注股票行情如下：\n排名,  股票,  最近回调/幅度,  大半年回调/幅度,  距离历史第1/2/3低点差值（有无破低点）,  突破支撑数和当前所处支撑及时间,  最近涨跌和是否新低\n"
for i, (name, rebound_latest, rebound_percent_latest, rebound_3_4_year, rebound_3_4_year_percent, gap_to_low1, gap_to_low2, gap_to_low3, break_low, break_count, position_last, break_keep_days, new_low, last2_gap_percent, last3_gap_percent, latest_up_down_status) in enumerate(sorted(stock_statistics_list, key=lambda x: x[4])):
    if position_last == u"":
        _support = u"跌破所有支撑)"
    else:
        _support = u"连续" + (str(break_keep_days) if break_keep_days <= 2 else u"多") + u"天处" + position_last + u"支撑上)"

    _output += str(i+1) + u", " + name + u", " + \
               str(rebound_latest) + u"/" + str(rebound_percent_latest) + u"%, " + \
               str(rebound_3_4_year) + u"/" + str(rebound_3_4_year_percent) + u"%, " + \
               str(gap_to_low1) + u"/" + str(gap_to_low2) + u"/" + str(gap_to_low3) + u"（" + (u"没有破任何低点" if break_low == 0 else (u"破第1低点" if break_low == 1 else (u"破第2低点" if break_low == 2 else u"破第3低点"))) + u"）, " + \
               ((u"当前突破" + str(break_count) + u"层支撑(" + _support) if break_count != 0 else u"当前没有突破任何支撑") + u", " + \
               (u"最近一天涨跌" + str(last2_gap_percent) + u"%/前一天" + str(last3_gap_percent) + u"%/处于" + latest_up_down_status + u"/" + (u"继续创新低" if new_low else u"没有创新低了")) + "\n"

print _output
with open(os.path.join(os.path.dirname(__file__), "..", "output", "%s.csv" % today.strftime("%Y_%m_%d_%H_%M")), "w") as wf:
    wf.write(_output.encode("utf-8"))
