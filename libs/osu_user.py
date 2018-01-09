
from comm import interRequest
from comm import Config

class Osuer():
    def __init__(self, uid=None, uname=None):
        self.userinfo = None
        self.userbp = None
        self.uid = uid
        self.uname = uname

    def get_user_info(self, uid=None):
        uid = uid if uid else self.uid
        url = 'https://osu.ppy.sh/api/get_user?k=%s&u=%s' % (Config.OSU_API_KEY, uid)
        r = interRequest.interReq(url)
        ret = r.get()
        self.userinfo = ret[0]
        return self.userinfo

    def get_user_bp(self, uid=None, m=0, limit=10):
        uid = uid if uid else self.uid
        url = 'https://osu.ppy.sh/api/get_user_best?k=%s&u=%s&m=%s&limit=%s' % (Config.OSU_API_KEY, uid, m ,limit)
        r = interRequest.interReq(url)
        ret = r.get()
        self.userbp = ret
        return self.userbp


