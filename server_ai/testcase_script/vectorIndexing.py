from testcase_script.config import loadConfig
from testcase_script.docmentpar import WordDocumentParser
from testcase_script.model import ZhiPu4
import faiss
import numpy as np
from testcase_script.vectordb import VectorDatabase
from testcase_script.prompts import Prompts
import re

class VectorIndexing:
    def __init__(self):
        self.config = loadConfig()
        self.configs = self.config.load_config()
        self.needs_names = self.configs['NEEDS_NAME']
        self.zhipu_ai = ZhiPu4()
        self.index = faiss.IndexFlatL2(1024)
        self.vector_id_to_text = []
        self.faiss_path_name = self.configs['FAISS_DB_PATH']
        self.host = self.configs['MYSQL_HOST']
        self.user = self.configs['MYSQL_USER']
        self.password = self.configs['MYSQL_PASSWORD']
        self.port = self.configs['MYSQL_PORT']
        self.db = self.configs['MYSQL_DATABASE']
        self.vectordb = VectorDatabase(self.host, self.user, self.password, self.port, self.db)

    def process_texts(self):
        needs_text_list = []
        for need_name in self.needs_names:
            need_path = 'media/requirements/documents/' + need_name
            parser = WordDocumentParser(need_path)
            sentences = parser.parse()
            needs_text_list.append(sentences)
        #print('needs_text_list------------------------')
        #print(needs_text_list)
        merged_needs_text_list = [sentence for sublist in needs_text_list for sentence in sublist]
        #print('merged_needs_text_list------------------------')
        #print(merged_needs_text_list)
        for text in merged_needs_text_list:
            reponse = self.zhipu_ai.zhipuai_request_vector(text)
            vector = reponse[1].data[0].embedding
            vector = np.array(vector).reshape(1, -1)
            self.index.add(vector)
            vector_id = self.index.ntotal - 1
            self.vector_id_to_text.append((vector_id + 1, text, vector_id))
            to_save_faiss_path = "media/requirements/documents_faiss/" + self.faiss_path_name
            #print('to_save_faiss_path------------------------')
            #print(to_save_faiss_path)
            faiss.write_index(self.index, to_save_faiss_path)

        #print('向量数据处理完毕')

        for id, text, vector_id in self.vector_id_to_text:
            self.vectordb.create(id=id, text=text, vector_id=vector_id)

        #print('数据关联存入数据库完毕')

    def case_embedding(self, case_list):
        

        for case in case_list:
            reponse = self.zhipu_ai.zhipuai_request_vector(case[0])
            vector = reponse[1].data[0].embedding
            vector = np.array(vector).reshape(1, -1)
            self.index.add(vector)
            vector_id = self.index.ntotal - 1
            # print(case)
            self.vectordb.create_vector_case(vector_id=vector_id, case_needs=case[0], case_info=str(case[1]))
            faiss.write_index(self.index, "data/" + self.faiss_path_name)
