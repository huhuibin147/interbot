# -*- coding: utf-8 -*-
import traceback
import random
import logging
from comm import interMysql
from comm import Config
from api import cbot_api

def msg_recollect(globValue):
    try:
        conn = interMysql.Connect()
        sql = '''
            SELECT content FROM chat_logs
        '''
        res = conn.query(sql)
        if not res:
            return
        shuf_res = res
        random.shuffle(shuf_res)
        limit_cnt = Config.LIMIT_SEQ_NUM
        msglist = globValue.get('msglist', set([]))
        for i in range(len(msglist)):
            msglist.pop()
        for r in shuf_res:
            if len(msglist) > limit_cnt:
                break 
            if len(r['content']) < 30:
                msglist.add(r['content'])
        globValue['msglist'] = msglist
        logging.info('词库自动更新,条数:%s' % len(msglist))
    except:
        traceback.print_exc()

def speak_task(bot, globValue):
    groupid = random.sample(Config.SPEAK_GROUP_LIST,1)[0]
    if random.randint(0,100) > 95 and cbot_api.speak_level_check(groupid):
        logging.info('触发群%s的speak'%groupid)
        bot.send_group_msg(group_id=groupid, message=cbot_api.speak(globValue))
    return