#coding:utf-8

import time
import unittest
import requests
from BeautifulReport import BeautifulReport
from threading import Thread
from concurrent.futures import ThreadPoolExecutor


# 封装一个类


class Demo:
    def __init__(self,path, params=None, **kwargs):
        self.url = 'http://earth.igengmei.com'
        self.req = requests
        self.path = path
        self.params = params
        self.kwargs = kwargs
    header_dict = {
        'IOS':{},
        'ANDROID':{}
    }

    @property
    def get(self):
        res = self.req.get(url=self.url + self.path, params=self.params, **self.kwargs)
        return res

    @property
    def post(self):
        res = self.req.post(url=self.url + self.path, params=self.params, **self.kwargs)
        return res


class UserRegister(unittest.TestCase):

    def test_discover(self):
        '''
        发现接口
        '''
        # time.sleep(3)
        self.result = Demo('/api/v1/discover', params={'page': 1, 'count': 4}).get
        self.assertEqual(self.result.status_code,200)

    def test_index(self):
        '''
        首页接口
        '''
        # time.sleep(5)
        self.result = Demo('/api/v1/index', params={'page': 1, 'count': 10}).get
        self.assertEqual(self.result.status_code, 200)

    def test_card_list(self):
        '''
        个人中心帖子卡片列表
        '''
        # time.sleep(2)
        self.result = Demo('/api/v1/topic/card/list',
                           params={'type': 0, 'page': 1, 'count': 10, 'user_id': 241581403}).get
        self.assertEqual(self.result.status_code, 200)


if __name__ == '__main__':

    suite = unittest.TestSuite()
    suite1 = unittest.TestSuite()
    result = BeautifulReport(suite1)
    suite.addTests([UserRegister('test_discover'),UserRegister('test_index'),UserRegister('test_card_list')])
    join_list = []
    executor = ThreadPoolExecutor(6)
    for item in suite:
        t = Thread(target=lambda x:x.run(result),args=(item,))
        t.start()
        join_list.append(t)
    [i.join() for i in join_list]
    result.report(filename='报告{0}.html'.format(str(time.time())),log_path='reporte',description='简单测试报告')
