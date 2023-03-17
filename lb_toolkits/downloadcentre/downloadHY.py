# -*- coding:utf-8 -*-
'''
@Project  : lb_toolkits
@File     : downloadHY.py
@Modify Time      @Author    @Version    
--------------    -------    --------    
2022/8/17 13:30      Lee       1.0         
@Description
------------------------------------
 
'''
import os
import sys
import datetime
import time

from lb_toolkits.tools import ftppro
from lb_toolkits.tools import writejson

FTPHOST = 'osdds-ftp.nsoas.org.cn'

class downloadHY(object):

    def __init__(self, username, password):

        self.ftp = ftppro(FTPHOST, username, password)
        self.connect()
        self.dstfilelist = []

    def connect(self):
        try:
            self.ftp.connect()
            # self.ftp.close()
        except BaseException :
            raise Exception('登录失败，请连接并进行FTP账号注册。http://fy4.nsmc.org.cn/data/en/data/realtime.html')





