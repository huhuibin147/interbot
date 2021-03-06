# -*- coding: utf-8 -*-
import logging
import traceback

from comm import interRedis
from comm import Config
from api import msg2cmd

class Bot():
    def __init__(self, bot, context, globValue, gV_Lock):
        # self.rds = interRedis.interRds()
        self.context = context
        self.bot = bot
        self.group_id = context['group_id']
        self.qq = context['user_id']
        msgs = context['message'].replace('&amp;', '&')
        msgs = msgs.replace('&#91;', '[')
        msgs = msgs.replace('&#93;', ']')
        msgs = msgs.replace('&#44;', ',')
        self.message = msgs
        self.globValue = globValue
        self.gV_Lock = gV_Lock
        # TODO 
        # self.usercard = bot.get_group_member_info(group_id=self.group_id,user_id=self.qq)['card']
        # self.group_name = self.rds.hget(Config.KEY_GROUP_NAME_PREFIX,self.group_id).decode()
        logging.info('[%s][%s] %s'%(self.group_id, self.qq, self.message))



def MsgCenter(bot, context, globValue, gV_Lock):
    try:
        # 群控制
        if context['group_id'] not in Config.PERMISSION_GROUP_LIST:
            return
        b = Bot(bot, context, globValue, gV_Lock)
        ret = msg2cmd.invoke(b)
        # auto_escape = False
        # if type(ret) == 'list':
        #     ret = ret[1]
        #     auto_escape = True
        if ret == 'not define':
            return
        # b.bot.send_group_msg(group_id=b.group_id, message=ret, auto_escape=auto_escape)
        b.bot.send(context, ret)
    except:
        traceback.print_exc()
        # b.bot.send_group_msg(group_id=b.group_id, message=Config.ERROR_MSG_RETURN)
    return
