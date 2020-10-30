#-*- coding = utf-8 -*-
#@Time : 2020/10/4 22:31
#@Author : straightup
def process_board_info(host_object, board_dict):
    """
    处理采集到的主板信息,在server上修改
    :param hostname: 主机
    :param board_dict: 主板信息
    :return:
    """
    if not board_dict['status']:
        print('获取内存资产时出错:', board_dict['error'])
        return
    # 取出采集到的内存信息
    new_board_dict = board_dict['data']

    #服务器对象

    for key, value in new_board_dict.items():
        old_value = getattr(host_object, key)
        print(old_value)
        if value == old_value:
            continue
        setattr(host_object, key, value)
    host_object.save()


