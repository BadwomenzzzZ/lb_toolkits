# coding:utf-8
'''
@Project: downloadsat
-------------------------------------
@File   : downloadSentinel.py
-------------------------------------
@Modify Time      @Author    @Version    
--------------    -------    --------
2021/6/22 15:09     Lee        1.0         
-------------------------------------
@Desciption
-------------------------------------

'''
import shapefile
import codecs
from json import dumps
from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt

def shp2geojson(fileshp, filegeojson):

    reader = shapefile.Reader(fileshp)
    fields = reader.fields[1:]
    field_names = [field[0] for field in fields]
    buffer = []

    for sr in reader.shapeRecords():
        record = sr.record
        record = [r.decode('gb2312', 'ignore') if isinstance(r, bytes)
                  else r for r in record]
        atr = dict(zip(field_names, record))
        geom = sr.shape.__geo_interface__
        buffer.append(dict(type="Feature", geometry=geom, properties=atr))
        # write the GeoJSON file
    geojson = codecs.open(filegeojson, "w", encoding="gb2312")
    geojson.write(dumps({"type": "FeatureCollection", "features": buffer}, indent=2) + "\n")
    geojson.close()

def downloadSentinel(username, password, starttime, endtime, outpath='./',
                     platformname='Sentinel-2', producttype='S2MSI2A',
                     footprint=None, geojson = None, filename='*', **keywords):

    '''
    see 'https://scihub.copernicus.eu/twiki/do/view/SciHubUserGuide/3FullTextSearch'
    :param username: 用户名
    :param password:密码
    :param starttime: 起始时间
    :param endtime: 结束时间
                    datetime : (str or datetime) or str, optional
                    A time interval filter based on the Sensing Start Time of the products.
                    Expects a tuple of (start, end), e.g. ("NOW-1DAY", "NOW").
                    The timestamps can be either a Python datetime or a string in one of the
                    following formats:

                        - yyyyMMdd
                        - yyyy-MM-ddThh:mm:ss.SSSZ (ISO-8601)
                        - yyyy-MM-ddThh:mm:ssZ
                        - NOW
                        - NOW-<n>DAY(S) (or HOUR(S), MONTH(S), etc.)
                        - NOW+<n>DAY(S)
                        - yyyy-MM-ddThh:mm:ssZ-<n>DAY(S)
                        - NOW/DAY (or HOUR, MONTH etc.) - rounds the value to the given unit

                    Alternatively, an already fully formatted string such as "[NOW-1DAY TO NOW]" can be
                    used as well.
    :param outpath: 输出路径
    :param platformname: Sentinel-1/Sentinel-2/Sentinel-3/Sentinel-5 Precursor
    :param producttype: Sentinel-1: SLC, GRD, OCN
                        Sentinel-2: S2MSI2A,S2MSI1C, S2MS2Ap
                        Sentinel-3: SR_1_SRA___, SR_1_SRA_A, SR_1_SRA_BS,
                                    SR_2_LAN___, OL_1_EFR___, OL_1_ERR___, OL_2_LFR___,
                                    OL_2_LRR___, SL_1_RBT___, SL_2_LST___, SY_2_SYN___,
                                    SY_2_V10___, SY_2_VG1___, SY_2_VGP___.
                        Sentinel-5P: L1B_IR_SIR, L1B_IR_UVN, L1B_RA_BD1, L1B_RA_BD2,
                                    L1B_RA_BD3, L1B_RA_BD4, L1B_RA_BD5, L1B_RA_BD6,
                                    L1B_RA_BD7, L1B_RA_BD8, L2__AER_AI, L2__AER_LH,
                                     L2__CH4, L2__CLOUD_, L2__CO____, L2__HCHO__,
                                     L2__NO2___, L2__NP_BD3, L2__NP_BD6,
                                     L2__NP_BD7, L2__O3_TCL, L2__O3____, L2__SO2___.
    :param footprint:
    :param geojson: optional, geogson format
    :param filename: 模糊匹配文件名，eg.*1SD?_20141003T003840*
    :return:
    '''

    #创建SentinelAPI，请使用哥白尼数据开放获取中心自己的用户名及密码
    # api =SentinelAPI(username, password,'https://scihub.copernicus.eu/apihub/')


    if platformname in ['Sentinel-5 Precursor'] :
        api =SentinelAPI(username, password,'https://s5phub.copernicus.eu/dhus/')
    else:
        api =SentinelAPI(username, password,'https://scihub.copernicus.eu/dhus/')
    #读入某地区的geojson文件并转换为wkt格式的文件对象，相当于足迹
    if footprint is None and geojson is not None:
        footprint =geojson_to_wkt(read_geojson(geojson))

    #通过设置OpenSearch API查询参数筛选符合条件的所有Sentinel-2
    products =api.query(area=footprint,                        #Area范围
                        date=(starttime, endtime),        #搜索的日期范围
                        platformname=platformname,        #卫星平台名，Sentinel-2
                        producttype=producttype,            #
                        filename=filename,
                        **keywords)

    #通过for循环遍历并打印、下载出搜索到的产品文件名
    for product in products:
        #通过OData API获取单一产品数据的主要元数据信息
        product_info = api.get_product_odata(product)

        #打印下载的产品数据文件名
        print(product_info['title'])

        #下载产品id为product的产品数据
        api.download(product,directory_path=outpath,checksum=True)




