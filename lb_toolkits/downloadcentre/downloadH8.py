# -*- coding:utf-8 -*-
'''
@Project  : lb_toolkits
@File     : downloadH8.py
@Modify Time      @Author    @Version    
--------------    -------    --------    
2022/7/25 9:53      Lee       1.0         
@Description
------------------------------------
 
'''
import os
import sys
import datetime
import time

from lb_toolkits.tools import ftppro
from lb_toolkits.tools import writejson

# /jma/netcdf/202103/30
# NC_H08_20210330_0210_R21_FLDK.02401_02401.nc
# NC_H08_20210330_0200_R21_FLDK.06001_06001.nc

class downh8file(object):

    def __init__(self, ftphost, username, password):

        self.ftp = ftppro(ftphost, username, password)
        self.dstfilelist = []

    def download_ahi8_l1_netcdf(self, nowdate, dstpath, okpath=None, pattern=['02401','06001']):
        '''
        下载葵花8号卫星L1 NetCDF数据文件
        # Available Himawari  L1 Gridded Data

        ## Full-disk
         Projection: EQR
         Observation area: 60S-60N, 80E-160W
         Temporal resolution: 10-minutes
         Spatial resolution: 5km (Pixel number: 2401, Line number: 2401)
                             2km (Pixel number: 6001, Line number: 6001)
         Data: albedo(reflectance*cos(SOZ) of band01~band06)
               Brightness temperature of band07~band16
               satellite zenith angle, satellite azimuth angle,
               solar zenith angle, solar azimuth angle, observation hours (UT)

        ## Japan Area
         Projection: EQR
         Observation area: 24N-50N, 123E-150E
         Temporal resolution: 10-minutes
         Spatial resolution: 1km (Pixel number: 2701, Line number: 2601)
         Data: albedo(reflectance*cos(SOZ) of band01~band06)
               Brightness temperature of band07, 14, 15
               satellite zenith angle, satellite azimuth angle,
               solar zenith angle, solar azimuth angle, observation hours (UT)
        :param nowdate:
        :param dstpath:
        :param okpath:
        :param pattern:
        :return:
        '''
        # 拼接H8 ftp 目录
        sourceRoot = os.path.join('/jma/netcdf', nowdate.strftime("%Y%m"), nowdate.strftime("%d"))
        sourceRoot = sourceRoot.replace('\\','/')

        self._download_ahi8_l1(nowdate, sourceRoot, dstpath, okpath, pattern)

    def download_ahi8_l1_hsd(self, nowdate, dstpath, okpath=None, pattern=None):
        '''
        # Available Himawari Standard Data

        ## Full-disk
         Observation area: Full-disk
         Temporal resolution: 10-minutes
         Spatial resolution: 0.5km (band 3), 1km (band 1,2,4), 2km (band 5-16)

        ## Japan Area
         Observation area: Japan area (Region 1 & 2)
         Temporal resolution: 2.5-minutes
         Spatial resolution: 0.5km (band 3), 1km (band 1,2,4), 2km (band 5-16)

        ## Target Area
         Observation area: Target area (Region 3)
         Temporal resolution: 2.5-minutes
         Spatial resolution: 0.5km (band 3), 1km (band 1,2,4), 2km (band 5-16)

        ## Color Image Data
         png images of Full-disk, Japan area and Target area, compositing three visible
         bands (blue: 0.47 micron; green: 0.51 micron; red: 0.64 micron).
        :param nowdate: datetime, 文件名中的时间（UTC）
        :param dstpath: 存储数据文件目录
        :param okpath: 输出OK文件路径
        :param pattern: 模糊匹配文件名
        :return:
        '''
        # 拼接H8 ftp 目录
        '''
        # Structure of FTP Directories

         /jma/hsd
               +---/[YYYYMM]
                      +---/[DD]
                             +---/[hh]
        
         where YYYY: 4-digit year of observation start time (timeline);
               MM: 2-digit month of timeline;
               DD: 2-digit day of timeline; and
               hh: 2-digit hour of timeline.
        '''
        sourceRoot = os.path.join('/jma/hsd',
                                  nowdate.strftime("%Y%m"),
                                  nowdate.strftime("%d"),
                                  nowdate.strftime("%H"))
        sourceRoot = sourceRoot.replace('\\','/')

        self._download_ahi8_l1(nowdate, sourceRoot, dstpath, okpath, pattern)

    def _download_ahi8_l1(self, nowdate, sourceRoot, dstpath, okpath=None, pattern=None):

        # 获取文件列表
        self.files = self.GetFileList(nowdate, sourceRoot, pattern)
        if len(self.files) == 0 :
            print('Not Match the file')
            return

        if not os.path.exists(dstpath):
            os.makedirs(dstpath)
            print('create dir <{0}> success !'.format(dstpath))

        if okpath is not  None :
            if not os.path.exists(okpath) :
                os.makedirs(okpath)
                print('create dir <{0}> success !'.format(okpath))

        for srcname in self.files:
            print('='*100)
            file = os.path.basename(srcname)
            dstname = os.path.join(dstpath, file)
            if okpath is None :
                okname = dstname + '.ok'
            else:
                okname = os.path.join(okpath, file + '.OK')

            self.dstfilelist.append(dstname)
            if os.path.isfile(okname) and os.path.isfile(dstname) :
                print('%s is exist, will continue...' %(dstname))
                continue

            downinfo = {}

            downinfo['srcname'] = srcname
            downinfo['dstname'] = dstname
            downinfo['okname'] = okname

            stime = time.time()
            print(datetime.datetime.now(), 'download file : ', srcname)

            downinfo['starttime'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if self.ftp.downloadFile(srcname, dstpath):
                downinfo['endtime'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                downinfo['status'] = 0
                self.writeok(okname, downinfo)
                print('download %s success...' %(dstname))

            etime = time.time()
            print('cost %.2f sec...' %(etime - stime))

    def GetFileList(self, nowdate, srcpath, pattern=None):

        downfiles = []

        srcpath = srcpath.replace('\\', '/')

        files = self.ftp.listdir(srcpath)
        files.sort()
        for file in files :
            strtime = nowdate.strftime('%Y%m%d_%H%M')
            downflag = True
            if not strtime in file :        # 匹配对应时间，精确到小时级
                continue

            # 根据传入的匹配参数，匹配文件名中是否包含相应的字符串
            # if pattern is not None and isinstance(pattern, list) :
            #     for item in pattern :
            #         if not item in file :
            #             downflag = False
            #             break
            if pattern is not None and isinstance(pattern, list) :
                for item in pattern :
                    if item in file :
                        downflag = True
                        break
                    else:
                        downflag = False

            if downflag :
                srcname = os.path.join(srcpath, file)
                srcname = srcname.replace('\\','/')

                downfiles.append(srcname)

        return downfiles

    def writeok(self, okname, info):

        writejson(okname, info)

    def _download(self, srcfile, dstfile, blocksize=5*1024, skip=True):
        ftp = self.ftp.connect()
        if ftp is None :
            return False

        srcsize = ftp.size(srcfile)
        if skip :
            if os.path.isfile(dstfile) :
                dstsize = os.path.getsize(dstfile)
        else:
            dstsize = 0

        if srcsize <= dstsize :
            return

        conn = ftp.transfercmd('RETR ' + srcfile, srcsize)

        with open(dstfile, 'ab') as fp :
            while True :
                data = conn.recv(blocksize)
                if not data :
                    break

                fp.write(data)

        self.ftp.close(ftp)

