#-*- coding = utf-8 -*-
#@Time : 2020/10/2 11:23
#@Author : straightup
import re
import traceback
import settings
from .base import BasePlugin
from lib.utils.log import logger
from lib.utils.response import BaseResponse
"""
用于采集基础信息
"""
class BasicPlugin(BasePlugin):
    """
    采集基础信息
    """
    def process(self, ssh, host):
        response = BaseResponse()
        try:
            uname = ssh(host, 'uname').strip()
            version = ssh(host, 'cat /etc/issue').strip().split('\n')[0]
            response.data = {
                'os_platform': uname,
                'os_version': version,
            }

        except Exception as e:
            logger.error(traceback.format_exc())
            response.status = False
            response.error = traceback.format_exc()
        return response.dict
