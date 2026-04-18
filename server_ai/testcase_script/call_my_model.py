import json
import time
import requests
import os
import re
from zai import ZhipuAiClient
from openai import OpenAI
 

API_URL = "http://124.156.195.125:3389/v1"
#API_KEY = "fc9abb69a1bc4fd99bc68cd4667422a0.wysA9AgtTUOL6wZW"

def call_ai_model(messages):
    
    client = OpenAI(
        api_key='EMPTY',  # 请填写您自己的 API Key
        base_url=API_URL,
        timeout=10
    )
    try:
        start_time = time.time()
        response = client.chat.completions.create(
            model="checkpoint-200-merged",
            messages=messages,
            stream=False,              # 启用流式输出
            temperature=0.1
        )
        print(f"API call time：{time.time() - start_time:.2f}seconds")
        print(response)
        if response and \
        hasattr(response, 'choices') and \
        len(response.choices) > 0 and \
        hasattr(response.choices[0], 'message') and \
        response.choices[0].message.content is not None:
            return response.choices[0].message.content
        else:
            print(f"API错误: HTTP {response.status_code}")
            return None
    except Exception as e:
        print(f"API调用异常: {str(e)}")
        return None
    
        
        
      
    
def process_data(testcase_descriptions):
    generated_testcases = []
    for each_testcase in testcase_descriptions:
        try:
            
            #print("data------------------------")
            #print(each_testcase)
            # 把前四个角色消息输入给模型    
            input_messages = each_testcase
            ai_response = call_ai_model(input_messages)
            #print("--------------------------------")
            #print(f"AI response: {ai_response}")
            #print("--------------------------------")
            if ai_response is None:
                print("API调用失败，跳过当前条目")
                continue
            
            
            # 用正则提取ai的生成测试点
            pattern_obj = r'(?s)\{([^}]*)\}'
            # 获得生成的测试用例
            ai_testcases = re.findall(pattern_obj, ai_response)
            #print(f"提取到的测试用例: {ai_testcases}")
            generated_testcases.append(ai_testcases)
            
        
        except json.JSONDecodeError:
            print("JSON解析错误，跳过无效行")
        except KeyError as e:
            print(f"数据结构错误: {str(e)}")
        except Exception as e:
            print(f"处理异常: {str(e)}")
    
    return generated_testcases

