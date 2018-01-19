# -*- coding: utf-8 -*-
import time
from apscheduler.schedulers.blocking import BlockingScheduler

from libs import job_msg
from api import chattrain_api 

def jobCenter(bot, globValue, gV_Lock):
    sched = BlockingScheduler()
    # 任务列表
    
    # msg信息更新
    sched.add_job(job_msg.msg_recollect, 'interval', minutes=1, args=[globValue, gV_Lock])
    # speak任务
    sched.add_job(job_msg.speak_task, 'interval', seconds=15, args=[bot, globValue])
    # 训练任务
    sched.add_job(chattrain_api.chat_train_job, 'interval', hours=1, args=[globValue, gV_Lock])
    
    sched.start()

