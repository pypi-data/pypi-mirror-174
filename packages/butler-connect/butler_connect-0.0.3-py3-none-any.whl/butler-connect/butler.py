#!/usr/bin/env python3
# Project: Ai Butler 
# Author: Oliver Birkholz
# Mail: oliver.birkholz@aibutler.de
# License: Ask Oliver Birkholz
#from urllib.error import 
from requests import HTTPError, ReadTimeout

import requests, json, sseclient
import datetime, time
import logging

LOG = logging.getLogger(__name__)
#TIMEOUT_LOGIN = 60
#sslVerification = False

class cButlerRest():

    def __init__(self,host,component,key,timeout_sse=10*60,timeout_login=30,sslVerification=False,port = None) -> None:
        # port is optional. If port== None default http/https willl be used. This is recommended 
        self.token = None
        self.host = host
        self.port = port
        self.component = component
        self.key = key
        self.dtLogIn = None
        self.callbackActionListener = None
        self.actionListenerActive = True
        self.logInfo = True
        self.timeout_sse = timeout_sse
        self.timeout_login = timeout_login
        self.sslVerification = sslVerification

    def logIn(self,useTimeout=True):
        LOG.info(f'Try Login for component:{self.component} with key:{self.key}')
        payload = {"id":int(self.component), "key":self.key}
        dtNow = datetime.datetime.now()
        reqUrl = f'{self.host}/login'
        if self.port != None:   reqUrl = f'{self.host}:{self.port}/login'
        if useTimeout and (self.dtLogIn != None):
            diff = dtNow - self.dtLogIn
            if diff.seconds <= self.timeout_login:
                ddiff = self.timeout_login - diff.seconds
                time.sleep(ddiff)
        try:
            response = requests.post(reqUrl,data=json.dumps(payload),verify=self.sslVerification)
            if response.status_code == 200:
                d = json.loads(response.content)
                self.token = d['token']
                self.dtLogIn = datetime.datetime.now()
            else:
                self.token = None
        except:
            LOG.exception("Error on connection: url:{}".format(reqUrl))
            self.token = None
    
    def isTokenValid(self):
        if self.token == None:  return False
        else:                   return True

    def reqSend(self,method,urlMethod,dSend={},recursiv=False):
        if self.token == None:
            self.logIn()
        headers = {'x-access-tokens':self.token}
        reqUrl = f'{self.host}/{urlMethod}'
        if self.port != None:   reqUrl = f'{self.host}:{self.port}/{urlMethod}'  
        LOG.info(f'request: {reqUrl}')
        LOG.debug(f'@token:{self.token}')
        LOG.debug(f'@data:{dSend}')

        d = {}
        try:
            resp = 0
            if method == 'get':
                resp = requests.get(reqUrl,headers=headers,data=json.dumps(dSend),verify=self.sslVerification)
            elif method == 'post':
                resp = requests.post(reqUrl,headers=headers,data=json.dumps(dSend),verify=self.sslVerification)
            elif method == 'put':
                resp = requests.put(reqUrl,headers=headers,data=json.dumps(dSend),verify=self.sslVerification)
            elif method == 'delete':
                resp = requests.delete(reqUrl,headers=headers,data=json.dumps(dSend),verify=self.sslVerification)
            # Process Data
            if resp.status_code == 200:
                d = json.loads(resp.content)
            elif resp.status_code == 401 :
                self.token  = None
        except:
            LOG.exception("Exception on connecion to butler")
            self.token  = None
            if recursiv==False:
                self.reqSend(method=method,urlMethod=urlMethod,dSend=dSend,recursiv=True)
            raise
        return  d

    def get(self,urlMethod,dSend={}):
        return self.reqSend(method='get',urlMethod=urlMethod,dSend=dSend)
    def put(self,urlMethod,dSend={}):
        return self.reqSend(method='put',urlMethod=urlMethod,dSend=dSend)
    def post(self,urlMethod,dSend={}):
        return self.reqSend(method='post',urlMethod=urlMethod,dSend=dSend)
    def delete(self,urlMethod,dSend={}):
        return self.reqSend(method='delete',urlMethod=urlMethod,dSend=dSend)

    def actionListener_setFunction(self,func):
        self.callbackActionListener = func
        
    def actionListener_task(self):
        url = f'{self.host}/actionListen'
        if self.port != None:  f'{self.host}:{self.port}/actionListen'
        
        LOG.info("Listen with sseclient to: {}".format(url))
        while(True):
            try:
                if self.token == None:
                    self.logIn()
                messages = sseclient.SSEClient(url,headers = {'x-access-tokens':self.token},verify=self.sslVerification,timeout=(self.timeout_sse,self.timeout_sse))
                #async for messages in sseclient.SSEClient(url,headers = {'x-access-tokens':self.token}):
                for resp in messages:
                    try:
                        LOG.info("actionListener msg='{}'".format(resp.data))
                        d = json.loads(resp.data)
                        self.callbackActionListener(d)
                    except:
                        LOG.exception("Fehler beim message auslesen")
            
            except HTTPError as eHttp:
                LOG.info(f'Error on connection. Set token=None')
                self.token=None
            except ReadTimeout:
                LOG.info(f'Reconnecting Reconnecting-Time={self.timeout_sse}')
            except Exception as e:
                LOG.exception(f'Unhandle Exception on sseclient.')

