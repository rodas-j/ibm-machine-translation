from unittest import TestCase
import sys
import unittest
sys.path.append("..")
from ibm_estimator import IBMEstimator
from vdd import VDD

FRENCH_ENGLISH_MODEL = "../model/french_to_english.json"
ENGLISH_TRAINING_DATA = "../../mt/english-senate-0.txt"
FRENCH_TRAINING_DATA = "../../mt/french-senate-0.txt"
FRENCH_FILE_PATH = "test_data/french-senate-2.txt"

class TESTVDD(TestCase):
    def __init__(self, *args, **kwargs):
        super(TESTVDD, self).__init__(*args, **kwargs)
    
    @classmethod
    def setUpClass(self):
        with open(FRENCH_TRAINING_DATA, mode="r", encoding="latin-1") as fp:
            self.french_data_lst = fp.readlines()
        self.ibm_estimator = IBMEstimator.from_json(FRENCH_ENGLISH_MODEL)
        
    
    @classmethod 
    def setUp(self):
        self.dumb_estimator = VDD()
        self.dumb_estimator.ibm_estimator = self.ibm_estimator
        
        
    def test_translate_sentence(self):
        TEST_SENTENCE = self.french_data_lst[0]
        expected = "debates de M. Senate ( Hansard ) \n"
        translated = self.dumb_estimator.translate_sentence(TEST_SENTENCE)
        self.assertEqual(expected, translated)
        
    def test_decode_document(self):
        self.dumb_estimator.decode_document(FRENCH_FILE_PATH)
        self.dumb_estimator.to_file("test.txt")
        
        
if __name__ == "__main__":
    unittest.main()