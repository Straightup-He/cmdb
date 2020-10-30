#-*- coding = utf-8 -*-
#@Time : 2020/10/3 14:49
#@Author : straightup
"""
数据封装
"""
class BaseResponse(object):
    def __init__(self, status=True, data=None, error=None):
        self.status = status
        self.data = data
        self.error = error
    @property
    def dict(self):
        return self.__dict__
