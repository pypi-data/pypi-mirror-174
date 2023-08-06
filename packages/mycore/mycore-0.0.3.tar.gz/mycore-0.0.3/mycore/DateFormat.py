import time
import datetime
import plat.Plat_Config as Config


root = Config.project_root()
module_name = "sjtu"
S = Config.system_config(root, module_name)
FULL_FMT_001 = "%Y-%m-%d %H:%M:%S"
HALF_FMT_001 = "%Y-%m-%d"
timedelta = datetime.timedelta


def formatter(type, ts):
    if isinstance(ts, list):  # 数组
        ret = []
        for item in ts:
            ret.append(time.strftime(type, time.localtime(int(item) / 1000)))
        return ret
    else:  # 单个
        return time.strftime(type, time.localtime(int(ts) / 1000))


def formatTs(scale, assign):
    ret = time.time()*1000 if assign is None else assign
    t = time.localtime(int(ret) / 1000)
    y, M, d, H, m, s, mills = t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec, ret % 1000
    if scale == "y":
        return int(time.mktime((y, 1, 1, 0, 0, 0, 0, 0, 0)) * 1000)
    elif scale == "M":
        return int(time.mktime((y, M, 1, 0, 0, 0, 0, 0, 0)) * 1000)
    elif scale == "w":
        a = datetime.datetime.fromtimestamp(int(ret) / 1000)
        weekStart = a - timedelta(days=a.weekday())
        return formatTs('d', int(weekStart.timestamp() * 1000))
    elif scale == "d":
        return int(time.mktime((y, M, d, 0, 0, 0, 0, 0, 0)) * 1000)
    elif scale == "H":
        return int(time.mktime((y, M, d, H, 0, 0, 0, 0, 0)) * 1000)
    elif scale == "m":
        return int(time.mktime((y, M, d, H, m, 0, 0, 0, 0)) * 1000)
    elif scale == "s":
        return int(time.mktime((y, M, d, H, m, s, 0, 0, 0)) * 1000)


def now():
    return int(time.time()*1000)


def timeMove(scale, exp, assign):
    if isinstance(assign, list):
        rets = []
        for i in assign:
            rets.append(timeMove(scale, exp, i))
        return rets
    ret = int(time.time()*1000) if assign is None else assign
    t = datetime.datetime.fromtimestamp(int(ret) / 1000)
    if scale == "y" or scale == "Y":
        ret = t.replace(year=t.year + int(exp))
    elif scale == "M":
        return monthMove(exp, assign)
    elif scale == "w":
        ret = t + timedelta(weeks=int(exp))
    elif scale == "d":
        ret = t + timedelta(days=int(exp))
    elif scale == "H":
        ret = t + timedelta(hours=int(exp))
    elif scale == "m":
        ret = t + timedelta(minutes=int(exp))
    elif scale == "s":
        ret = t + timedelta(seconds=int(exp))
    return int(ret.timestamp() * 1000)


def monthMove(exp, assign):
    ret = time.time() if assign is None else assign
    t = datetime.datetime.fromtimestamp(int(ret) / 1000)
    targetM = t.month + int(exp)
    if 1 <= targetM <= 12:
        t = t.replace(month=targetM)
    elif targetM < 1:
        yearGap = int(abs(targetM) / 12) + 1
        t = t.replace(month=targetM + yearGap*12)
        t = t.replace(year=t.year - yearGap)
    elif targetM > 12:
        yearGap = int(targetM / 12)
        t = t.replace(month=targetM - yearGap * 12)
        t = t.replace(year=t.year + yearGap)
    return int(t.timestamp() * 1000)


def dateRange(scale, assign):
    ret = time.time() if assign is None else assign
    return [formatTs(scale, ret), formatTs(scale, timeMove(scale, 1, ret))]


def accTimeRange(scale, assign):
    ret = time.time() if assign is None else assign
    range = [formatTs(scale, ret), formatTs(scale, timeMove(scale, 1, ret))]
    return [timeMove(rangeToScale(scale), "1", range[0]), range[1]]


def rangeToScale(range):
    if range == S.TimeScale["y"]:
        return S.TimeScale["M"]
    elif range == S.TimeScale["M"]:
        return S.TimeScale["d"]
    elif range == S.TimeScale["w"]:
        return S.TimeScale["d"]
    elif range == S.TimeScale["d"]:
        return S.TimeScale["H"]
    elif range == S.TimeScale["H"]:
        return S.TimeScale["m"]
    elif range == S.TimeScale["m"]:
        return S.TimeScale["s"]


def scaleTs(scale):
    if scale == "s":
        return 1000
    elif scale == "m":
        return 60*1000
    elif scale == "H":
        return 60*60*1000
    elif scale == "d":
        return 24*60*60*1000
    elif scale == "w":
        return 7*24*60*60*1000
    elif scale == "M":
        return None
    elif scale == "y":
        return None


def tsSeries(range, scale):
    start, end, ret = range[0], range[1], []
    while start < end:
        ret.append(start)
        start += scaleTs(scale)
    return ret


def selfDefine(assign, scale, val):
    ret = time.time() if assign is None else assign
    t = datetime.datetime.fromtimestamp(int(ret) / 1000)
    if scale == S.TimeScale["y"]:
        t = t.replace(year=val)
    elif scale == S.TimeScale["M"]:
        t = t.replace(month=val)
    elif scale == S.TimeScale["w"]:
        print("w")
        # t = t.replace(week=)
    elif scale == S.TimeScale["d"]:
        t = t.replace(day=val)
    elif scale == S.TimeScale["H"]:
        t = t.replace(hour=val)
    elif scale == S.TimeScale["m"]:
        t = t.replace(minute=val)
    elif scale == S.TimeScale["s"]:
        t = t.replace(second=val)
    return formatTs(scale, int(t.timestamp() * 1000))

test = 1631005937279
test0 = int(time.time() * 1000)
# print(formatTs("w", test))
# print(timeMove("m", "-1", test0))

# print(format("%Y-%m-%d %H:%M:%S", test0))
# print(format("%Y-%m-%d %H:%M:%S", timeMove("M", "-360", test0)))
# print(format("%Y-%m-%d %H:%M:%S", timeMove("d", "-1", accTimeRange("d", test0))))


# t = time.time()
# millis1 = int(t)
# print('10位时间戳：{}'.format(millis1))
#
# millis2 = int(t * 1000)
# print('13位时间戳：{}'.format(millis2))
#
# now = time.strftime("%Y-%m-%d %H:%M:%S")
# print('当前时间格式化：{}'.format(now))
#
# now2 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(1594368331))
# print('指定时间格式化：{}'.format(now2))
#
# str = '2020-07-10 16:05:31'
# ts = time.mktime(time.strptime(str,"%Y-%m-%d %H:%M:%S"))
# print('格式化时间转时间戳：{}'.format(int(ts)))
#
# ttuple = time.localtime()
# print('当前时间元组：{}'.format(ttuple))
# print('当前年：{}'.format(ttuple.tmyear))
# print('当前月：{}'.format(ttuple.tmmon))
# print('当前日：{}'.format(ttuple.tmmday))
# print('当前时：{}'.format(ttuple.tmhour))
# print('当前分：{}'.format(ttuple.tmmin))
# print('当前秒：{}'.format(ttuple.tmsec))
# print('当前周几：{}'.format(ttuple.tmwday))
# print('当前是一年中第几天：{}'.format(ttuple.tmyday))
# print('当前是否是夏令时：{}'.format(ttuple.tmisdst))
#
# ttuple2 = time.localtime(1594368331)
# print('时间戳转时间元组：{}'.format(ttuple2))
#
# tts = time.strptime('2018-09-30 11:32:23', '%Y-%m-%d %H:%M:%S')
# print('格式化时间转时间元组：{}'.format(tts))
#
# tt = time.mktime((2020, 7, 10, 16, 5, 31, 0, 0, 0))
# print('时间元组转时间戳：{}'.format(int(tt)))
#
# today1 = time.strftime("%Y-%m-%d")
# print(today1)
#
# today2 = datetime.date.today()
# print(today2)
#
# d = datetime.date.today().timetuple()
# print(d)
#
# d1 = time.strftime('%Y-%m-%d',time.localtime(1594804107))
# print('时间戳转日期：{}'.format(d1))
#
# d2 = datetime.date.fromtimestamp(1594804107)
# print('时间戳转日期：{}'.format(d2))
#
# a = datetime.date(2020, 7, 1)
# b = datetime.date(2020, 7, 15)
# print('b的日期减去a的日期：{}'.format(b.sub(a).days))
# print('a的日期减去b的日期：{}'.format(a.sub(b).days))
#
# # 3小时之后
# laterhours = datetime.datetime.now() + datetime.timedelta(hours=3)
# print(laterhours.strftime('%Y-%m-%d %H:%M:%S'))
#
# # 3小时之后的时间戳
# print(int(laterhours.timestamp()))
#
# # 10分钟之后
# laterminutes = datetime.datetime.now() + datetime.timedelta(minutes=10)
# print(laterminutes.strftime('%Y-%m-%d %H:%M:%S'))
#
# # 10分钟之后的时间戳
# print(int(laterminutes.timestamp()))
#
# # 7天之后
# laterdays = datetime.datetime.now() + datetime.timedelta(days=7)
# print(laterdays.strftime('%Y-%m-%d %H:%M:%S'))
#
# # 7天之后的时间戳
# print(int(laterdays.timestamp()))
#
# # 上个月第一天
# date = datetime.datetime.today()
# year,month = date.year,date.month
# if month == 1:
#     startDate = datetime.date(year-1, 12, 1)
# else:
#     startDate = datetime.date(year, month-1, 1)
# print(startDate)
#
# # 上个月最后一天
# today = datetime.datetime.today()
# endDate = datetime.date(today.year, today.month, 1) - datetime.timedelta(days=1)
# print(endDate)
#
# # 上个月开始时间戳
# if month == 1:
#     startTime = int(time.mktime(datetime.date(year-1,12,31).timetuple()))
# else:
#     startTime = int(time.mktime(datetime.date(datetime.date.today().year,datetime.date.today().month-1,1).timetuple()))
# print(startTime)
#
# # 上个月结束时间戳
# endTime = int(time.mktime(datetime.date(datetime.date.today().year,datetime.date.today().month,1).timetuple())) - 1
# print(endTime)
#
# # 本月第一天
# date = datetime.datetime.today()
# year,month = date.year,date.month
# startDate = datetime.date(year, month, 1)
# print(startDate)
#
# # 本月最后一天
# today = datetime.datetime.today()
# if month == 12:
#     endDate = datetime.date(year, month, 31)
# else:
#     endDate = datetime.date(today.year, today.month + 1, 1) - datetime.timedelta(days=1)
# print(endDate)
#
# # 本月开始时间戳
# startTime = int(time.mktime(datetime.date(datetime.date.today().year,datetime.date.today().month,1).timetuple()))
# print(startTime)
#
# # 本月结束时间戳
# if month == 12:
#     endTime = int(time.mktime(datetime.date(datetime.date.today().year + 1,1, 1).timetuple())) - 1
# else:
#     endTime = int(time.mktime(datetime.date(datetime.date.today().year,month+1, 1).timetuple())) - 1
# print(endTime)
#
# # 本周一的时间
# today = datetime.datetime.today()
# mondaydate = today - datetime.timedelta(today.isoweekday()-1)
# t = mondaydate.strftime('%Y-%m-%d')
# print(t)
#
# # 本周一的时间戳
# ts = time.mktime(time.strptime(t,"%Y-%m-%d"))
# print(int(ts))
#
# # 上周一的时间
# lastmondaydate = today - datetime.timedelta(days=today.weekday()+7)
# ta = lastmondaydate.strftime('%Y-%m-%d')
# print(ta)
#
# # 上周一的时间戳
# tas = time.mktime(time.strptime(ta,"%Y-%m-%d"))
# print(int(tas))
#
# # 上周的结束时间
# lastoverdate = today - datetime.timedelta(days=today.weekday()+1)
# o = lastoverdate.strftime('%Y-%m-%d')
# print(o)
#
# # 上周的结束时间戳
# oa = time.mktime(time.strptime(o,"%Y-%m-%d"))
# oat = int(oa)+86400-1
# print(oat)
#
# today = datetime.datetime.today()
#
# # 今年开始时间
# startyeardate = datetime.datetime(today.year, 1, 1)
# syd = startyeardate.strftime('%Y-%m-%d')
# print(syd)
#
# # 今年开始时间戳
# print(int(startyeardate.timestamp()))
#
# # 今年结束时间
# endyeardate = datetime.datetime(today.year,12,31,23,59,59)
# eyd = endyeardate.strftime('%Y-%m-%d')
# print(eyd)
#
# # 今年结束时间戳
# print(int(endyeardate.timestamp()))
#
#
# # 去年开始时间
# lastyeardate = datetime.datetime(today.year-1, 1, 1)
# lyd = lastyeardate.strftime('%Y-%m-%d')
# print(lyd)
#
# # 去年开始时间戳
# print(int(lastyeardate.timestamp()))
#
# # 去年结束时间
# lastyearenddate = datetime.datetime(today.year, 1, 1,23,59,59) - datetime.timedelta(days=1)
# lyed = lastyearenddate.strftime('%Y-%m-%d')
# print(lyed)
#
# # 去年结束时间戳
# print(int(lastyearenddate.timestamp()))
