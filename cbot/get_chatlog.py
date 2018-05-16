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
                c = r['content'].strip().replace('\n','')
                if c:
                    fc.write(c + '\n')

def check_content(content):
    filters = ['!', '！', '~', '～', '个人信息', 'BP指标', '目前潜力', 'Beatmap by', '[@M', 'inter去ppy', 'inter忘',\
        'inter推荐给', '目前的词库量', 's 战绩', '星级:', 'winner榜' , 'loser榜', 'Stamina :', '[视频]', '今日更新的bp',\
        '更新了bp', 'rank:' ,'s skill', '相关词', '游玩次数','金币数变更','更新打图信息','记录在案的pc',
        '玩家已得到的卡','推荐图如下','bot经过一番计算','解除成功,游戏结束','建议修改群名片','玩家信息',
        'Load','机票数变更','roll','排名信息']
    for f in filters:
        if f in content:
            return False
    return True

# if __name__ == '__main__':

#     chat2txt(chatlog)

