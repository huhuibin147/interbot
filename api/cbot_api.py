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
    if random.randint(0,100) > 99:
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

def msg2Redis(b):
    chatlog.Chat2Redis(b.group_id, b.qq, b.message)

def msg2Mysql(b):
    f_msg = re.sub('\[.*\]','',b.message)
    if not f_msg or f_msg == ' ' or len(f_msg) > 250:
        return
    chatlog.Chat2DB(b.group_id, b.qq, f_msg)