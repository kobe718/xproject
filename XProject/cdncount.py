#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 2015年6月16日

@author: kobe
'''


import pymysql 

if __name__ == '__main__':
    conn = pymysql.connect(host='10.102.1.8',
                           user='root',
                           passwd='123456',
                           db='xproject',
                           charset='utf8')
    
    try:
        wordcnt = []
        count = 0
        with conn.cursor() as cursor:
            sql = 'select distinct rdata from target_dns where `type`=5'
            cursor.execute(sql)
            while 1:
                res = cursor.fetchmany(100)
                if len(res) == 0:
                    break
                #print len(res)
                for line in res:
                    count +=1
                    words = line[0].split('.')
                    #print line[0]
                    #print count
                    for word in words:
                        if word != '':
                            #print word
                            wordcnt.append(word)
                try:
                    with conn.cursor() as cursor2:
                        insert = r'insert into target_dns_wordcnt (`word`) values (%s)' 
                        cursor2.executemany(insert, wordcnt)
                        conn.commit()
                        wordcnt = []
                finally:
                    pass
    finally:
        conn.close()
        print count
        