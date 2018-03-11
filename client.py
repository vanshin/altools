#coding=utf8

'''client'''

import time
import requests

class HttpClient(object):
    def __init__(self, server):
        self.address = server['address']
        self.port = server['port']
        self.server = 'http://{}:{}/'.format(self.address, self.port)

    def get(self, path, data={}):
        ret = requests.get(self.server+path, data)
        return ret.json()

    def post(self, path, data={}):
        ret = requests.post(self.server+path, data)
        return ret.json()

if __name__ == '__main__':
    server = {
        'address': '116.196.113.214',
        'port': '5000'
    }
    hc = HttpClient(server)
    ret = hc.get('ping')
    print(ret)
