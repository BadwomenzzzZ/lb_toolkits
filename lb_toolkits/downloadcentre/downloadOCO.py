# -*- coding:utf-8 -*-
'''
@Project  : lb_toolkits
@File     : downloadOCO.py
@Modify Time      @Author    @Version    
--------------    -------    --------    
2022/8/11 15:34      Lee       1.0         
@Description
------------------------------------
 
'''
import os
import platform
import sys
import numpy as np
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup

LOGIN_URL = 'https://urs.earthdata.nasa.gov/home'

URL_ROOT = 'https://oco2.gesdisc.eosdis.nasa.gov/data'


from lb_toolkits import bin
exedir = os.path.abspath(list(bin.__path__)[0])

# WGET = os.path.join(exedir, 'wget.exe')
# if not os.path.isfile(WGET) :
#     raise Exception('wget is not command')

class downloadOCO():

    def __init__(self, username, password):

        self.username = username
        self.password = password

        self.session = requests.Session()
        # self.login(username, password)

    def login(self, username, password):
        """Login to Earth Explorer."""
        rsp = self.session.get(LOGIN_URL)

        token = self.get_tokens(rsp.text)
        # payload= {
        #     "commit": "Sign in",
        #     "utf8":"✓",
        #     "authenticity_token":token,
        #     "login":username,
        #     "password":password
        # }
        payload= {
            "action": "login",
            "authenticity_token":token,
            "username":username,
            "password":password
        }
        rsp = self.session.post(LOGIN_URL, data=payload, allow_redirects=True)

        self.cookie = rsp.cookies.get_dict()
        return rsp

    def get_tokens(self, html):
        '''
        处理登录后页面的html
        :param html:
        :return: 获取csrftoken
        '''
        soup = BeautifulSoup(html,'lxml')
        res = soup.find("input",attrs={"name":"authenticity_token"})
        token = res["value"]
        return token

    def searchfile(self, nowdate, satid='OCO2_DATA', prodversion='OCO2_L2_Standard.10r'):
        '''

        :param nowdate:
        :return:
        '''
        import re
        # https://oco2.gesdisc.eosdis.nasa.gov/data/OCO2_DATA/OCO2_L2_Standard.10r/2022/059/
        url = os.path.join(URL_ROOT, satid, prodversion,
                           nowdate.strftime('%Y'), nowdate.strftime('%j'))
        url = url.replace('\\', '/')

        res = self.session.get(url)

        soup = BeautifulSoup(res.text, 'lxml')
        r = soup.find_all(href=re.compile('.h5'))
        filelist = []
        for name in r :
            if name.get_text().endswith('.h5') :
                filelist.append(url + '/' + name.get_text())
        # print(filelist)

        return filelist

    def download(self, output_dir, url, timeout=5*60, skip=False):

        os.makedirs(output_dir, exist_ok=True)

        filename = self._download(output_dir, url, timeout=timeout, skip=skip)

        return filename

    def _download(self, output_dir, url, timeout, chunk_size=1024, skip=False):
        local_filename = os.path.basename(url)
        local_filename = os.path.join(output_dir, local_filename)
        if skip :
            return local_filename

        if platform.system().lower() == 'windows' :
            cmd = f'{WGET} {url} --tries=3 ' \
                  f'--http-user={self.username} ' \
                  f'--http-passwd={self.password} ' \
                  f'--timeout={timeout}' \
                  f'  -P {output_dir}'
        else:
            cmd = f'wget {url} --tries=3 ' \
                  f'--http-user={self.username} ' \
                  f'--http-passwd={self.password} ' \
                  f'--timeout={timeout}' \
                  f'  -P {output_dir}'
        print('Command : [%s]' %(cmd))
        os.system(cmd)

        return local_filename

        #  暂未实现爬虫方式下载，只能通过wget方式下载文件
        download_url = url
        try:
            with self.session.get(
                    download_url, stream=True, allow_redirects=True, timeout=timeout
            ) as r:
                headers = r.headers

                file_size = int(r.headers.get("Content-Length"))
                with tqdm(
                        total=file_size, unit_scale=True, unit="B", unit_divisor=1024
                ) as pbar:
                    local_filename = os.path.basename(download_url)
                    local_filename = os.path.join(output_dir, local_filename)
                    if skip:
                        return local_filename
                    with open(local_filename, "wb") as f:
                        for chunk in r.iter_content(chunk_size=chunk_size):
                            if chunk:
                                f.write(chunk)
                                pbar.update(chunk_size)
        except requests.exceptions.Timeout:
            raise Exception(
                "Connection timeout after {} seconds.".format(timeout)
            )
        print('download 【%s】 success...' %(local_filename))

        return local_filename