# -*- coding: utf-8 -*-
import time
import copy
import traceback
import numpy as np
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

def check2(uid):
    u = osu_user.Osuer(uid=uid)
    userinfo = u.get_user_info()
    bp = u.get_user_bp(limit=10)
    acc = float(userinfo['accuracy'])
    pc = float(userinfo['playcount'])
    tth = float(int(userinfo['count300']) + int(userinfo['count100']) + int(userinfo['count50']))
    bpacc = bppp = 0
    for r in bp:
        bppp += float(r['pp'])
        bpacc += float(mods.get_acc(r['count300'], r['count100'], r['count50'], r['countmiss']))
    newpp, acc_c, bpacc_c, bppp_c, pc_c, tth_c = pp2(acc, bpacc, bppp, pc, tth)
    print(acc, bpacc, bppp, pc, tth)
    return "%s\n实际pp:%spp\n预测水平:%spp" % (uid, round(float(userinfo['pp_raw']),2), newpp)

def pp2(acc, bpacc, bppp, pc, tth):
    w = [0.22483119, -0.1217108, 0.82082623, 0.0294727, 0.06772371]
    b = [4.95929298e-09]
    pp_m = 2218.589021413463
    pp_s = 1567.8553119973133
    acc_m = 95.69755708902649
    acc_s = 3.014845506352131
    bpacc_m = 961.4064515140441
    bpacc_s = 38.812586876313496
    bppp_m = 1177.9167271984384
    bppp_s = 808.798796955419
    pc_m = 15030.912107867616
    pc_s = 17940.253798480247
    tth_m = 2756676.6760339583
    tth_s = 3498224.778143693
    acc_c = (acc-acc_m)/acc_s*(w[0])
    bpacc_c = (bpacc-bpacc_m)/(bpacc_s)*(w[1])
    bppp_c = (bppp-bppp_m)/bppp_s*(w[2])
    pc_c = (pc-pc_m)/pc_s*(w[3])
    tth_c = (tth-tth_m)/tth_s*(w[4]) + (b[0])
    pp = acc_c + bpacc_c + bppp_c + pc_c + tth_c
    res = [pp, acc_c, bpacc_c, bppp_c, pc_c, tth_c]
    res = [round(r*pp_s+pp_m,2) for r in res]
    return res

def add_api(num1, num2):
    try:
        num1, num2 = int(num1), int(num2)
        decres, binres = add(num1, num2)
        returnres = '%s+%s结果' % (num1, num2)
        if (num1 + num2) >= 256:
            returnres += '溢出'
        returnres += '\n%s\n%s' % (decres, binres)
        return returnres
    except:
        traceback.print_exc()
        return 'interbot被玩坏了'

def add(num1, num2):
    binary_dim = 8
    synapse_0 = np.array([[ -3.59519530e-01,   2.33958993e+00,  -3.20338283e-01,
         -1.23380148e+00,   8.23329522e-02,  -1.45748081e-01,
         -6.45250995e+00,   4.49331950e+00,   3.26692732e+00,
         -1.20738586e+00,   1.15429892e+00,  -2.40883011e-03,
         -1.33888050e+00,   8.52716118e-01,  -5.14494757e+00,
         -1.06330714e+00],
       [ -2.68069543e+00,   1.89873078e+00,   1.87995848e+00,
          1.36240935e+00,   1.49624674e+00,   1.13808369e+00,
          5.07559597e+00,   3.84828275e+00,  -1.60133079e+00,
         -6.85907484e-01,  -2.99388346e+00,   3.72908685e+00,
         -2.03880654e+00,  -1.85161240e+00,  -5.18525010e+00,
          1.15066749e+00]])
    synapse_1 = np.array([[ 2.03071179],
       [-0.66162995],
       [-2.46164979],
       [-2.14926531],
       [-1.316041  ],
       [-1.26025501],
       [ 7.9664284 ],
       [ 6.39502015],
       [-1.38569981],
       [-0.28722474],
       [ 1.84409219],
       [-3.92645053],
       [ 1.06560186],
       [ 0.96352614],
       [-8.58559082],
       [-2.02362742]])
    synapse_h = np.array([[ 0.03181292, -1.57610668,  0.02068267,  0.15980357,  0.51340376,
        -0.54424461, -2.37928976,  0.16707457, -0.10072398, -0.07600941,
         0.09385251, -1.18412748,  0.50169375, -0.43218294,  1.58562712,
        -0.54266278],
       [-0.65419518,  0.22925434,  0.76290475, -0.83081858,  0.67274591,
        -0.66477158,  2.73452205, -2.35568549,  1.6093527 , -0.18013518,
        -0.46082073, -0.47483798, -0.79219389, -1.4475196 , -1.74391352,
        -0.67660372],
       [-0.29566957, -0.14515312, -0.96830975,  0.24622941, -0.00588823,
        -0.33812007,  0.93265849, -1.61233371,  0.68600202,  0.3934923 ,
        -1.00488647,  0.20010635, -0.80244805, -0.10380378, -0.60413093,
        -0.78597967],
       [ 0.15943183, -1.34861031,  0.58052277, -0.79993508,  0.17865188,
        -0.41207984, -0.6390113 ,  1.13361444, -0.49446918,  0.21561124,
        -0.03540312,  0.06256037, -0.13271672,  0.96838917,  0.74859709,
         0.73047402],
       [ 0.34869417, -0.2431448 ,  0.61619874, -0.27138817,  0.70766359,
         0.29838068,  1.66712502, -0.93158872,  1.02359046, -0.46577053,
         0.06179862,  0.52136402, -0.4659724 , -0.43674099, -1.41580205,
        -0.45366324],
       [ 0.12436744, -0.13425276,  0.19222372, -0.050556  , -0.55385554,
        -0.13988762,  0.50394111, -0.8090668 ,  0.5253116 , -0.12963408,
        -0.28035719, -0.08840669,  0.52029958, -0.84576588, -0.71729001,
         0.77746124],
       [ 1.18032983, -0.95224643, -1.19507943,  1.05081765,  0.00652372,
         0.96173471, -2.41926577,  1.63630089, -0.90617352,  0.58054031,
        -0.27354501, -0.66075364,  1.35042705,  0.68751897,  1.68421467,
        -0.77307115],
       [ 1.11105834, -1.04905073,  0.04878561,  0.8126651 ,  0.20047739,
         0.40857149, -1.25233084,  0.87260283,  0.10607076,  0.08100951,
        -0.0704001 , -1.09310938,  0.68790574, -0.59887111,  0.55503872,
        -0.39693485],
       [-0.31040234,  0.92768181,  0.3978287 , -0.9246784 , -0.7558818 ,
         0.66933396,  1.86431354, -2.20293814,  1.35168391, -0.35416802,
        -0.68689088,  0.10906915,  0.32033828, -1.288814  , -1.49078566,
        -0.49590446],
       [-0.28218851, -0.26628482,  0.34265901,  0.04403331, -1.10214692,
        -0.48419089, -2.38505233,  0.87989146, -0.5262599 ,  0.7186787 ,
        -0.1440471 , -1.18837266,  0.02346226, -0.48749235,  1.53628314,
        -0.12545696],
       [ 0.4340515 , -0.62742089,  0.84567214, -0.31368354, -0.1729571 ,
        -0.21270624, -2.2271734 ,  1.24506826, -0.76829302,  0.07778248,
         0.46123087, -0.2290079 ,  1.55825931,  0.98848587,  0.63211562,
         0.84318512],
       [-0.48095922,  1.25608632,  0.2525628 , -0.72019784,  0.82385304,
         0.31849202,  0.89306824, -1.70791041,  0.57434782, -1.11819422,
        -1.16787109, -0.11624765, -0.56187563, -0.43328798, -1.06240294,
         0.09348005],
       [ 1.10375198, -1.84870891, -0.23875625, -0.52964414,  0.09403066,
        -0.03487203, -1.50815526,  0.7442655 , -1.09837206,  0.3297744 ,
         0.03361467,  0.13758756,  1.65449918,  0.83370811,  1.51217242,
        -0.79356488],
       [ 0.59035046, -1.14848827,  0.69580869, -0.20384397, -1.07977277,
        -0.74877129, -2.33023849,  1.88741274, -0.12612334,  1.13006919,
        -0.06686066, -0.64959205,  0.46163558,  0.45794248,  2.02077812,
         0.947547  ],
       [-0.69301034,  1.09375177, -0.44975003,  0.66410715,  1.09781567,
         0.80014258,  0.02553356,  1.21997398,  0.00698922,  0.14474051,
        -0.01058037, -0.71710903, -0.52475367, -1.20956399,  0.29715381,
        -0.30589397],
       [ 0.11550181, -0.27654194, -0.3428275 , -0.51735203,  0.44155736,
        -0.57633273, -1.2621032 , -0.05282625, -0.88338172,  0.90145372,
         0.91711727,  0.58807147,  1.41716245,  0.74379707,  0.94776698,
        -0.74644035]])
    a = dec2bin(num1)
    b = dec2bin(num2)

    layer_1_values = list()
    layer_1_values.append(np.zeros(16))
    res = ''
    for position in range(binary_dim):
        x = np.array([a[binary_dim-position-1],b[binary_dim-position-1]])
        layer_1 = sigmoid(np.dot(x,synapse_0)+np.dot(layer_1_values[-1],synapse_h))
        layer_2 = sigmoid(np.dot(layer_1,synapse_1))
        layer_1_values.append(copy.deepcopy(layer_1))
        res = str(int(np.round(layer_2[0]))) + res
    decres = bin2dec(res)
    binres = res
    return decres, binres

def bin2dec(num):
    out = 0
    for index, x in enumerate(num[::-1]):
        out += int(x)*pow(2,index)
    return out

def dec2bin(num):
    l = []
    if num < 0:
        return '-' + dec2bin(abs(num))
    while True:
        num, remainder = divmod(num, 2)
        l.append(str(remainder))
        if num == 0:
            break
    l.reverse()
    p = (8 - len(l)) * ['0']
    p.extend(l)
    r = [int(r) for r in p]

    return np.array(r, dtype='uint8')

def sigmoid(x):
    return 1/(1+np.exp(-x))