# -*- coding: utf-8 -*-
import random
import traceback
from api import help_api
from api import test_api
from api import user_api
from api import cbot_api
from api import rank_api
from api import req_api
from api import sp_api
from api import chattrain_api
from libs import args_func
from libs import chatlog
from comm import Config

def invoke(b):

    # 信息收集
    cbot_api.msg2Redis(b)
    cbot_api.msg2Mysql(b)

    if b.message == '!inter':
        return help_api.new_help()

    elif '!test' in b.message:
        uid = args_func.uid_find_or_input(b.message[6:], b.qq)
        if not uid:
            return '你不适合屙屎，删游戏吧(请绑定ID'
        return test_api.test(uid)

    elif '!myinfo' == b.message:
        return user_api.myinfo(b.qq)

    elif '!bbp' in b.message:
        uid = args_func.uid_find_or_input(b.message[5:], b.qq, return_type=1)
        if not uid:
            return '你有能看bp吗???(请绑定ID'
        return user_api.get_bp5info(uid)

    elif '!check' in b.message:
        uid = args_func.uid_find_or_input(b.message[7:], b.qq, return_type=1)
        if not uid:
            return '你太才菜了不想check你(请绑定ID'
        return user_api.check(uid)

    elif '!map' in b.message:
        uid = args_func.uid_find_or_input(b.message[5:], b.qq, return_type=1)
        if not uid:
            return '本bot根本不想给你推荐图QwQ(请绑定ID'
        return user_api.map(uid)

    elif '!repeat' in b.message:
        return b.message[8:]

    elif '!helpme' == b.message:
        return 'inter已经去世，请求你群程序猿解救!!!'

    elif '[CQ:at,qq=%s]'%Config.LOGGING_QQ in b.message:
        return cbot_api.speak(b.globValue)

    elif '!!' == b.message:
        return 'iinterbot.github.io  招前端py后端人员!!!'

    elif '!mc' == b.message:
        msg = test_api.mc()
        return '[CQ:at,qq=%s] %s' % (b.qq, msg)

    elif '!setid' in b.message:
        uid = b.message[7:]
        msg = user_api.setid(uid, b.qq, b.group_id)
        return '[CQ:at,qq=%s] %s' % (b.qq, msg)
        
    elif '!kw' in b.message:
        try:
            return chattrain_api.kw(b.message[4:], b.globValue)
        except:
            return '%s不在interbot的词汇表中' % b.message[4:]

    elif '!trainwords' == b.message and b.qq == Config.SUPER_QQ:
        try:
            b.bot.send_group_msg(group_id=b.group_id, message='啊啊啊!interbot被抓去训练了!')
            chattrain_api.chat_train_job(b.globValue, b.gV_Lock, skip_rds=True)
            return 'interbot感觉还行,训练归来!'
        except:
            traceback.print_exc()
            return 'interbot感觉不对劲,训练异常!'

    elif '!skill' in b.message:
        uid = args_func.uid_find_or_input(b.message[7:], b.qq, return_type=1)
        return req_api.get_skill(uid)

    elif '!vssk' in b.message:
        uid = args_func.uid_find_or_input(qq=b.qq, return_type=1)
        if not uid:
            return '本bot根本不认识你(请绑定ID'
        return req_api.skill_vs(uid, b.message[6:])

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

    elif '!todaybp' in b.message:
        uid = args_func.uid_find_or_input(b.message[9:], b.qq, return_type=1)
        return test_api.todaybp(uid)

    elif '!rctpp' in b.message:
        uid = args_func.uid_find_or_input(b.message[7:], b.qq, return_type=1)
        return test_api.rctpp(uid)


    else:
        msg = cbot_api.autoreply(b.globValue)
        chatlog.Chat2Redis(b.group_id, Config.LOGGING_QQ, msg)
        return msg if msg else 'not define'

