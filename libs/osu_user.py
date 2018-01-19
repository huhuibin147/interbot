# -*- coding: utf-8 -*-
import random
import traceback
from comm import interRequest
from comm import interMysql
from comm import Config

class Osuer():
    def __init__(self, uid=None, uname=None):
        self.userinfo = None
        self.userdbinfo = None
        self.userbp = None
        self.uid = uid
        self.uname = uname

    def get_user_info(self, uid=None):
        uid = uid if uid else self.uid
        url = 'https://osu.ppy.sh/api/get_user?k=%s&u=%s' % (Config.OSU_API_KEY, uid)
        r = interRequest.interReq(url)
        ret = r.get()
        if not ret:
            return None
        self.userinfo = ret[0]
        return self.userinfo

    def get_user_bp(self, uid=None, m=0, limit=10):
        uid = uid if uid else self.uid
        url = 'https://osu.ppy.sh/api/get_user_best?k=%s&u=%s&m=%s&limit=%s' % (Config.OSU_API_KEY, uid, m ,limit)
        r = interRequest.interReq(url)
        ret = r.get()
        self.userbp = ret
        return self.userbp

    def get_user_from_db(self, qq):
        conn = interMysql.Connect()
        sql = 'SELECT * FROM user where qq = %s'
        ret = conn.query(sql, qq)
        if not ret:
            return None
        self.userdbinfo = ret[0]
        return self.userdbinfo

    def get_user_pp(self, uid):
        if not self.get_user_info(uid):
            return None
        return self.userinfo['pp_raw']

    def get_recent(self, uid=None, m=0, limit=10):
        uid = uid if uid else self.uid
        url = 'https://osu.ppy.sh/api/get_user_recent?k=%s&u=%s&m=%s&limit=%s' % (Config.OSU_API_KEY, uid, m ,limit)
        r = interRequest.interReq(url)
        ret = r.get()
        self.userbp = ret
        return self.userbp
        

    def insert2DB(self, qq, osuid, groupid, osuname, name=None):
        try:
            conn = interMysql.Connect()
            sql = '''
                insert into user
                    (qq, osuid, name, groupid, osuname) 
                values
                    (%s,%s,%s,%s,%s)
                on duplicate key update
                    osuid = %s, osuname = %s, name = %s
            '''
            args = [qq, osuid, name, groupid, osuname, osuid, osuname, name]
            ret = conn.execute(sql, args)
            conn.commit()
            return ret
        except:
            traceback.print_exc()
            conn.rollback()
            return 0

    def check_user(self, uid):
        '''pp估计计算'''
        try:
            userinfo = self.get_user_info(uid)
            if not userinfo:
                return 0,0,0
            bpinfo = self.get_user_bp(uid)
            pp = userinfo['pp_raw']
            count_num = 0
            count_pp = 0
            maxpp = 0
            conn = interMysql.Connect()
            for r in bpinfo:
                maxcombo1 = int(r['maxcombo']) - 10
                maxcombo2 = int(r['maxcombo']) + 10
                c50 = float(r['count50'])
                c100 = float(r['count100'])
                c300 = float(r['count300'])
                cmiss = float(r['countmiss'])
                acc = round((c50*50+c100*100+c300*300)/(c50+c100+c300+cmiss)/300*100,2)
                acc1 = acc - 0.2
                acc2 = acc + 0.2
                args = [r['beatmap_id'], r['enabled_mods'], acc1, acc2, maxcombo1, maxcombo2]
                sql='''
                    SELECT avg(u.pp_raw) a, count(1) b from osu_bp b INNER JOIN osu_user u on b.user_id=u.user_id where b.beatmap_id = %s and b.mods=%s and b.acc BETWEEN %s and %s and b.maxcombo BETWEEN %s and %s 
                '''
                res = conn.query(sql, args)
                
                res = res[0]
                if res['a'] is None:
                    continue
                if res['a'] > maxpp:
                    maxpp = res['a']
                if res['b'] != 1: 
                    count_num += 1
                    count_pp += res['a']
            if count_num == 0:
                yugu_pp = pp
            else:
                yugu_pp = round(count_pp/count_num)
            if maxpp == 0:
                maxpp = float(pp)
            return pp,yugu_pp,round(maxpp)
        except:
            traceback.print_exc()
            return 0,0,0

    def choiceMap(self, uid):
        '''低端推荐pp图'''
        try:
            conn = interMysql.Connect()
            pp = self.get_user_pp(uid)
            if not pp:
                return 0,0
            pp = float(pp)
            sql = '''
                SELECT beatmap_id,count(beatmap_id) num FROM osu_user ta INNER JOIN osu_bp tb on ta.user_id = tb.user_id where ta.pp_raw BETWEEN %s and %s GROUP BY beatmap_id ORDER BY num desc limit 0,20; 
            '''
            res = conn.query(sql, [pp, pp+20])
            if not res:
                return 0,0
            ret = random.choice(res)
            return ret['beatmap_id'],ret['num']
        except:
            traceback.print_exc()
            return 0,0