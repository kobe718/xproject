#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 2015年5月15日

@author: kobe
'''

import urllib2
import pymysql 
import time
import threading

if __name__ == '__main__':
    conn = pymysql.connect(host='172.16.33.72',
                           user='root',
                           passwd='xproject',
                           db='xproject',
                           charset='utf8')
try:
    with conn.cursor() as cursor:
        sql = "select `id`,`url` from `targets`"
        cursor.execute(sql) 
        while 1:
            res = cursor.fetchmany(5)
            if len(res) == 0:
                break
            print res
            

finally:
    conn.close()
    