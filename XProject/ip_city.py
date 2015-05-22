#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 2015年5月21日

@author: kobe
'''

#import urllib2
import pymysql 
from ip import find
from time import sleep
#import threading
#import socket

if __name__ == '__main__':
    conn = pymysql.connect(host='10.102.1.8',
                           user='root',
                           passwd='123456',
                           db='xproject',
                           charset='utf8')
try:
    with conn.cursor() as cursor:
        sql = "select `ip`,`urlid` from `target_ip` where `urlid` > 83871"
        cursor.execute(sql) 
        output = []
        while 1:
            try:
                res = cursor.fetchmany(10)
                if len(res) == 0:
                    #cursor.scroll(0,mode='absolute')
                    break
                for line in res:
                    ipstr = line[0]
                    urlid = line[1]
                    res = find(ipstr)
                    if res is not None:
                        res = res.split('\t', 3)
                        if len(res) == 3:
                            country, province, city = res
                        if len(res) == 2:
                            counry, province = res
                            city = ''
                        if len(res) ==1:
                            country = res
                            province = city = ''
                        print urlid,country,province,city
                        output.append((urlid, country, province, city))
                try:
                    with conn.cursor() as cursor2:
                        insert = r"insert into target_city (id,country,province,city) values (%s,%s,%s,%s) "
                        #print output
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
