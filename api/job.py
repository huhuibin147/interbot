# -*- coding: utf-8 -*-
import time
import traceback
import os
import sys
from apscheduler.schedulers.blocking import BlockingScheduler

from libs import job_msg
from api import chattrain_api 
from api import stats 

def jobCenter(bot, globValue, gV_Lock):
    try:
        sched = BlockingScheduler()
        # 任务列表
        
        # msg信息更新
        sched.add_job(job_msg.msg_recollect, 'interval', minutes=30, args=[globValue, gV_Lock])
        # speak任务
        sched.add_job(job_msg.speak_task, 'interval', seconds=15, args=[bot, globValue])
        # 训练任务
        # sched.add_job(chattrain_api.chat_train_job, 'interval', hours=6, args=[globValue, gV_Lock])
        # 定时重启任务
        sched.add_job(restart, 'cron', hour='9', args=[])

        sched.start()
    except:
        traceback.print_exc()
    return

def restart():
    python = sys.executable
    os.execl(python, python, * sys.argv)