#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 2015年5月15日

@author: kobe
'''

import urllib2
import pymysql 
import time
#import threading
import sys

if __name__ == '__main__':
    conn = pymysql.connect(host='10.102.1.8',
                           user='root',
                           passwd='123456',
                           db='xproject',
                           charset='utf8')
#     urllib2.install_opener(
#         urllib2.build_opener(
#             urllib2.ProxyHandler({'http': '127.0.0.1:8888'})
#         )
#     )
    headers={'User-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36',
             'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
             'Accept-encoding': 'gzip'
             }
try:
    with conn.cursor() as cursor:
        sql = "select `id`,`url` from `targets` where id > 1430"
        cursor.execute(sql)
        output=[]
        i = 0
        while 1:
            res = cursor.fetchmany(5)
            #i+=5
            if len(res) == 0:
                break;
            for line in res:
                request = urllib2.Request(line[1],None,headers)
                #request.get_method = lambda:'HEAD'
                try:
                    #print line[1]
                    ts = time.time()
                    response = urllib2.urlopen(request,None,timeout=5)
                    ts = (time.time() - ts)*1000 #ms
                    size = len(response.read())
                    speed = size/ts #kb/s
                    print line[0],line[1],ts,size,speed
                    output.append((line[0],ts,size,speed,'200'))
                    #print response.info()
                except urllib2.HTTPError as e:
                    print time.strftime('%H-%M-%S'),line[1],e.code
                    output.append((line[0],0,0,0,str(e.code)))
                    pass
                except urllib2.URLError as e:
                    print time.strftime('%H-%M-%S'),line[1],e.reason
                    output.append((line[0], 0, 0,0,str(e.reason)))
                    pass
                except KeyboardInterrupt:
                    #print str(e)
                    break
                except :
                    pass
            try:
                with conn.cursor() as cursor2:
                    insert = r"insert into target_available (id,`time`,`size`,`speed`,`status`) values (%s,%s,%s,%s,%s) "
                    #print output
                    cursor2.executemany(insert,output)
                    conn.commit()
                    output = []
            finally:
                pass       

finally:
    conn.close()
    
