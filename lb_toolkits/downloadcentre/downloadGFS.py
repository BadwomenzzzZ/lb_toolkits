# -*- coding:utf-8 -*-
'''
@Project  : lb_toolkits

@File     : downloadGFS.py

@Modify Time : 2022/8/11 15:34

@Author : Lee

@Version : 1.0

@Description :

'''

import os
import sys
import datetime
from lb_toolkits.tools import spiderdownload
import platform

from .config import WGET

def downloadGFS(outdir, nowdate, issuetime=0, forecasttime=[0], regoin=None, timeout=5*60) :
    '''
    参考：“https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl”
         “https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/”

    Parameters
    ----------
    outdir: str
        下载文件输出路径
    nowdate: datetime
        下载时间
    issuetime: int
        发布时间，GFS是0、6、12、18点起始预报
    forecasttime: list
        根据预报时间往后多少小时
    regoin: list
        区域范围，[minX, maxX, minY, maxY]
    timeout: int
        超时限制（秒，sec）

    Returns
    -------

    '''

    issuetime = int(issuetime)
    if not issuetime in [0, 6, 12, 18] :
        raise Exception('forecast[%d] is not "0, 6, 12, 18", please check it...' %(issuetime))


    for mhour in forecasttime :
        if regoin is None :
            url = r'https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/' \
                  r'gfs.{YYYYMMDD}/{issuetime}/atmos/gfs.t{issuetime}z.pgrb2.0p25.f{forecasttime}'.format(
                issuetime='%02d' %(issuetime),
                forecasttime='%03d' %(mhour),
                YYYYMMDD=nowdate.strftime('%Y%m%d')
            )
            spider = spiderdownload()
            spider.download(outdir, url)
        else:
            url = r'https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl?' \
              r'file=gfs.t{issuetime}z.pgrb2.0p25.f{forecasttime}&lev_100_mb=on&lev_2_mb=on&var_UGRD=on&subregion=&' \
              r'leftlon={leftlon}&rightlon={rightlon}&toplat={toplat}&bottomlat={bottomlat}&' \
              r'dir=%2Fgfs.{YYYYMMDD}%2F{issuetime}%2Fatmos'.format(
            issuetime='%02d' %(issuetime),
            forecasttime='%03d' %(mhour),
            leftlon=regoin[0], rightlon=regoin[1],
            bottomlat=regoin[2],toplat=regoin[3],
            YYYYMMDD=nowdate.strftime('%Y%m%d'))

            outname = os.path.join(outdir, 'gfs.t{issuetime}z.pgrb2.0p25.f{forecasttime}'.format(
                issuetime='%02d' %(issuetime),
                forecasttime='%03d' %(mhour)))

            try:

                if platform.system().lower() == 'windows' :
                    cmd = f'{WGET} "{url}" --tries=3 ' \
                          f'--timeout={timeout}' \
                          f'  -P {outdir}'
                else:
                    cmd = f'wget "{url}" --tries=3 ' \
                          f'--timeout={timeout}' \
                          f'  -P {outdir}'
                print(cmd)
                os.system(cmd)
                print('download %s success...' %(outname))
            except BaseException as e:
                print(e)



