# -*- coding: utf-8 -*-
import traceback
import json
from comm import interMysql
from comm import Config

class chart(object):

    def chart2DB(self, hid, bid, gid, admin, mod, starttime, endtime, intro, resultjson, pprange, expect):
        try:
            conn = interMysql.Connect()
            sql = '''
                insert into chart
                    (hid, bid, gid, admin, `mod`, starttime, endtime, intro, resultjson, pprange, modifytime, expect) 
                values
                    (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now(),%s)
            '''
            args = [hid, bid, gid, admin, mod, starttime, endtime, intro, resultjson, pprange, expect]
            ret = conn.execute(sql, args)
            conn.commit()
            return ret
        except:
            traceback.print_exc()
            conn.rollback()
            return 0

    def chartexpect2DB(self, expect, gid, hid, bidjson, starttime, endtime):
        try:
            conn = interMysql.Connect()
            sql = '''
                insert into chartexpect
                    (expect, gid, hid, bidjson, starttime, endtime) 
                values
                    (%s,%s,%s,%s,%s,%s)
            '''
            args = [expect, gid, hid, bidjson, starttime, endtime]
            ret = conn.execute(sql, args)
            conn.commit()
            return ret
        except:
            traceback.print_exc()
            conn.rollback()
            return 0

    def searchExpect(self, expect, gid):
        conn = interMysql.Connect()
        sql = '''
            SELECT * FROM chartexpect 
            WHERE expect = %s and gid = %s
        '''
        args = [expect, gid]
        ret = conn.query(sql, args)
        return ret