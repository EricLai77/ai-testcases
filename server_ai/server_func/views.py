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
import re
import mimetypes
import json
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.sessions.models import Session
from django.contrib.auth import logout

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer

from rest_framework.permissions import AllowAny
from openai import OpenAI
from zai import ZhipuAiClient

#生成测试用例需要的库
from mydocuments.models import Project, RequirementDocument, DocumentSection, InputRequirementDocument
from testcase_script.config import loadConfig
from testcase_script.vectorIndexing import VectorIndexing
from testcase_script.utl import generate_and_download_docx
from testcase_script.utl import clean_json_text
from testcase_script.utl import clean_and_parse_json
from testcase_script.utl import extract_outer_braces
from testcase_script.utl import remove_json_comments
from testcase_script.model import ZhiPu4
from testcase_script.docmentpar import WordDocumentParser
from testcase_script.sentencesearch import SimilarSentenceSearch
from testcase_script.testcase_prompts import TestcasePrompts
from testcase_script.call_my_model import process_data
from docx import Document
from docx.shared import Pt


config = loadConfig()
configs = config.load_config()

@require_http_methods(['POST'])
def generate_testcase(request):
    response = {}
    if not request.user.is_authenticated:
        return JsonResponse({'error':'illegal user!'}, status = 401)
    pass
    
    #获取文档id
    body = json.loads(request.body.decode("utf-8"))
    inputdocument_id = body.get("inputdocument_id")
    
    document = InputRequirementDocument.objects.get(id=inputdocument_id)
    if document is None:
        response['code'] = 2
        response['msg'] = 'this document is not available!'
        return JsonResponse(response)
    inputdocument_name = document.name
    #convert docx to vector
    #print('inputdocument_name------------------------')
    SUMMARY_LENGTH = configs['SUMMARY_LENGTH']
    
    #vector_indexing = VectorIndexing()
    #vector_indexing.process_texts()
    print('Step 1: Vector indexing completed.')
    
    
    #deal with with document
    needs_text_list = []
    parser = WordDocumentParser("media/requirements/inputdocuments/" + inputdocument_name + ".docx")
    sentences = parser.parse()
    needs_text_list.append(sentences)
    merged_needs_text_list = [sentence for sublist in needs_text_list for sentence in sublist]
    print('merged_needs_text_list------------------------分析出来的原始需求')
    print(merged_needs_text_list)  
    
    
    zhipu_4 = ZhiPu4()
    #print("-------------------------------------")
    information_document = merged_needs_text_list
    #print(f"information_document：{information_document}")
    #print("-------------------------------------")
    information_document_list = zhipu_4.split_list_by_text_length(information_document, SUMMARY_LENGTH)
    print(f"information_document_list_SUMMARY_LENGTH：{information_document_list}")
    print("-------------------------------------")
    reponse = zhipu_4.concurrent_zhipuai_request_text(information_document_list)
    print("切分好后的句子-------------------------------------")
    print(f"reponse：{reponse}")
    
    
    print('开始封装输入')
    
    #封装需求格式
    testcase_descriptions = []
    for response_sentence in reponse:
        
        
        pre_testcase_description = TestcasePrompts.requirement_extraction_prompt(response_sentence )
        
        print(f"pre_testcase_description：{pre_testcase_description}")
        print("**************************************")
        reponse_testcase_description = zhipu_4.concurrent_zhipuai_request_text([pre_testcase_description])
        print(f"reponse_testcase_description1：{reponse_testcase_description}")
        print("-------------------------------------")
        #生成的测试用例描述的预处理
        reponse_testcase_description = reponse_testcase_description[0].strip("```python").strip("```")
        #print(f"reponse_testcase_description2：{reponse_testcase_description}")
        #print(type(reponse_testcase_description))
        reponse_testcase_description = extract_outer_braces(reponse_testcase_description)
        #print(f"reponse_testcase_description3：{reponse_testcase_description}")
        #print(type(reponse_testcase_description))
        clean_text = reponse_testcase_description.replace("\\n", "\n")
        clean_text = remove_json_comments(clean_text)

        #print(f"reponse_testcase_description：{reponse_testcase_description}")
        clean_text = reponse_testcase_description.replace("'", '"')
        clean_text = clean_json_text(clean_text)
        
        # eng-remove JavaScript style comments
    
        # eng-
       
        print("*******************清理小标点和清洗后*******************")
        print(clean_text)
        print("**************************************")
        clean_text = json.loads(clean_text)
        print(clean_text)
        #print(type(clean_text))
        for test_direction, testpoints in clean_text.items():
            #print(f"\n【{test_direction}】")
            for i, testpoint in enumerate(testpoints, 1):
                #print(f"  {i}. {testpoint}")
            
                #final_testcase_description = json.loads(clean_text)
                final_testcase_description = TestcasePrompts.phrase_to_natural_language(clean_text,test_direction,testpoint)
                print(f"final_testcase_description：{final_testcase_description}")
                testcase_descriptions.append(final_testcase_description)
    print('Step 2: Inputed requirements analysis completed.')
    print('testcase_requirements_analysis_descriptions------------------------')
    print(testcase_descriptions)
    #准备可访问模型了
    #generated_testcases = process_data(testcase_descriptions)
    print('Step 3: Generated testcases have been completed. Ready to export them.')
    #response = generate_and_download_docx(request, generated_testcases, inputdocument_name)
    print(f"✅ Step 4: Your testcases have been generated successfully!")
    
    
    
    
    
    response['code'] = 0
    response['msg'] = 'your testcases have been generated successfully!'
    print(response)
    return response
    
    
@require_http_methods(['POST'])
def zhipu_model(request):
    '''
    @return code 0 信息获取成功；1 信息获取失败
    @return msg    返回所有配置信息；返回空值
    '''
    # 确保用户已经登陆了
    #if not request.user.is_authenticated:
    #    return JsonResponse({'error':'illegal user!'}, status = 401)
    response2Client = {}
    output = ""
    try:
        # Initialize client
        client = ZhipuAiClient(api_key="fc9abb69a1bc4fd99bc68cd4667422a0.wysA9AgtTUOL6wZW")  # 请填写您自己的 API Key

        response = client.chat.completions.create(
            model="GLM-Z1-Flash",
            messages=[
                {"role": "user", "content": "在新西兰的冬天，如何才能吃上便宜的蔬菜？"},
                #{"role": "assistant", "content": "当然，要创作一个吸引人的口号，请告诉我一些关于您产品的信息"},
                #{"role": "user", "content": "智谱AI开放平台"}
            ],
            thinking={
                "type": "enabled",    # 启用深度思考模式
            },
            stream=True,              # 启用流式输出
            max_tokens=1024*10,          # 最大输出tokens
            temperature=0.3           # 控制输出的随机性
        )
        print('begin to answer!')
        # 获取回复
        for chunk in response:
            if chunk.choices[0].delta.content:
                print(chunk.choices[0].delta.content, end='')
                output = output + chunk.choices[0].delta.content
                print(chunk.choices[0])
                print(chunk.choices[0].delta)
            
        print(output)
    except:
        response2Client['code'] = 1
        response2Client['msg'] = 'There are some problems in your program!'
    else:
        response2Client['code'] = 0
        response2Client['msg'] = output
    
    return JsonResponse(response2Client)

@require_http_methods(['POST'])
def deepseek_model(request):
    '''
    @return code 0 信息获取成功；1 信息获取失败
    @return msg    返回所有配置信息；返回空值
    '''
    # 确保用户已经登陆了
    #if not request.user.is_authenticated:
    #    return JsonResponse({'error':'illegal user!'}, status = 401)
    response = {}
    #try:
    client = OpenAI(api_key="sk-14b4820b5cd84261a752052c9cc71a44", base_url="https://api.deepseek.com")
    print(client)
    responseFromModel = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": "Hello"},
        ],
        stream=True
    )

    print(responseFromModel.choices[0].message.content)
    
    
    #except:
    #    response['code'] = 1
    #    response['msg'] = 'There are some problems in your program!'
    #else:
    response['code'] = 0
    response['msg'] = response.choices[0].message.content
    
    return JsonResponse(response)

class UserRegistrationView(APIView):
    permission_classes = [AllowAny]  # 允许未认证用户访问
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
    print("config_key",config_key)
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
    # 确保用户已经登陆了
    if not request.user.is_authenticated:
        return JsonResponse({'error':'illegal user!'}, status = 401)
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











