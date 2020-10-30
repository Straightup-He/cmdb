#-*- coding = utf-8 -*-
#@Time : 2020/10/4 20:31
#@Author : straightup
from api import models

def process_memory_info(host_object, memory_dict):
    """
    处理汇报的内存信息
    :param host_object: 主机
    :param memory_dict: 状态 内存信息 错误信息
    :return:
    """
    if not memory_dict['status']:
        print('获取内存资产时出错:', memory_dict['error'])
        return
    # 取出采集到的内存信息
    new_memory_dict = memory_dict['data']
    new_memory_slot_dict = set(new_memory_dict)

    db_memory_queryset = models.Memory.objects.filter(server=host_object).all()
    db_memory_dict = {row.slot: row for row in db_memory_queryset}
    db_memory_slot_dict = set(db_memory_dict)

    # 新增
    create_slot_set = new_memory_slot_dict - db_memory_slot_dict
    # 删除
    remove_slot_set = db_memory_slot_dict - new_memory_slot_dict
    # 更新
    update_slot_set = new_memory_slot_dict & db_memory_slot_dict

    # print('新增', create_slot_set)
    # print('删除', remove_slot_set)
    # print('更新', update_slot_set)

    record_str_list = []

    # 新增
    for slot in create_slot_set:
        models.Memory.objects.create(**new_memory_dict[slot], server=host_object)
        msg = '[新增内存]槽位:{slot}, 容量:{capacity}, 型号:{model}, 速度:{speed}, 制造商:{manufacturer}, 序列号:{sn}'.format(**new_memory_dict[slot])
        record_str_list.append(msg)

    # 删除
    if remove_slot_set:
        models.Memory.objects.filter(server=host_object, slot__in=remove_slot_set).delete()
        msg = '[删除内存]槽位:{}'.format(','.join(remove_slot_set))
        record_str_list.append(msg)

    # 更新
    for slot in update_slot_set:
        temp = []
        for key, value in new_memory_dict[slot].items():
            old_value = getattr(db_memory_dict[slot], key)
            if value == old_value:
                continue
            msg = "内存的{}, 由{}变更成{}".format(key, old_value, value)
            temp.append(msg)
            setattr(db_memory_dict[slot], key, value)
        if temp:
            db_memory_dict[slot].save()
            row_msg = "[更新内存]槽位:{}, 更新的内容:{}".format(slot, ';'.join(temp))
            record_str_list.append(row_msg)

    print(record_str_list)
    # 资产变更记录处理
    if record_str_list:
        models.AssetsRecord.objects.create(server=host_object, content="\n".join(record_str_list))

