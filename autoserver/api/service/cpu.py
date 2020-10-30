#-*- coding = utf-8 -*-
#@Time : 2020/10/5 8:54
#@Author : straightup

def process_cpu_info(host_object, cpu_dict):
    """
        处理采集到的主板信息,在server上修改
        :param hostname: 主机
        :param board_dict: cpu信息
        :return:
        """
    if not cpu_dict['status']:
        print('获取内存资产时出错:', cpu_dict['error'])
        return
    # 取出采集到的内存信息
    new_cpu_dict = cpu_dict['data']

    # 服务器对象

    for key, value in new_cpu_dict.items():
        old_value = getattr(host_object, key)
        print(old_value)
        if value == old_value:
            continue
        setattr(host_object, key, value)
    host_object.save()
