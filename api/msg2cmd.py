# -*- coding: utf-8 -*-
import sys
import os
import time
import json
import requests
import random
import traceback
import threading
from api import help_api
from api import test_api
from api import user_api
from api import cbot_api
from api import rank_api
from api import req_api
from api import sp_api
from api import stats
from api import chattrain_api
from api import rank_tab
from api import chart_api
from api import play_api
from libs import args_func
from libs import chatlog
from api import msg_permission
from comm import Config
from draws import drawRank
from draws import drawRLine
from draws import draw_data

def invoke(b):

    # 信息收集
    cbot_api.msg2Redis(b)
    cbot_api.msg2Mysql(b)

    # test
    # play_api.recieve(b)

    if b.qq == Config.BOT2:
        return 'not define'

    eggmsg = cbot_api.egg(b)
    if eggmsg:
        return eggmsg


    if b.message == '!inter':
        return help_api.new_help()

    # elif b.message == '!roll':
    #     return str(random.randint(0, 100))

    # elif b.message == '!mu':
    #     uid = args_func.uid_find_or_input(b.message[4:], b.qq, gid=b.group_id)
    #     return 'https://osu.ppy.sh/u/%s' % uid

    # elif b.message == '!tt':
    #     uid = args_func.uid_find_or_input(b.message[4:], b.qq, gid=b.group_id)
    #     if not uid:
    #         return '请绑定ID'
    #     return uid

    # elif '!test' in b.message:
    #     uid = args_func.uid_find_or_input(b.message[6:], b.qq, gid=b.group_id)
    #     if not uid:
    #         return '你不适合屙屎，删游戏吧(请绑定ID'
    #     return test_api.test(uid)

    # elif '!myinfo' == b.message:
    #     return user_api.myinfo(b.qq, gid=b.group_id)

    # elif '!bbp' in b.message:
    #     uid = args_func.uid_find_or_input(b.message[5:], b.qq, return_type=1, gid=b.group_id)
    #     if not uid:
    #         return '你有能看bp吗???(请绑定ID'
    #     return user_api.get_bp5info(uid)

    elif '!check' in b.message:
        uid = args_func.uid_find_or_input(b.message[7:], b.qq, return_type=1, gid=b.group_id)
        if not uid:
            return '你太才菜了不想check你(请绑定ID'
        return user_api.check(uid)

    elif '!map' in b.message:
        uid = args_func.uid_find_or_input(b.message[5:], b.qq, return_type=1, gid=b.group_id)
        if not uid:
            return '本bot根本不想给你推荐图QwQ(请绑定ID'
        return user_api.map(uid)

    elif '!repeats' in b.message:
        return b.message[8:]

    # elif '!help' == b.message:
    #     return 'inter已经去世，没有留下任何文档!!!'

    elif '[CQ:at,qq=%s]'%Config.LOGGING_QQ in b.message and b.qq != Config.DALOUBOT_QQ:
        return cbot_api.speak(b.globValue)

    # elif '!!' == b.message[:2]:
    #     uid = args_func.uid_find_or_input(b.message[3:], b.qq, return_type=1, gid=b.group_id)
    #     if not uid:
    #         return '请绑定ID,usage{setid uid}'
    #     url = "http://interbot.cn/osu2/stat2?u=%s" % uid
    #     r = requests.get(url, timeout=10)
    #     staturl = r.text
    #     return "[CQ:image,file=%s]" % staturl

    elif '!rl' == b.message:
        url = "http://interbot.cn/osu2/me"
        data = {
            "qqid": b.qq,
            "groupid": b.group_id
        }
        r = requests.post(url, timeout=10, data=data)
        if 'http' in r.text:
            staturl = r.text
            return "[CQ:image,cache=0,file=%s]" % staturl
        else:
            return r.text
        return '异常'

    elif '!mc' == b.message:
        msg = test_api.mc()
        return '[CQ:at,qq=%s] %s' % (b.qq, msg)

    elif '!setid' in b.message:
        uid = b.message[7:]
        msg = user_api.setid(uid, b.qq, b.group_id)
        return '[CQ:at,qq=%s] %s' % (b.qq, msg)
        
    # elif '!kw' in b.message:
    #     try:
    #         return chattrain_api.kw(b.message[4:], b.globValue)
    #     except:
    #         return '%s不在interbot的词汇表中' % b.message[4:]

    elif '!trainwords' == b.message and b.qq == Config.SUPER_QQ:
        try:
            b.bot.send_group_msg(group_id=b.group_id, message='啊啊啊!interbot被抓去训练了!')
            chattrain_api.chat_train_job(b.globValue, b.gV_Lock, skip_rds=True)
            return 'interbot感觉还行,训练归来!'
        except:
            traceback.print_exc()
            return 'interbot感觉不对劲,训练异常!'

    # elif '!skill' in b.message:
    #     uid = args_func.uid_find_or_input(b.message[7:], b.qq, return_type=1, gid=b.group_id)
    #     return req_api.get_skill(uid)

    # elif '!vssk' in b.message:
    #     uid = args_func.uid_find_or_input(qq=b.qq, return_type=1, gid=b.group_id)
    #     if not uid:
    #         return '本bot根本不认识你(请绑定ID'
    #     return req_api.skill_vs(uid, b.message[6:])

    elif '!sp' == b.message:
        return sp_api.get_xinrenqun_replay()

    elif '!upage' in b.message:
        slist = b.message[7:].replace('，',',').split(',')
        page = 1 if len(slist) == 1 else int(slist[1])
        return req_api.get_userpage(slist[0], page)
        
    elif '!kr' == b.message:
        return rank_api.talk_rank(b.bot, b.group_id, nums=7)

    elif '!cr' == b.message:
        return rank_api.cmd_rank(b.group_id, nums=7)

    elif '!cr2' in b.message and b.qq == Config.SUPER_QQ:
        date = b.message[5:]
        return rank_api.cmd_rank2(date, nums=7)

    # elif '!todaybp' in b.message and b.group_id not in msg_permission.PermissionGroup:
    #     uid = args_func.uid_find_or_input(b.message[9:], b.qq, return_type=1, gid=b.group_id)
    #     return test_api.todaybp(uid)

    elif '!2rctpp' in b.message and b.group_id not in msg_permission.PermissionGroup:
        uid = args_func.uid_find_or_input(b.message[7:], b.qq, return_type=1, gid=b.group_id)
        try:
            rank_tab.upload_rec(uid, b.group_id, limit=10)
        except:
            traceback.print_exc()
        return test_api.rctpp(uid)

    elif '!upd' == b.message:
        uid = args_func.uid_find_or_input(qq=b.qq, return_type=1, gid=b.group_id)
        if not uid:
            return '请绑定ID,再进行upload操作!'
        return rank_tab.upload_rec(uid, b.group_id, limit=10)

    elif '!hd' == b.message:
        return 'dalou选的 %s (下载请去这里http://osu.uu.gl/d/26932 )' % (Config.MAP_URL_PREF + str(Config.MAPID))

    elif '!hdrank2' == b.message:
        uid = args_func.uid_find_or_input(qq=b.qq, return_type=1, gid=b.group_id)
        if not uid:
            uid = -1
        return rank_tab.get_rankinfo(uid, b.group_id, Config.MAPID, hid=1, mod=-1)

    elif '!rank2' == b.message[0:6]:
        uid = args_func.uid_find_or_input(qq=b.qq, return_type=1, gid=b.group_id)
        if not uid:
            uid = None
        msgs = b.message.split(' ')
        if len(msgs) > 1:
            bid = str(msgs[1])
        return rank_tab.get_rankinfo(uid, b.group_id, bid, hid=1, mod=-1)

    elif '!hdrank' == b.message:
        uid = args_func.uid_find_or_input(qq=b.qq, return_type=0, gid=b.group_id)
        if not uid:
            uid = -1
        drawRank.start(Config.MAPID, b.group_id, hid=1, mods=-1, uid=uid)
        return '[CQ:image,file=file://%s\%s]' % (Config.IMAGE_PATH, 'rank.png')

    elif '!rank' == b.message[0:5] and b.message != '!rankme':
        uid = args_func.uid_find_or_input(qq=b.qq, return_type=0, gid=b.group_id)
        if not uid:
            uid = -1
        msgs = b.message.split(' ')
        bid = args_func.alias2bid(msgs)
        try:
            drawRank.start(bid, b.group_id, hid=1, mods=-1, uid=uid)
        except:
            traceback.print_exc()
            return '打了就是你的top\nosu.ppy.sh/b/%s'%bid
        return '[CQ:image,file=file://%s\%s]' % (Config.IMAGE_PATH, 'rank.png')

    elif '!setb' == b.message[0:5]:
        return rank_tab.set_alias(b.message)

    elif '!del' == b.message[0:4]:
        msgs = b.message.split(' ')
        return rank_tab.del_alias(msgs[1])

    elif '!bind' == b.message[0:5]:
        return rank_tab.bind_irc(b.message, b.qq)

    elif '!top' in b.message:
        uid,uname = args_func.uid_uname(uname=b.message[5:], qq=b.qq)
        if not uname:
            return '这谁啊???本Bot不认识这个人'
        ret = rank_tab.get_topsnum(uid, b.group_id, hid=1, mod=-1)
        return ret.replace('{uid}', uname)

    elif '!ts' == b.message:
        return rank_tab.get_topsrank(b.group_id)

    elif '榜单介绍' == b.message:
        return help_api.rank_help()

    elif b.message == '!upimg':
        uid = args_func.uid_find_or_input(qq=b.qq, return_type=0, gid=b.group_id)
        if not uid:
            return '请绑定ID,再进行upimg操作!'
        draw_data.down_images_from_ppy([uid])
        return '刷新成功(可能吧?'

    elif '!s' == b.message:
        return stats.get_stats(b.qq, gid=b.group_id)

    elif '!days' in b.message:
        try:
            days = b.message.split(' ')
            if len(days) > 1:
                days = int(days[1])
            else:
                days = 0
            msg = stats.get_stats(b.qq, days, gid=b.group_id)
        except:
            msg = '请好好输参数...(!days 2)'
        return msg

    elif b.message == '!status' and b.qq == Config.SUPER_QQ:
        return stats.update_status()
        
    elif b.message == '!restart' and b.qq == Config.SUPER_QQ:
        python = sys.executable
        os.execl(python, python, * sys.argv)

    elif b.message == 'interbot':
        return '[CQ:image,file=file://%s\%s]' % (Config.IMAGE_PATH, 'bq\\wutou.jpg')

    elif b.message == 'interbot2':
        return '[CQ:image,file=file://%s\%s]' % (Config.IMAGE_PATH, 'bq\\buwutou.jpg')

    elif b.message == 'interbot3':
        return '[CQ:image,file=file://%s\%s]' % (Config.IMAGE_PATH, 'bq\\interqb.jpg')

    elif b.message == '!zfb':
        return '[CQ:image,file=file://%s\%s] 记得留下备注(id)!' % (Config.IMAGE_PATH, 'bq\\zfb.jpg')

    elif b.message == 'interbot4':
        return '快给钱不然不卖萌!!!'

    elif '!pp' in b.message:
        uid = args_func.uid_find_or_input(b.message[4:], b.qq, return_type=1, gid=b.group_id)
        return test_api.check2(uid)

    elif '!add' in b.message:
        mls = b.message.split(' ')
        if len(mls) != 3:
            return 'usage:{add x1 x2}'
        return test_api.add_api(mls[1], mls[2])

    elif '!chartadd' in b.message:
        args = b.message.split(' ')[1:]
        return chart_api.add(*args)

    elif '!expectadd' in b.message:
        args = b.message.split(' ')[1:]
        return chart_api.addexpect(*args)

    elif 'pick' in b.message or 'up' in b.message \
        or 'my' in b.message or 'submit' or 'rctpp' in b.message:
        uid = args_func.uid_find_or_input(qq=b.qq, return_type=1, gid=b.group_id)
        rank_tab.upload_rec(uid, b.group_id, limit=10)
        return 'not define'

    elif '!copy' == b.message and b.qq == Config.SUPER_QQ:
        t = threading.Thread(target=delaySend, args=(b, 'interbot?', 3))
        t.start()
        print(os.system('E:\\interbot\\interbot\\2st.bat'))

    else:
        msg = cbot_api.autoreply(b.globValue)
        if b.group_id not in Config.SPEAK_GROUP_LIST:
            return 'not define'
        chatlog.Chat2Redis(b.group_id, Config.LOGGING_QQ, msg)
        return msg if msg else 'not define'

    return 'not define'

def delaySend(b, msg, dtime):
    time.sleep(dtime)
    b.bot.send(b.context, msg)