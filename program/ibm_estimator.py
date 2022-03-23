

import heapq
import os
from pyclbr import Class
from typing import List
import json

ENGLISH_PATH = "../mt/english-senate-0.txt"
FRENCH_PATH = "../mt/french-senate-0.txt"

class NValues:
    def __init__(self) -> None:
        self.n_values = {}
        self.n_sums = {}
        
    def reset(self):
        self.n_sums = {}
        self.n_values = {}
    
    
    def to_dict(self):
        return self.n_values
    
    
    def get_n_word_align_everything(self, word):
        return self.n_sums[word]
    
    def get_n_value_from_pair(self, pair):
        first = pair[1]
        second = pair[0]
        
        if second in self.n_values:
            nested_dic = self.n_values[second]
            if (isinstance(nested_dic, dict)):
                if first in self.n_values[second]:
                    res = self.n_values[second][first]
                    return res
        return 0
    
    def add_to_n_values_from_pair(self, pair, new_n_v):
        first = pair[1]
        second = pair[0]
        if (second in self.n_values):
            if first in self.n_values[second]:
                self.n_values[second][first] += new_n_v
            else:
                self.n_values[second][first] = new_n_v
            self.n_sums[second] += new_n_v
        else:
            self.n_values[second] = {}
            self.n_values[second][first] = new_n_v
            self.n_sums[second] = new_n_v

class Taus:
    def __init__(self, default_tau: int = 1) -> None:
        self.taus =  {}       
        self.default_tau = default_tau
    
    def get_word_values(self, word) -> dict:
        word_dict = self.taus.get(word)
        return word_dict
    @staticmethod
    def cut_off(word_dict, threshold):
        new = {}

        new = dict(filter(lambda elem: elem[1] > threshold, word_dict.items()))
        if len(new) == 0:
            word_value_lst = heapq.nlargest(30, word_dict, word_dict.get)
            for word in word_value_lst:
                new[word] = word_dict[word]
        return new
    
    def to_dict(self):
        return self.taus
    
    def to_json(self, path):
        with open(path, 'w', encoding="latin-1") as fp:
            json.dump(self.taus, fp)
    
    @classmethod
    def from_json(cls, path):
        with open(path, 'r', encoding="latin-1") as fp:
            data = json.load(fp)
            taus = cls()
            taus.taus = data
        return taus 
    
    def get_tau_from_pair(self, pair: tuple) -> int:
        """This function returns the tau that we want from the dictionary of all
        taus.

        Args:
            pair (tuple): _description_
            dictionary (dict): _description_

        Returns:
            int: _description_
        """
        first = pair[0]
        second = pair[1]
        
        if second in self.taus:
            nested_dic = self.taus[second]
            if (isinstance(nested_dic, dict)):
                if first in self.taus[second]:
                    res = self.taus[second][first]
                    return res
                else:
                    self.taus[second][first] =  self.default_tau
                    res =  self.default_tau
                    return res
                    
            else:
                self.taus[second][first] =  self.default_tau
                res =  self.default_tau
                return res
            
        else:
            self.taus[second] = {}
            self.taus[second][first] = self.default_tau
            res = self.default_tau
            return res
        
    
    def set_tau_from_pair(self, pair: tuple, new_tau: int):
        first = pair[0]
        second = pair[1]
        res = self.taus[second]
        if (isinstance(res, dict)):
            res[first] = new_tau
        else:
            raise Exception("There's an empty french tau. {mange:{}}")
            
    def get_word_align_everything(self, word):
        res = 0
        for french_word in self.taus:
            french_word_dict = self.taus[french_word]
            if word in french_word_dict:
                word_tau = french_word_dict[word]
                sum_of_all_taus = sum(french_word_dict.values())
                res+= word_tau / sum_of_all_taus
        return res 
    
class SentencePair:    
    def __init__(self, src: str, dest: str) -> None:
        self.src_sentence = src
        self.tokenized_src = self.tokenize(self.src_sentence)
        self.dest_sentence = dest
        self.tokenized_dest = self.tokenize(self.dest_sentence)
    
    @classmethod
    def from_sentences(cls, src_sentence: str, dest_sentence: str)-> Class:
        sentence_pair = cls(src_sentence, dest_sentence)
        return sentence_pair
         
    @classmethod
    def from_file(cls, src_path: str, dest_path: str)-> List[Class]:
        directory = ""
        
        infile = open(
            os.path.join(directory, src_path), "r", encoding="latin-1"
        )
        src_file_lst = infile.readlines()
        infile.close()
        infile = open(
            os.path.join(directory, dest_path), "r", encoding="latin-1"
        )
        dest_file_lst = infile.readlines()
        infile.close()
        print("Files Loaded")
        
        sentence_pair_lst = []
        for i in range(len(src_file_lst)):
            sentence_pair = cls(src_file_lst[i], dest_file_lst[i])
            sentence_pair_lst.append(sentence_pair)
            
        return sentence_pair_lst

    @staticmethod
    def tokenize(string: str) -> List[str]:
        return string.split(" ")
    
    
    def get_n_value(self, pair: tuple) -> int:
        if len(self.n_values) == 0:
            raise Exception("The entire n_values dictionary is empty. No structure has been built yet.")
        if pair in self.n_values:
            return self.n_values[pair]
        else:
            return 0
        
    
    def get_probability_pairs(self, word: str) -> list:
        #TODO: FIX THE ISSUE HERE. CHECK UNITTEST FOR MORE INFO.
        if word not in self.tokenized_src:
            raise Exception("The word you are trying to get probabilty of doesn't exist in the source sentence.")
        output = []
        for complement in self.tokenized_dest:
            output.append((word, complement))
        return output
    
    @staticmethod
    def add_all_n_values(pair: tuple, sentence_pair_lst) -> int:
        
        n_sum = 0
        for sentence_pair in sentence_pair_lst:
            n_sum+=sentence_pair.get_n_value(pair)
        return n_sum
        

        

class IBMEstimator:
    def __init__(self, tau_assumption = 1) -> None:
        self.TAU_ASSUMPTION = tau_assumption
        self.taus = Taus(tau_assumption)
        self.n_values = NValues()
        
        
    def get_taus(self):
        return self.taus
    
    def get_n_values(self):
        return self.n_values

    def get_tau_from_pair(self, pair: tuple) -> int:
        """This function returns the tau that we want from the dictionary of all
        taus.

        Args:
            pair (tuple): _description_
            dictionary (dict): _description_

        Returns:
            int: _description_
        """
        res = self.taus.get_tau_from_pair(pair)
        return res
    
    def set_tau_from_pair(self, pair: tuple, new_tau) -> None:
        self.taus.set_tau_from_pair(pair, new_tau)

    def get_probability(self, french_word: str, sentence_pair: SentencePair) -> int:
        probability = 0
        dest_lst = sentence_pair.tokenized_dest
        for english_word in dest_lst:
            current_tau =  self.get_tau_from_pair((english_word, french_word))
            probability = probability + current_tau
        return probability
    
    @staticmethod  
    def get_all_possible_alignments(lst1: List[str], lst2: List[str]):
        combinations = []
        for word1 in lst1:
            for word2 in lst2:
                combinations.append((word1, word2))
        return combinations
    
    def get_alignment_pair_lst(self, sentence_pair_lst):
        alignment_pair_lst = []
        for i in range(len(sentence_pair_lst)):
            sentence_pair = sentence_pair_lst[i]
            tokenized_src = sentence_pair.tokenized_src
            tokenized_dest  = sentence_pair.tokenized_dest
        
            alignment_pairs = self.get_all_possible_alignments(tokenized_dest, tokenized_src)
            alignment_pair_lst.append(alignment_pairs)
        return alignment_pair_lst
    
    @classmethod
    def from_file(cls, src_path: str, dest_path: str):
        ibm_estimator = cls()
        ibm_estimator.sentence_pair_lst = SentencePair.from_file(src_path, dest_path)
        return ibm_estimator 
    
    @classmethod
    def from_json(cls, path):
        ibm_estimator = cls()
        ibm_estimator.taus = Taus.from_json(path) 
        return ibm_estimator
        
    
    def get_word_align_everything(self, word: str):
        return self.n_values.get_n_word_align_everything(word)
        
    
    def train(self, turns=10):
        for i in range(turns):
            print(f":Iteration {i+1} out of {turns}")
            self.n_values.reset()
            self.build()
             
    
    def build(self):
        for i in range(len(self.sentence_pair_lst)):
            sentence_pair = self.sentence_pair_lst[i]
            probability_dictionary = {}
            for src_word in sentence_pair.tokenized_src:
                if src_word not in probability_dictionary:
                    probability = self.get_probability(src_word, sentence_pair)
                    probability_dictionary[src_word] = probability
            
            
            for f in sentence_pair.tokenized_src:
                for e in sentence_pair.tokenized_dest:
                    pair = (e, f)
                    current_tau = self.get_tau_from_pair(pair) #NOTE: IF IT'S EMPTY IT SHOULD RETURN THE DEFAULT TAU VALUE.
                    probability = probability_dictionary.get(f) 
                    self.n_values.add_to_n_values_from_pair(pair, current_tau/probability)
                    
           
        for i in range(len(self.sentence_pair_lst)):
            sentence_pair = self.sentence_pair_lst[i]   

            for f in sentence_pair.tokenized_src:
                for e in sentence_pair.tokenized_dest:
                    pair = (e, f)
                    sum_n_values = self.n_values.get_n_value_from_pair(pair) # TODO: This might be a bottleneck. Maybe if you store all the sums of all the pairs
                    new_tau = sum_n_values/ self.n_values.get_n_word_align_everything(e) # TODO: Check if we need to do log here.
                    self.set_tau_from_pair(pair, new_tau)  
      
        
        
    def translate(self, word):
        translated_dict = self.taus.get_word_values(word) 
        try:
            translated_word = max(translated_dict, key=translated_dict.get)
        except:
            return word
        return translated_word
            



def main():
    ibm_estimator = IBMEstimator.from_file(FRENCH_PATH, ENGLISH_PATH)
    ibm_estimator.train()
    ibm_estimator.taus.to_json("french_to_english.json")
    # words = ["important", "honorable", "nomination", "talent", "criminel"]
    # for word in words:
    #     translated_word = ibm_estimator.translate(word)
    #     print("Original Word: ", word)
    #     print("Translated Word: ", translated_word)
    #     print()
    
    
if __name__ == "__main__":
    main()
    