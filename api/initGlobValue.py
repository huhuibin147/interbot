# -*- coding: utf-8 -*-
from libs import job_msg
from api import chattrain_api


def init(globValue, gV_Lock):

    # 初始化msg信息
    job_msg.msg_recollect(globValue, gV_Lock)
    # 初始化words信息
    # chattrain_api.chat_train_job(globValue, gV_Lock)
    return
