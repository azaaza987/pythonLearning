#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: liangliangyy
@license: MIT Licence 
@contact: liangliangyy@gmail.com
@site: https://www.lylinux.net/
@software: PyCharm
@file: SftpTool.py
@time: 2018/5/7 下午9:41
"""

import paramiko
import stat
import os


class SftpTool():
    def __init__(self, host, port, username, password):
        transport = paramiko.Transport((host, port))
        transport.connect(username=username, password=password)
        self._sftp = paramiko.SFTPClient.from_transport(transport)

    def listdir(self, remotedir):
        return self._sftp.listdir(remotedir)

    def download(self, remote, local, ignore_dir=(), ignore_file_extension=()):
        for fileattr in self._sftp.listdir_attr(remote):
            localpath = os.path.join(local, fileattr.filename)
            remotepath = os.path.join(remote, fileattr.filename)
            if stat.S_ISDIR(fileattr.st_mode):
                # 过滤不需要的目录
                if fileattr.filename in ignore_dir:
                    continue
                print('enter remote path ' + remotepath)
                if not os.path.exists(localpath):
                    os.mkdir(localpath)
                self.download(remotepath, localpath, ignore_dir)
            else:
                if ignore_file_extension:
                    name, ext = os.path.splitext(fileattr.filename)
                    if ext and ext in ignore_file_extension:
                        print('ignore file  ' + fileattr.filename, 'ext: ' + ext)
                        continue
                print('start download...remote:%s local:%s' % (remotepath, localpath))
                self._sftp.get(remotepath, localpath)

    def _check_remote_path_exist(self, remotepath):
        try:
            self._sftp.stat(remotepath)
        except IOError as e:
            return False
        else:
            return True

    def _mkdir_p(self, remote_directory):
        dir_path = str()
        for dir_folder in remote_directory.split("/"):
            if dir_folder == "":
                continue
            dir_path += r"/{0}".format(dir_folder)
            try:
                self._sftp.listdir(dir_path)
            except IOError:
                self._sftp.mkdir(dir_path)

    def upload(self, localdir, remotedir, ignore_dir=(), ignore_file_extension=()):
        if not self._check_remote_path_exist(remotedir):
            self._mkdir_p(remotedir)
        for root, dirs, files in os.walk(localdir):
            new_root = root.replace(localdir, '')
            if new_root.startswith('/'):
                new_root = new_root[1:]
            check = [f for f in root.split('/') if f in ignore_dir]
            if check:
                print('ignore filedir : ' + ','.join(check))
                continue
            for dir in dirs:
                remote = os.path.join(remotedir, new_root, dir)
                local = os.path.join(root, dir)

                if dir in ignore_dir:
                    continue
                if not self._check_remote_path_exist(remote):
                    self._sftp.mkdir(remote)

            for file in files:
                local = os.path.join(root, file)
                remote = os.path.join(remotedir, new_root, file)
                name, ext = os.path.splitext(file)
                if ext and ext in ignore_file_extension:
                    print('ignore file  ' + file, 'ext: ' + ext)
                    continue
                print('start upload...remote:%s local:%s' % (remote, local))
                self._sftp.put(local, remote)


if __name__ == '__main__':
    t = SftpTool('192.168.21.12', 22, 'pi', '1')
    # dir = t.download('/home/pi/.homeassistant/', '/Users/liangliang/Source/Python/python/temp/',
    #                ('.git', 'deps', 'www', 'tts', '.AppleDouble'), ('.db'))
    t.upload('/Users/liangliang/Source/Python/python', '/home/pi/testupload/python',
             ('.git', 'deps', 'www', 'tts', '.AppleDouble'), ('.db'))
