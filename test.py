
from libs import osu_user

o=osu_user.Osuer()
ret = o.get_user_from_db(405622418)
print(ret)