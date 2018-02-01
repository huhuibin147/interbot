# -*- coding: utf-8 -*-
import os
import requests
import json
from io import TextIOWrapper

mod_list={
    0: 'NONE',
    1: 'NF',
    2: 'EZ',
    3: 'NV',
    4: 'HD',
    5: 'HR',
    6: 'SD',
    7: 'DT',
    8: 'Relax',
    9: 'HT',
    10: 'NC',
    11: 'FL',
    12: 'AT',
    13: 'SO',
    14: 'AP',
    15: 'PF',
    16: 'PF',
    
}

def getMod(num=16504):
    '''NC出现的话删除DT，PF出现的话删除SD'''
    mods = []
    i=1
    while num:
        if num&0x1:
            mods.append(mod_list.get(i))
        num=num>>1
        i+=1
    if not mods:
        return ['none']
    if 'NC' in mods:
        mods.remove('DT')
    if 'PF' in mods:
        mods.remove('SD')
    
    return mods

def get_acc(c300, c100, c50, cmiss):
    c300 = int(c300)
    c100 = int(c100)
    c50 = int(c50)
    cmiss = int(cmiss)

    tph = c50 * 50 + c100 * 100 + c300 * 300

    tnh = cmiss + c50 + c100 + c300

    acc = tph / tnh / 3
    return acc

def calcpp(bid, acc=100.0, combo=-1, mod="none", misses=0):
    if not os.path.exists("mapinfo/cache/" + str(bid) + ".osu"):
        if not download_file("http://osu.ppy.sh/osu/" + str(bid), str(bid) + ".osu", "mapinfo/cache"):
            return [False, 1]

    result = os.popen("\"oppai.exe\" mapinfo/cache/{0}.osu -ojson {1}% {2}x +{3} {4}m".format(bid, acc, combo, mod, misses))
    result1 = TextIOWrapper(result.buffer, "utf-8")
    return json.loads(result1.read(), encoding="utf-8")

def get_mods_name(bitset):
    mods = getMod(int(bitset))
    name = ""
    for m in mods:
        name = name + m

    return name

def download_file(url, savename, savepath="cache"):
    if not os.path.exists(savepath):
        os.makedirs(savepath)

    savepath = os.path.join(savepath, savename)

    r = requests.get(url, stream=True)
    f = open(savepath, "wb")
    for chunk in r.iter_content(chunk_size=512):
        if chunk:
            f.write(chunk)

    f.close()

    if not os.path.getsize(savepath):
        os.remove(savepath)
        return False

    return True