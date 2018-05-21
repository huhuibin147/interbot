# -*- coding: utf-8 -*-
import traceback
from libs import osu_user
from libs import mods

def myinfo(qq, gid=None):
    u = osu_user.Osuer()
    ret = u.get_user_from_db(qq, gid)
    if not ret:
        return '未绑定,请使用setid!'

    home_url = 'https://osu.ppy.sh/u/%s' % (ret['osuname'])
    msg = "osu:%s\nosuid:%s\nmoney:%s\nbagnum:%s\n%s" % (ret['osuname'], ret['osuid'], ret['money'], ret['bagnum'], home_url)
    return msg

def get_bp5info(uid):
    try:
        u = osu_user.Osuer()
        bp5 = u.get_user_bp(uid, m=0, limit=5)
        if not bp5:
            return '没有Bp,下一个!!'
        # TODO uid转uname
        s_msg = "%s's bp!!\n" % uid
        for i,r in enumerate(bp5[0:5]):
            msg = 'bp{x},{pp}pp,{acc}%,{rank},+{mod}'
            c50 = float(r['count50'])
            c100 = float(r['count100'])
            c300 = float(r['count300'])
            cmiss = float(r['countmiss'])
            acc = round((c50*50+c100*100+c300*300)/(c50+c100+c300+cmiss)/300*100,2)
            msg = msg.format(x=i+1,pp=round(float(r['pp'])),acc=acc,rank=r['rank'],mod=','.join(mods.getMod(int(r['enabled_mods']))))
            s_msg = s_msg + msg + '\n'
        return s_msg[0:-1]
    except:
        traceback.print_exc()
        return '没有Bp,下一个!!'


def setid(uid, qq, groupid):
    uinfo = get_osuer_info(uid)
    if not uinfo:
        return '绑定失败!(why?你自己猜吧'
    u = osu_user.Osuer()
    if not u.insert2DB(qq, uinfo['user_id'], groupid, uinfo['username']):
        return '绑定失败,interBot数据库被玩坏了!'
    return '绑定成功,使用myinfo查询信息!'

def get_osuer_info(uid):
    u = osu_user.Osuer()
    return u.get_user_info(uid)

def check(uid):
    u = osu_user.Osuer()
    pp,pp2,maxpp = u.check_user(uid)
    if not pp:
        return '你在逗我把,哪来的pp???'
    return '%s\npp:%spp\ninter手算:%spp\n目前潜力:%spp' % (uid,pp,pp2,maxpp)

def map(uid):
    u = osu_user.Osuer()
    map_id,num = u.choiceMap(uid)
    if not map_id:
        return '本bot根本不想给你推荐图'
    return 'inter推荐给%s的图:https://osu.ppy.sh/b/%s  推荐指数:%s' %(uid, map_id, num)