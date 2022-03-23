
from dbm import dumb
import os
from ibm_estimator import IBMEstimator

class VDD:
    def __init__(self) -> None:
        self.ibm_estimator = IBMEstimator()
        self.decoded = None
    
    def to_string(self):
        return "\n".join(self.decoded)
    
    def to_file(self, dest_path):
        outfile = open(dest_path, mode="w", encoding="latin-1")
        output = self.to_string()
        outfile.write(output)
        outfile.close()
       
    def decode_document(self, src_path):
        directory = ""
        infile = open(
            os.path.join(directory, src_path), "r", encoding="latin-1"
        )
        src_file_lst = infile.readlines()
        infile.close()
        
        translated_document = []
        for sentence in src_file_lst:
            
            sentence = sentence.strip()
            translated_sentence = self.translate_sentence(sentence)
            translated_document.append(translated_sentence)
        self.decoded = translated_document
        
        
    
    def translate_sentence(self, sentence):
        tokenized_sentence = VDD.tokenize(sentence)
        translated_sentence = []
        for word in tokenized_sentence:
            tranlated_word = self.ibm_estimator.translate(word)
            translated_sentence.append(tranlated_word)
            
        return " ".join(translated_sentence)
            
    def decode_sentence(self, sentence):
        self.decoded = list(self.translate_sentence(sentence))
    
    @staticmethod 
    def tokenize(string: str):
        return string.split(" ")
    
    @classmethod
    def from_file(cls, src_path, dest_path):
        vdd = cls()
        vdd.ibm_estimator = IBMEstimator.from_file(src_path, dest_path)
        return vdd
    
def main():
    ENGLISH_PATH = "../mt/english-senate-0.txt"
    FRENCH_PATH = "../mt/french-senate-0.txt"
    TEST_ENGLISH_PATH = "../mt/english-senate-2.txt"
    TEST_FRENCH_PATH = "../mt/french-senate-2.txt"
    
    new_estimator = IBMEstimator()
    new_estimator.taus = new_estimator.taus.from_json("taus.json")

    dumb_decoder = VDD()
    dumb_decoder.ibm_estimator = new_estimator
    dumb_decoder.decode_document(TEST_FRENCH_PATH)
    dumb_decoder.to_file("test2.txt")
    
if __name__ == "__main__":
    main()