# -*- coding:utf-8 -*-
'''
@Project  : lb_toolkits
@File     : downloadFY.py
@Modify Time      @Author    @Version    
--------------    -------    --------    
2022/7/31 22:35      Lee       1.0         
@Description
------------------------------------
 
'''
import os
import sys
import numpy as np
import time
import datetime


from lb_toolkits.tools import ftppro

ftphost = 'ftp.nsmc.org.cn'

FYProdInfo = {
    'FY4A' : {
        'AGRI' : ['ACI', 'AMV',
                               'CFR', 'CIX', 'CLM', 'CLP', 'CLT', 'CTH', 'CTP', 'CTT',
                               'DLR', 'DSD', 'FHS', 'FOG', 'LPW', 'LSE', 'LST', 'OLR',
                               'QPE', 'RSR', 'SSI', 'SST', 'TBB', 'TFP', 'ULR'],
        'GIIRS' : ['AVP'],
    },
    'FY4B' : {
        'AGRI' : ['CTH', 'CTP', 'CTT', 'QPE'],
    },
    'FY3D' : {
        'MERSI' : ['CLA', 'NVI', 'PWS', 'PWV'],
    }

}


class downloadFY(object):

    def __init__(self, username, password):

        self.ftp = ftppro(ftphost, username, password)
        self.connect()
        self.dstfilelist = []

    def connect(self):
        try:
            self.ftp.connect()
            # self.ftp.close()
        except BaseException :
            raise Exception('登录失败，请连接并进行FTP账号注册。http://fy4.nsmc.org.cn/data/en/data/realtime.html')


    def download_fy_l1(self, dstpath, starttime, endtime=None, satid='FY4A',
                   instid='AGRI', regionid='DISK',resolution=0.04,
                   geoflag=False, pattern=None, skip=False):
        '''
        下载FY3D MERSI、FY4A AGRI、GIITS、LMI L1数据文件
        :param starttime: datetime, 数据下载时间(UTC)
        :param dstpath: 下载存储路径
        :param satid: 卫星名, FY3D/FY4A/FY4B
        :param instid: 载荷名 MERSI/AGRI/GIIRS/LMI
        :param regionid: 观测区域，DISK/REGC
        :param resolution: float, degree，数据分辨率
        :param geoflag: bool, default False,是否需要
                        下载对应时间的GEO文件，默认是不下载，
                        如果需要下载对应的GEO，需要将geoflag=True
        :return:
        '''

        # /FY4A/AGRI/L1/FDI/DISK/4000M/2022/20220609
        # /FY4A/GIIRS/L1/IRD/REGX/2022/20220609

        if endtime is None :
            endtime = starttime

        L1FileList = []
        # 拼接目录
        if satid in ['FY4A'] :
            L1FileList = self._PathForFY4AL1(starttime, endtime,
                                                  satid=satid, instid=instid,
                                                  regionid=regionid, resolution=resolution,
                                                  pattern=pattern, geoflag=geoflag)

        elif satid in ['FY4B'] :
            raise Exception('官方暂未发布FY4B L1数据')
        elif satid in ['FY3D'] :
            L1FileList = self._PathForFY3DMERSIL1(starttime, endtime,
                                                       satid=satid, instid=instid,
                                                       regionid=regionid, resolution=resolution,
                                                       pattern=pattern, geoflag=geoflag)
        else:
            raise Exception('暂不支持【%s / %s】L1数据下载' %(satid, instid))


        if skip :
            return L1FileList
        else:
            self.download(dstpath, L1FileList)
            return L1FileList


    def download_fy_l2(self, dstpath, starttime, endtime=None,
                       satid='FY4A', instid='AGRI', prodid='CLM',
                       regionid='DISK',resolution=0.04,
                       pattern=None, skip=False):
        '''
        下载FY3D MERSI、FY4A AGRI、GIITS、LMI L1数据文件
        :param starttime: datetime, 数据下载时间(UTC)
        :param dstpath: 下载存储路径
        :param satid: 卫星名, FY3D/FY4A/FY4B
        :param instid: 载荷名 MERSI/AGRI/GIIRS/LMI
        :param regionid: 观测区域，DISK/REGC
        :param resolution: float, degree，数据分辨率
        :return:
        '''

        if endtime is None :
            endtime = starttime

        L2FileList = []
        # 拼接目录
        if satid in ['FY4A'] :
            L2FileList = self._PathForFY4AL2(starttime, endtime,
                                             satid=satid, instid=instid,
                                             prodid=prodid, regionid=regionid,  pattern=pattern)

        elif satid in ['FY4B'] :
            L2FileList = self._PathForFY4BL2(starttime, endtime,
                                             satid=satid, instid=instid,
                                             prodid=prodid, regionid=regionid,  pattern=pattern)
        # elif satid in ['FY3D'] :
        #     L2FileList = self._PathForFY3DMERSIL2(starttime, endtime,
        #                                           satid=satid, instid=instid, prodid=prodid,
        #                                           regionid=regionid, resolution=resolution,
        #                                           pattern=pattern)
        else:
            raise Exception('暂不支持【%s %s】产品【%s】下载' %(satid, instid, prodid))


        if skip :
            return L2FileList
        else:
            self.download(dstpath, L2FileList)
            return L2FileList



    def _PathForFY4AL1(self, starttime, endtime,
                       satid='FY4A', instid='AGRI',
                       regionid='DISK', resolution=0.04,
                       pattern=None, geoflag=False):

        matchfiles = []

        strRes = '%dM' %(int(resolution * 100 * 1000))
        if not strRes in ['500M', '1000M', '2000M', '4000M'] :
            raise Exception("请确认输入的分辨率是否正确，只支持下载【'500M', '1000M', '2000M', '4000M'】")

        nowdate = starttime
        while nowdate <= endtime :

            if instid in ['AGRI'] :
                L1Path = os.path.join('/FY4A/AGRI/L1/FDI', regionid, strRes,
                                          nowdate.strftime("%Y"), nowdate.strftime("%Y%m%d"))
                GeoPath = os.path.join('/FY4A/AGRI/L1/FDI', regionid, 'GEO',
                                       nowdate.strftime("%Y"), nowdate.strftime("%Y%m%d"))
            elif instid in ['GIIRS'] :
                L1Path = os.path.join('/FY4A/GIIRS/L1/IRD/REGX/',
                                          nowdate.strftime("%Y"), nowdate.strftime("%Y%m%d"))
                GeoPath = None
            else:
                raise Exception('只支持下载FY4A AGRI和GIIRS L1近实时数据')

            files = self.GetFileList(L1Path,
                                     pattern='*%s*%s*' %(nowdate.strftime('%Y%m%d%H'), strRes))
            matchfiles = self._checktime(matchfiles, starttime, endtime, files)

            if geoflag :
                files = self.GetFileList(GeoPath,
                                         pattern='*%s*%s*' %(nowdate.strftime('%Y%m%d%H'), strRes))
                matchfiles = self._checktime(matchfiles, starttime, endtime, files)

            nowdate += datetime.timedelta(hours=1)

        return matchfiles

    def _PathForFY4AL2(self, starttime, endtime,
                       satid='FY4A', instid='AGRI', prodid=None,
                       regionid='DISK', resolution=0.04,
                       pattern=None):

        matchfiles = []

        self._checkprodid(satid, instid, prodid)

        nowdate = starttime
        while nowdate <= endtime :

            if instid in ['AGRI'] :
                L1Path = os.path.join('/', satid, instid, 'L2/', prodid, regionid, 'NOM',
                                      nowdate.strftime("%Y"), nowdate.strftime("%Y%m%d"))
            elif instid in ['GIIRS'] :
                L1Path = os.path.join('/', satid, instid, 'L2/', prodid, 'DWELL',
                                      nowdate.strftime("%Y"), nowdate.strftime("%Y%m%d"))
            else:
                raise Exception('只支持下载FY4A AGRI和GIIRS L2近实时数据')

            files = self.GetFileList(L1Path,
                                     pattern='*%s*' %(nowdate.strftime('%Y%m%d%H')))
            matchfiles = self._checktime(matchfiles, starttime, endtime, files)

            nowdate += datetime.timedelta(hours=1)

        return matchfiles

    def _PathForFY4BL2(self, starttime, endtime,
                       satid='FY4B', instid='AGRI', prodid=None,
                       regionid='DISK', resolution=0.04,
                       pattern=None):

        matchfiles = []

        self._checkprodid(satid, instid, prodid)

        nowdate = starttime
        while nowdate <= endtime :

            if instid in ['AGRI'] :
                L1Path = os.path.join('/', satid, instid, 'L2/', prodid, regionid, 'NOM',
                                      nowdate.strftime("%Y"), nowdate.strftime("%Y%m%d"))
            elif instid in ['GIIRS'] :
                L1Path = os.path.join('/', satid, instid, 'L2/', prodid, 'DWELL',
                                      nowdate.strftime("%Y"), nowdate.strftime("%Y%m%d"))
            else:
                raise Exception('只支持下载FY4B AGRI L2近实时数据')

            files = self.GetFileList(L1Path,
                                     pattern='*%s*' %(nowdate.strftime('%Y%m%d%H')))
            matchfiles = self._checktime(matchfiles, starttime, endtime, files)

            nowdate += datetime.timedelta(hours=1)

        return matchfiles

    def _PathForFY3DMERSIL1(self, starttime, endtime,
                            satid='FY3D', instid='MERSI',
                            regionid='GBAL', resolution=0.01,
                            pattern=None, geoflag=False):
        matchfiles = []
        strRes = '%dM' %(int(resolution * 100 * 1000))
        if not strRes in ['250M', '1000M'] :
            raise Exception("请确认输入的分辨率是否正确，只支持下载【'250M', '1000M'】")

        nowdate = starttime
        while nowdate <= endtime :
            if instid in ['MERSI'] :
                L1Path = os.path.join('/L1/', nowdate.strftime("%Y%m%d"))
                GeoPath = os.path.join('/L1/', nowdate.strftime("%Y%m%d"))
            else:
                raise Exception('只支持下载FY3D MERSI L1 近实时数据')

            files = self.GetFileList(L1Path,
                                     pattern='*%s*%s*' %(nowdate.strftime('%Y%m%d_%H'), strRes))
            matchfiles = self._checktime(matchfiles, starttime, endtime, files)

            if geoflag :
                files = self.GetFileList(GeoPath,
                                         pattern='*%s*%s*' %(nowdate.strftime('%Y%m%d_%H'), strRes))
                matchfiles = self._checktime(matchfiles, starttime, endtime, files)

            nowdate += datetime.timedelta(hours=1)

        return matchfiles

    # def _PathForFY3DMERSIL2(self, starttime, endtime,
    #                         satid='FY3D', instid='MERSI',
    #                         regionid='GBAL', resolution=0.01,
    #                         pattern=None, prodid=None):
    #
    #     self._checkprodid(satid, instid, prodid)
    #
    #     matchfiles = []
    #     strRes = '%dM' %(int(resolution * 100 * 1000))
    #     if not strRes in ['250M', '1000M'] :
    #         raise Exception("请确认输入的分辨率是否正确，只支持下载【'250M', '1000M'】")
    #
    #     nowdate = starttime
    #     while nowdate <= endtime :
    #         if instid in ['MERSI'] :
    #             L2Path = os.path.join('/L2L3/', prodid, nowdate.strftime("%Y%m%d"))
    #         else:
    #             raise Exception('只支持下载FY3D MERSI L2 近实时数据')
    #
    #         files = self.GetFileList(L2Path,
    #                                  pattern='*%s*%s*' %(nowdate.strftime('%Y%m%d_%H'), strRes))
    #         matchfiles = self._checktime(matchfiles, starttime, endtime, files)
    #
    #         nowdate += datetime.timedelta(hours=1)
    #
    #     return matchfiles

    def download(self, dstpath, filelist):
        '''
        下载数据文件
        :param dstpath:
        :param filelist:
        :return:
        '''


        if not os.path.exists(dstpath):
            os.makedirs(dstpath)
            print('create dir <{0}> success !'.format(dstpath))

        # if okpath is not  None :
        #     if not os.path.exists(okpath) :
        #         os.makedirs(okpath)
        #         print('create dir <{0}> success !'.format(okpath))

        for srcname in filelist:
            print('='*100)
            file = os.path.basename(srcname)
            dstname = os.path.join(dstpath, file)
            # if okpath is None :
            #     okname = dstname + '.ok'
            # else:
            #     okname = os.path.join(okpath, file + '.OK')

            self.dstfilelist.append(dstname)
            # if os.path.isfile(okname) and os.path.isfile(dstname) :
            #     print('%s is exist, will continue...' %(dstname))
            #     continue

            downinfo = {}

            downinfo['srcname'] = srcname
            downinfo['dstname'] = dstname
            # downinfo['okname'] = okname

            stime = time.time()
            print(datetime.datetime.utcnow().strftime('【%Y-%m-%d %H:%M:%S(UTC)】'), 'download file : ', srcname)

            downinfo['starttime'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if self.ftp.downloadFile(srcname, dstpath):
                downinfo['endtime'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                downinfo['status'] = 0
                # self.writeok(okname, downinfo)
                print('download %s success...' %(dstname))

            etime = time.time()
            print('cost %.2f sec...' %(etime - stime))

    def listDir(self, path, pattern=None):
        '''
        列出远程路径下的文件或者文件夹
        :param path: 远程路径
        :return: list
        '''
        files = self.ftp.listdir(path, pattern)
        files.sort()

        return files

    def GetFileList(self, srcpath, pattern=None):

        downfiles = []

        srcpath = srcpath.replace('\\', '/')

        files = self.ftp.listdir(srcpath, pattern)
        files.sort()
        for file in files :
            downflag = True
            # 根据传入的匹配参数，匹配文件名中是否包含相应的字符串
            # if pattern is not None and isinstance(pattern, list) :
            #     for item in pattern :
            #         if not item in file :
            #             downflag = False
            #             break
            # if pattern is not None and isinstance(pattern, list) :
            #     for item in pattern :
            #         if item in file :
            #             downflag = True
            #             break
            #         else:
            #             downflag = False

            if downflag :
                srcname = os.path.join(srcpath, file)
                srcname = srcname.replace('\\','/')

                downfiles.append(srcname)

        return downfiles

    def _checktime(self, matchfiles, starttime, endtime, files, pattern=None):
        '''
        通过起始结束时间匹配满足条件的文件名
        :param matchfiles:
        :param starttime:
        :param endtime:
        :param files:
        :param pattern:
        :return:
        '''
        for file in files :
            matchfiles.append(file)

        return matchfiles


    def _checkprodid(self, satid, instid, prodid):
        if satid in FYProdInfo :
            SatInfo = FYProdInfo[satid]
            if instid in SatInfo :
                if prodid in SatInfo[instid] :
                    return True
                else:
                    raise Exception('产品【%s】不在官方发布【%s/%s】的产品范围内，请参考风云官网发布产品详情！'
                                    %(prodid, satid, instid), SatInfo[instid])
                    return False
            else:
                raise Exception('暂不支持【%s/%s】下载' %(satid, instid), '当前支持', list(SatInfo.keys()))
        else:
            raise Exception('暂不支持【%s】卫星下载' %(satid), '当前支持', list(FYProdInfo.keys()))


    # def writeok(self, okname, info):
    #
    #     writejson(okname, info)
    #

