#coding: utf-8

import time
import constants

def format_ct():
    '''return current format time'''
    return time.strftime(constants.DATE_TIME, time.localtime())
