#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: liangliangyy
@license: MIT Licence 
@contact: liangliangyy@gmail.com
@site: https://www.lylinux.net/
@software: PyCharm
@file: storage.py
@time: 2017/10/22 上午2:51
"""

import json

from .utils import utf8_data_to_file


class Singleton(object):
    """Singleton Class
    This is a class to make some class being a Singleton class.
    Such as database class or config class.

    usage:
        class xxx(Singleton):
            def __init__(self):
                if hasattr(self, '_init'):
                    return
                self._init = True
                other init method
    """

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kwargs)
        return cls._instance


class Storage(Singleton):
    def __init__(self):
        '''
        Database stores every info.

        version int
        #if value in file is unequal to value defined in this class.
        #An database update will be applied.
        user dict:
            username str
            key str
        collections list:
            collection_info(dict):
                collection_name str
                collection_type str
                collection_describe str
                collection_songs list:
                    song_id(int)
        songs dict:
            song_id(int) dict:
                song_id int
                artist str
                song_name str
                mp3_url str
                album_name str
                album_id str
                quality str
                lyric str
                tlyric str
        player_info dict:
            player_list list:
                songs_id(int)
            playing_list list:
                songs_id(int)
            playing_mode int
            playing_offset int


        :return:
        '''
        if hasattr(self, '_init'):
            return
        self._init = True
        self.version = 4
        self.database = {
            'version': 4,
            'user': {
                'username': '',
                'password': '',
                'user_id': '',
                'nickname': '',
            },
            'collections': [[]],
            'songs': {},
            'player_info': {
                'player_list': [],
                'player_list_type': '',
                'player_list_title': '',
                'playing_list': [],
                'playing_mode': 0,
                'idx': 0,
                'ridx': 0,
                'playing_volume': 60,
            }
        }
        self.storage_path = 'database.json'
        self.cookie_path = 'cookie'
        self.file = None

    def load(self):
        try:
            self.file = open(self.storage_path, 'r')
            self.database = json.loads(self.file.read())
            self.file.close()
        except (ValueError, OSError, IOError):
            self.__init__()
        if not self.check_version():
            self.save()

    def check_version(self):
        if self.database['version'] == self.version:
            return True
        else:
            # Should do some update.
            if self.database['version'] == 1:
                self.database['version'] = 2
                self.database['cache'] = False
            elif self.database['version'] == 2:
                self.database['version'] = 3
                self.database.pop('cache')
            elif self.database['version'] == 3:
                self.database['version'] = 4
                self.database['user'] = {'username': '',
                                         'password': '',
                                         'user_id': '',
                                         'nickname': ''}
            self.check_version()
            return False

    def save(self):
        self.file = open(self.storage_path, 'w')
        db_str = json.dumps(self.database)
        utf8_data_to_file(self.file, db_str)
        self.file.close()
