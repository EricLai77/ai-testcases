

class TestcasePrompts:

    @staticmethod
    def phrase_to_natural_language(text_list,test_direction,testpoint):

#         system_content = """
# You are a software test engineer. Your task is to generate test cases based on the requirements.
# """
#         user_content = """
# You must utilize the complete set of requirements to understand business relationships and logic. Based on this comprehensive business understanding, generate necessary test cases for specified requirements with emphasis on test coverage - designing multiple test points to ensure completeness. For new requirements, focus extensively on coverage breadth; for iterative requirements, prioritize regression test coverage. Avoid creating duplicate test cases and do not invent requirements beyond what is provided.
# """
        
#         assistant_content = """
# Understood. I will generate test cases that meet the specified requirements and strictly adhere to the Python list-of-dictionaries format:  [{"testpoint": "Test point 1 description", "operation": "1. Step one. 2. Step two", "expectedresult": "1. Expected outcome one. 2. Expected outcome two"}, {"testpoint": "Test point 2 description", "operation": "1. Step one. 2. Step two", "expectedresult": "1. Expected outcome one. 2. Expected outcome two"}].
# """
        

        
#         prompt = [
#             {"role": "system", "content": str(system_content)},
#             {"role": "user", "content": user_content},
#             {"role": "assistant", "content": assistant_content},
#             {"role": "user", "content": str(text_list) + ", Testing scope includes：" + test_direction + ",Specified requirements for test case generation are：" + testpoint}
            
#         ]
        
            system_content = """
你是一名软件测试工程师。你的任务是根据需求生成测试用例。
"""
            user_content = """
你必须充分利用完整的业务需求，理解其中的业务关联与逻辑。基于这种全面的业务认知，针对指定需求生成必要的测试用例，并重点保障测试覆盖率——通过设计多个测试点来确保完备性。对于新增需求，要重点拓展覆盖广度；对于迭代需求，则应优先考虑回归测试覆盖。避免编写重复的测试用例，且不得自行添加超出既定范围的额外需求。
"""
        
            assistant_content = """
明白。我将按照要求生成测试用例，并严格遵循Python字典列表格式：[{"testpoint": "测试点1描述", "operation": "1. 步骤一 2. 步骤二", "expectedresult": "1. 预期结果一 2. 预期结果二"},{"testpoint": "测试点2描述", "operation": "1. 步骤一 2. 步骤二", "expectedresult": "1. 预期结果一 2. 预期结果二"}]
"""
        

        
            prompt = [
                {"role": "system", "content": str(system_content)},
                {"role": "user", "content": user_content},
                {"role": "assistant", "content": assistant_content},
                {"role": "user", "content": str(text_list) + ", 测试范围包括：" + test_direction + ",测试用例生成的具体测试点要求是：" + testpoint}
                
            ]
            return prompt
    

    @staticmethod
    def requirement_extraction_prompt(text):
        """
        requirement_extraction
        """

        example = {
            "功能需求": [
                "实现学习承诺的随机展示功能。",
                "学习承诺的展示为自动触发，无需用户操作。",
                "每次刷新页面时，展示一条新的学习承诺。"
            ],
            "业务规则": [
                "学习承诺来源于学员在学习计划中的创建。",
                "每天最多展示10个不同学员的学习承诺。",
                "超过10次展示后，当天不再展示新的学习承诺。"
            ],
            "界面和交互": [
                "学习承诺展示位置：页面左上角。",
                "学习承诺展示方式：呼吸灯效果。",
                "无需用户操作，页面刷新时自动展示新的学习承诺。"
            ],
            "异常处理": [
                "当学习承诺数量不足10条时，确保仍能正常展示。",
                "当学习承诺数量超过10条时，不再展示新的学习承诺。",
                "处理页面刷新过程中可能出现的展示异常，如数据加载失败、页面渲染错误等。"
            ],
            "性能需求": [
                "确保学习承诺的展示速度，不影响页面加载，需遵循258定理。",
                "优化数据查询和缓存机制，提高学习承诺展示的响应速度。"
            ],
            "安全需求": [
                "保证学习承诺数据的安全性，防止数据泄露。",
                "确保展示过程不会对服务器和客户端造成安全风险。",
                "对学习承诺内容进行审核，防止展示不当信息。"
            ]
            # "Functional Requirements": [
            #     "Implement random display functionality for learning commitments",
            #     "Learning commitments are displayed automatically without requiring user interaction",
            #     "A new learning commitment is displayed each time the page is refreshed"
            # ],
            # "Business Rules": [
            #     "Learning commitments are sourced from students' created study plans",
            #     "A maximum of 10 different students' learning commitments can be displayed per day",
            #     "No new learning commitments will be displayed after exceeding 10 daily displays"
            # ],
            # "Interface and Interaction": [
            #     "Display position: Upper-left corner of the page",
            #     "Display method: Breathing light effect",
            #     "Automatic display of new learning commitments upon page refresh without user interaction"
            # ],
            # "Exception Handling": [
            #     "Ensure normal display when the number of learning commitments is less than 10",
            #     "Stop displaying new learning commitments when the number exceeds 10",
            #     "Handle display exceptions during page refresh, such as data loading failures and page rendering errors"
            # ],
            # "Performance Requirements": [
            #     "Ensure learning commitment display speed does not affect page loading, complying with the 258 principle",
            #     "Optimize data query and caching mechanisms to improve response speed of learning commitment display"
            # ],
            # "Security Requirements": [
            #     "Ensure the security of learning commitment data and prevent data leakage",
            #     "Ensure the display process poses no security risks to servers and clients",
            #     "Review learning commitment content to prevent display of inappropriate information"
            # ]
        }

        prompt = [
            {"role": "user", "content": """作为一名高级软件测试工程师，请为我的需求文档做总结、分析、优化。并以python字典数据类型的方式生成。生成的内容保证唯一性。请严格按照要求的{"功能需求": [],"业务规则": [],"界面和交互": [],"异常处理": [],"性能需求": [],"安全需求": []}格式生成内容"""},
            {"role": "assistant", "content": "当然，请提供您的需求文档，我会从1. 功能需求 2. 业务规则 3. 界面和交互 4. 异常处理 5. 性能需求 6. 安全需求这几个维度为您进行分析和优化，并保证各个维度内容的唯一性。"},
            {"role": "user", "content": "左上角展示学员的学习承诺，学习承诺在学习计划中创建。学习承诺每次随机只展示一条，展示效果为呼吸灯效果。学习承诺自动展示，不需要任何权限，每刷新一次就会展示一条新的学习承诺。学习承诺需要限制每天最多只能展示10个不同的学员的学习承诺，当超过10次就不再展示。"},
            {"role": "assistant", "content": str(example)},
            {"role": "user", "content": str(text)}
        ]
        # prompt = [
        #     {"role": "user", "content": """As a senior software test engineer, please summarize, analyze, and optimize my requirements document, then generate the content in Python dictionary format with guaranteed uniqueness while strictly adhering to the specified requirements.Please follow the following format:{"Functional Requirements": [],"Business Rules": [],"Interface and Interaction": [],"Exception Handling": [],"Performance Requirements": [],"Security Requirements": []}"""},
        #     {"role": "assistant", "content": "Certainly. Please provide your requirements document. I will analyze and optimize it across the following six dimensions, ensuring uniqueness within each category:1.Functional Requirements2.Business Rules3.Interface and Interaction4.Exception Handling5.Performance Requirements6.Security Requirements"},
        #     {"role": "user", "content": "The learning commitment is displayed in the upper-left corner, with content sourced from students' study plans. Each display shows one randomly selected commitment using a breathing light effect. The system automatically displays these commitments without requiring any permissions, presenting a new commitment with each page refresh. A daily limit restricts display to a maximum of 10 different students' commitments, after which no further commitments will be shown."},
        #     {"role": "assistant", "content": str(example)},
        #     {"role": "user", "content": str(text)}
        # ]
        #print(text)
        return prompt
