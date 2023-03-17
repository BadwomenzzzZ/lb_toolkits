# -*- coding:utf-8 -*-
'''
@Project  : lb_toolkits
@File     : RasterAndVector.py
@Modify Time      @Author    @Version    
--------------    -------    --------    
2022/7/13 17:49      Lee       1.0         
@Description
------------------------------------
 
'''
import os
import sys
import numpy as np
import shapefile
from .jsonpro import writejson
from tqdm import tqdm
from osgeo import gdal, ogr, osr, gdalconst


class RasterPro() :

    def __init__(self, encoding='GBK'):
        gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES")
        gdal.SetConfigOption("SHAPE_ENCODING", encoding)
        gdal.UseExceptions()
        ogr.RegisterAll()

    def mask(self, InRaster, MaskShp, burn_name=None, burn_values=None):
        '''
        根据参考的tiff文件创建同等投影类型和数据维度的掩膜文件
        ref_tif--参考模板的geotiff文件
        input_shp--待转换的掩膜矢量文件
        burn_name--栅格化的属性字段名称
        :param InRaster:
        :param MaskShp:
        :param burn_name:
        :param burn_values:
        :return:
        '''
        ref_info=gdal.Open(InRaster)
        ref_data=ref_info.GetRasterBand(1).ReadAsArray()
        y_size,x_size=ref_data.shape

        geotransform=ref_info.GetGeoTransform()
        srs=ref_info.GetProjection()
        ref_info=None
        ref_data=None
        vector=ogr.Open(MaskShp)
        vl=vector.GetLayer(0)
        dst_ds = gdal.GetDriverByName('MEM').Create('',x_size,y_size,1,gdal.GDT_Byte)
        dst_ds.SetGeoTransform(geotransform)  # specify gettransform
        dst_ds.SetProjection(srs)  # export coords to file
        if burn_name is not None :
            gdal.RasterizeLayer(dst_ds,[1],vl,options=["ATTRIBUTE=%s"%burn_name])
        if burn_values is not None :
            gdal.RasterizeLayer(dst_ds,[1],vl,burn_values=burn_values)
        vector=None
        bd=dst_ds.GetRasterBand(1)
        dd=bd.ReadAsArray()
        # dst_ds.FlushCache()
        dst_ds=None

        return dd

    def resample(self):
        raise Exception('本功能待开发，请耐心等待')

    def clip(self):
        raise Exception('本功能待开发，请耐心等待')

    def merge(self, filelist, outname=None, resolution=None, fillvalue=None,
              epsg=4326, extent=None, resampleAlg=0):

        if resampleAlg == 0:
            resampleType = gdalconst.GRA_NearestNeighbour
        elif resampleAlg == 1:
            resampleType = gdalconst.GRA_Bilinear
        else:
            resampleType = gdalconst.GRA_Cubic

        if outname is None :
            mode = 'MEM'
            outname=''
        else:
            mode = 'GTiff'
        options = gdal.WarpOptions(
            dstSRS='EPSG:%d' %(epsg),
            format=mode,
            outputBounds=extent,    # (minX, minY, maxX, maxY)
            resampleAlg=resampleType,
            xRes=resolution, yRes=resolution,
            dstNodata=fillvalue,
            creationOptions=["COMPRESS=LZW"])
        ds = gdal.Warp(outname, filelist, options=options)

        if outname is None :
            im_data = ds.ReadAsArray(0, 0, ds.RasterXSize, ds.RasterYSize)#获取数据
            ds = None

            return im_data
        else:
            return outname

    def to_vector(self, shpname, rastername, layername=None, field=None):
        '''
        栅格转矢量
        :param shpname: 输出的矢量文件名
        :param rastername: 输入的栅格数据名
        :param layername: option, 待转图层名称
        :param field: option，图层属性字段名
        :return:
        '''
        rasterid = gdal.Open(rastername)
        inband = rasterid.GetRasterBand(1)
        maskband = inband.GetMaskBand()

        prj = osr.SpatialReference()
        prj.ImportFromWkt(rasterid.GetProjection())

        drv = ogr.GetDriverByName('ESRI Shapefile')
        if os.path.isfile(shpname) :
            drv.DeleteDataSource(shpname)

        polygon = drv.CreateDataSource(shpname)
        if layername is not None :
            poly_layer = polygon.CreateLayer(layername, srs=prj,
                                             geom_type=ogr.wkbMultiPolygon)
        else:
            poly_layer = polygon.CreateLayer(rastername[:-4], srs=prj,
                                             geom_type=ogr.wkbMultiPolygon)

        if field is not None :
            newfield = ogr.FieldDefn(field, ogr.OFTReal)
        else:
            newfield = ogr.FieldDefn('value', ogr.OFTReal)
        poly_layer.CreateField(newfield)

        gdal.FPolygonize(inband, maskband, poly_layer, 0)
        polygon.SyncToDisk()
        polygon = None



class VectorPro():
    '''
    https://blog.csdn.net/summer_dew/article/details/87930241
    '''
    def __init__(self, encoding='GBK'):
        gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES")
        gdal.SetConfigOption("SHAPE_ENCODING", encoding)
        gdal.UseExceptions()
        ogr.RegisterAll()

    def split(self, outpath, shapefilename, field):
        """
        拆分矢量文件为多个单要素矢量文件,注意拆分后的fid需要重置。
        :param shapefilename: 要拆分的矢量文件
        :param outpath: 生成的矢量文件保存目录
        :param field: 根据提供的字段进行矢量拆分
        :return:
        """
        if not os.path.isdir(outpath) :
            os.makedirs(outpath)



        data = ogr.Open(shapefilename)
        layer = data.GetLayer()
        spatial = layer.GetSpatialRef()
        geomType = layer.GetGeomType()
        layerDefn = layer.GetLayerDefn()
        fieldCount = layerDefn.GetFieldCount()
        feature = layer.GetNextFeature()
        while feature:
            fid = feature.GetFieldAsString(field)
            fileName, layerName = str(fid), str(fid)
            driverName = "ESRI Shapefile"
            driver = ogr.GetDriverByName(driverName)
            outShapeFileName = fileName + ".shp"
            outShapeFilePath = os.path.join(outpath, outShapeFileName)
            outData = driver.CreateDataSource(outShapeFilePath)
            gdal.SetConfigOption("SHAPE_ENCODING", "CP936")
            outLayer = outData.CreateLayer(layerName, spatial, geomType)
            for fieldIndex in range(fieldCount):
                fieldDefn = layerDefn.GetFieldDefn(fieldIndex)
                outLayer.CreateField(fieldDefn)
            outLayer = outData.GetLayer()
            feature.SetFID(0)
            outLayer.CreateFeature(feature)
            outData.Destroy()
            feature = layer.GetNextFeature()
        data.Destroy()

        return True

    def to_raster(self, outname, shpname, field, resolution,
                  fillvalue=None, all_touch=False):
        '''
        矢量转栅格
        :param outname: 输出栅格文件的名称
        :param shpname: 输入矢量文件的名称
        :param resolution: 输出栅格数据的分辨率
        :param field: str, 矢量文件中的字段信息转换成栅格数据的像元值
        :param fillvalue: 输出tif的填充值（NoData）
        :param all_touch: bool，是否进行八方向处理
        :return:
        '''
        vec = ogr.Open(shpname)
        layer = vec.GetLayer()

        extent = layer.GetExtent()
        srs = layer.GetSpatialRef()

        feature = layer.GetFeature(0)
        # for feat in layer.schema :
        #     name = feat.GetName()#获取字段名称
        #     if name == field :
        #         type = feat.GetTypeName()#获取字段类型
        #         type = feat.GetField(field)#获取字段类型
        #         print('字段名称：%s ,字段类型：%s'%(name, type))

        fid = feature.GetField(field)
        dtype = str(type(fid))

        dtype = getNPDType(dtype)

        lonmin, lonmax, latmin, latmax = extent

        line = int(np.ceil((latmax - latmin)/resolution))
        pixel = int(np.ceil((lonmax - lonmin)/resolution))
        band = 1

        trans = [lonmin, resolution, 0, latmax, 0, -resolution]

        driver = gdal.GetDriverByName('GTiff')
        ds = driver.Create(outname, pixel, line, band, dtype)

        ds.SetGeoTransform(trans)
        ds.SetProjection(str(srs))

        bands = ds.GetRasterBand(1)
        if fillvalue is not None :
            bands.SetNoDataValue(fillvalue)

        # bands.FlushCache()

        if all_touch :
            all_touch = 'True'
        else:
            all_touch = 'False'

        if field :
            gdal.RasterizeLayer(ds, [1], layer,
                                options=["ALL_TOUCHED="+all_touch, "ATTRIBUTE="+field])
        else:
            gdal.RasterizeLayer(ds, [1], layer,
                                options=["ALL_TOUCHED="+all_touch])

    def to_geojson(self, outname, shapename, shp_encoding='utf-8', json_encoding='utf-8'):

        reader = shapefile.Reader(shapename, encoding=shp_encoding)
        fields = reader.fields[1:]
        fieldname = [field[0] for field in fields]
        buffer = []
        for sr in tqdm(reader.shapeRecords()) :
            record = sr.record

            record = [r.decode('gb2312', 'ignore') if isinstance(r, bytes) else r for r in record]

            attr = dict(zip(fieldname, record))

            geom = sr.shape.__geo_interface__

            buffer.append(dict(type='Feature',
                               geometry=geom,
                               properties=attr))

        writejson(outname, dict(type= 'FeatureCollection', features=buffer))

    def createPoint(self, shpname, coords={'lat':[], 'lon':[]}, epsg=4326):
        '''
        利用GDAL 创建点矢量，将point转换成矢量数据
        :param shpname: 输出文件名
        :param coords: dict, eg. {'lat':[], 'lon':[]} 或者
                       list, eg. [[lon1, lat1], [lon2, lat2],... ]
        :param epsg: int,
        :return: None
        '''
        driver = ogr.GetDriverByName('ESRI Shapefile')
        # 如果文件存在，则删除后再创建
        if os.access(shpname, os.F_OK) :
            driver.DeleteDataSource(shpname)

        srs = osr.SpatialReference()
        srs.ImportFromEPSG(int(epsg))

        ds = driver.CreateDataSource(shpname)
        lyr = ds.CreateLayer('point', srs, ogr.wkbPoint)

        if isinstance(coords, dict) :
            if len(coords['lat']) != len(coords['lon']) :
                raise Exception('输入的经、纬度点数不一致，经度：[%d]  纬度：[%d]'
                                %(len(coords['lon']), len(coords['lat'])))

            for i in range(len(coords['lat'])):
                val_lat = float(coords['lat'][i])
                val_lon = float(coords['lon'][i])

                wkt = 'POINT(%f %f)' %(val_lon, val_lat)

                geom = ogr.CreateGeometryFromWkt(wkt)
                feature = ogr.Feature(lyr.GetLayerDefn())
                feature.SetGeometry(geom)
                lyr.CreateFeature(feature)
        elif isinstance(coords, list) :
            for item in coords:
                val_lat = float(item[1])
                val_lon = float(item[0])

                wkt = 'POINT(%f %f)' %(val_lon, val_lat)

                geom = ogr.CreateGeometryFromWkt(wkt)
                feature = ogr.Feature(lyr.GetLayerDefn())
                feature.SetGeometry(geom)
                lyr.CreateFeature(feature)
        else:
            raise Exception('coords类型必须是dict或者list')

        ds = None
        driver =None

    def createPolyline(self, shpname, coords={'lat':[], 'lon':[]}, epsg=4326):
        '''
        利用GDAL 创建线矢量，将polyline转换成矢量数据
        :param shpname: 输出文件名
        :param coords: dict, eg. {'lat':[], 'lon':[]} 或者
                       list, eg. [[lon1, lat1], [lon2, lat2],... ]
        :param epsg: int,
        :return: None
        '''
        driver = ogr.GetDriverByName('ESRI Shapefile')
        if os.access(shpname, os.F_OK) :
            driver.DeleteDataSource(shpname)

        srs = osr.SpatialReference()
        srs.ImportFromEPSG(int(epsg))

        ds = driver.CreateDataSource(shpname)
        lyr = ds.CreateLayer('polyline', srs, ogr.wkbLineString)

        if isinstance(coords, dict) :
            if len(coords['lat']) != len(coords['lon']) :
                raise Exception('输入的经、纬度点数不一致，经度：[%d]  纬度：[%d]'
                                %(len(coords['lon']), len(coords['lat'])))

            count = len(coords['lat'])
            for i in range(count-1):
                if i == count-1:
                    wkt = 'LINESTRING(%f %f,%f %f)' %(float(coords['lon'][i]), float(coords['lat'][i]),
                                                      float(coords['lon'][0]), float(coords['lat'][0]))
                else:
                    wkt = 'LINESTRING(%f %f,%f %f)' %(float(coords['lon'][i]  ), float(coords['lat'][i]  ),
                                                      float(coords['lon'][i+1]), float(coords['lat'][i+1]))
                geom = ogr.CreateGeometryFromWkt(wkt)
                feature = ogr.Feature(lyr.GetLayerDefn())
                feature.SetGeometry(geom)
                lyr.CreateFeature(feature)
        elif isinstance(coords, list) :
            pass
        else:
            raise Exception('coords类型必须是dict或者list')

        ds = None
        driver =None

    def createPolygon(self, shpname, coords={'lat':[], 'lon':[]}, epsg=4326):
        '''
        利用GDAL 创建面矢量，将polygon转换成矢量数据
        :param shpname: 输出文件名
        :param coords: dict, eg. {'lat':[], 'lon':[]}
        :param epsg: int,
        :return: None
        '''
        driver = ogr.GetDriverByName('ESRI Shapefile')
        if os.access(shpname, os.F_OK) :
            driver.DeleteDataSource(shpname)

        srs = osr.SpatialReference()
        srs.ImportFromEPSG(int(epsg))

        ds = driver.CreateDataSource(shpname)
        lyr = ds.CreateLayer('polygon', srs, ogr.wkbPolygon)

        if isinstance(coords, dict) :
            wkt = 'POLYGON(('
            for i in range(len(coords)) :
                item = coords[i]
                if i == len(coords)-1:
                    wkt = wkt + '%f %f' %(float(item['lon']), float(item['lat']))
                else:
                    wkt = wkt + '%f %f,' %(float(item['lon']), float(item['lat']))
            wkt = wkt + '))'

            geom = ogr.CreateGeometryFromWkt(wkt)
            feature = ogr.Feature(lyr.GetLayerDefn())
            feature.SetGeometry(geom)
            lyr.CreateFeature(feature)
        elif isinstance(coords, list) :
            wkt = 'POLYGON(('
            for i in range(len(coords)) :
                item = coords[i]
                if i == len(coords)-1:
                    wkt = wkt + '%f %f' %(float(item['lon']), float(item['lat']))
                else:
                    wkt = wkt + '%f %f,' %(float(item['lon']), float(item['lat']))
            wkt = wkt + '))'

            geom = ogr.CreateGeometryFromWkt(wkt)
            feature = ogr.Feature(lyr.GetLayerDefn())
            feature.SetGeometry(geom)
            lyr.CreateFeature(feature)
        else:
            raise Exception('coords类型必须是dict或者list')

        ds = None
        driver =None



def getGDALType(datatype):
    '''
    根据numpy的数据类型，匹配GDAL中的数据类型
    :param datatype:
    :return: GDAL数据类型
    '''

    if datatype == np.byte or datatype == np.uint8:
        return gdal.GDT_Byte
    elif datatype == np.uint16 :
        return gdal.GDT_UInt16
    elif datatype == np.int16 :
        return gdal.GDT_Int16
    elif datatype == np.uint32 :
        return gdal.GDT_UInt32
    elif datatype == np.int32 :
        return gdal.GDT_Int32
    elif datatype == np.float32 :
        return gdal.GDT_Float32
    elif datatype == np.float64 :
        return gdal.GDT_Float64
    else:
        return gdal.GDT_Unknown


def getNPDType(datatype) :

    if 'int' in datatype:
        return gdal.GDT_Int32
    elif 'float' in datatype:
        return gdal.GDT_Float32
    else:
        return gdal.GDT_Unknown