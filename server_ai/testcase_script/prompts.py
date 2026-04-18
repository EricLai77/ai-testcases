

class Prompts:

    @staticmethod
    def phrase_to_natural_language(text_list):

        user_content = """
你是一个产品经理，你的任务是根据我的需求内容，提炼更加精准准确的需求内容，将需求内容用几句话概括，不要创造需求内容。
"""
        assistant_content = """
好的，我会根据你的内容提取核心逻辑和内容概括，不会丢掉核心逻辑的，请发告知我你的需求吧，我会按照json格式以类似[1,2,3,4,5,6,7,8,9]的方式返回给你，其中1,2,3,4,5分别代表我提炼的核心逻辑和内容，
"""
        user_content_one = [
            '本需求文档旨在详细阐述在线商城的购物车功能。', 
            '该功能允许用户将商品添加到购物车中，进行数量的增减和删除操作，并可查看购物车中商品的总价和数量。', 
            '本需求文档将详细描述购物车功能的需求、功能、界面设计等方面的内容。'
        ]

        assistant_content_one = [
            "购物车功能：允许用户添加、删除和修改商品数量。", 
            "用户操作：点击商品图片或名称添加到购物车。", 
            "系统计算：自动计算商品总价并在购物车页面显示。", 
            "优惠券：默认不勾选，勾选后系统自动计算优惠后的总价。"
        ]
        
#         user_content = """
# You are a product manager. Your task is to refine my input requirements into more precise and accurate descriptions, summarizing them in a few concise sentences. Do not create additional requirements.
# """
#         assistant_content = """
# Please provide your requirements for me to distill into core logic points, which will be returned as a JSON array numbered 1 through 9 where each sequential element contains one extracted essential concept without omission.
# """
#         user_content_one = [
#             'This requirements document provides a detailed specification for the shopping cart functionality of the online commerce platform.', 
#             'The shopping cart functionality enables users to add items, modify quantities, remove products, and view both the total price and total item count within the cart.', 
#             'This requirements document specifies the operational parameters, functional capabilities, and user interface elements of the shopping cart feature.'
#         ]

#         assistant_content_one = [
#             "The shopping cart functionality enables users to add items, remove products, and modify product quantities.", 
#             "Users can add items to the shopping cart by clicking either the product image or product name.", 
#             "The system automatically calculates the total price of all items and displays this amount on the shopping cart page.", 
#             "The coupon option remains unselected by default; when selected, the system automatically calculates the final price after applying the discount."
#         ]
        
        prompt = [
            {"role": "user", "content": user_content},
            {"role": "assistant", "content": assistant_content},
            {"role": "user", "content": str(user_content_one)},
            {"role": "assistant", "content": str(assistant_content_one)},
            {"role": "user", "content": str(text_list)}
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
            {"role": "user", "content": text}
        ]
        # prompt = [
        #     {"role": "user", "content": """As a senior software test engineer, please summarize, analyze, and optimize my requirements document, then generate the content in Python dictionary format with guaranteed uniqueness while strictly adhering to the specified requirements.Please follow the following format:{"Functional Requirements": [],"Business Rules": [],"Interface and Interaction": [],"Exception Handling": [],"Performance Requirements": [],"Security Requirements": []}"""},
        #     {"role": "assistant", "content": "Certainly. Please provide your requirements document. I will analyze and optimize it across the following six dimensions, ensuring uniqueness within each category:1.Functional Requirements2.Business Rules3.Interface and Interaction4.Exception Handling5.Performance Requirements6.Security Requirements"},
        #     {"role": "user", "content": "The learning commitment is displayed in the upper-left corner, with content sourced from students' study plans. Each display shows one randomly selected commitment using a breathing light effect. The system automatically displays these commitments without requiring any permissions, presenting a new commitment with each page refresh. A daily limit restricts display to a maximum of 10 different students' commitments, after which no further commitments will be shown."},
        #     {"role": "assistant", "content": str(example)},
        #     {"role": "user", "content": text}
        # ]

        return prompt
