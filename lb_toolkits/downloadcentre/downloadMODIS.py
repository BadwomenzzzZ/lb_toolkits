# -*- coding:utf-8 -*-
'''
@Project  : lb_toolkits
@File     : downloadMODIS.py
@Modify Time      @Author    @Version    
--------------    -------    --------    
2022/8/12 15:48      Lee       1.0         
@Description
------------------------------------
 https://wiki.earthdata.nasa.gov/display/EDSC/Earthdata+Search+URL+Parameters
 https://ladsweb.modaps.eosdis.nasa.gov/archive/allData/
'''
import os
import platform
import sys
import re
import numpy as np
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup

URL_LOGIN = 'https://urs.earthdata.nasa.gov/home'

# URL_ROOT = 'https://e4ftl01.cr.usgs.gov/'
URL_ROOT = ' https://ladsweb.modaps.eosdis.nasa.gov/archive/allData/'

from lb_toolkits import bin
exedir = os.path.abspath(list(bin.__path__)[0])

WGET = os.path.join(exedir, 'wget.exe')
if not os.path.isfile(WGET) :
    raise Exception('wget is not command')

class downloadMODIS():

    def __init__(self, username, password):

        self.username = username
        self.password = password

        self.session = requests.Session()
        # self.login(username, password)

    def login(self, username, password):
        """Login to Earth Explorer."""
        rsp = self.session.get(URL_LOGIN)

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
        rsp = self.session.post(URL_LOGIN, data=payload, allow_redirects=True)

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

    def searchfile(self, nowdate, satid='TERRA', instid='MODIS',
                         version='61', prodid='MOD06_L2'):
        '''

        :param nowdate:
        :return:
        '''

        url = os.path.join(URL_ROOT, version, prodid,
                           nowdate.strftime('%Y'), '%03d.json' %(int(nowdate.strftime('%j'))))
        url = url.replace('\\', '/')

        res = self.session.get(url)
        for name in res.json() :
            print(name.get("name"))
        exit()

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

#
# class downpy() :
#     #!/usr/bin/env python
#
#     # script supports either python2 or python3
#     #
#     # Attempts to do HTTP Gets with urllib2(py2) urllib.requets(py3) or subprocess
#     # if tlsv1.1+ isn't supported by the python ssl module
#     #
#     # Will download csv or json depending on which python module is available
#     #
#
#     from __future__ import (division, print_function, absolute_import, unicode_literals)
#
#     import argparse
#     import os
#     import os.path
#     import shutil
#     import sys
#
#     try:
#         from StringIO import StringIO   # python2
#     except ImportError:
#         from io import StringIO         # python3
#
#
#     ################################################################################
#
#
#     USERAGENT = 'tis/download.py_1.0--' + sys.version.replace('\n','').replace('\r','')
#
#
#     def geturl(url, token=None, out=None):
#         headers = { 'user-agent' : USERAGENT }
#         if not token is None:
#             headers['Authorization'] = 'Bearer ' + token
#         try:
#             import ssl
#             CTX = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
#             if sys.version_info.major == 2:
#                 import urllib2
#                 try:
#                     fh = urllib2.urlopen(urllib2.Request(url, headers=headers), context=CTX)
#                     if out is None:
#                         return fh.read()
#                     else:
#                         shutil.copyfileobj(fh, out)
#                 except urllib2.HTTPError as e:
#                     print('HTTP GET error code: %d' % e.code(), file=sys.stderr)
#                     print('HTTP GET error message: %s' % e.message, file=sys.stderr)
#                 except urllib2.URLError as e:
#                     print('Failed to make request: %s' % e.reason, file=sys.stderr)
#                 return None
#
#             else:
#                 from urllib.request import urlopen, Request, URLError, HTTPError
#                 try:
#                     fh = urlopen(Request(url, headers=headers), context=CTX)
#                     if out is None:
#                         return fh.read().decode('utf-8')
#                     else:
#                         shutil.copyfileobj(fh, out)
#                 except HTTPError as e:
#                     print('HTTP GET error code: %d' % e.code(), file=sys.stderr)
#                     print('HTTP GET error message: %s' % e.message, file=sys.stderr)
#                 except URLError as e:
#                     print('Failed to make request: %s' % e.reason, file=sys.stderr)
#                 return None
#
#         except AttributeError:
#             # OS X Python 2 and 3 don't support tlsv1.1+ therefore... curl
#             import subprocess
#             try:
#                 args = ['curl', '--fail', '-sS', '-L', '--get', url]
#                 for (k,v) in headers.items():
#                     args.extend(['-H', ': '.join([k, v])])
#                 if out is None:
#                     # python3's subprocess.check_output returns stdout as a byte string
#                     result = subprocess.check_output(args)
#                     return result.decode('utf-8') if isinstance(result, bytes) else result
#                 else:
#                     subprocess.call(args, stdout=out)
#             except subprocess.CalledProcessError as e:
#                 print('curl GET error message: %' + (e.message if hasattr(e, 'message') else e.output), file=sys.stderr)
#             return None
#
#
#
#     ################################################################################
#
#
#     DESC = "This script will recursively download all files if they don't exist from a LAADS URL and stores them to the specified path"
#
#
#     def sync(src, dest, tok):
#         '''synchronize src url with dest directory'''
#         try:
#             import csv
#             files = [ f for f in csv.DictReader(StringIO(geturl('%s.csv' % src, tok)), skipinitialspace=True) ]
#         except ImportError:
#             import json
#             files = json.loads(geturl(src + '.json', tok))
#
#         # use os.path since python 2/3 both support it while pathlib is 3.4+
#         for f in files:
#             # currently we use filesize of 0 to indicate directory
#             filesize = int(f['size'])
#             path = os.path.join(dest, f['name'])
#             url = src + '/' + f['name']
#             if filesize == 0:
#                 try:
#                     print('creating dir:', path)
#                     os.mkdir(path)
#                     sync(src + '/' + f['name'], path, tok)
#                 except IOError as e:
#                     print("mkdir `%s': %s" % (e.filename, e.strerror), file=sys.stderr)
#                     sys.exit(-1)
#             else:
#                 try:
#                     if not os.path.exists(path):
#                         print('downloading: ' , path)
#                         with open(path, 'w+b') as fh:
#                             geturl(url, tok, fh)
#                     else:
#                         print('skipping: ', path)
#                 except IOError as e:
#                     print("open `%s': %s" % (e.filename, e.strerror), file=sys.stderr)
#                     sys.exit(-1)
#         return 0
#
#
#     def _main(argv):
#         parser = argparse.ArgumentParser(prog=argv[0], description=DESC)
#         parser.add_argument('-s', '--source', dest='source', metavar='URL', help='Recursively download files at URL', required=True)
#         parser.add_argument('-d', '--destination', dest='destination', metavar='DIR', help='Store directory structure in DIR', required=True)
#         parser.add_argument('-t', '--token', dest='token', metavar='TOK', help='Use app token TOK to authenticate', required=True)
#         args = parser.parse_args(argv[1:])
#         if not os.path.exists(args.destination):
#             os.makedirs(args.destination)
#         return sync(args.source, args.destination, args.token)
#
#
#     if __name__ == '__main__':
#         try:
#             sys.exit(_main(sys.argv))
#         except KeyboardInterrupt:
#             sys.exit(-1)
#







