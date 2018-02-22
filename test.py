
# from libs import osu_user
# from libs import mods
# from comm import interRedis
# from api import skill_api
# from api import rank_api
# from api import test_api
from api import rank_tab
from libs import score
# from draws import draw_data
# from draws import drawRank
# from api import chattrain_api
# from cbot import get_chatlog
# from cbot import segment
import json
import threading
import traceback

# o=osu_user.Osuer()
# ret = o.get_user_from_db(405622418)
# print(ret)


# rds = interRedis.interRds()
# key = 'chatlog_514661057'
# chatlog = rds.get(key)
# chatlog = chatlog.decode('utf8')
# print(json.loads(chatlog)[0].get('qq'))

# o=osu_user.Osuer()
# ret = o.get_user_info('-inter2-')
# print(ret)
# try:
#     globValue = {}
#     gV_Lock = threading.RLock()
#     chattrain_api.Ctrain(globValue, gV_Lock).chat_train()

# except:
#     traceback.print_exc()

# print(skill_api.get_skill('-inter-'))
 
# print(mods.get_acc(100, 200, 300, 0))
# print(rank_api.cmd_rank(614892339)) 
# print(test_api.todaybp('yimoQWQ'))

############# 成绩提取  ###############
#     JRC888   IronWitness   -inter-  Trustless532   614892339  641236878 ykzl1969497633
# rank_tab.upload_rec('-inter-', 641236878, limit=10)
#######################################
# uid, groupid, bid, hid=1, mods=-1
# rank_tab.get_rankinfo('-inter-', 614892339, 1050200, 1, -1)
# print(rank_tab.get_topsrank('514661057'))

# print(score.alias2db('竹取', bid='86324', uid=''))
print(score.get_alias('竹取'))