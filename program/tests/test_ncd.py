import time
from unittest import TestCase
import sys
import unittest


sys.path.append("..")
from ibm_estimator import IBMEstimator
from ncd import NCD
from vdd import VDD
from bigram import add_padding_and_tokenize


FRENCH_ENGLISH_MODEL = "../model/french_to_english.json"
ENGLISH_TRAINING_DATA = "../../mt/english-senate-0.txt"
FRENCH_TRAINING_DATA = "../../mt/french-senate-0.txt"
FRENCH_FILE_PATH = "test_data/french-senate-2.txt"
ENGLISH_FRENCH_MODEL = "../model/english_to_french.json"
FRENCH_TEST = "../../mt/french-senate-2.txt"

class TESTNCD(TestCase):
    def __init__(self, *args, **kwargs):
        super(TESTNCD, self).__init__(*args, **kwargs)
        
    @classmethod
    def setUpClass(self):
        with open(FRENCH_TRAINING_DATA, encoding="latin-1") as fp:
            self.french_data_lst = fp.readlines()
        self.eng_to_fre = IBMEstimator.from_json(ENGLISH_FRENCH_MODEL)
        self.fre_to_eng = IBMEstimator.from_json(FRENCH_ENGLISH_MODEL)
        self.noisy_decoder = NCD()
        self.dumb_decoder = VDD()
        self.dumb_decoder.ibm_estimator = self.fre_to_eng
        self.noisy_decoder.build_bigram(ENGLISH_TRAINING_DATA)
        with open(FRENCH_TEST, encoding="latin-1") as fp:
            self.french_test_data = fp.readlines()
        
    @classmethod 
    def setUp(self):
        self.noisy_decoder.eng_to_french_estimator = self.eng_to_fre
        self.noisy_decoder.french_to_eng_estimator = self.fre_to_eng
        
    def test_build_bigram(self):
        self.noisy_decoder.build_bigram(ENGLISH_TRAINING_DATA)
    
    def test_translate_word(self):
        test_word = "débats"
        expected = "debates"
        actual = self.noisy_decoder.translate(test_word)
        self.assertEqual(expected, actual)
        
    def test_translate_sentence(self):
        TRAINING_SENTENCE = self.french_data_lst[5]
        TEST_SENTENCE = self.french_test_data[358]
        expected = 'table of des Contents'
        
        translated = self.noisy_decoder.translate_sentence(TEST_SENTENCE)
        print(repr(translated))
        print(repr(TEST_SENTENCE))
        self.assertEqual(expected, translated)
        
    def test_decode_time_complexity(self):
        start_time = time.time()
        for i in range(len(self.french_data_lst)):
            if i == 100:
                break
            self.noisy_decoder.translate_sentence(self.french_data_lst[i])
        end_time = time.time()
        elapsed = end_time-start_time
        expected = 1.9652535915374756
        self.assertAlmostEqual(expected, elapsed,delta=5)
        
    def test_decode_document(self):
        SHORT_FRENCH_PATH = "test_data/test_french-senate-2.txt"
        self.noisy_decoder.decode_document(SHORT_FRENCH_PATH) 
        
    def test_is_padding(self):
        self.assertTrue(self.noisy_decoder.is_padding("*END*"))   
        
        
if __name__ == "__main__":
    unittest.main()
