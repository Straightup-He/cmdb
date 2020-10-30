#-*- coding = utf-8 -*-
#@Time : 2020/10/3 19:02
#@Author : straightup
import traceback
from .base import BasePlugin
from lib.utils.log import logger
from lib.utils.response import BaseResponse
"""
用于采集cpu信息
"""
class CpuPlugin(BasePlugin):
    """
    采集cpu信息
    """
    def process(self, ssh, host):
        # 执行命令
        response = BaseResponse()
        try:
            shell_command = 'cat /proc/cpuinfo'
            output = ssh(host, shell_command)
            response.data = self.parse(output)
        except Exception as e:
            logger.error(traceback.format_exc())
            response.status = False
            response.error = traceback.format_exc()
        return response.dict

    @staticmethod
    def parse(content):
        """
        解析shell命令返回结果
        :param content: shell 命令结果
        :return:解析后的结果
        """
        response = {'cpu_count': 0, 'cpu_physical_count': 0, 'cpu_model': ''}

        cpu_physical_set = set()

        content = content.strip()
        for item in content.split('\n\n'):
            for row_line in item.split('\n'):
                key, value = row_line.split(':')
                key = key.strip()
                if key == 'processor':
                    response['cpu_count'] += 1
                elif key == 'physical id':
                    cpu_physical_set.add(value)
                elif key == 'model name':
                    if not response['cpu_model']:
                        response['cpu_model'] = value
        response['cpu_physical_count'] = len(cpu_physical_set)

        return response
