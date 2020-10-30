from django.db import models

class UserInfo(models.Model):
    """
    用户表
    """
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    email = models.CharField(max_length=32)


class BusinessUnit(models.Model):
    """
    业务线(部门)
    """
    name = models.CharField(verbose_name='业务线', max_length=64, unique=True)
    def __str__(self):
        return self.name


class IDC(models.Model):
    """
    机房信息:世纪互联6层,兆维8层...
    """
    name = models.CharField(verbose_name='机房', max_length=32)
    floor = models.IntegerField(verbose_name='楼层', default=1)
    def __str__(self):
        return self.name+'(%s层)'%self.floor

class Server(models.Model):
    """
    服务器表
    """
    # 状态
    status_choices = (
        (1, '上线'),
        (2, '下线')
    )
    status = models.IntegerField(verbose_name='状态', choices=status_choices, default=1)

    business_unit = models.ForeignKey(verbose_name='业务线', to='BusinessUnit', null=True, blank=True, on_delete=models.CASCADE)

    # IDC有关的
    idc = models.ForeignKey(verbose_name='机房', to='IDC', null=True, blank=True, on_delete=models.CASCADE)
    cabinet_num = models.CharField(verbose_name='机柜号', max_length=32, null=True, blank=True)
    cabinet_order = models.CharField(verbose_name='机柜中序号', max_length=32, null=True, blank=True)

    hostname = models.CharField(verbose_name='主机名', max_length=32)
    last_date = models.DateField(verbose_name='最近汇报的时间', null=True, blank=True)

    # 系统数据
    os_platform = models.CharField(verbose_name='系统', max_length=16, null=True, blank=True)
    os_version = models.CharField(verbose_name='系统版本', max_length=16, null=True, blank=True)
    # 主板
    manufacturer = models.CharField(verbose_name='制造商', max_length=32, null=True, blank=True)
    model = models.CharField(verbose_name='型号', max_length=64, null=True, blank=True)
    sn = models.CharField(verbose_name='序列号', max_length=64, null=True, blank=True)
    # cpu
    cpu_count = models.IntegerField(verbose_name='cpu个数', null=True, blank=True)
    cpu_physical_count = models.IntegerField(verbose_name='cpu物理个数', null=True, blank=True)
    cpu_model = models.CharField(verbose_name='cpu型号', max_length=64, null=True, blank=True)


class Disk(models.Model):
    """
    硬盘信息表
    """
    slot = models.CharField(verbose_name='槽位', max_length=32)
    pd_type = models.CharField(verbose_name='类型', max_length=32)
    capacity = models.CharField(verbose_name='容量', max_length=32)
    model = models.CharField(verbose_name='型号', max_length=64)
    server = models.ForeignKey(verbose_name='服务器', to='Server', on_delete=models.CASCADE)


class Memory(models.Model):
    """
    内存信息表
    """
    capacity = models.FloatField(verbose_name='容量', null=True, blank=True)
    slot = models.CharField(verbose_name='槽位', max_length=32)
    model = models.CharField(verbose_name='型号', max_length=64, null=True, blank=True)
    speed = models.CharField(verbose_name='速度', max_length=16, null=True, blank=True)
    manufacturer = models.CharField(verbose_name='制造商', max_length=32, null=True, blank=True)
    sn = models.CharField(verbose_name='序列号', max_length=64, null=True, blank=True)
    server = models.ForeignKey(verbose_name='服务器', to='Server', on_delete=models.CASCADE)


class NetWork(models.Model):
    """
    网卡信息表
    """
    name = models.CharField(verbose_name='网卡名称', max_length=128, null=True, blank=True)
    up = models.BooleanField(default=False)
    hwaddr = models.CharField(verbose_name='网卡mac地址', max_length=64, null=True, blank=True)
    ipaddrs = models.CharField(verbose_name='ip地址', max_length=256, null=True, blank=True)
    netmask = models.CharField(verbose_name='子网掩码', max_length=32, null=True, blank=True)
    broadcast = models.CharField(verbose_name='广播', max_length=32, null=True, blank=True)
    server = models.ForeignKey(verbose_name='服务器', to='Server', on_delete=models.CASCADE)


class AssetsRecord(models.Model):
    """
    资产变更记录
    """
    server = models.ForeignKey(verbose_name='服务器', to='Server', on_delete=models.CASCADE)
    content = models.TextField(verbose_name='内容')
    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
