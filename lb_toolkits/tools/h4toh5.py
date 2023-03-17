#coding:utf-8

import os
import sys
import h5py



def h4toh5(h4file, h5file):
    from pyhdf import SD

    if not os.path.isfile(h4file):
        print('%s is not exist, will continue...' %(h4file))
        return False

    fp4 = SD.SD(h4file, SD.SDC.READ)
    fp5 = h5py.File(h5file, 'w')
    attrs = fp4.attributes(full=1)
    # for item in fp4.attributes().keys() :
        # print(item)
        # print(fp4.attributes(item))
        # fp5.attrs[item] = fp4.attr(item)
    for item in fp4.attributes().keys():
        print(item)

        try:
            fp5.attrs[item] = attrs[item][0]
        except BaseException as e:
            print(e)

    for sdsname in fp4.datasets().keys() :
        print(sdsname)
        try:
            if 'Albedo_Map' in sdsname :
                sds4id = fp4.select(sdsname)
                data = sds4id[:]
                dsetid = fp5.create_dataset(name= 'Albedo_Map', data=data, compression=9)
                attrs = sds4id.attributes(full=1)
                for key in sds4id.attributes() :
                    dsetid.attrs[key] =  attrs[key][0]
            else:
                sds4id = fp4.select(sdsname)
                data = sds4id[:]
                dsetid = fp5.create_dataset(name= sdsname, data=data, compression=9)
                attrs = sds4id.attributes(full=1)
                for key in sds4id.attributes() :
                    dsetid.attrs[key] =  attrs[key][0]
        except BaseException as e:
            print(e)
    fp4.end()
    fp5.close()

    return True











