# -*- coding: utf-8 -*-
import traceback
import random
import logging
from comm import interMysql
from comm import Config
from api import cbot_api
from libs import chatlog

def msg_recollect(globValue, gV_Lock):
    try:
        conn = interMysql.Connect()
        sql = '''
            SELECT content FROM chat_logs
        '''
        csql = 'SELECT count(1) c FROM chat_logs'
        num = conn.query(sql)[0]['c']
        if Config.DEBUG == 1:
            sql += ' limit %s,10000' % random.randint(0, int(num)-10000)
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
        gV_Lock.acquire()
        globValue['msglist'] = msglist
        gV_Lock.release()
        logging.info('词库自动更新,条数:%s' % len(msglist))
    except:
        traceback.print_exc()
    return

def speak_task(bot, globValue):
    try:
        groupid = random.sample(Config.SPEAK_GROUP_LIST,1)[0]
        if random.randint(0,100) > Config.AUTOSPEAK_PCT and cbot_api.speak_level_check(groupid):
            logging.info('触发群%s的speak'%groupid)
            msg = cbot_api.speak(globValue)
            bot.send_group_msg(group_id=groupid, message=msg)
            # 自消息处理
            chatlog.Chat2Redis(groupid, Config.LOGGING_QQ, msg)
    except:
        traceback.print_exc()
    return