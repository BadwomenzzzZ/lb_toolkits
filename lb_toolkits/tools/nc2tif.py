# -*- coding:utf-8 -*-
'''
@Project  : lb_toolkits
@File     : nc2tif.py
@Modify Time      @Author    @Version    
--------------    -------    --------    
2022/8/5 16:05      Lee       1.0         
@Description
------------------------------------
 
'''
import os
import sys
import numpy as np

import netCDF4
from lb_toolkits.tools import writetiff


def nc2tif(outname, filename, sdsname, fillvalue=-999):
    '''
    将NC文件中的数据集根据lat\lon维度进行投影输出geotiff文件
    :param outname: str, 输出tif文件名
    :param filename: str, 输入的nc文件名
    :param sdsname: str， 需要转换的数据集名
    :param fillvalue: 数据填充值
    :return: bool，成功返回TRUE，失败返回FALSE
    '''
    try:
        fp = netCDF4.Dataset(filename, 'r')

        dsetid = fp[sdsname]
        dims = dsetid.dimensions

        grid = False
        xdim = None
        ydim = None
        for item in dims :
            if 'lon' in item.lower() :
                grid = True
                xdim = item

            if 'lat' in item.lower() :
                grid = True
                ydim = item

        sdsinfo = dsetid.ncattrs()
        if xdim is not None and ydim is not None :
            x = fp[xdim][:]
            y = fp[ydim][:]
            xres = x[1] - x[0]
            yres = y[1] - y[0]

            trans = [x[0], xres, 0, y[0], 0, yres]
            data = fp[sdsname][:]
            if '_FillValue' in sdsinfo :
                fillvalue = sdsinfo['_FillValue']
            writetiff(outname, data, im_geotrans=trans, fillvalue=fillvalue)
        fp.close()

        return True
    except BaseException as e :
        print(e)
        return False

    # 后续更新根据coordinate属性来完成投影设置

    for item in sdsinfo :
        if 'coordinate' in item.lower() :
            grid = True



