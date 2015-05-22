#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 2015年5月21日

@author: kobe
'''

import urllib2
import pymysql 
import time
import threading
import socket

if __name__ == '__main__':
    conn = pymysql.connect(host='10.102.1.8',
                           user='root',
                           passwd='123456',
                           db='xproject',
                           charset='utf8')
try:
    with conn.cursor() as cursor:
        sql = "select `id`,`url` from `targets` where id > 121036"
        cursor.execute(sql) 
        output = []
        while 1:
            try:
                res = cursor.fetchmany(5)
                if len(res) == 0:
                   #cursor.scroll(0,mode='absolute')
                   break
                for line in res:
                    id = line[0]
                    url = line[1]
                    ip = socket.gethostbyname(url.replace("http://",""))
                    if ip is not None:
                        output.append((ip,id))
                try:
                    with conn.cursor() as cursor2:
                        insert = r"insert into target_ip (ip,urlid) values (%s,%s) "
                        print output
                        cursor2.executemany(insert,output)
                        conn.commit()
                        output = []
                finally:
                    pass
            except KeyboardInterrupt:
                break
            except:
                continue
finally:
    conn.close()
    
