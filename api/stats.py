# -*- coding: utf-8 -*-
import pymysql  
import time
import json
import sched
import requests
import threading
import datetime
import traceback
from qqbot import qqbotsched


def stats_sched():
    t = threading.Thread(target=sched_day_insert, args=())
    t.start()
    return


def sched_day_insert():
    o = osu()
    try:
        o.time_insert()
    except:
        print('定时任务出错')
        traceback.print_exc()

def get_stats(qq, days=0, gid=None):
    o = osu()
    res = o.get_myinfo(qq, gid)
    if not res:
        return '未绑定,请使用setid!'
    return o.osu_stats(res[5], days)

def update_status():
    o = osu()
    # 今日更新数量
    uplist = o.today_updates()
    # 绑定用户数量
    bindlist = o.get_osuid_list_fromDB()
    # 调整为osuid
    uplist_new = uplist
    bindlist_new = bindlist
    len_up = len(set(uplist))
    len_bind = len(set(bindlist))
    auto_flag = 0
    error_user = set(bindlist_new) - set(uplist_new)
    len_error = len(error_user)
    # print('up的数量:%s,bind的数量:%s,error的数量:%s'%(len_up,len_bind,len_error))
    if len_error == 0:
        msg = '今日更新数据无误,更新条数:%s' % len_up
    elif len_error < 0:
        msg = '今日更新数据异常,更新条数:%s大于绑定用户数:%s' % (len_up,len_bind)
    else:
        msg = '今日更新条数:%s,未更新数量:%s' % (len_up,len_error)
        if len_bind-len_up > 3:
            # msg += ',开始自动更新剩余用户...'
            print('自动更新列表:%s'%error_user)
            auto_flag = 1
        else:
            msg += ',这几个用户被放弃了:%s' % list(error_user)
    if auto_flag:
        error_user = list(error_user)
        o._inerts_many(error_user)
        print('***********待清理列表:%s**********'%error_user)
        msg += '\n操作:自动插入完成!'
        # 自动清理
        # if o.del_users(error_user):
        #     bot.SendTo(contact, '如下列表用户被自动清理:%s'%error_user)
        # else:
        #     bot.SendTo(contact, '自动清理异常!')
    return msg


def data_format(lists):
    res_list = []
    for l in lists:
        new_data = l.lower()
        new_data = new_data.replace('_',' ')
        new_data = new_data.replace('%20',' ')
        res_list.append(new_data)
    return res_list

class osu:

    def __init__(self):
        self.con = pymysql.connect(host='127.0.0.1',user='root',password='123456',db='osu')
        self.headers = {
            'accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding' : 'gzip, deflate, br',
            'accept-language' : 'zh-CN,zh;q=0.9',
            'cookie' : '__cfduid=dcd84cc446800e949d5088570b4fa54c21490246214; _ga=GA1.2.2055967706.1490246215; cf_clearance=a233723e29ddfea8d91182fce773a828db7cc04e-1512707357-31536000; __utmz=226001156.1518163818.69.5.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; _encid=%7B%22name%22%3A%22interbot%22%2C%22email%22%3A%22%22%2C%22_source%22%3A%22a%22%7D; phpbb3_2cjk5_u=11788070; phpbb3_2cjk5_u=11788070; phpbb3_2cjk5_k=5e74a60e99ec406f; phpbb3_2cjk5_k=5e74a60e99ec406f; phpbb3_2cjk5_sid=fbca0496b3d5366edf1e0b929c75c363; phpbb3_2cjk5_sid=fbca0496b3d5366edf1e0b929c75c363; phpbb3_2cjk5_sid_check=d3165160830ec9259e84adc94a9660fbca629157; phpbb3_2cjk5_sid_check=d3165160830ec9259e84adc94a9660fbca629157; __utma=226001156.2055967706.1490246215.1519746481.1520072282.81',
            'upgrade-insecure-requests' :  '1',
            'user-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        } 
        self.osu_api_key = 'b68fc239f6b8bdcbb766320bf4579696c270b349'

    def get_con(self):
        self.con = pymysql.connect(host='127.0.0.1',user='root',password='123456',db='osu')

    def get_cursor(self):
        return self.con.cursor()

    def get_myinfo(self, qq, gid=None):
        '''qq绑定信息'''
        try:
            cur = self.get_cursor()
            sql = '''
                SELECT * FROM user where qq = %s
            '''
            args = [qq]
            if gid:
                sql += ' and groupid = %s'
                args.append(gid)
            cur.execute(sql, args)
            res = cur.fetchall()
            if not res:
                return 0
            return  res[0]
        except:
            traceback.print_exc()
            return 0

    def today_updates(self):
        '''今日更新数据'''
        cur = self.get_cursor()
        sql = '''
            SELECT osuid FROM user2 where time=%s
        '''
        today = self.get_today()
        cur.execute(sql, today)
        res = cur.fetchall()
        ret = [r[0] for r in res]
        return  ret

    def del_users(self, users):
        '''清理用户'''
        try:
            cur = self.get_cursor()
            sql = '''
                DELETE FROM user where osuname in (%s)
            '''
            in_p = ','.join(map(lambda x: '%s', users))
            sql = sql % in_p
            res = cur.execute(sql, users)
            self.con.commit()
            return res
        except:
            self.con.rollback()
            traceback.print_exc()
            return 0


    def __del__(self):
        self.con.close()

    def insert_user(self,*user):
        try:
            cur = self.get_cursor()
            sql = 'insert into user2(username,pp,acc,pc,rank,tth,time,osuid) values(%s,%s,%s,%s,%s,%s,%s,%s)'
            result = cur.execute(sql,tuple(user))
            print('插入数据结果:'+str(result))
            self.con.commit()
        except:
            self.con.rollback()
            pass

    def get_user_fromDB(self,username,days=0):
        cur = self.get_cursor()
        if not days:
            if self.is_today():
                time = self.get_today()
            else:
                time = self.get_yes()
        else:
            time = self.get_daystime(days)
        sql = 'select * from user2 where username=%s and time>=%s limit 1'
        print('查询时间:'+time)
        result = cur.execute(sql,(username,time))
        print('查询数据结果:'+str(result))
        if result:
            user_info = cur.fetchall()
            #print(user_info)
            return user_info
        else:
            return ''

    def get_user_list_fromDB(self):
        print('查询用户列表..')
        cur = self.get_cursor()
        sql = 'SELECT osuname from user GROUP BY osuname'
        result = cur.execute(sql)
        user_list = cur.fetchall()
        ret = [r[0] for r in user_list]
        return  ret
        return user_list

    def get_osuid_list_fromDB(self):
        print('查询用户列表..')
        cur = self.get_cursor()
        sql = 'SELECT osuid from user GROUP BY osuid'
        result = cur.execute(sql)
        user_list = cur.fetchall()
        ret = [r[0] for r in user_list]
        return  ret
        return user_list

    def exist_user(self,uid):
        #print('查询用户是否存在')
        cur = self.get_cursor()
        sql = 'SELECT 1 from user2 where username="'+uid+'" limit 1'
        result = cur.execute(sql)
        user_list = cur.fetchall()
        return user_list

    def check_today_user(self,uid,time):
        print('%s已存在今日数据'%uid)
        cur = self.get_cursor()
        sql = '''SELECT 1 from user2 where username=%s and time = %s limit 1'''
        result = cur.execute(sql, [uid,time])
        user_list = cur.fetchall()
        return user_list

    def osu_stats(self,uid,days=0):
        try:
            print('查询用户:'+uid)
            res = requests.get('https://osu.ppy.sh/api/get_user?k=%s&u=%s'%(self.osu_api_key,str(uid)),timeout=5) # headers=self.headers

            result = json.loads(res.text)
            if not result:
                return ''
            #print(result)
            result = result[0]
            username = result['username']
            osuid = result['user_id']
            pp = result['pp_raw']
            in_pp = float(pp)
            #print(in_pp)
            rank = result['pp_rank']
            acc1 = round(float(result['accuracy']),2)
            #print(acc1)
            acc = str(acc1)
            pc =  result['playcount']
            count300 = result['count300']
            count100 = result['count100']
            count50 = result['count50']
            tth = eval(count300)+eval(count50)+eval(count100)
            tth_w = str(tth//10000)
            #与本地数据比较
            u_db_info = self.get_user_fromDB(uid, days)
            if u_db_info:
                info = u_db_info[0]
                add_pp = str(round(in_pp - float(info[2]),2))
                add_rank = info[5] - int(rank)
                if add_rank >= 0:
                    add_rank = '+'+str(add_rank)
                else:
                    add_rank = str(add_rank)
                add_acc =  round(acc1 - float(info[3]),2)
                if add_acc >=0.0:
                    add_acc = '+'+str(add_acc)
                else:
                    add_acc = str(add_acc)
                add_pc = str(int(pc) - int(info[4]))
                add_tth = str(tth - int(info[6]))
                times = info[7].strftime('%Y-%m-%d')
                d = username+'\n'+pp+'pp(+'+add_pp+')\n'+'rank: '+rank+'('+add_rank+')\n'+'acc  : '+acc+'%('+add_acc+')\n'+'pc    : '+pc+'pc(+'+add_pc+')\n'+'tth   : '+tth_w+'w(+'+add_tth+')\n'+times
            else:
                d = username+'\n'+pp+'pp(+0)\n'+'rank: '+rank+'(+0)\n'+'acc : '+acc+'%(+0)\n'+'pc  : '+pc+'pc(+0)\n'+'tth  : '+tth_w+'w(+0)\n'+str(datetime.date.today())
            #in_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            is_exist = self.exist_user(uid)
            # if not is_exist:
            #     print('用户不存在,进行插入')
            #     #检测时间段0-9点
            #     if self.is_today():
            #         in_time = self.get_today()
            #     else:
            #         in_time = self.get_yes()
            #     self.insert_user(username,in_pp,acc1,pc,rank,tth,in_time,osuid)
            return d
        except:
            traceback.print_exc()

    def getU(self,uid):
        try:
            print('获取用户:'+uid)
            res = requests.get('https://osu.ppy.sh/api/get_user?k=%s&u=%s'%(self.osu_api_key,str(uid)),timeout=2)#headers=self.headers
        except:
            print('获取失败:'+uid)
            res = ''
        return res

    def get_today(self):
        today = datetime.date.today()
        return str(today)+' 9:00:00'

    def get_yes(self):
        now = datetime.datetime.now()
        date = now - datetime.timedelta(days = 1)
        return date.strftime('%Y-%m-%d')+' 9:00:00'

    def get_daystime(self, days):
        now = datetime.datetime.now()
        date = now - datetime.timedelta(days = days)
        return date.strftime('%Y-%m-%d')+' 9:00:00'

    def is_today(self):
        #0昨天 1今天
        now_hour = time.strftime("%H%M%S")
        cmp_hour = 90000
        if int(now_hour) - cmp_hour < 0:
            return 0
        else:
            return 1

    def is_insert_today(self):
        cur = self.get_cursor()
        time = self.get_today()
        sql = 'SELECT 1 from user2 where time="'+time+'" LIMIT 1'
        result = cur.execute(sql)
        user_list = cur.fetchall()
        return user_list

    def auto_inert(self):
        self._inerts_many(self.get_user_list_fromDB())

    def _inerts_many(self, userlist):
        try:
            today = datetime.date.today()
            in_time = str(today)+' 9:00:00'
            for uid in userlist:
                try:
                    res = self.getU(uid)
                    get_num = 0
                    while not res:
                        if get_num < 5:
                            get_num += 1
                            res = self.getU(uid)
                        else:
                            break 
                    if not res:
                        continue
                    result = json.loads(res.text)  
                    if result:         
                        result = result[0]
                    else:
                        continue
                    username = result['username']
                    osuid = result['user_id']
                    pp = result['pp_raw']
                    in_pp = float(pp)
                    rank = result['pp_rank']
                    acc1 = round(float(result['accuracy']),2)
                    pc =  result['playcount']
                    count300 = result['count300']
                    count100 = result['count100']
                    count50 = result['count50']
                    tth = eval(count300)+eval(count50)+eval(count100)
                    self.insert_user(username,in_pp,acc1,pc,rank,tth,in_time,osuid)
                    print(uid+'插入成功')
                except:
                    print('[%s]插入失败'%uid)
                    traceback.print_exc()
        except:
            print('auto_inert错误')
            traceback.print_exc()

    def insert_forday(self):
        print('开始执行定时插入任务')
        self.auto_inert()
        print('定时插入任务结束')

    def time_insert(self):
        '''定时任务'''
        today = datetime.date.today()
        now_hour = time.strftime('%H%M%S')
        is_run = int(now_hour) - 90000
        if  is_run < 0:
            print('延时执行')
            now = datetime.datetime.now()
            stats = datetime.datetime(today.year,today.month,today.day,9,0,0)
            delay = (stats - now).seconds
            print(delay)
            s = sched.scheduler(time.time, time.sleep)
            s.enter(delay,0,self.insert_forday,())
            s.run()
        else:
            print('超过时间,立即执行定时任务')
            if not self.is_insert_today():
                print('今日数据不存在,准备抓取...')
                self.insert_forday()
            else:
                print('今日数据已存在,不需要抓取')
            #self.insert_forday()
            print('定时任务结束')

    ###############数据库扩展方法#################
    def up(self):
        uplist = []
        for username in uplist:
            cur = self.get_cursor()
            print('查询用户:'+username)
            res = requests.get('https://osu.ppy.sh/api/get_user?k=%s&u=%s'%(self.osu_api_key,username),headers=self.headers,timeout=5)

            result = json.loads(res.text)
            if not result:
                print ('%s查询失败'%username)
                continue
            result = result[0]
            user_id = result['user_id']
            sql = '''
                UPDATE user2 set osuid = %s where username = %s
            '''
            ret = cur.execute(sql, [user_id, username])
            print (ret)
            self.con.commit()
    ###############数据库扩展方法#################