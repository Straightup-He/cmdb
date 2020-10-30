#-*- coding = utf-8 -*-
#@Time : 2020/10/7 14:31
#@Author : straightup

def process_basic_info(host_object, basic_dict):
    """
    处理采集到的版本信息,在server上修改
    :param hostname: 主机
    :param board_dict: 版本信息
    :return:
    """
    if not basic_dict['status']:
        print('获取内存资产时出错:', basic_dict['error'])
        return
    # 取出采集到的内存信息
    new_basic_dict = basic_dict['data']

    # 服务器对象

    for key, value in new_basic_dict.items():
        old_value = getattr(host_object, key)
        print(old_value)
        if value == old_value:
            continue
        setattr(host_object, key, value)
    host_object.save()

