# -*- coding: utf-8 -*-
import redis
from comm import Config

def interRds(host='127.0.0.1', port=6379):
    return interRedis(host, port).getRds()
    
class interRedis():

    def __init__(self, host='127.0.0.1', port=6379):
        self.rds = redis.Redis(host, port)

    def getRds(self):
        return self.rds

    # 初始化群列表
    def init_group_name(self, bot):
        group_list = bot.get_group_list()
        group_map = {}
        for g in group_list:
            group_map[g['group_id']] = g['group_name']
        self.rds.hmset(Config.KEY_GROUP_NAME_PREFIX, group_map)


