# -*- coding: utf-8 -*-

import traceback
import json
from comm import interRedis
from comm import interMysql
from comm import interRedis



def talk_rank(b, groupid, nums=7):
    key = 'TALK_RANK_%s' % groupid
    try:
        rds = interRedis.interRds()
        v = rds.get(key)
        if not v:
            rank_list = talkFromDB(groupid, nums)
            msg = '话痨榜\n'
            for i,r in enumerate(rank_list):
                try:
                    usercard = b.get_group_member_info(group_id=groupid,user_id=r['qq'])['card']
                except:
                    usercard = '%s(褪群了' % r['qq']
                msg = msg + '%s.%s  --%s\n' % (i+1, usercard, r['cnt'])
            ret = msg[:-1]
            rds.setex(key, json.dumps(ret), 60)
        else:
            ret = json.loads(v)
        return ret
    except:
        traceback.print_exc()
        return 'emmm...炸了...'

def cmd_rank(groupid, nums=7):
    key = 'CMD_RANK_%s' % groupid
    try:
        rds = interRedis.interRds()
        v = rds.get(key)
        if not v:
            rank_list = cmdFromDB(groupid, nums)
            msg = '指令榜\n'
            for i,r in enumerate(rank_list):
                msg = msg + '%s.%s  --%s\n' % (i+1, r['content'], r['cnt'])
            ret = msg[:-1]
            rds.setex(key, json.dumps(ret), 60)
        else:
            ret = json.loads(v)
        return ret
    except:
        traceback.print_exc()
        return 'emmm...炸了...'



def talkFromDB(groupid, nums):
    try:
        conn = interMysql.Connect()
        sql = '''
            SELECT qq, count(1) cnt 
            FROM chat_logs 
            WHERE group_number=%s GROUP BY qq 
            ORDER BY cnt desc limit %s'''
        args = [groupid, nums]
        ret = conn.query(sql, args)
        if not ret:
            return []
        return ret
    except:
        traceback.print_exc()
    return

def cmdFromDB(groupid, nums):
    try:
        conn = interMysql.Connect()
        sql = '''
            SELECT content,count(1) cnt 
            FROM chat_logs 
            WHERE group_number=%s and content like '!%%' 
            GROUP BY content 
            ORDER BY cnt desc LIMIT %s'''
        args = [groupid, nums]
        ret = conn.query(sql, args)
        if not ret:
            return []
        return ret
    except:
        traceback.print_exc()
    return