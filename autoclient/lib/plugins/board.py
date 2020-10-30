#-*- coding = utf-8 -*-
#@Time : 2020/10/2 11:24
#@Author : straightup
import traceback
from .base import BasePlugin
from lib.utils.log import logger
from lib.utils.response import BaseResponse
"""
用于采集主板信息
"""
class BoardPlugin(BasePlugin):
    """
    采集主板信息
    """
    def process(self, ssh, host):
        # 执行命令
        response = BaseResponse()
        try:
            result = ssh(host, 'dmidecode -t1')
            response.data = self.parse(result)
        except Exception as e:
            logger.error(traceback.format_exc())
            response.status = False
            response.error = traceback.format_exc()
        return response.dict

    def parse(self, content):
        result = {}
        key_map = {
            'Manufacturer': 'manufacturer',
            'Product Name': 'model',
            'Serial Number': 'sn',
        }
        for item in content.split('\n'):
            row_data = item.strip().split(':')
            if len(row_data) == 2:
                if row_data[0] in key_map:
                    result[key_map[row_data[0]]] = row_data[1].strip() if row_data[1] else row_data[1]
        return result
