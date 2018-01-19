# -*- coding: utf-8 -*-
import time
import traceback
from libs import osu_user
from libs import healthCheck
from libs import mods


def test(uid):
    u = osu_user.Osuer(uid=uid)
    userinfo = u.get_user_info()
    bp = u.get_user_bp(limit=5)
    return healthCheck.health_check(userinfo, bp)

def new_test():
    return '你不适合屙屎,请你去世!(给我加id'

def mc():
    msg = "'s card:\n【SSR系列】\ninterbot (1)"
    return msg


def todaybp(uid):
    # 来自int100
    u = osu_user.Osuer(uid=uid)
    bps = u.get_user_bp(limit=100)

    if len(bps) == 0:
        return '这人没有bp!!!'


    todaybp = []
    today = int(time.strftime("%Y%m%d", time.localtime()))
    i = 1
    for bp in bps:
        date = int(time.strftime("%Y%m%d", time.localtime(time.mktime(time.strptime(bp['date'], "%Y-%m-%d %H:%M:%S")))))
        if date == today:
            bp['num'] = i
            todaybp.append(bp)
        i = i + 1

    if len(bp) == 0:
        return "你太菜了!一个bp都没更新!!"

    mtext = "%s today's bp：\n" % uid

    for bp in todaybp:
        acc = mods.get_acc(bp['count300'], bp['count100'], bp['count50'], bp['countmiss'])
        mod = mods.get_mods_name(bp['enabled_mods'])
        mtext = mtext + "bp%s,%.2fpp,%.2f%%,%s,+%s\n" % (bp['num'], float(bp['pp']), acc, bp['rank'], mod)

    return mtext[:-1]