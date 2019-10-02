from datetime import datetime, timedelta
import re

# 月份键值对
month_kv = dict(Jan=1, Feb=2, Mar=3, Apr=4, May=5, Jun=6, Jul=7, Aug=8, Sep=9, Oct=10, Nov=11, Dec=12, )


def get_pydt_based_logdt(logdt_str):
    dt1 = re.match("(\d+)/(\w+)/(\d+):(\d+):(\d+):(\d+)",  logdt_str)
    dt2 = re.match("(\d+)/(\w+)/(\d+):(\d+):(\d+):(\d+) [+|-]\d{4}",  logdt_str)
    dt3 = re.match("\w+\s*(\w+)\s*(\d+)\s*(\d+):(\d+):(\d+)\s*(\d+)", logdt_str)
    mflag = False
    if dt1:
        dt_matched = dt1
        mflag = True
    if dt2:
        mflag = True
        dt_matched = dt2
    if dt3:
        # 审计日志匹配的 'Wed Oct  2 08:20:01 2019'
        return datetime(**dict(
            day=int(dt3.group(2)),
            month=month_kv[dt3.group(1)],
            year=int(dt3.group(6)),
            hour=int(dt3.group(3)),
            minute=int(dt3.group(4)),
            second=int(dt3.group(5)),
        ))
    if not mflag:
        print('=====NOTE_MATCH_DATE{}'.format(logdt_str) )
        return datetime.now()

    return datetime(**dict(
        day=int(dt_matched.group(1)),
        month=month_kv[dt_matched.group(2)],
        year=int(dt_matched.group(3)),
        hour=int(dt_matched.group(4)),
        minute=int(dt_matched.group(5)),
        second=int(dt_matched.group(6)),
    ))


def get_ua_and_os_from_User_Agent(ua_str):
    # 需要安装这个包的哦
    from ua_parser import user_agent_parser
    up = user_agent_parser.Parse(ua_str)
    return dict(
        user_agent=up["user_agent"]["family"],
        os=up["os"]["family"],
        device=up["device"]["family"]
    )

