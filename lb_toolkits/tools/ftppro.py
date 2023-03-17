# -*- coding:utf-8 -*-

import ftplib 
import os
import datetime
import re

class ftppro(object):

    def __init__(self, ip, user, password, remotepath=None, savepath=None):

        self.host = ip
        self.user = user
        self.pwd = str(password)
        self.remotePath = remotepath
        self.savePath = savepath


    def connect(self, timeout=3*60):
        try:
            ftp = ftplib.FTP(self.host, timeout=timeout)
            ftp.encoding = 'utf'
            ftp.login(self.user, self.pwd)

            return ftp
        except BaseException as e:
            raise Exception('connect error"%s"' % self.host)
            # ftp.quit()
            return None

    def remotePath(self,remotePath):
        self.remotePath = remotePath

    def localPath(self,localPath):
        self.savePath = localPath

    def __makedir(self,dirname):
        if not os.path.isdir(dirname):
            os.makedirs(dirname)

    def list_dir_regex(self,regexStr):
        ftp = self.connect()
        try:
            ftp.cwd(self.remotePath)
            fileList = ftp.nlst()

            p = re.compile(regexStr)
            matchedFiles = []
            for file in fileList:
                match = p.search(file)
                if match:
                    matchedFiles.append(match.string)

            return matchedFiles
        except BaseException as e:
            print(e)

        self.close(ftp)

    def listdir(self, dirname, pattern=None):
        ftp = self.connect()
        try:
            ftp.cwd(dirname)
            if pattern is None :
                fileList = ftp.nlst()
            else:
                fileList = ftp.nlst(pattern)
            self.close(ftp)
            return fileList

        except BaseException as e:
            print(e)
            return []

    def __makeRemoteDir(self, dirPath):
        ftp = self.connect()

        dirs = dirPath.split('/')

        for dirName in dirs:
            if dirName:
                try:
                    if dirName == 'home':
                        ftp.cwd( '/' + dirName)
                    else:
                        ftp.cwd(dirName)
                except Exception as e:
                    ftp.mkd(dirName)
                    ftp.cwd(dirName)

        self.close(ftp)

    def get(self, ftp, tempfile, remoteFile, blocksize=1024, rest=None):
        ftp.voidcmd('TYPE I')

        def callback(block):
            fp.write(block)
            pbar.update(len(block))

        with open(tempfile, "wb") as fp:
            from tqdm import tqdm
            with tqdm(
                    total=ftp.size(remoteFile), unit="B", unit_scale=True, unit_divisor=blocksize
            ) as pbar:

                cmd = 'RETR %s' % (remoteFile)

                with ftp.transfercmd(cmd, rest) as conn:
                    while 1:
                        data = conn.recv(blocksize)
                        if not data:
                            break
                        callback(data)

            try:
                import ssl
            except ImportError:
                _SSLSocket = None
            else:
                _SSLSocket = ssl.SSLSocket
            # shutdown ssl layer
            if _SSLSocket is not None and isinstance(conn, _SSLSocket):
                conn.unwrap()

        return ftp.voidresp()

    def downloadFile(self, remoteFile, savePath, blocksize = 1024):
        '''
        通过ftp下载文件
        :param remoteFile:
        :param savePath:
        :param blocksize:
        :return:
        '''


        localFile = os.path.join(savePath, os.path.basename(remoteFile))
        tempfile = localFile + '.download'

        self.__makedir(savePath)
        if os.path.isfile(localFile):
            # os.remove(localFile)
            return True

        ftp = self.connect()
        if ftp is None :
            return False

        try:
            self.get(ftp, tempfile, remoteFile, blocksize=blocksize)

            # with open(tempfile, "wb") as fp:
            #     ftp.retrbinary('RETR %s' % remoteFile, fp.write, blocksize=block_size)
            self.close(ftp)
            if os.path.isfile(tempfile) :
                os.rename(tempfile, localFile)
            return True
        except BaseException as e:
            print(e)
            return False

    def uploadFile(self, localfile, remotePath, remoteFile, block_size = 1 * 1024):
        ftp = self.connect()

        filename = os.path.basename(localfile)
        try:
            remotePath = remotePath.replace('\\','/')
            self.__makeRemoteDir(remotePath)
            remotePath = os.path.join(remotePath,remoteFile)
            remotePath = remotePath.replace('\\','/')
            with open(localfile,"rb") as fp:
                ftp.storbinary("STOR %s" % remotePath,fp,block_size)
        except BaseException as e:
            print(e)


        self.close(ftp)


    def close(self, ftp):
        if ftp is not None:
            ftp.quit()


    # def __del__(self):
    #     if ftp is not None:
    #         ftp.quit()
