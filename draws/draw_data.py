# coding: utf-8

import json
import os
from libs import score
from libs import osu_user
from comm import interRequest

bloodcat_bg = 'http://bloodcat.com/osu/i/%s'
bg_path = 'image/bg/'
img_path = 'image/userimg/'


def map_ranks_info(bid='1028215', groupid='641236878', hid=1, mods=-1):
    # map信息，榜单信息
    ret = score.hid_ranks(bid, groupid, hid, mods)[0]
    maps = json.loads(ret['mapjson'])
    rankjson = json.loads(ret['rankjson'])
    return maps,rankjson

def get_user_stats(uid='8505303'):
    o = osu_user.Osuer()
    ret = o.get_user_stats_today(uid)
    if not ret:
        return {}
    return ret[0]

def check_bg(bid='1028215'):
    for i in range(3):
        if not os.path.exists(bg_path+bid+'.jpg'):
            down_bg(bid)
        else:
            return 1
    return 0

def down_bg(bid='1028215'):
    iq = interRequest.interReq()
    return iq.down_image(iname=bid, url=bloodcat_bg % bid, path=bg_path)

def check_img(uids, isup=0):
    downlist = []
    if isup == 0:
        for u in uids:
            if not os.path.exists(img_path+u+'.jpg'):
                downlist.append(u)
    else:
        downlist = uids
    if downlist:
        down_images_from_ppy(downlist)


def down_images_from_ppy(uids):
    imgs_url = get_images_ppy_url(uids)
    r = interRequest.interReq()
    for idx,imgs_url in enumerate(imgs_url):
        res = r.down_image(uids[idx], url=imgs_url, path=img_path)

def get_images_ppy_url(uids):
    raw_url = "http://www.int100.org/api/get_avatars.php?u={u}"
    r = interRequest.interReq()
    ustr = ','.join(uids)
    url = raw_url.format(u=ustr)
    print(url)
    res = r.get(url)
    res = res[:-1]
    return res.split(',')

