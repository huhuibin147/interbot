# -*- coding: utf-8 -*-
# 抓取接口

import re
import json
import traceback
import requests
import html.parser
from comm import Config

def get_skill(uid):
    try:
        res = requests.get('http://osuskills.tk/user/'+str(uid),timeout=10)
        if not res:
            return '没有数据,太弱了!!'
        s_msg = uid+"'s skill\n"
        value = re.compile(r'<output class="skillValue">(.*?)</output>')
        values = value.findall(res.text)
        if not values:
            return '那个破网站连不上!!'
        skills = ['Stamina', 'Tenacity', 'Agility', 'Accuracy', 'Precision', 'Reaction', 'Memory', 'Reading']
        #skills_list = list(map(lambda x,y:x+y ,skills,values))
        for i,s in enumerate(skills):
            val = int(values[i])
            if  1000 > val >= 100:
                snum = int(values[i][0:1])
            elif val >= 1000:
                snum = int(values[i][0:2])
            else:
                snum = 0
            star = '*' * snum
            skillkey = '%s:' % s
            valueskey = '%s ' % values[i]
            s_msg = s_msg+skillkey+valueskey+star+'\n'
        return s_msg[0:-1]
    except:
        traceback.print_exc()
        return '那个破网站连不上!!'


def skill_vs(uid,uid2):
    try:
        res = requests.get('http://osuskills.tk/user/%s/vs/%s'%(uid,uid2),timeout=5)
        if not res:
            return '实力太强p坏了,你们还是去床上解决吧!!'
        value = re.compile(r'<output class="skillValue">(.*?)</output>')
        values = value.findall(res.text)
        if not values:
            return '那个破网站连不上,你们还是去床上解决吧!!'
        skills = ['Stamina', 'Tenacity', 'Agility', 'Accuracy', 'Precision', 'Reaction', 'Memory', 'Reading']
        s_msg = '%s vs %s\n'%(uid,uid2)
        for i,s in enumerate(skills):
            v1 = int(values[i])
            v2 = int(values[i+8])
            vv = str(abs(v1-v2))
            fuhao = ' -- '
            if v1 > v2:
                s_msg = s_msg + s + ' : ' + values[i]+'(+'+vv+')' + fuhao + values[i+8] +'\n'
            elif v1 < v2:
                s_msg = s_msg + s + ' : ' + values[i] + fuhao + values[i+8] +'(+'+vv+')'+'\n'
            else:
                s_msg = s_msg + s + ' : ' + values[i] + fuhao + values[i+8] +'\n'
        return s_msg[0:-1]
    except:
        traceback.print_exc()
        return '那个破网站连不上,你们还是去床上解决吧!!'


def get_userpage(uid, page):
    try:
        if page <= 0:
            return '你是想找Bug吗??'
        res = requests.get('https://osu.ppy.sh/api/get_user?k=%s&u=%s'%(Config.OSU_API_KEY, uid),timeout=5)
        if not res:
            return 'id都错了醒醒!'
        s_msg = uid+"'s userpage   "
        result = json.loads(res.text)
        if not result:
            return 'id都错了醒醒!'
        uid = result[0]['user_id']

        url = 'https://osu.ppy.sh/pages/include/profile-userpage.php?u=%s'
        res = requests.get(url % uid,timeout=5)
        if len(res.text) < 1:
            return 'support都没有,先氪金好吧!'
        result = (res.text).replace('<br />','\n')
        repatt = re.compile(r'<.*?>')
        result = re.sub(repatt,'',result)
        result = html.parser.unescape(result)
        pagesize = 250
        total = (len(result)+pagesize)//pagesize
        if page > total:
            page = total
        s_msg = s_msg + '第%s页,共%s页\n'%(str(page),str(total))
        return s_msg + result[pagesize*(page-1):pagesize*page]
    except:
        traceback.print_exc()
        return 'ppy炸了,请骚等!!'