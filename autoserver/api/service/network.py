# -*- coding = utf-8 -*-
# @Time : 2020/10/4 21:04
# @Author : straightup
from api import models


def process_network_info(host_object, network_dict):
    """
    处理汇报的网卡信息
    :param host_object: 主机
    :param network_dict: 状态 网卡数据 错误信息
    :return:
    """
    if not network_dict['status']:
        print('获取网卡资产信息时出错:', network_dict['error'])
    new_network_dict = network_dict['data']
    new_network_name_dict = set(new_network_dict)  # 以网卡名
    """
        {
        'ens33': {
            'up': True,
            'hwaddr': '00:0c:29:ee:f3:58',
            'inet': [{
                'address': '192.168.10.128',
                'netmask': '255.255.255.0',
                'broadcast': '192.168.10.255'
                }]
            }
        },
    """
    # 从数据库查取该主机的网卡信息
    db_network_query = models.NetWork.objects.filter(server=host_object).all()
    # 生成一个以网卡名为key,对象为value的字典
    db_network_dict = {row.name: row for row in db_network_query}
    db_network_name_dict = set(db_network_dict)

    # 新增
    create_name_set = new_network_name_dict - db_network_name_dict
    # 删除
    remove_name_set = db_network_name_dict - new_network_name_dict
    # 更新
    update_name_set = new_network_name_dict & db_network_name_dict

    print('新增', create_name_set)
    print('删除', remove_name_set)
    print('更新', update_name_set)

    record_str_list = []

    # 新增
    for name in create_name_set:
        new_network_obj = {
            'name': name,
            'up': new_network_dict[name]['up'],
            'hwaddr': new_network_dict[name]['hwaddr'],
            'ipaddrs': new_network_dict[name]['inet'][0]['address'],
            'netmask': new_network_dict[name]['inet'][0]['netmask'],
            'broadcast': new_network_dict[name]['inet'][0]['broadcast'],
        }
        models.NetWork.objects.create(**new_network_obj, server=host_object)
        msg = '[新增网卡]网卡名称:{name}, 网卡mac地址:{hwaddr}, ip地址:{ipaddrs}, 子网掩码:{netmask}, 广播:{broadcast}, 连接状态:{up}'.format(**new_network_obj)
        record_str_list.append(msg)

    # 删除
    if remove_name_set:
        models.NetWork.objects.filter(server=host_object, name__in=remove_name_set).delete()
        msg = '[删除网卡]网卡名称:{}'.format(','.join(remove_name_set))
        record_str_list.append(msg)

    # 更新
    for name in update_name_set:
        new_network_obj = {
            'name': new_network_dict[name],
            'up': new_network_dict[name]['up'],
            'hwaddr': new_network_dict[name]['hwaddr'],
            'ipaddrs': new_network_dict[name]['inet'][0]['address'],
            'netmask': new_network_dict[name]['inet'][0]['netmask'],
            'broadcast': new_network_dict[name]['inet'][0]['broadcast'],
        }
        temp = []
        for key, value in new_network_obj.items():
            old_value = getattr(db_network_dict[name], key)
            if value == old_value:
                continue
            msg = "网卡的{}, 由{}变更成{}".format(key, old_value, value)
            temp.append(msg)
            setattr(db_network_dict[name], key, value)
            if temp:
                db_network_dict[name].save()
                row_msg = "[更新网卡]网卡名称:{}, 更新的内容:{}".format(name, ';'.join(temp))
                record_str_list.append(row_msg)
