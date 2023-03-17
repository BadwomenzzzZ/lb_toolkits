# coding:utf-8
'''
@Project: downloadsat
-------------------------------------
@File   : downloadGFS.py
-------------------------------------
@Modify Time      @Author    @Version    
--------------    -------    --------
2021/6/23 9:55     Lee        1.0         
-------------------------------------
@Desciption
-------------------------------------

'''

import os
import sys
import datetime
from lb_toolkits.tools import spiderdownload

# def check_file_status(filepath, filesize):
#
#     sys.stdout.write('\r')
#
#     sys.stdout.flush()
#
#     size = int(os.stat(filepath).st_size)
#
#     percent_complete = (size/filesize)*100
#     print('%.3f %s' % (percent_complete, '% Completed'))
#     sys.stdout.write('%.3f %s' % (percent_complete, '% Completed'))
#
#     sys.stdout.flush()

def downloadGFS(outdir, nowdate, issuetime=0, forecasttime=[0], regoin=[0.0, 360.0, 90.0, -90.0]) :
    '''
    see 'https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl'
    or 'https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/'
    :param nowdate: datetime, 当前时间
    :param issuetime: int, 发布时间，GFS是0、6、12、18点起始预报
    :param forecasttime: 根据预报时间往后多少小时
    :param regoin: 区域范围，[leftlon, rightlon, toplat, bottomlat]
    :return:
    '''


    issuetime = int(issuetime)
    if not issuetime in [0, 6, 12, 18] :
        print('forecast[%d] is not "0, 6, 12, 18", please check it...' %(issuetime))


    for mhour in forecasttime :

        url = r'https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/' \
              r'gfs.{YYYYMMDD}/{issuetime}/atmos/gfs.t{issuetime}z.pgrb2.0p25.f{forecasttime}'.format(
            issuetime='%02d' %(issuetime),
            forecasttime='%03d' %(mhour),
            YYYYMMDD=nowdate.strftime('%Y%m%d')
        )

        # url = r'https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl?' \
        #       r'file=gfs.t{issuetime}z.pgrb2.0p25.f{forecasttime}&lev_100_mb=on&lev_2_mb=on&var_UGRD=on&subregion=&' \
        #       r'leftlon={leftlon}&rightlon={rightlon}&toplat={toplat}&bottomlat={bottomlat}&' \
        #       r'dir=%2Fgfs.{YYYYMMDD}%2F{issuetime}%2Fatmos'.format(
        #     issuetime='%02d' %(issuetime),
        #     forecasttime='%03d' %(mhour),
        #     leftlon=regoin[0],
        #     rightlon=regoin[1],
        #     toplat=regoin[2],
        #     bottomlat=regoin[3],
        #     YYYYMMDD=nowdate.strftime('%Y%m%d')
        # )

        outname = 'gfs.t{issuetime}z.pgrb2.0p25.f{forecasttime}'.format(
            issuetime='%02d' %(issuetime),
            forecasttime='%03d' %(mhour)
        )

        spider = spiderdownload()
        spider.download(outdir, url)

        # try:
        #
        #     cmd = 'wget "%s"' %(url)
        #     os.system(cmd)
        #     print('download %s success...' %(outname))
        # except BaseException as e:
        #     print(e)



