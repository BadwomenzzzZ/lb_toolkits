#coding:utf-8
import sys
import os
import cdsapi
import datetime

# from config import *


def checkdict(key, dictinfo) :

    if key in dictinfo :
        return True
    else:
        raise Exception('The key "%s" not in dict' %(key))
        return False

def download_era5_profile(outname,
                          strdate,
                          prof_info,
                          area_info=None,
                          m_client=None,
                          redownload=False):
    '''
    下载ERA5 再分析的廓线数据
    :param strdate: string, 下载的数据时间
    :param outname: string, 输出文件名
    :param prof_info: dict, 下载廓线的相关信息
    :param area_info: dict or list[maxlat, minlon, minlat, maxlon],
                        所需下载的区域范围，默认为全球
    :param m_client: 登录官网连接
    :param redownload: bool, 重新下载标识
    :return:
    '''

    startdate = datetime.datetime.strptime(strdate, '%Y%m%d%H%M%S')

    # 拼接输出文件名
    # if outpath is None:
    #     outname = os.path.join('./', '%s_pl.nc' % (startdate.strftime('%Y%m%d%H%M')))
    # else:
    #     outname = os.path.join(outpath, '%s_pl.nc' % (startdate.strftime('%Y%m%d%H%M')))

    # 文件是否重复下载
    if os.path.isfile(outname) and not redownload:
        return None

    if m_client is None:
        m_client = cdsapi.Client()

    downinfo = {}
    downinfo['product_type'] = 'reanalysis'
    if checkdict('variable', prof_info) :
        downinfo['variable'] = prof_info['variable']

    if checkdict('pressure_level', prof_info) :
        downinfo['pressure_level'] = prof_info['pressure_level']

    downinfo['year']  = startdate.strftime('%Y')
    downinfo['month'] = startdate.strftime('%m')
    downinfo['day']   = startdate.strftime('%d')
    downinfo['time']  = [ startdate.strftime('%H:%M'),]

    if area_info is not None :
        if isinstance(area_info, dict) :
            downinfo['area'] = [
                area_info['maxlat'],
                area_info['minlon'],
                area_info['minlat'],
                area_info['maxlon'],
            ]
        elif isinstance(area_info, list) :
            downinfo['area'] = area_info
        else:
            raise Exception('area_info need to include "maxlat, minlon, minlat, maxlon"')

    downinfo['format'] = 'netcdf'
    # downinfo['format'] = 'grib'

    m_client.retrieve(
        'reanalysis-era5-pressure-levels',
        # {
        #     'product_type': 'reanalysis',
        #     # 下载变量
        #     'variable': prof_info['variable'],
        #     # 下载气压层
        #     'pressure_level': prof_info['pressure_level'],
        #     'year': startdate.strftime('%Y'),
        #     'month': startdate.strftime('%m'),
        #     'day': startdate.strftime('%d'),
        #     'time': [
        #         startdate.strftime('%H:%M'),
        #     ],
        #     'area': [
        #         area_info['maxlat'],
        #         area_info['minlon'],
        #         area_info['minlat'],
        #         area_info['maxlon'],
        #     ],
        #     'format': 'netcdf',  # 下载数据文件为netcdf格式
        #     # 'format': 'grib',   # 下载数据文件为grib格式
        # },
        downinfo,
        outname)
    print('download ==>[%s]  success...' %(outname))

def download_era5_surface(strdate,
                          outname,
                          surf_info,
                          area_info=None,
                          m_client=None,
                          redownload=False):
    '''
    下载ERA5 再分析的地面数据
    :param strdate: string, 下载的数据时间
    :param outname: string, 输出文件名
    :param surf_info: dict, 下载廓线的相关信息
    :param area_info: dict or list[maxlat, minlon, minlat, maxlon],
                        所需下载的区域范围，默认为全球
    :param m_client: 登录官网连接
    :param redownload: bool, 重新下载标识
    :return:
    '''

    startdate = datetime.datetime.strptime(strdate, '%Y%m%d%H%M%S')

    # if outpath is None:
    #     outname = os.path.join('./', '%s_sf.nc' % (startdate.strftime('%Y%m%d%H%M')))
    # else:
    #     outname = os.path.join(outpath, '%s_sf.nc' % (startdate.strftime('%Y%m%d%H%M')))

    # 文件是否重复下载
    if os.path.isfile(outname)  and not redownload:
        return None

    if m_client is None :
        m_client = cdsapi.Client()

    downinfo = {}
    downinfo['product_type'] = 'reanalysis'
    if checkdict('variable', surf_info) :
        downinfo['variable'] = surf_info['variable']

    downinfo['year']  = startdate.strftime('%Y')
    downinfo['month'] = startdate.strftime('%m')
    downinfo['day']   = startdate.strftime('%d')
    downinfo['time']  = [ startdate.strftime('%H:%M'),]

    if area_info is not None :
        if isinstance(area_info, dict) :
            downinfo['area'] = [
                area_info['maxlat'],
                area_info['minlon'],
                area_info['minlat'],
                area_info['maxlon'],
            ]
        elif isinstance(area_info, list) :
            downinfo['area'] = area_info
        else:
            raise Exception('area_info need to include "maxlat, minlon, minlat, maxlon"')

    downinfo['format'] = 'netcdf'
    # downinfo['format'] = 'grib'


    m_client.retrieve(
        'reanalysis-era5-single-levels',
        # {
        #     'product_type': 'reanalysis',
        #     'variable': surf_info['variable'],
        #     'year': startdate.strftime('%Y'),
        #     'month': startdate.strftime('%m'),
        #     'day': startdate.strftime('%d'),
        #     'time': [
        #         startdate.strftime('%H:%M'),
        #     ],
        #     'area': [
        #         area_info['maxlat'],
        #         area_info['minlon'],
        #         area_info['minlat'],
        #         area_info['maxlon'],
        #     ],
        #     'format': 'netcdf',  # 下载数据文件为netcdf格式
        #     # 'format': 'grib',   # 下载数据文件为grib格式
        # },
        downinfo,
        outname )
    print('download ==>[%s]  success...' %(outname))






