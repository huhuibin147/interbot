# -*- coding: utf-8 -*-
import datetime
import traceback
import json
from comm import interRedis
from comm import interMysql
from comm import Config

def Chat2DB(groupid, qq, content):
    try:
        conn = interMysql.Connect()
        now = datetime.datetime.now()
        createtime=now.strftime('%Y-%m-%d %H:%M:%S')  
        # 插入数据  
        sql = '''
            INSERT INTO chat_logs (group_number,qq,content,create_time) 
            VALUES ( %s, %s, %s, now())
        ''' 
        args = [groupid, qq, content]
        conn.execute(sql, args)  
        conn.commit() 
    except:
        traceback.print_exc()
        conn.rollback()
    return

def Chat2Redis(groupid, qq, message):
    try:
        rds = interRedis.interRds()
        key = 'chatlog_%s' % groupid
        chatlog = rds.get(key)
        chatlog = json.loads(chatlog.decode('utf8')) if chatlog else []
        chat_msg = {'qq':qq, 'content':message, 'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        chatlog.insert(0, chat_msg)
        if len(chatlog) > 50:
            chatlog.pop()
        rds.set(key, json.dumps(chatlog))
    except:
        traceback.print_exc()
    return