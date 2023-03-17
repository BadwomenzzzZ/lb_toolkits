# -*- coding:utf-8 -*-
'''
@Project  : lb_toolkits

@File     : downloadLandsat.py

@Modify Time : 2022/8/11 15:34

@Author : Lee

@Version : 1.0

@Description :

'''
import os
import datetime

from lb_toolkits.utils.api import API
from lb_toolkits.utils.earthexplorer import EarthExplorer
from .cmr import cmr

class downloadLandsat(cmr):

    def __init__(self, username, password):
        self.username = username
        self.password = password


    def searchfile(self, product,
                   startdate, enddate=None,
                   longitude=None, latitude=None,
                   bbox=None, cloud_cover_max=None,
                   months=None, max_results=100):
        '''
        Search for scenes.

        - Dataset Name	                         >>        Dataset ID
        - Landsat 5 TM Collection 1 Level 1	     >>      landsat_tm_c1
        - Landsat 5 TM Collection 2 Level 1	     >>      landsat_tm_c2_l1
        - Landsat 5 TM Collection 2 Level 2	     >>      landsat_tm_c2_l2
        - Landsat 7 ETM+ Collection 1 Level 1	 >>      landsat_etm_c1
        - Landsat 7 ETM+ Collection 2 Level 1	 >>      landsat_etm_c2_l1
        - Landsat 7 ETM+ Collection 2 Level 2	 >>      landsat_etm_c2_l2
        - Landsat 8 Collection 1 Level 1	     >>      landsat_8_c1
        - Landsat 8 Collection 2 Level 1	     >>      landsat_ot_c2_l1
        - Landsat 8 Collection 2 Level 2	     >>      landsat_ot_c2_l2
        - Sentinel 2A	                         >>      sentinel_2a

        Parameters
        ----------
        product: str
                Case-insensitive dataset alias (e.g. landsat_tm_c1).
                LANDSAT_TM_C1、LANDSAT_ETM_C1和LANDSAT_8_C1
        longitude : float, optional
                Longitude of the point of interest.
        latitude : float, optional
                Latitude of the point of interest.
        bbox : tuple, optional
                (xmin, ymin, xmax, ymax) of the bounding box.
        cloud_cover_max: int, optional
                Max. cloud cover in percent (1-100).
        startdate: datetime
                YYYY-MM-DD
        enddate : datetime, optional
                YYYY-MM-DD. Equal to startdate if not provided.
        months: list of int, optional
                Limit results to specific months (1-12).
        max_results: int, optional
                Max. number of results. Defaults to 100.

        Returns
        -------
            list of dict
                Matching scenes as a list of dict containing metadata.
        '''
        if enddate is None :
            enddate = startdate

        start_date = startdate.strftime('%Y-%m-%d')
        end_date   = enddate.strftime('%Y-%m-%d')
        api = API(self.username, self.password)

        scenes = api.search(dataset=product,
            latitude=latitude,     longitude=longitude,
            start_date=start_date, end_date=end_date,
            bbox = bbox,           max_cloud_cover=cloud_cover_max,
            months=months,         max_results=max_results)

        print('{} scenes found.'.format(len(scenes)))
        api.logout()

        return scenes

    def download(self, Landsat_name, outdir,
                 scene_id=None, retry=3, timeout=5*60):
        '''
        Download a Landsat scene.

        Parameters
        ----------
        Landsat_name
        outdir: str;
            Output directory. Automatically created if it does not exist.
        scene_id: str, optional
        retry: int, optional
            尝试失败次数
        timeout : int, optional
        Connection timeout in seconds.:

        Returns
        -------
            str
            Path to downloaded file.
        '''

        if scene_id is not None:
            Earth_Down = EarthExplorer(self.username, self.password)
            Earth_Down.download(identifier=scene_id, output_dir=outdir, timeout=timeout)
            Earth_Down.logout()

            return None

        for scene in Landsat_name:
            for i in range(retry) :
                try:
                    Earth_Down = EarthExplorer(self.username, self.password)
                    ID = scene['entity_id']
                    # IDpro = ID[3:9]
                    Earth_Down.download(identifier=ID, output_dir=outdir, timeout=timeout)
                    Earth_Down.logout()
                    break
                except BaseException as e :
                    continue

    def searchfileByCMR(self, starttime, endtime=None, satid='Landsat',
                   prodversion='Landsat_8', Provider='USGS_LTA', pattern='.hdf'):
        '''
        利用cmr进行查询检索相关产品的下载地址

        Parameters
        ----------
        starttime : datetime
            起始时间
        endtime : datetime, optional
            起始时间
        satid : str, optional
            卫星名
        prodversion : str
            对应cmr中的short name
        Provider : str, optional
            产品提供的组织结构
        pattern : str or list
            预留接口，对文件名进行模糊匹配（未实现改功能）
        Returns
        -------
            list
            根据条件所匹配到的产品下载链接
        '''

        CMR_ProviderURL = 'https://cmr.earthdata.nasa.gov/search/site/' \
                          'collections/directory/{Provider}/gov.nasa.eosdis'.format(Provider=Provider)

        if not self.cmr_check_provider(shortname=prodversion) :
            raise Exception('请参考Short Name>>"%s"' %(CMR_ProviderURL))

        if endtime is None :
            endtime = starttime

        filelist = self.cmr_search(starttime=starttime, endtime=endtime,
                                   short_name=prodversion)
        return filelist

    def downloadByCMR(self, outdir, url, timeout=5 * 60, skip=False):
        '''
        根据输入url下载相应的文件

        Parameters
        ----------
        outdir: str
            输出路径
        url : str
            下载链接
        token : str
            EarthData账号的APP Keys
        timeout : int
            时间限制
        skip : bool
            是否不做数据下载，直接返回文件名。默认是FALSE，下载文件。
        Returns
        -------
            str
            下载数据的文件名
        '''

        if not os.path.isdir(outdir) :
            os.makedirs(outdir, exist_ok=True)

        filename = self.cmr_download(outdir, url, token=self.token,
                                     username=self.username, password=self.password,
                                     timeout=timeout, skip=skip)

        return filename
