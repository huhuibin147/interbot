# -*- coding: utf-8 -*-
import traceback
import json
from libs import chart

def add(hid, bid, gid, admin, mod, starttime, endtime, intro, resultjson, pprange, expect):
    '''
    args:
        2 2 614 xx hd 2018-5-4 2018-5-6 test test 1~100 1
    '''
    c = chart.chart()
    r = c.chart2DB(hid, bid, gid, admin, mod, starttime, endtime, intro, resultjson, pprange, expect)
    if r:
        return 'add suc'
    else:
        return 'add fail'


def addexpect(expect, gid, hid, bidjson, starttime, endtime):
    '''
    args:
        1 614 2 {1,2,3} 2018-5-4 2018-5-6
    '''
    c = chart.chart()
    r = c.chartexpect2DB(expect, gid, hid, bidjson, starttime, endtime)
    if r:
        return 'add suc'
    else:
        return 'add fail'

    