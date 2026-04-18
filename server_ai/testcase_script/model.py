

from abc import abstractmethod
from typing import List
from zhipuai import ZhipuAI
from testcase_script.config import loadConfig
from concurrent.futures import ThreadPoolExecutor, as_completed
from testcase_script.prompts import Prompts


class BaseModel:
    def __init__(self):
        pass

    @abstractmethod
    def get_model_response(self, prompt: str, images: List[str]):
        pass


class ZhiPu4:
    def __init__(self) -> None:
        loadconfig = loadConfig()
        self.config_data = loadconfig.load_config()
        self.api_key = self.config_data['OPENAI_API_KEY']
        # vector embedding model
        self.embedding_model = self.config_data['OPENAI_API_MODEL_EMBEDDING']
        # text generation model
        self.glm4_model = self.config_data['OPENAI_API_MODEL_GLM4']
        self.max_threads = self.config_data['MAX_THREADING']

    def zhipuai_request_vector(self, input):
        try:
            client = ZhipuAI(api_key=self.api_key)
            response = client.embeddings.create(
                model=self.embedding_model,
                input=input,
            )
            return True, response
        except Exception as e:
            return False, f'zhipuai request is fail: {str(e)}'
        
    def zhipuai_request_text(self, messages):
        try:
            client = ZhipuAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model=self.glm4_model,
                messages=messages,
                temperature=0.1
            )
            return True, response.choices[0].message.content
        except Exception as e:
            return False, f'zhipuai request is fail: {str(e)}'

    def concurrent_zhipuai_request_text(self, messages_list: List[List[str]]):
        # set up a thread pool
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            
            futures = [executor.submit(self.zhipuai_request_text, messages) for messages in messages_list]
            responses = []
            for future in as_completed(futures):
                # get the result
                is_success, response = future.result()
                if is_success:
                    responses.append(response)
                else:
                    # deal with the error
                    print(response)
            return responses
        
    def split_list_by_text_length(self, input_list, threshold):
       
        # create a list to hold the split sublists
        split_lists = []
        # create a temporary list to hold the current sublist
        current_sublist = []
        
        # iterate over each item in the input list
        for item in input_list:
            
            if sum(len(text) for text in current_sublist) + len(item) <= threshold:
                current_sublist.append(item)
            else:
                
                phrase_to_natural_language_prompts = Prompts.phrase_to_natural_language(current_sublist)
                split_lists.append(phrase_to_natural_language_prompts)
                current_sublist = [item]
        
        # add the last sublist if not empty
        if current_sublist:
            phrase_to_natural_language_prompts = Prompts.phrase_to_natural_language(current_sublist)
            split_lists.append(phrase_to_natural_language_prompts)
        
        return split_lists