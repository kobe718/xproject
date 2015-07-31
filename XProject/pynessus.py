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

    def addscan(self):
        if self._token is None:
            self._authenticate()
        if self._token is None:
            return -1
        
        
        pass
    
    def getstatus(self,scanid):
        pass
    
    def getresult(self,scanid):
        pass

        
    

if __name__ == '__main__':
    
    nessus = pynessus(url='https://10.101.1.53:8834',username='api',password='api@123')
    
    
    

    
    
    

    
    