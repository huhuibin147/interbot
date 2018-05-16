# -*- coding: utf-8 -*-
import random
import json
import traceback
import datetime
import re
from comm import interRedis
from comm import Config
from libs import chatlog

def speak(globValue):
    return randMsg(globValue)

def autoreply(globValue):
    if random.randint(0,100) > Config.AUTOREPLY_PCT:
        return randMsg(globValue)
    return None

def randMsg(globValue):
    if not globValue.get('msglist'):
        return 'emmm...'
    msg = random.sample(globValue['msglist'],1)
    return msg[0]

def speak_level_check(groupid):
    try:
        rds = interRedis.interRds()
        key = 'chatlog_%s' % groupid
        chatlog = rds.get(key)
        chatlog = json.loads(chatlog.decode('utf8')) if chatlog else [{}]
        if int(chatlog[0].get('qq',0)) == Config.LOGGING_QQ:
            return 0
        else:
            return 1
    except:
        traceback.print_exc()
        return

def msg2Redis(b):
    chatlog.Chat2Redis(b.group_id, b.qq, b.message)
    return

def msg2Mysql(b):
    f_msg = re.sub('\[.*\]','',b.message)
    if not f_msg or f_msg == ' ' or len(f_msg) > 250:
        return
    chatlog.Chat2DB(b.group_id, b.qq, f_msg)
    return

def egg(b):
    if b.message == '彩蛋':
        return '你想探索点什么?'
    elif b.message == 'interbot0':
        return '这不是彩蛋，你好像发现了什么?'
    elif b.message == '傻dalou':
        return '解锁1号彩蛋，调戏dalou!'

    if b.qq == 1004121460:
        if b.message == 'int妹妹':
            return '解锁专属彩蛋,int妹妹qwq'

    return 0