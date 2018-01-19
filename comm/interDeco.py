# -*- coding: utf-8 -*-

import traceback
import json
from comm import interRedis


def cache(**kw):
    key = 'AUTO_CACHE_%s' % kw.get('cmd', 'ERROR')
    times = kw.get('times', 300)
    def _deco(func):
        def proc(*args, **kwargs):
            try:
                rds = interRedis.interRds()
                v = rds.get(key)
                if not v:
                    ret = func(*args, **kwargs)
                    rds.setex(key, json.dumps(ret), times)
                else:
                    ret = json.loads(v)
                return ret
            except:
                traceback.print_exc()
        return proc
    return _deco