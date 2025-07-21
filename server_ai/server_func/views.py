from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponse
from server_func import models
import time
from datetime import date
from django.db.models import Count, Max, Min
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
from django.utils import timezone
from django.core import serializers
from django.http import StreamingHttpResponse
import os
import mimetypes
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.sessions.models import Session
from django.contrib.auth import logout

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        response = {}
        print(serializer)
        print(serializer.is_valid())
        print("验证错误:", serializer.errors)  # 打印到控制台
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            response['code'] = 0
            response['msg'] = 'User registered successfully!'
            response['username'] = serializer.validated_data.get('username')
            return JsonResponse(response)
        
        response['code'] = 1
        response['msg'] = 'There are some problems in your program!'
        return JsonResponse(response)
    
    
    
@require_http_methods(['GET'])
def all_project_config(request):
    '''
    @return code 0 信息获取成功；1 信息获取失败
    @return msg    返回所有配置信息；返回空值
    '''
    # 确保用户已经登陆了
    if not request.user.is_authenticated:
        return JsonResponse({'error':'illegal user!'}, status = 401)
    
    response = {}
    try:
        config_objs = models.projectconfig.objects.all().values_list()
    except:
        response['code'] = 1
        response['msg'] = 'There are some problems in your program!'
    else:
        response['code'] = 0
        response['msg'] = list(config_objs)
    
    return JsonResponse(response)


#require_http_methods 代表调用请求时请求方法必须为POST请求
@require_http_methods(['POST']) 
def create_config_info(request):
    '''
    创建配置信息
    @return code 0创建成功; 1创建失败
    @return msg, You have created a new configer successfully!; There are some problems in your program!	
    '''
    # 确保用户已经登陆了
    if not request.user.is_authenticated:
        return JsonResponse({'error':'illegal user!'}, status = 401)
    
    id = 0
    config_count = models.projectconfig.objects.all().values_list().count()
    if config_count != 0:
        #表示不是空表
        last_id = models.projectconfig.objects.all().values_list('id').last()[0]
        id = last_id + 1
    else:
        id = 1
    
    #创建学生信息
    config_id = id
    config_key = request.POST.get('key')
    config_value = request.POST.get('value')
    config_memo = request.POST.get('memo')
    config_create_time = date.today()

    response = {}
    
    #参数判断
    if config_key is None or len(config_key) == 0:
        response['code'] = 2
        response['msg'] = 'key is not correct!'
        return JsonResponse(response)
    #
    if config_value is None or len(config_value) == 0:
        response['code'] = 3
        response['msg'] = 'value is not correct!'
        return JsonResponse(response)
    
    #判断是否已存在
    # 检查某个字段值是否存在
    key_to_check = config_key
    exists = models.projectconfig.objects.filter(key=key_to_check).exists()

    if exists:
        response['code'] = 4
        response['msg'] = 'this key is already here!'
        return JsonResponse(response)

    try:
        #创建数据
        models.projectconfig.objects.create(id = config_id, key = config_key, value = config_value, create_time = config_create_time, memo = config_memo)

    except:
        response['code'] = 1
        response['msg'] = 'There are some problems in your program!'
    else:
        response['code'] = 0
        response['msg'] = 'You have created a new configer successfully!'
  
    
    return JsonResponse(response)

#require_http_methods 代表调用请求时请求方法必须为POST请求
@require_http_methods(['POST']) 
def user_logout(request):
    response = {}
    try:
        logout(request)
    except:
        response['code'] = 1
        response['msg'] = 'There are some problems in your program!'
    else:
        response['code'] = 0
        response['msg'] = 'Loginout successfully!'
    return JsonResponse(response)

        
#require_http_methods 代表调用请求时请求方法必须为POST请求
@require_http_methods(['POST']) 
def user_login(request):
    
    username = request.POST['username']
    password = request.POST['password']
           
    response = {}
    try:
        #用户登陆
        user = authenticate(request, username=username, password=password)

    except:
        response['code'] = 1
        response['msg'] = 'There are some problems in your program!'
    else:
    
        if user is not None:
            login(request, user)
            response['code'] = 0
            response['msg'] = 'login successfully!'
            response['username'] = username
        else:
            # 返回错误信息
            response['code'] = 2
            response['msg'] = 'username or password is not correct!'
            
    return JsonResponse(response)


#require_http_methods 代表调用请求时请求方法必须为POST请求
@require_http_methods(['POST']) 
def edit_config_info(request):
    '''
    编辑配置信息
    @return code 0编辑成功; 1编辑失败
    @return msg, You have created a new configer successfully!; There are some problems in your program!	
    '''
    # 确保用户已经登陆了
    if not request.user.is_authenticated:
        return JsonResponse({'error':'illegal user!'}, status = 401)
    #配置信息
    #config_id = request.POST.get('id')
    config_key = request.POST.get('key')
    config_value = request.POST.get('value')
    config_memo = request.POST.get('memo')
    print(config_key)
    response = {}
    
    #参数判断
    if config_key is None or len(config_key) == 0:
        response['code'] = 2
        response['msg'] = 'key is not correct!'
        return JsonResponse(response)
    
    if config_value is None or len(config_value) == 0:
        response['code'] = 3
        response['msg'] = 'value is not correct!'
        return JsonResponse(response)
    
    
    # 检查key字段值是否存在
    key_to_check = config_key
    exists = models.projectconfig.objects.filter(key=key_to_check).exists()

    if not exists:
        response['code'] = 6
        response['msg'] = "'this key doesn't exist!'"
        return JsonResponse(response)

    try:
        #编辑数据数据
        config = get_object_or_404(models.projectconfig, key = config_key )

    except:
        response['code'] = 1
        response['msg'] = 'There are some problems in your program!'
    else:
        #config.key = config_key
        config.value = config_value
        config.create_time = date.today()
        if config_memo:
            config.memo = config_memo
        config.save()
    
        response['code'] = 0
        response['msg'] = 'You have edited this configer successfully!'
  
    
    return JsonResponse(response)


#require_http_methods 代表调用请求时请求方法必须为POST请求
@require_http_methods(['POST']) 
def delete_config_info(request):
    '''
    删除配置信息
    @return code 0删除成功; 1删除失败
    @return msg, You have created a new configer successfully!; There are some problems in your program!	
    '''
    # 确保用户已经登陆了
    if not request.user.is_authenticated:
        return JsonResponse({'error':'illegal user!'}, status = 401)
    #配置信息
    config_id = request.POST.get('id')
    config_key = request.POST.get('key')
    config_value = request.POST.get('value')
    config_memo = request.POST.get('memo')

    response = {}
    
    #参数判断
    if config_key is None or len(config_key) == 0:
        response['code'] = 4
        response['msg'] = 'key is not correct!'
        return JsonResponse(response)
    
    #判断是否已存在
    # 检查id字段值是否存在
    key_to_check = config_key
    exists = models.projectconfig.objects.filter(key=key_to_check).exists()

    if not exists:
        response['code'] = 5
        response['msg'] = 'this key is not available!'
        return JsonResponse(response)

    try:
        #编辑数据数据
        config = get_object_or_404(models.projectconfig, key = config_key )
        config.delete()
    except:
        response['code'] = 1
        response['msg'] = 'There are some problems in your program!'
    else:
        
        response['code'] = 0
        response['msg'] = 'You have deleted this configer successfully!'
  
    
    return JsonResponse(response)











