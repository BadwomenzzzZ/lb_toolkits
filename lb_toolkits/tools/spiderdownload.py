# -*- coding:utf-8 -*-
'''
@Project  : lb_toolkits
@File     : spiderdownload.py
@Modify Time      @Author    @Version    
--------------    -------    --------    
2022/7/14 10:28      Lee       1.0         
@Description
------------------------------------
 
'''
import os
import shutil
import sys
import numpy as np
import re
import requests
from tqdm import tqdm
import re
from bs4 import BeautifulSoup

class spiderdownload(object):

    def __init__(self, username=None, password=None):

        self.session = requests.Session()
        # if username is not None and password is not None :
        #     self.login(username, password)

    def logged_in(self):
        """Check if the log-in has been successfull based on session cookies."""
        eros_sso = self.session.cookies.get("EROS_SSO_production_secure")
        return bool(eros_sso)

    def login(self, username, password, url_login):
        """Login to URL."""

        rsp = self.session.get(url_login)
        csrf = self.get_tokens(rsp.text)
        payload = {
            "username": username,
            "password": password,
            "csrf": csrf,
        }
        rsp = self.session.post(url_login, data=payload, allow_redirects=True)

        if not self.logged_in():
            raise Exception("login failed.")

    def logout(self, url_logout):
        """Log out from URL."""
        self.session.get(url_logout)

    def get_tokens(self, body, pattern=r'name="csrf" value="(.+?)"'):
        """Get `csrf_token` and `__ncforminfo`."""
        tokens = re.findall(pattern, body)[0]
        # ncform = re.findall(r'name="__ncforminfo" value="(.+?)"', body)[0]

        if not tokens:
            raise Exception("login failed (token not found).")

        return tokens

    def download(self, output_dir, url, timeout=5*60, skip=False):
        """Download a Landsat scene.

        Parameters
        ----------
        identifier : str
            Scene Entity ID or Display ID.
        output_dir : str
            Output directory. Automatically created if it does not exist.
        dataset : str, optional
            Dataset name. If not provided, automatically guessed from scene id.
        timeout : int, optional
            Connection timeout in seconds.
        skip : bool, optional
            Skip download, only returns the remote filename.

        Returns
        -------
        filename : str
            Path to downloaded file.
        """
        os.makedirs(output_dir, exist_ok=True)
        # if not dataset:
        #     dataset = guess_dataset(identifier)
        # if is_display_id(identifier):
        #     entity_id = self.api.get_entity_id(identifier, dataset)
        # else:
        #     entity_id = identifier
        # url = EE_DOWNLOAD_URL.format(
        #     data_product_id=DATA_PRODUCTS[dataset], entity_id=entity_id
        # )
        filename = self._download(output_dir, url, timeout=timeout, skip=skip)

        return filename

    def _download(self, output_dir, url, timeout, chunk_size=1024, skip=False):
        """Download remote file given its URL."""

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

                    tempfile = local_filename + '.download'
                    if skip:
                        return local_filename
                    with open(tempfile, "wb") as f:
                        for chunk in r.iter_content(chunk_size=chunk_size):
                            if chunk:
                                f.write(chunk)
                                pbar.update(chunk_size)
                    shutil.move(tempfile, local_filename)
        except requests.exceptions.Timeout:
            raise Exception(
                "Connection timeout after {} seconds.".format(timeout)
            )
        print('download 【%s】 success...' %(local_filename))

        return local_filename

    def searchfile(self, url, pattern='.tif', attrs={}):
        '''

        :param nowdate:
        :return:
        '''


        url = url.replace('\\', '/')

        res = self.session.get(url)

        soup = BeautifulSoup(res.text, 'lxml')
        r = soup.find_all(href=re.compile(pattern), attrs=attrs)
        filelist = []
        for name in r :
            if name['href'].endswith(pattern) :
                filelist.append(name['href'])
        # print(filelist)

        return filelist

