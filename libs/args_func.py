# -*- coding: utf-8 -*-
from libs import osu_user
from libs import score

def uid_find_or_input(uid=None, qq=None, can_input=True, return_type=0, gid=None):
    # 是否允许读入uid
    if can_input and uid:
        return uid

    u = osu_user.Osuer()
    ret = u.get_user_from_db(qq, gid)
    if not ret:
        return 0

    if return_type == 0:
        return ret['osuid']
    elif return_type == 1:
        return ret['osuname']
    elif return_type == 2:
        return ret['osuid'],ret['osuname']

def uid_uname(uname=None, qq=None):
    u = osu_user.Osuer()
    if uname:
        ret = u.get_user_from_db2(uname)
        if ret:
            return ret['osuid'],ret['osuname']

    ret = u.get_user_from_db(qq)
    if not ret:
        return 0,0
    return ret['osuid'],ret['osuname']

def alias2args(cname, rtype=1):
    return score.get_alias(cname, rtype)
 
def alias2bid(args):
    aob = args[1] if len(args) > 1 else Config.MAPID
    try:
        bid = int(aob)
    except:
        bid = alias2args(aob, rtype=1)
    return bid