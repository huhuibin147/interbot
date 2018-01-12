
from libs import osu_user
from libs import healthCheck

def test(uid):
    u = osu_user.Osuer(uid=uid)
    userinfo = u.get_user_info()
    bp = u.get_user_bp(limit=5)
    return healthCheck.health_check(userinfo, bp)

def new_test():
    return '你不适合屙屎,请你去世!(给我加id'

