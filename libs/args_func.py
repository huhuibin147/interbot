
from libs import osu_user

def uid_find_or_input(uid=None, qq=None, can_input=True, return_type=0):
    # 是否允许读入uid
    if can_input and uid:
        return uid

    u = osu_user.Osuer()
    ret = u.get_user_from_db(qq)
    if not ret:
        return 0

    if return_type == 0:
        return ret['osuid']
    elif return_type == 1:
        return ret['osuname']
