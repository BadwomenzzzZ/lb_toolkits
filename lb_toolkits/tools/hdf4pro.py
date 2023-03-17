# -*- coding:utf-8 -*-
'''
@Project  : lb_toolkits
@File     : hdf4pro.py
@Modify Time      @Author    @Version    
--------------    -------    --------    
2022/7/12 18:09      Lee       1.0         
@Description
------------------------------------
 
'''
import os

def readhdf4(h4file, sdsname, dictsdsattrs=None, dictfileattrs=None):
    from pyhdf import SD
    if not os.path.isfile(h4file):
        print('%s is not exist, will continue...' %(h4file))
        return False

    fp4 = SD.SD(h4file, SD.SDC.READ)

    if sdsname in fp4.datasets().keys() :
        try:
            sds4id = fp4.select(sdsname)
            data = sds4id[:]
        except BaseException as e:
            print(e)
    fp4.end()

    if dictfileattrs is not None and dictsdsattrs is not None :
        return data, dictfileattrs, dictsdsattrs
    elif dictfileattrs is not None and dictsdsattrs is None :
        return data, dictfileattrs
    elif dictfileattrs is None and dictsdsattrs is not None :
        return data, dictsdsattrs
    else:
        return data


def readhdf4sdsattrs(h4file, sdsname):
    from pyhdf import SD

    sdsattrs = {}
    if not os.path.isfile(h4file):
        print('%s is not exist, will continue...' %(h4file))
        return sdsattrs
    try:
        fp4 = SD.SD(h4file, SD.SDC.READ)
        sds4id = fp4.select(sdsname)
        attrs = sds4id.attributes(full=1)
        for key in sds4id.attributes() :
            sdsattrs[key] =  attrs[key][0]
    except BaseException as e:
        print(e)

    return sdsattrs


def readhdf4fileattrs(h4file):
    from pyhdf import SD

    fileattrs = {}

    if not os.path.isfile(h4file):
        print('%s is not exist, will continue...' %(h4file))
        return fileattrs

    fp4 = SD.SD(h4file, SD.SDC.READ)

    attrs = fp4.attributes(full=1)

    for item in fp4.attributes().keys():
        try:
            fileattrs[item] = attrs[item][0]
        except BaseException as e:
            print(e)

    return fileattrs