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
import pygeoip
import json
#import socket

if __name__ == '__main__':
    conn = pymysql.connect(host='10.102.1.8',
                           user='root',
                           passwd='123456',
                           db='xproject',
                           charset='utf8')
    gi = pygeoip.GeoIP('GeoIPCity.dat')
try:
    with conn.cursor() as cursor:
        sql = "select `ip`,`urlid` from `target_ip` where urlid > 84311"
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
                    res = gi.record_by_addr(ipstr)
                    if res is not None:
                        print urlid,res['longitude'], res['latitude']
                        output.append((urlid, res['longitude'], res['latitude']))
                try:
                    with conn.cursor() as cursor2:
                        insert = r"insert into target_geo (id,longitude,latitude) values (%s,%s,%s) "
                        #print output
                        cursor2.executemany(insert,output)
                        conn.commit()
                        output = []
                finally:
                    pass
            except KeyboardInterrupt:
                break
 #           except:
 #               continue
finally:
    conn.close()
