import json
import datetime

from django.views import View
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt  #避开csrf认证
from rest_framework.views import APIView

from api import models
from api.service.board import process_board_info
from api.service.cpu import process_cpu_info
from api.service.disk import process_disk_info
from api.service.memory import process_memory_info
from api.service.network import process_network_info
from api.service.basic import process_basic_info


# @method_decorator(csrf_exempt, name='dispatch')
# class ServerView(View):

class ServerView(APIView):

    def get(self, request, *args, **kwargs):
        """
        获取今日未采集的服务器列表
        :param request:
        :return:
        """
        today = datetime.date.today()
        # 最近汇报时间小于今天 or None(新资产)
        server_queryset = models.Server.objects.filter(Q(last_date__lt=today) | Q(last_date__isnull=True)).filter(status=1).values_list("hostname")

        server_list = [item[0] for item in server_queryset]

        return JsonResponse({'status': True, 'data': server_list})

    def post(self, request, *args, **kwargs):
        """
        获取中控机汇报的资产信息,并进行入库操作以及变更记录
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        content = request.body.decode('utf-8')
        server_info_dict = json.loads(content)
        hostname = server_info_dict['host']
        info_dict = server_info_dict['info']

        host_object = models.Server.objects.filter(hostname=hostname).first()
        if not host_object:
            return HttpResponse('服务器不存在,请检查...')

        # 版本信息入库
        process_basic_info(host_object, info_dict['basic'])

        # 主板信息入库
        process_board_info(host_object, info_dict['board'])

        # CPU信息入库
        process_cpu_info(host_object, info_dict['cpu'])

        # 硬盘信息入库
        process_disk_info(host_object, info_dict['disk'])

        # 内存信息入库
        process_memory_info(host_object, info_dict['memory'])

        # 网卡信息入库
        process_network_info(host_object, info_dict['network'])

        # 该服务器采集完数据并入库后更改最近一次汇报的时间
        host_object.last_date = datetime.date.today()
        host_object.save()

        return HttpResponse("成功!")

# FBV版本
# def get_server(request):
#     """
#     获取今日未采集的服务器列表
#     :param request:
#     :return:
#     """
#     today = datetime.date.today()
#     # 最近汇报时间小于今天 or None(新资产)
#     """
#     con = Q()
#     con.connector = 'OR'
#     con.children.append(('last_date__lt', today))
#     con.children.append(('last_date__isnull', True))
#     server_list = models.Server.objects.filter(con)
#     """
#     server_queryset = models.Server.objects.filter(Q(last_date__lt=today) | Q(last_date__isnull=True)).values_list("hostname")
#
#     server_list = [item[0] for item in server_queryset]
#
#     return JsonResponse({'status': True, 'data': server_list})
#
#
# @csrf_exempt
# def get_data(request):
#
#     content = request.body.decode('utf-8')
#     server_info_dict = json.loads(content)
#     hostname = server_info_dict['host']
#     info_dict = server_info_dict['info']
#
#     host_object = models.Server.objects.filter(hostname=hostname).first()
#     if not host_object:
#         return HttpResponse('服务器不存在,请检查...')
#     # 硬盘信息入库
#     process_disk_info(host_object, info_dict['disk'])
#
#     # 该服务器采集完数据并入库后更改最近一次汇报的时间
#     host_object.last_date = datetime.date.today()
#     host_object.save()
#
#     return HttpResponse("成功!")

