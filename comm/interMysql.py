# -*- coding:utf8 -*-

import pymysql
from DBUtils.PooledDB import PooledDB

config = {
    'creator'      :   pymysql, 
    'mincached'    :   1, 
    'maxcached'    :   20,
    'host'         :   '127.0.0.1', 
    'port'         :   3306, 
    'user'         :   'root', 
    'passwd'       :   '123456',
    'db'           :   'osu',
    'use_unicode'  :   True,
    'charset'      :   'utf8',
    'cursorclass'  :   pymysql.cursors.DictCursor
}

class Connect(object):

    __pool = None

    def __init__(self):
        self._conn = Connect.__getConn()
        self._cursor = self._conn.cursor()

    @staticmethod
    def __getConn():
        '''从连接池取连接'''
        if Connect.__pool is None:
            __pool = PooledDB(**config)

        return __pool.connection()

    def query(self, *args, **kwargs):
        self._cursor.execute(*args, **kwargs)
        return self._cursor.fetchall()

    def queryOne(self, *args, **kwargs):
        self._cursor.execute(*args, **kwargs)
        return self._cursor.fetchone()

    def execute(self, *args, **kwargs):
        self._cursor.execute(*args, **kwargs)
        return self._cursor.rowcount

    def executeMany(self, *args, **kwargs):
        return self._cursor.executemany(*args, **kwargs)

    def insert(self, *args, **kwargs):
        self._cursor.execute(*args, **kwargs)
        return self._cursor.lastrowid

    def queryPage(self, *args, pn=0, rn=10, **kwargs):
        pn,rn = self.format_pn_rn(pn, rn)
        newargs = list(args)
        newargs[0] += ' limit %s,%s'
        if len(newargs) > 1:
            newargs[1].extend([pn,rn])
        else:
            newargs.append([pn,rn])
        self._cursor.execute(*newargs, **kwargs)
        return self._cursor.fetchall()

    def commit(self):
        return self._conn.commit()

    def rollback(self):
        return self._conn.rollback()

    def __del__(self):
        self._cursor.close()
        self._conn.close()

    def format_pn_rn(self, pn, rn):
        pn,rn = int(pn),int(rn)
        pn = 0 if pn < 0 else pn 
        rn = 0 if rn < 0 else rn 
        return pn*rn, rn


if __name__ == '__main__':
    m = Connect()
    res = m.queryPage('select osuid from user', pn=1, rn=5)
    print(res)


