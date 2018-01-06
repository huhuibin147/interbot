import logging

from comm import interRedis
from comm import Config

class Bot():
    def __init__(self, bot, context):
        self.rds = interRedis.interRds()
        self.context = context
        self.bot = bot
        self.group_id = context['group_id']
        self.user_id = context['user_id']
        self.message = context['message']
        self.usercard = bot.get_group_member_info(group_id=self.group_id,user_id=self.user_id,no_cache=True)['card']
        self.group_name = self.rds.get(Config.KEY_GROUP_NAME_PREFIX+str(self.group_id)).decode()
        logging.info('[%s][%s] %s'%(self.group_name, self.usercard, self.message))

    def test(self):
        if self.user_id == 405622418 and self.message == '!hello':
            self.bot.send_group_msg(group_id=self.group_id,message='响应test')

def MsgCenter(bot, context):  
    b = Bot(bot, context)
    b.test()