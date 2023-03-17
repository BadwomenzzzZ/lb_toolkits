# coding:utf-8
'''
@Project: downloadsat
-------------------------------------
@File   : downloadLandsat.py
-------------------------------------
@Modify Time      @Author    @Version    
--------------    -------    --------
2021/6/23 15:34     Lee        1.0         
-------------------------------------
@Desciption
-------------------------------------

'''
import datetime

from lb_toolkits.utils.api import API
from lb_toolkits.utils.earthexplorer import EarthExplorer

def searchlandsat(username, password, product,
                  longitude=None,
                  latitude=None,
                  bbox=None,
                  cloud_cover_max=None,
                  startdate=None,
                  enddate=None,
                  months=None,
                  max_results=100):
    '''
    Search for scenes.

    :param username:
    :param password:
    :param product: str
            Case-insensitive dataset alias (e.g. landsat_tm_c1).
    :param longitude: float, optional
            Longitude of the point of interest.
    :param latitude: float, optional
            Latitude of the point of interest.
    :param bbox: tuple, optional
            (xmin, ymin, xmax, ymax) of the bounding box.
    :param cloud_cover_max: int, optional
            Max. cloud cover in percent (1-100).
    :param startdate: datetime, optional
            YYYY-MM-DD
    :param enddate: datetime, optional
            YYYY-MM-DD. Equal to startdate if not provided.
    :param months: list of int, optional
            Limit results to specific months (1-12).
    :param max_results:int, optional
            Max. number of results. Defaults to 100.
    :return: scenes : list of dict
            Matching scenes as a list of dict containing metadata.
    '''
    start_date = startdate.strftime('%Y-%m-%d')
    end_date   = enddate.strftime('%Y-%m-%d')
    api = API(username, password)

    scenes = api.search(
        dataset=product,
        latitude=latitude,
        longitude=longitude,
        bbox = bbox,
        start_date=start_date,
        end_date=end_date,
        max_cloud_cover=cloud_cover_max,
        months=months,
        max_results=max_results
    )

    print('{} scenes found.'.format(len(scenes)))
    api.logout()
    return scenes

def downloadlandsat(username, password, Landsat_name, output_dir, scene_id=None, retry=3, timeout=5*60):
    '''
    Download a Landsat scene.
    :param username:
    :param password:
    :param Landsat_name:
    :param output_dir: str
            Output directory. Automatically created if it does not exist.
    :param scene_id:
    :param timeout : int, optional
            Connection timeout in seconds.:
    :return: filename : str
            Path to downloaded file.
    '''

    if scene_id is not None:
        Earth_Down = EarthExplorer(username, password)
        Earth_Down.download(identifier=scene_id, output_dir=output_dir, timeout=timeout)
        Earth_Down.logout()

        return None

    for scene in Landsat_name:
        for i in range(retry) :
            try:
                Earth_Down = EarthExplorer(username, password)
                ID = scene['entity_id']
                # IDpro = ID[3:9]
                Earth_Down.download(identifier=ID, output_dir=output_dir, timeout=timeout)
                Earth_Down.logout()
                break
            except BaseException as e :
                continue

