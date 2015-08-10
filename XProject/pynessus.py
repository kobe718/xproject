#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 2015年6月4日

@author: Administrator
'''

from urllib import urlencode
from urllib2 import urlopen,Request,build_opener,HTTPSHandler
import json
#from xml.dom.minidom import parse as parse_xml
import ssl
import urllib2
from time import sleep
import control

class pynessus(object):
    def __init__(self, url, username, password):
        self._username = username
        self._password = password
        self._url = url
        self._token = None
        
   
    def _get_reply(self,url,params={},methods='GET'):
        context = ssl._create_unverified_context()
        opener = build_opener(HTTPSHandler(context=context))
        #f=urlopen(url,data=urlencode(params),context=context)
        request = Request(url,data=urlencode(params))
        if self._token is not None :
            request.add_header('X-Cookie','token='+self._token)
        if methods != 'GET':
            request.get_method = lambda: methods
        try:
            f = opener.open(request)
        except urllib2.HTTPError as e:
            print str(e.code)
        except urllib2.URLError as e:
            print str(e.reason)
            
        _msg=f.read(8192)
        if len(_msg) > 0:
            msg=json.loads(_msg)
            return msg
        else:
            return None
    
    def _authenticate(self):
        if self._token is None :
            url = self._url + "/session"
            params = dict(username=self._username, password=self._password)
            reply = self._get_reply(url, params)
            self._token = reply["token"]

    
    def close(self):
        if self._token is not None :
            url = self._url + "/session"
            reply = self._get_reply(url,methods='DELETE')
            self._token = None

    def addscan(self, target, template):
        if self._token is None:
            self._authenticate()
        if self._token is None:
            return -1
        
        
        pass
    
    def getstatus(self,scanid):
        pass
    
    def getprogress(self,scanid):
        pass
    
    def getresult(self,scanid):
        pass

    def geterrmsg(self,scanid):
        pass
    
    def deletescan(self,scanid):
        pass
    
    def parseresult(self, result):
        pass
        
    

if __name__ == '__main__':
    
    nessus = pynessus(url='https://127.0.0.1:8834',username='api',password='api@123')
    
    sc = control.SectotalControl(server='1.1.1.1',apikey='1q2w3e4r5t6y',scanner='nessus001')
    
    ntarget = sc.gettarget(1)
    
    scanid = nessus.addscan(target=ntarget,template='basic')
    
    while nessus.getstatus(scanid) == 'running':
        sc.statusreport(ntarget, nessus.getprogress(scanid))
        sleep(100)
    
    if nessus.getstatus(scanid) == 'finished':
        result = nessus.getresult(scanid)
        sc.putresult(ntarget, nessus.parseresult(result))
    else:
        sc.errorreport(ntarget, nessus.geterrmsg())
 
    
    nessus.deletescan(scanid)
    
    
    

    
    
    

    
    