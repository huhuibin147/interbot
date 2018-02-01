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


def rctpp(uid):
    # 来自int100

    u = osu_user.Osuer(uid=uid)
    recent = u.get_recent(limit=1)

    if len(recent) == 0:
        return '这人最近没有打图！快去打图爆曲奇！！！'

    recent = recent[0]
    bid = recent['beatmap_id']

    # now
    now_acc = mods.get_acc(recent['count300'], recent['count100'], recent['count50'], recent['countmiss'])
    
    now_res = mods.calcpp(bid, now_acc, int(recent['maxcombo']), mods.get_mods_name(recent['enabled_mods']), recent['countmiss'])

    # if fc
    fc_acc = mods.get_acc(recent['count300'], recent['count100'], recent['count50'], 0)
    
    fc_res = mods.calcpp(bid, fc_acc, -1, mods.get_mods_name(recent['enabled_mods']))

    # if 98acc
    a98_res = mods.calcpp(bid, 98.0, -1, mods.get_mods_name(recent['enabled_mods']))
    
    artist = ""
    title = ""
    modstr = ""
    
    if  'artist_unicode' in fc_res.keys():
        artist = fc_res['artist_unicode']
    else:
        artist = fc_res['artist']

    if 'title_unicode' in fc_res.keys():
        title = fc_res['title_unicode']
    else:
        title = fc_res['title']

    if not fc_res['mods_str'] == "NONE":
        modstr = "Mods: " + fc_res['mods_str'] + " "
        
    return '%s - %s [%s]\nBeatmap by %s\nhttps://osu.ppy.sh/b/%s\n%sRank: %s Star: %.2f*\n\n对比: (现在 / fc / 98%%)\n%.2f%% / %.2f%% / %.2f%%\n%.2fpp / %.2fpp / %.2fpp\n%sx / %sx / %sx' % \
                                    (artist, title, fc_res['version'], fc_res['creator'], bid, \
                                     modstr, recent['rank'],fc_res['stars'],\
                                     now_acc, fc_acc, 98.00, now_res['pp'], fc_res['pp'], a98_res['pp'],\
                                     now_res['combo'], fc_res['max_combo'], fc_res['max_combo'])