import threading
import logging
from cqhttp import CQHttp
from api import msg
from comm import interRedis
from comm import Config

bot = CQHttp(api_root='http://127.0.0.1:5700/')


@bot.on_message()
def handle_msg(context):
    t = threading.Thread(target=msg.MsgCenter, args=(bot, context))
    t.start()
    return


# 初始化日志格式
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s][%(levelname)s]%(message)s',
    datefmt='%Y-%d-%m %H:%M:%S'
)
# 初始化群列表信息
rds = interRedis.interRds()
group_list = bot.get_group_list()
for g in group_list:
    rds.set(Config.KEY_GROUP_NAME_PREFIX+str(g['group_id']), g['group_name'])

# 监听启动
bot.run(host='127.0.0.1', port=8888)



