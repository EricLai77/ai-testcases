import faiss
import numpy as np
from testcase_script.model import ZhiPu4
from testcase_script.vectordb import VectorDatabase
from testcase_script.config import loadConfig
import jieba, re
from collections import defaultdict

class SimilarSentenceSearch:
    def __init__(self, faiss_index_path):
        self.config = loadConfig()
        self.configs = self.config.load_config()
        self.host = self.configs['MYSQL_HOST']
        self.user = self.configs['MYSQL_USER']
        self.password = self.configs['MYSQL_PASSWORD']
        self.port = self.configs['MYSQL_PORT']
        self.db = self.configs['MYSQL_DATABASE']
        # loadong faiss index
        self.index = faiss.read_index(faiss_index_path)
        # set metric type
        self.index.metric_type = faiss.METRIC_INNER_PRODUCT
        # self.index.metric_type = faiss.METRIC_L2
        # connecting to vector database
        self.vectordb = VectorDatabase(self.host, self.user, self.password, self.port, self.db)
        self.zhipu_ai = ZhiPu4()

    def load_vector_id_to_text(self, vector_id_list):
        
        records = self.vectordb.query(vector_id_list)
        
        vector_id_to_text = {record['vector_id']: record['text'] for record in records}
        return vector_id_to_text

    def search(self, query_text, similarity_threshold):
        
        reponse = self.zhipu_ai.zhipuai_request_vector(query_text)
        query_vector = reponse[1].data[0].embedding
        query_vector = np.array(query_vector).reshape(1, -1)

        query_vector /= np.linalg.norm(query_vector)

        # searching in faiss index
        num_vectors = self.index.ntotal
        search_result = self.index.search(query_vector, num_vectors)  
        distances, indices = search_result

        # filtering results based on similarity threshold
        
        similar_ids = [idx for dist, idx in zip(distances[0], indices[0]) if dist > similarity_threshold]

        if not similar_ids:
            return None

        vector_id_to_text = self.load_vector_id_to_text(similar_ids)

        return vector_id_to_text
    
    @staticmethod
    def is_valid_phrase(phrase, min_length=2, max_length=10):
        # check phrase length
        if min_length <= len(phrase) <= max_length:
            # check phrase does not contain digits
            if not re.search(r'\d', phrase):
                # check phrase does not contain special characters
                if not re.search(r'[^\u4e00-\u9fa5]+', phrase):
                    return True
        return False
    
    def get_hot_phrases(self, n=4, top_n=None):
        # get all records from the database
        records = self.vectordb.query_all()
        if not records:
            return []

        # segment text into words using jieba
        words = []
        for record in records:
            words.extend(jieba.cut(record['text']))

        
        phrase_count = defaultdict(int)
        for i in range(len(words) - n + 1):
            phrase = ' '.join(words[i:i+n])
            phrase_count[phrase] += 1

        # sort phrases by their frequency in descending order
        sorted_phrase_count = sorted(phrase_count.items(), key=lambda x: x[1], reverse=True)

        # filter out phrases containing punctuation
        punctuation_pattern = re.compile(r'[.,;!?()""，。！？、：（）；“”]')
        filtered_phrases = [(punctuation_pattern.sub('', phrase), count) for phrase, count in sorted_phrase_count]

         # remove spaces in phrases
        sorted_phrase_count = [(phrase.replace(' ', ''), count) for phrase, count in filtered_phrases]

        # connect overlapping phrases
        merged_phrases = []
        prev_phrase = None
        for phrase, count in sorted_phrase_count:
            if prev_phrase and phrase.startswith(prev_phrase[:-1]):
                merged_phrases[-1] = (prev_phrase + phrase[-1], count)
            else:
                merged_phrases.append((phrase, count))
            prev_phrase = phrase

        # filter invalid phrases
        valid_phrases = [(phrase, count) for phrase, count in merged_phrases if SimilarSentenceSearch.is_valid_phrase(phrase)]

        if not top_n:
            return valid_phrases

        
        return valid_phrases[:top_n]

    def filter_words_by_frequency(self, word_list, threshold):
        """
        filter words by frequency threshold
        """
       
        filtered_words = [(word, count) for word, count in word_list if count >= threshold]
        return filtered_words

    def get_information_document(self):
        """
        extract all text information via ZHI PU AI  
        """

        records = self.vectordb.query_all()
        text_values = [record['text'] for record in records]
        
        return text_values
