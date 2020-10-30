#-*- coding = utf-8 -*-
#@Time : 2020/10/2 13:31
#@Author : straightup
import importlib
from settings import PLUGIN_CLASS_DICT

def get_server_info(ssh, host):
    """
    远程连接，采集服务器资产数据
    :param ssh: 负责远程连接的函数
    :param host: 要采集的主机（服务器）
    :return:
    """
    server_info = {}
    for key, path in PLUGIN_CLASS_DICT.items():
        """
        key="disk"   path="lib.plugins.disk.DiskPlugin"
        rsplit从右往左切,maxsplit=1 切一次 --> lib.plugins.disk  DiskPlugin
        """
        module_path, class_name = path.rsplit('.', maxsplit=1)
        module = importlib.import_module(module_path)
        cls = getattr(module, class_name)
        plugin_object = cls()
        info = plugin_object.process(ssh, host)
        server_info[key] = info
    return server_info
