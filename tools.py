#coding=utf-8

'''data struct'''

import queue

class Pool(object):
    '''pool for db'''

    def __init__(self, size):
        self.qu = queue.Queue(size)

    def get(self):
        return self.qu.get(True)

    def put(self, item):
        self.qu.put(item, True)

