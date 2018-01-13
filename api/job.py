# -*- coding: utf-8 -*-
import time
from apscheduler.schedulers.blocking import BlockingScheduler

from libs import job_msg

def jobCenter(bot, globValue):
    sched = BlockingScheduler()
    # 任务添加
    sched.add_job(job_msg.msg_recollect, 'interval', minutes=1, args=[globValue])
    sched.add_job(job_msg.speak_task, 'interval', seconds=15, args=[bot, globValue])
    sched.start()

