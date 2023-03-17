# lb_toolkits  
```angular2html
安装命令：
python -m pip install lb_toolkits
python -m pip install --upgrade lb_toolkits
```

## 更新记录
<table>
    <tr>
        <th>更新日期</th>
        <th>库名</th>
        <th>文件</th>
        <th>函数名</th>
        <th>功能</th>
    </tr>
    <tr>
        <td> 2022年8月13日 </td>
        <td> tools </td>
        <td> modis2tif </td>
        <td> modis2tif </td>
        <td>将MODIS产品hdf文件进行投影转换，输出geotif可处理MODIS 5分钟段产品和sin grid产品文件</td>
    </tr>
    <tr>
        <td> 2022年8月6日 </td>
        <td> tools </td>
        <td> nc2tif </td>
        <td> nc2tif </td>
        <td>将NC文件中的数据集转成geotif</td>
    </tr>
    <tr>
        <td> 2022年8月6日 </td>
        <td> tools </td>
        <td> tifpro </td>
        <td> readtiff </td>
        <td>读取geotif数据</td>
    </tr>
    <tr>
        <td> 2022年8月6日 </td>
        <td> tools </td>
        <td> tifpro </td>
        <td> writetiff </td>
        <td>写入geotif数据</td>
    </tr>
    <tr>
        <td> 2022年8月1日 </td>
        <td> downloadcentre </td>
        <td> downloadERA5 </td>
        <td> download_era5_profile </td>
        <td>下载ERA5廓线数据</td>
    </tr>
    <tr>
        <td> 2022年8月1日 </td>
        <td> downloadcentre </td>
        <td> downloadERA5 </td>
        <td> download_era5_profile </td>
        <td>下载ERA5地表数据</td>
    </tr>
    <tr>
        <td> 2022年8月1日 </td>
        <td> downloadcentre </td>
        <td> downloadGFS </td>
        <td> downloadGFS </td>
        <td>下载GFS数据</td>
    </tr>
    <tr>
        <td> 2022年8月1日 </td>
        <td> downloadcentre </td>
        <td> downloadLandsat </td>
        <td> searchlandsat </td>
        <td>通过设置查找条件，返回匹配满足条件的数据ID</td>
    </tr>
    <tr>
        <td> 2022年8月1日 </td>
        <td> downloadcentre </td>
        <td> downloadLandsat </td>
        <td> downloadlandsat </td>
        <td>根据返回的数据ID，下载相应的文件</td>
    </tr>
    <tr>
        <td> 2022年8月1日 </td>
        <td> downloadcentre </td>
        <td> downloadSentinel </td>
        <td> downloadSentinel </td>
        <td>下载哨兵数据，支持下载Sentinel-1、Sentinel-2、 Sentinel-3、Sentinel-5P</td>
    </tr>
    <tr>
        <td> 2022年8月1日 </td>
        <td> downloadcentre </td>
        <td> downloadH8 </td>
        <td> download_ahi8_l1_netcdf </td>
        <td>下载葵花8号卫星L1 NetCDF数据文件</td>
    </tr>
    <tr>
        <td> 2022年8月1日 </td>
        <td> downloadcentre </td>
        <td> downloadH8 </td>
        <td> download_ahi8_l1_hsd </td>
        <td>下载葵花8号卫星L1 HSD数据文件</td>
    </tr>
    <tr>
        <td> 2022年8月1日 </td>
        <td> tools </td>
        <td> hdfpro </td>
        <td> readhdf </td>
        <td>读取hdf5文件, 返回数据（也可返回数据集属性信息）</td>
    </tr>
    <tr>
        <td> 2022年8月1日 </td>
        <td> tools </td>
        <td> hdfpro </td>
        <td> readhdf_fileinfo </td>
        <td>读取hdf5文件全局属性, 返回文件全局属性信</td>
    </tr>
    <tr>
        <td> 2022年8月1日 </td>
        <td> tools </td>
        <td> hdfpro </td>
        <td> writehdf </td>
        <td>写入hdf5文件</td>
    </tr>
    <tr>
        <td> 2022年8月1日 </td>
        <td> tools </td>
        <td> hdfpro </td>
        <td> writehdf_fileinfo </td>
        <td>写入hdf5文件全局属性</td>
    </tr>
    <tr>
        <td> 2022年8月1日 </td>
        <td> tools </td>
        <td> hdf4pro </td>
        <td> readhdf4 </td>
        <td>读取hdf4文件, 返回数据（也可返回数据集属性信息）</td>
    </tr>
    <tr>
        <td> 2022年8月1日 </td>
        <td> tools </td>
        <td> hdf4pro </td>
        <td> readhdf4sdsattrs </td>
        <td>读取hdf4文件数据集属性信息</td>
    </tr>
    <tr>
        <td> 2022年8月1日 </td>
        <td> tools </td>
        <td> hdf4pro </td>
        <td> readhdf4fileattrs </td>
        <td>读取hdf4文件全局属性信息</td>
    </tr>
    <tr>
        <td> 2022年8月1日 </td>
        <td> tools </td>
        <td> ncpro </td>
        <td> readnc </td>
        <td>读取netcdf4文件, 返回数据（也可返回数据集属性信息）</td>
    </tr>
    <tr>
        <td> 2022年8月1日 </td>
        <td> tools </td>
        <td> ncpro </td>
        <td> readnc_fileinfo </td>
        <td>读取netcdf4文件全局属性信息</td>
    </tr>
    <tr>
        <td> 2022年8月1日 </td>
        <td> tools </td>
        <td> ncpro </td>
        <td> readnc_sdsinfo </td>
        <td>读取netcdf4文件数据集属性信息</td>
    </tr>
    <tr>
        <td> 2022年8月1日 </td>
        <td> tools </td>
        <td> ncpro </td>
        <td> writenc </td>
        <td>写入netcdf4文件数据集</td>
    </tr>
    <tr>
        <td> 2022年8月1日 </td>
        <td> tools </td>
        <td> ncpro </td>
        <td> writenc_fileinfo </td>
        <td>写入netcdf4文件全局属性</td>
    </tr>
    <tr>
        <td> 2022年8月1日 </td>
        <td> tools </td>
        <td> ncpro </td>
        <td> writenc_sdsinfo </td>
        <td>写入netcdf4文件数据集属性</td>
    </tr>
    <tr>
        <td> 2022年8月1日 </td>
        <td> tools </td>
        <td> ncpro </td>
        <td> writencfortimes </td>
        <td>写入netcdf4文件**时间戳**数据集</td>
    </tr>
    <tr>
        <td> 2022年8月1日 </td>
        <td> tools </td>
        <td> jsonpro </td>
        <td> readjson </td>
        <td>读取json文件, 返回dict</td>
    </tr>
    <tr>
        <td> 2022年8月1日 </td>
        <td> tools </td>
        <td> jsonpro </td>
        <td> writejson </td>
        <td>写入json文件</td>
    </tr>
</table>

## 依赖库
<table>
    <tr>
        <th> 库名 </th>
        <th> 版本号 </th>
    </tr>
    <tr>
        <td> numpy </td>
        <td> 1.2.0 </td>
    </tr>
    <tr>
        <td> pyhdf </td>
        <td> 0.10.0 </td>
    </tr>
    <tr>
        <td> h5py </td>
        <td> 1.0.0 </td>
    </tr>
    <tr>
        <td> netcdf4 </td>
        <td> 1.0.0 </td>
    </tr>
    <tr>
        <td> tqdm </td>
        <td> 4.0.0 </td>
    </tr>
    <tr>
        <td> gdal </td>
        <td> 2.0.0 </td>
    </tr>
    <tr>
        <td> pillow </td>
        <td> 7.0.0 </td>
    </tr>
    <tr>
        <td> paramiko </td>
        <td> 2.10.0 </td>
    </tr>
    <tr>
        <td> cdsapi </td>
        <td> 0.5.0 </td>
    </tr>
    <tr>
        <td> landsatxplore </td>
        <td> 0.10.0 </td>
    </tr>
    <tr>
        <td> sentinelsat </td>
        <td> 1.1.0 </td>
    </tr>
</table>

------------------------------------------------
## downloadcentre 
支持各类数据下载，例如：ERA5、GFS、AHI8、LandSat、Sentinel  
### downloadERA5:
- **download_era5_profile：** 下载ERA5的大气分层数据
```angular2html
download_era5_profile(strdate,outname, prof_info, area_info=None,m_client=None, redownload=False)
```

- **download_era5_surface：** 下载ERA5的地表数据
```angular2html
download_era5_surface(strdate, outname, surf_info, area_info=None, m_client=None, redownload=False)
```
-------------------------------------------------------------
### downloadGFS:
- **downloadGFS：** 下载GFS的预报数据  
```angular2html
downloadGFS(outdir, nowdate, issuetime=0, forecasttime=[0], regoin=[0.0, 360.0, 90.0, -90.0])
```
-------------------------------------------------------------
### downloadLandsat:
- **searchlandsat：** 通过设置查找条件，匹配满足条件的数据ID
```angular2html
searchlandsat(username, password, product,
              longitude=None,
              latitude=None,
              bbox=None,
              cloud_cover_max=None,
              startdate=None,
              enddate=None,
              months=None,
              max_results=100)
```  

- **downloadlandsat：** 根据返回的数据ID，下载相应的文件
```angular2html
downloadlandsat(username, password, Landsat_name, output_dir, scene_id=None, retry=3, timeout=5*60)
```
-------------------------------------------------------------
### downloadSentinel:
- **downloadSentinel：** 下载哨兵数据，支持下载Sentinel-1、Sentinel-2、
  Sentinel-3、Sentinel-5P  
```angular2html
downloadSentinel(username, password, starttime, endtime, outpath='./',
                platformname='Sentinel-2', producttype='S2MSI2A',
                footprint=None, geojson = None, filename='*', **keywords)
```

------------------------------------------------
------------------------------------------------


## tools  
1、对hdf4、hdf5、netcdf4、tiff、json、grib1/2、ASCII文件操作   
2、通过ftp、sftp、wget、爬虫下载相关文件  

### hdfpro
- **readhdf：** 读取hdf5文件, 返回数据（也可返回数据集属性信息）
```angular2html
readhdf(filename, sdsname, dictsdsinfo=None)
```

- **readhdf_fileinfo：** 读取hdf5文件全局属性, 返回文件全局属性信息
```angular2html
readhdf_fileinfo(filename)
```

- **writehdf：** 写入hdf5文件
```angular2html
writehdf(filename, sdsname, data, overwrite=True,
        dictsdsinfo = None, dictfileinfo = None,
        compression = 9, info = False)
```

- **writehdf_fileinfo：** 写入hdf5文件全局属性
```angular2html
writehdf_fileinfo(filename, sdsname, data, overwrite=True,
        dictsdsinfo = None, dictfileinfo = None,
        compression = 9, info = False)
```
-------------------------------------------------------------

### hdf4pro
- **readhdf4：** 读取hdf4文件, 返回数据（也可返回数据集属性信息）
```angular2html
readhdf4(h4file, sdsname, dictsdsattrs=None, dictfileattrs=None)
```

- **readhdf4sdsattrs：** 读取hdf4文件数据集属性信息
```angular2html
readhdf4sdsattrs(h4file, sdsname)
```

- **readhdf4fileattrs：** 读取hdf4文件全局属性信息
```angular2html
readhdf4fileattrs(h4file)
```
-------------------------------------------------------------

### ncpro
- **readnc：** 读取netcdf4文件, 返回数据（也可返回数据集属性信息）
```angular2html
readnc(filename, sdsname, dictsdsinfo=None)
```

- **readnc_fileinfo：** 读取netcdf4文件全局属性信息
```angular2html
readnc_fileinfo(filename)
```

- **readnc_sdsinfo：** 读取netcdf4文件数据集属性信息
```angular2html
readnc_sdsinfo(filename, sdsname)
```

- **writenc：** 写入netcdf4文件数据集
```angular2html
writenc(filename, sdsname, srcdata, dimension=None, overwrite=1,
        complevel=9, dictsdsinfo=None, fill_value=None,
        standard_name=None, long_name=None, description=None, units=None,
        valid_range=None,
        scale_factor=None, add_offset=None, **kwargs)
```

- **writenc_fileinfo：** 写入netcdf4文件全局属性
```angular2html
writenc_fileinfo(filename, dictfileinfo, overwrite=1)
```

- **writenc_sdsinfo：** 写入netcdf4文件数据集属性
```angular2html
writenc_sdsinfo(filename, sdsname, dictsdsinfo, overwrite=1)
```

- **writencfortimes：** 写入netcdf4文件**时间戳**数据集
```angular2html
writencfortimes(filename, sdsname, srcdata, overwrite=1,
                units = 'hours since 1900-01-01 00:00:00.0',
                calendar = "gregorian",
                complevel=9, dictsdsinfo=None)
```
-------------------------------------------------------------

### jsonpro
- **readjson：** 读取json文件, 返回dict
```angular2html
readjson(jsonname, **kwargs)
```

- **writejson：** 写入json文件
```angular2html
writejson(jsonname, dict_info, indent=4, chinese=False)
```

- **readbinary：** 读取二进制文件
```angular2html
readbinary(filename, shape, dtype=np.float32, offset=0, encodine='utf-8')
```

- **writebinary：** 写入二进制文件
```angular2html
writebinary(filename, data, overwrite=1, offset=0, encodine='utf-8')
```

- **readascii：** 读取ASCII文件
```angular2html
readascii(filename, dtype=float, comments='#', delimiter=None,
            converters=None, skiprows=0, usecols=None, unpack=False,
            ndmin=0, encoding='bytes', max_rows=None)
```

- **writeascii：** 写入ASCII文件
```angular2html
writeascii(filename, data,  fmt='%.18e', delimiter=' ', newline='\n', header='',
            footer='', comments='# ', encoding=None)
```

- **loadarray：** 读取npy文件
```angular2html
loadarray(file, mmap_mode=None, allow_pickle=False, fix_imports=True, encoding='ASCII')
```

- **savearray：** 写入npy文件
```angular2html
savearray(filename, data, allow_pickle=True, fix_imports=True)
```



