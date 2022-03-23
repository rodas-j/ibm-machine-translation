
TRAINING_DATA_PATH = "../mt/english-senate-0.txt"


from itertools import islice
import os

from vdd import VDD
from ibm_estimator import IBMEstimator, Taus
from bigram import *


class NCD(VDD):
    def __init__(self) -> None:
        super().__init__()
        self.decoded = None
        self.ALPHA = 1.595977110540115
        self.BETA = 113
        self.ITERATIONS = 10
        self.START_PADDING = "*START*"
        self.END_PADDING = "*END*"
        self.ibm_estimator = None
        self.prev_word = self.START_PADDING
        self.THRESHOLD = 0.3
    
    @classmethod
    def from_file(cls, src_path, dest_path):
        ncd = cls()
        ncd.build(src_path, dest_path)
        
    
    def build(self, src_path, dest_path):
        self.eng_to_french_estimator = IBMEstimator.from_file(dest_path, src_path) # Because we get the reverse translation probabilities 
        self.french_to_eng_estimator = IBMEstimator.from_file(dest_path, src_path)
        self.eng_to_french_estimator.train()
        self.french_to_eng_estimator.train()
        self.build_bigram(dest_path)
        
        
    
    def build_bigram(self, dest_path):  
        directory = ""
        infile = open(
        os.path.join(directory, dest_path), "r", encoding="latin-1"
        )
        self.training_data_lst = infile.readlines()
        infile.close()
        self.padded_training_data_lst = add_padding_and_tokenize(self.training_data_lst)
        self.training_bigram_dictionary = create_bigram_dictionary(
        self.padded_training_data_lst
        )
        self.training_corpus_dictionary = make_dictionary(self.padded_training_data_lst)  
    
    def get_bigram(self, bigram_dictionary):
        bigram_likelihood = get_likelihood_bigram(
            self.training_corpus_dictionary,
            self.padded_training_data_lst,
            self.training_bigram_dictionary,
            bigram_dictionary,
            self.ALPHA,
            self.BETA,
        )
        return bigram_likelihood
    
    
    def translate_sentence(self, sentence):
        translated_sentence = []
        if type(sentence) != list:
            sentence = add_padding_and_tokenize([sentence])
        for word in sentence:
            if self.is_padding(word):
                if word == self.START_PADDING:
                    self.prev_word = self.START_PADDING
                continue 
            translated_word = self.translate(word)
            self.prev_word = word
            translated_sentence.append(translated_word)      
        return " ".join(translated_sentence)
    

        
    def translate(self, word):
        
        curr_log_max = float("-inf")
        curr_possible_translation = word #TODO: CHECK IF THIS AFFECTS WORDS THAT HAVE THE SAME TRANSLATION
        
        translated_word_dict = self.french_to_eng_estimator.taus.get_word_values(word)
        
        if not isinstance(translated_word_dict, dict):
            return word
        filtered_dict = Taus.cut_off(translated_word_dict, self.THRESHOLD)
        assert len(filtered_dict) != 0
        for curr_word in filtered_dict:
            
            
            curr_tau = translated_word_dict[curr_word]
            assert isinstance(self.prev_word, str)
            assert isinstance(curr_word, str)
            
            curr_bigram_dictionary = create_bigram_dictionary([self.prev_word, curr_word])
            curr_bigram = self.get_bigram(curr_bigram_dictionary) #NOTE: THIS IS LOG PROBABILITY
            
            french_translation = self.eng_to_french_estimator.translate(curr_word)
            french_translation_tau = self.eng_to_french_estimator.get_tau_from_pair((word, curr_word))
            
            assert curr_bigram != 0
            assert curr_tau != 0
            log_fre_tau = math.log(french_translation_tau)
            
            new_log_max = log_fre_tau + curr_bigram
            # print("New Log Max", new_log_max)
            # print("Current Word:", curr_word)
            # print("Prev Word:", self.prev_word)
            # print("Curr Tau:", curr_tau)
            # print("Curr Bigram:", curr_bigram)
            # print("Log Tau", log_fre_tau)
            if curr_log_max < new_log_max:
                # print("Max Log Changed")
                curr_log_max = new_log_max
                curr_possible_translation = curr_word
            # print()   
         
        return curr_possible_translation
            
        
    def decode_document(self, src_path):
        directory = ""
        infile = open(
            os.path.join(directory, src_path), "r", encoding="latin-1"
        )
        src_file_lst = infile.readlines()
        infile.close()
        
        translated_document = []
        src_file_lst_tokenized = NCD.tokenize_to_lst(src_file_lst)
        
        for sentence in src_file_lst_tokenized:
            translated_sentence = self.translate_sentence(sentence)
            translated_document.append(translated_sentence)
        self.decoded = translated_document
            
    def is_padding(self, word):
        return word.strip() in (self.START_PADDING, self.END_PADDING)
    
    @staticmethod
    def tokenize_to_lst(lines):
        res = []
        for sentence in lines:
            tokenized_sentence = add_padding_and_tokenize([sentence])
            res.append(tokenized_sentence)
            
        return res
        
        
    
                
             
            
                

                
            
        
        
        
        