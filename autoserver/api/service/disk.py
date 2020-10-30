#-*- coding = utf-8 -*-
#@Time : 2020/10/4 11:09
#@Author : straightup
from api import models

def process_disk_info(host_object, disk_dict):
    """
    处理汇报来的硬盘信息
    :param host: 主机
    :param disk_dict: 状态,硬盘信息,错误信息
    :return:
    """
    if not disk_dict['status']:
        print('获取硬盘资产时出错:', disk_dict['error'])
        return
    # 取出采集到的硬盘资产数据
    new_disk_dict = disk_dict['data']
    # 集合,看key(槽位)
    new_disk_slot_dict = set(new_disk_dict)

    # 从数据库查取该主机的数据(用于对比)
    db_disk_queryset = models.Disk.objects.filter(server=host_object).all()
    # 生成一个以槽位为key,对象为value的字典,通过槽位进行比对
    db_disk_dict = {row.slot: row for row in db_disk_queryset}
    # 旧数据槽位
    db_disk_slot_dict = set(db_disk_dict)

    # 新增(新旧求差集)
    create_slot_set = new_disk_slot_dict - db_disk_slot_dict
    # 删除(旧新求差集)
    remove_slot_set = db_disk_slot_dict - new_disk_slot_dict
    # 更新(新旧求交集)
    update_slot_set = new_disk_slot_dict & db_disk_slot_dict

    # print('新增', create_slot_set)
    # print('删除', remove_slot_set)
    # print('更新', update_slot_set)

    record_str_list = []

    # 新增
    for slot in create_slot_set:
        models.Disk.objects.create(**new_disk_dict[slot], server=host_object)
        msg = "[新增硬盘]槽位:{slot}, 类型:{pd_type}, 容量: {capacity}, 型号: {model}".format(**new_disk_dict[slot])
        record_str_list.append(msg)

    # 删除
    if remove_slot_set:
        models.Disk.objects.filter(server=host_object, slot__in=remove_slot_set).delete()
        msg = "[删除硬盘]槽位:{}".format(','.join(remove_slot_set))
        record_str_list.append(msg)

    # 更新
    for slot in update_slot_set:
        # print(new_disk_dict[slot])  # 字典,直接取值
        # print(db_disk_dict[slot])  # 对象, 对象.x / getattr(对象,'x')
        temp = []
        for key, value in new_disk_dict[slot].items():
            old_value = getattr(db_disk_dict[slot], key)
            if value == old_value:
                continue
            # 变更信息
            msg = "硬盘的{}, 由{}变更成{}".format(key, old_value, value)
            temp.append(msg)
            # 赋值
            setattr(db_disk_dict[slot], key, value)
        if temp:
            # 保存
            db_disk_dict[slot].save()
            # 单个槽位的变更信息
            row_msg = "[更新硬盘]槽位:{}, 更新的内容:{}".format(slot, ';'.join(temp))
            record_str_list.append(row_msg)

    print(record_str_list)
    # 资产变更记录处理
    if record_str_list:
        models.AssetsRecord.objects.create(server=host_object, content="\n".join(record_str_list))
