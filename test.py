
from libs import osu_user
from comm import interRedis
import json

# o=osu_user.Osuer()
# ret = o.get_user_from_db(405622418)
# print(ret)


# rds = interRedis.interRds()
# key = 'chatlog_514661057'
# chatlog = rds.get(key)
# chatlog = chatlog.decode('utf8')
# print(json.loads(chatlog)[0].get('qq'))

o=osu_user.Osuer()
ret = o.get_user_info('-inter-')
print(ret)