=================================
fypy调用示例
=================================

fy3pro
-----------------------------------------

.. code-block:: python

    from lb_toolkits.fypy import fy3pro
    from lb_toolkits.tools import readhdf


fy4pro
-----------------------------------------

.. code-block:: python

    from lb_toolkits.fypy import fy4pro
    from lb_toolkits.tools import readhdf

    l1name = r'FY4A-_AGRI--_N_DISK_1047E_L1-_FDI-_MULT_NOM_20220810040000_20220810041459_4000M_V0001.HDF'

    fillvalue = 0.0
    data = readhdf(l1name, 'NOMChannel01')
    cal = readhdf(l1name, 'CALChannel01')
    flag = (data<0) | (data>=len(cal))
    data[flag] = 0

    ref = cal[data]
    ref[flag] = fillvalue
    mpro = fy4pro()
    mpro.nom2gll(ref, outname='./data/FY4A-_AGRI--_N_DISK_1047E_L1-_GEO-_MULT_NOM_20220810040000.tif',
                 fillvalue=fillvalue, bbox=(70, 18, 140, 55),)

ahi8_l1_pro
-----------------------------------------

.. code-block:: python

    from lb_toolkits.fypy import hsd2hdf
    outdir = r'./H8/20211012'
    hsdpath = r'./H8'
    nowdate = datetime.datetime.strptime('20211012_0320', '%Y%m%d_%H%M')

    hsd2hdf(outdir, nowdate, hsdpath)



