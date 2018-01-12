import threading
import logging
from cqhttp import CQHttp
from api import msg
from comm import interRedis
from comm import Config

bot = CQHttp(api_root='http://127.0.0.1:5700/')


@bot.on_message()
def handle_msg(context):
    try:
        t = threading.Thread(target=msg.MsgCenter, args=(bot, context))
        t.start()
        return
    except:
        return


# 初始化日志格式
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s][%(levelname)s]%(message)s',
    datefmt='%Y-%d-%m %H:%M:%S'
)
# 初始化群列表信息
r = interRedis.interRedis()
r.init_group_name(bot)
# 初始化群员昵称
# TODO

# 监听启动
bot.run(host='127.0.0.1', port=8888)



