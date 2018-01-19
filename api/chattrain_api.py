# -*- coding: utf-8 -*-
# 训练模块接口

import logging
import traceback
from comm import Config
from comm import interRedis
from cbot import get_chatlog
from cbot import seg_train
from cbot import segment
from gensim import models


def chat_train_job(globValue, gV_Lock, skip_rds=False):
    # 训练任务接口
    Ctrain(globValue, gV_Lock).chat_train(skip_rds)
    return
    
def kw(key, globValue):
    # 查询接口
    segmodel = globValue['words_train_model']
    res = segmodel.most_similar(key,topn=5)
    msg = "%s's 相关词\n" % key
    for idx,item in enumerate(res):
        msg += '%s.%s %s\n' % (idx+1, key, item[0])
    return msg[:-1]

class Ctrain():
    def __init__(self, globValue, gV_Lock):
        self.globValue = globValue
        self.gV_Lock = gV_Lock

    def chat_train(self, skip_rds=False):
        try:
            if not skip_rds and self.is_train():
                return
            get_chatlog.chat2txt(get_chatlog.chatlog())
            logging.info('chatlog写入成功！')
            # 切词
            segment.run()
            logging.info('切词完成！')
            # train
            seg_train.run()
            logging.info('训练完成！')
            self.load_seg_model()
        except:
            traceback.print_exc()

    def is_train(self):
        # 1-跳过 0-未跳过
        key = Config.CHAT_TRAIN_KEY
        rds = interRedis.interRds()
        try:
            if rds.exists(key):
                logging.info('跳过训练！')
                self.load_seg_model()
                return 1
            rds.setex(key, 1, Config.WORDS_TRAIN_SEC)
        except:
            traceback.print_exc()
        return 0

    def load_seg_model(self):
        try:
            model = models.Word2Vec.load('cbot\chat500.model.bin')
            self.gV_Lock.acquire()
            self.globValue.update({'words_train_model':model})
            self.gV_Lock.release()
            logging.info('模型载入成功！')
        except:
            traceback.print_exc()
