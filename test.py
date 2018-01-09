
from libs import osu_user

o=osu_user.Osuer()
ret = o.get_user_bp('-interesting-',limit=5)
print(ret)