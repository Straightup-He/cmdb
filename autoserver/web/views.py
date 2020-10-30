from django.shortcuts import render, HttpResponse, redirect
from django.db.models import Count
from django.http import JsonResponse

from api import models

def index(request):
    """
    后台管理页
    :param request:
    :return:
    """
    server_list = models.Server.objects.all()
    return render(request, 'index.html', {'server_list': server_list})


# 新增服务器
from django import forms
class ServerModelForm(forms.ModelForm):
    class Meta:
        model = models.Server
        fields = ['hostname', 'business_unit', 'idc', 'cabinet_num', 'cabinet_order', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for index, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

def create_server(request):
    if request.method == 'GET':
        form = ServerModelForm()
        return render(request, 'create_server.html', {'form': form})
    else:
        form = ServerModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            return render(request, 'create_server.html', {'form': form})

def pie(request):
    """
    返回饼图
    :param request:
    :return:
    """
    return render(request, 'pie.html')

def pie_data(request):
    """
    获取饼状图数据,构造数据结构
    [
        {'name': '销售', 'y': 4},
        {'name': '销售', 'y': 4}
    ]
    name 和 y 是根据官方文档来的
    :param request:
    :return:
    """
    result = models.Server.objects.values('business_unit__name').annotate(y=Count('business_unit__id'))
    """
    [
        {'business_unit': '销售', 'y': 4},
        {'business_unit': '运营', 'y': 4}
    ]
    """
    data = [{'name': item['business_unit__name'], 'y': item['y']} for item in result]
    print(data)
    return JsonResponse(data, safe=False)  #列表不能直接传输