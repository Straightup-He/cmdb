#-*- coding = utf-8 -*-
#@Time : 2020/10/2 11:17
#@Author : straightup
class BasePlugin(object):
    """
    基类,约束子类中必须实现process方法
    """
    def process(self, ssh, host):
        raise NotImplementedError('%s中必须实现process方法!' % self.__class__.__name__)   #标志


