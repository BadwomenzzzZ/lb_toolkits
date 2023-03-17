# -*- coding:utf-8 -*-
'''
@Project     : lb_toolkits

@File        : downloadLandcover.py

@Modify Time :  2022/11/11 17:11   

@Author      : Lee    

@Version     : 1.0   

@Description :

'''
import os
import sys
import numpy as np
import datetime
from lb_toolkits.tools import spiderdownload

def downloadLandcover(outdir,  minX=70, minY=10, maxX=140, maxY=55, skip=False):

    urllist = []
    for lat in np.arange(int(np.floor(minY)/2)*2, np.ceil(maxY), step=2) :
        for lon in np.arange(int(np.floor(minX)), np.ceil(maxX), step=2) :
            if lat < -90 or lat > 90 :
                continue

            if lon < -180 or lat > 180 :
                continue

            if lat >= 0 :
                strlat = 'N%02d' %(lat)
            else:
                strlat = 'S%02d' %(lat)

            if lon >= 0 :
                strlon = 'E%03d' %(lon)
            else:
                strlon = 'W%03d' %(lon)

            url = r'http://data.ess.tsinghua.edu.cn/data/fromglc10_2017v01/' \
                  r'fromglc10v01_%d_%d.tif' %(lat, lon)
            urllist.append(url)

            spider = spiderdownload()
            spider.download(outdir, url=url, skip=skip)

    return urllist