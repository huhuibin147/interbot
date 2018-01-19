# -*- coding: utf-8 -*-
import threading
import logging
from cqhttp import CQHttp
from api import msg
from api import job
from api import initGlobValue
from comm import interRedis
from comm import Config

bot = CQHttp(api_root='http://127.0.0.1:5700/')

# 全局变量锁
gV_Lock = threading.RLock()
# 初始化共享变量
globValue = {}

@bot.on_message()
def handle_msg(context):
    try:
        # TODO线程池
        t = threading.Thread(target=msg.MsgCenter, args=(bot, context, globValue))
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
logging.info('interbot各种加载初始化中...')
# 初始化群列表信息
# r = interRedis.interRedis()
# r.init_group_name(bot)
# 初始化群员昵称
# TODO

# 初始化全局变量
initGlobValue.init(globValue, gV_Lock)


# 定时任务
sched_t = threading.Thread(target=job.jobCenter, args=(bot, globValue, gV_Lock))
sched_t.setDaemon(True)
sched_t.start()


# 监听启动
bot.run(host='127.0.0.1', port=8888)



