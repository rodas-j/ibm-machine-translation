

import numbers
from vdd import VDD
FRENCH_PATH = "../mt/french-senate-2.txt"
EXPECTED_ENGLISH_PATH = "../mt/english-senate-2.txt"
NCD_ENGLISH_OUTPUT = "../mt/english-translation-ncd.txt"
VDD_ENGLISH_OUTPUT = "../mt/english-translation-vdd.txt"

class FScore():
    #TODO: Lower all the values
    def __init__(self) -> None:
        self.fscore = None
        self.expected_english_set = []
        self.tokenized_english_output = []
        self.expected_english_lst_tokenized = []
        self.count_expected = 0
        self.returned_res_count = 0
    
    @classmethod
    def from_decoded_document(cls, expected_english_path):
        object = cls()
        with open(expected_english_path, mode="r", encoding="latin-1") as fp:
            expected_english_lst = fp.readlines()
        for sentence in expected_english_lst:
            tokenized = VDD.tokenize(sentence)
            object.expected_english_set.append(set(tokenized))
            
        with open(expected_english_path, mode="r", encoding="latin-1") as fp:
            expected_english_lst = fp.readlines()
        for sentence in expected_english_lst:
            tokenized = VDD.tokenize(sentence)
            object.expected_english_lst_tokenized.append(tokenized)
        for sentence in expected_english_lst:
            tokenized = VDD.tokenize(sentence)
            object.expected_english_lst_tokenized.append(tokenized)
        
        
    @classmethod
    def from_file(cls, expected_english_path, english_output_path):
        object = cls()
        with open(expected_english_path, mode="r", encoding="latin-1") as fp:
            expected_english_lst = fp.readlines()
        with open(english_output_path, mode="r", encoding="latin-1") as fp:
            english_output_lst = fp.readlines()
        with open(expected_english_path, mode="r", encoding="latin-1") as fp:
            expected_english_lst = fp.readlines()
            
        for i in range(len(expected_english_lst)):
            expected_english_sentence = expected_english_lst[i]
            expected_english_sentence = expected_english_sentence.strip()
            tokenized = VDD.tokenize(expected_english_sentence)
            if len(tokenized) > 10:
                continue
            

            for _ in expected_english_sentence.split(" "):
                object.count_expected+=1
                    
                    
            
            object.expected_english_set.append(set(tokenized))
            object.expected_english_lst_tokenized.append(tokenized)
            english_output_sentence = english_output_lst[i]
            english_output_sentence = english_output_sentence.strip()
            
            for _ in english_output_sentence.split(" "):
                object.returned_res_count+=1
                    
            english_output_sentence = english_output_sentence.strip()
            tokenized_sentence = VDD.tokenize(english_output_sentence)
            object.tokenized_english_output.append(tokenized_sentence)

        
                    
        

        
        return object
        
    def calculate(self):
        numerator = (self.precision*self.recall)
        denominator = (self.precision+self.recall)
        self.fscore = 2 * numerator/denominator
        return self.fscore
        
    def set_precision(self, precision=None):
        if precision is not None:
            self.precision = precision
            return
        self.correct_res_count = 0
        assert len(self.tokenized_english_output) == len(self.expected_english_lst_tokenized), len(self.expected_english_lst_tokenized)
        for i in range(len(self.tokenized_english_output)):
            sentence = self.tokenized_english_output[i]
            for word in sentence:
                if word in self.expected_english_set[i]:
                    self.correct_res_count+=1
        count = sum( [ len(listElem) for listElem in self.tokenized_english_output])
        
        res = self.correct_res_count/self.returned_res_count
        # print("Correct Results:", self.correct_res_count)
        # print("Precision:", res)
        self.precision = res
    
    def set_recall(self, recall=None):
        if recall is not None:
            self.recall = recall
            return
        res = self.correct_res_count/self.count_expected
        self.recall = res
        
    
    def build(self):
        self.set_precision()
        self.set_recall()
        
    
    