import logging
import traceback

from comm import interRedis
from comm import Config
from api import msg2cmd

class Bot():
    def __init__(self, bot, context):
        self.rds = interRedis.interRds()
        self.context = context
        self.bot = bot
        self.group_id = context['group_id']
        self.user_id = context['user_id']
        self.message = context['message']
        # TODO 
        # self.usercard = bot.get_group_member_info(group_id=self.group_id,user_id=self.user_id)['card']
        self.group_name = self.rds.hget(Config.KEY_GROUP_NAME_PREFIX,self.group_id).decode()
        logging.info('[%s][%s] %s'%(self.group_name, self.user_id, self.message))

    def test(self):
        if self.user_id == 405622418 and self.message == '!hello':
            self.bot.send_group_msg(group_id=self.group_id,message='响应test')



def MsgCenter(bot, context):
    try:
        b = Bot(bot, context)
        ret = msg2cmd.invoke(b)
        if ret == 'not define':
            return
        b.bot.send_group_msg(group_id=b.group_id, message=ret)
    except:
        traceback.print_exc()
        b.bot.send_group_msg(group_id=b.group_id, message=Config.ERROR_MSG_RETURN)
