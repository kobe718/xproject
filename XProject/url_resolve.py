#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gevent
from gevent import monkey
monkey.patch_socket(dns=True)
import pymysql
from gevent.pool import Pool
from scapy.all import *

conn = pymysql.connect(host='10.102.1.212',
                           user='root',
                           passwd='root',
                           db='ttscan-biz-sh-v1.0.2',
                           charset='utf8')

targets = []

pool = Pool(20)

finished = 0

output = []

def resolv(target):
    global output
    global finished
    ans = sr1(IP(dst="114.114.114.114")/UDP(sport=RandShort(),dport=53)/DNS(rd=1,qd=DNSQR(qname=target)),timeout=2,verbose=0)
    if ans is not None:
        finished += 1
        print finished, target
        for i in range(ans.ancount):
            #print "http://%s"%target, ans.an[i].rrname, ans.an[i].type, ans.an[i].rdata
            output.append(("http://%s"%target, ans.an[i].rrname, ans.an[i].type, ans.an[i].rdata))


try:
    output = []
    with conn.cursor() as cursor:
        sql = "select `url` from `t_site`"
        cursor.execute(sql) 
        while 1:
            res = cursor.fetchmany(100)
            if len(res) == 0:
                break
            for line in res:
                targets.append(line[0].replace("http://","").replace("\\",""))

            with gevent.Timeout(2,False):
                jobs = [pool.spawn(resolv, target) for target in targets]
                pool.join()
            try:
                with conn.cursor() as cursor2:
                    #print output
                    insert = r"insert into t_targetdns (`url`, `rname`, `type`, `rdata`) values (%s, %s, %s, %s)"
                    cursor2.executemany( insert, output)
                    conn.commit()
                    output = []
                    targets = []
            finally:
                pass

except KeyboardInterrupt:
    conn.close()

finally:
    conn.close()


#targets = ["www.gov.cn","www.xerk.gov.cn","www.shanghai.gov.cn"]



