import json
import interMysql
db=interMysql.Connect()
sql = '''SELECT a.tth, a.pc, a.acc, a.pp_raw,sum(b.acc) bpacc,sum(b.pp) bppp FROM osu_user a INNER JOIN osu_bp b on a.user_id = b.user_id GROUP BY a.user_id'''
with open('us.txt','w') as f:
    res = db.query(sql)
    f.write(json.dumps(res))