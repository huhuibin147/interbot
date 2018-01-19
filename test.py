
from libs import osu_user
from comm import interRedis
from api import chattrain_api
from cbot import get_chatlog
from cbot import segment
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
# ret = o.get_user_info('-inter-')
# print(ret)
try:
    globValue = {}
    gV_Lock = threading.RLock()
    chattrain_api.Ctrain(globValue, gV_Lock).chat_train()

except:
    traceback.print_exc()