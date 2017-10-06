#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: liangliangyy
@license: MIT Licence 
@contact: liangliangyy@gmail.com
@site: https://www.lylinux.org/
@software: PyCharm
@file: HttpProxySpider.py
@time: 2017/9/17 下午1:17
"""

from abc import ABCMeta, abstractmethod, abstractproperty
from bs4 import BeautifulSoup
import requests
from SpiderModels import HttpProxyIp, ProxyType, ProxyStatus


class BaseProxySpider():
    Source = ''

    def __init__(self):
        self.ips = {}

    @abstractmethod
    def get_proxy_ips(self):
        pass

    def check_available(self, ip, port):
        proxies = {'http': 'http://{ip}:{port}'.format(ip=ip, port=port)}
        try:
            requests.get('http://ip.cip.cc', timeout=20, proxies=proxies)
            return True
        except Exception as e:
            return False

    def save(self):
        models = []
        if self.ips:
            for ip in self.ips:
                is_avaliable = self.check_available(ip, self.ips[ip])
                m = HttpProxyIp()
                m.source = self.Source
                m.ip = ip
                m.port = self.ips[ip]
                m.status = ProxyStatus.ok if is_avaliable else ProxyStatus.expired
                models.append(m)
        HttpProxyIp.batch_save(models, source=self.Source)

    def useragent(self, url):
        i_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36",
            "Referer": 'https://www.baidu.com'
        }
        rsp = requests.get(url, headers=i_headers)
        rsp.encoding = 'utf-8'
        return rsp.text.encode('utf-8')


class KuaiDaiLi(BaseProxySpider):
    def __init__(self):
        super().__init__()
        self.high_anonymousurl = 'http://www.kuaidaili.com/free/inha/'
        self.commonurl = "http://www.kuaidaili.com/free/intr/"

    def get_proxy_ips(self):
        html = self.useragent(self.commonurl)
        html = html.decode('utf-8')
        with open('1.html', 'w') as file:
            file.write(html)
        soup = BeautifulSoup(html, "lxml")
        div = soup.find(id='list')
        trs = div.find_all('tr')
        for tr in trs:
            print(tr)


if __name__ == '__main__':
    kuaidaili = KuaiDaiLi()
    kuaidaili.get_proxy_ips()
