# -*- coding: utf-8 -*-

import traceback
from comm import interMysql


def chatlog():
    try:
        conn = interMysql.Connect()
        sql = '''
            SELECT * FROM chat_logs
        '''
        res = conn.query(sql)
        if not res:
            return []
        return res
    except:
        traceback.print_exc()

def chat2txt(chatlist):
    with open('cbot\chat.txt','w',encoding='utf8') as fc:
        for r in chatlist:
            if check_content(r['content']):
                fc.write(r['content']+'\n')

def check_content(content):
    filters = ['!', '！', '~', '～', '个人信息', 'BP指标', '目前潜力', 'Beatmap by', '[@M', 'inter去ppy', 'inter忘',\
        'inter推荐给', '目前的词库量', 's 战绩', '星级:', 'winner榜' , 'loser榜', 'Stamina :', '[视频]', '今日更新的bp',\
        '更新了bp', 'rank:' ,'s skill', '相关词']
    for f in filters:
        if f in content:
            return False
    return True

# if __name__ == '__main__':

#     chat2txt(chatlog)

