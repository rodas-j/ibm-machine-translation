from unittest import TestCase
import sys
import unittest
sys.path.append("..")
from fscore import FScore

FRENCH_PATH = "../../mt/french-senate-2.txt"
EXPECTED_ENGLISH_PATH = "../../mt/english-senate-2.txt"
NCD_ENGLISH_OUTPUT = "../../mt/english-translation-ncd.txt"
VDD_ENGLISH_OUTPUT = "../../mt/english-translation-vdd.txt"

class TestFScore(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestFScore, self).__init__(*args, **kwargs)
        
    @classmethod
    def setUp(self):
        # self.fscore = FScore.from_file(EXPECTED_ENGLISH_PATH, NCD_ENGLISH_OUTPUT)
        # self.fscore.build()
        pass
        
    def test_fscore_from_file(self):
        self.fscore = FScore.from_file(EXPECTED_ENGLISH_PATH, NCD_ENGLISH_OUTPUT)
        self.fscore.build()
        actual= self.fscore.calculate()
        expected = 0.6569471736986399
        # self.assertEqual(expected, actual)
    
    def test_calculate(self):
        self.fscore.set_precision(4)
        self.fscore.set_recall(4)
        self.fscore.calculate()
        self.assertEqual(self.fscore.fscore, 4)
        
        self.fscore.set_precision(7)
        self.fscore.set_recall(6)
        self.fscore.calculate()
        self.assertAlmostEqual(self.fscore.fscore, 6.461538461538462)
    
    def test_fscore_small_data(self):
        VDD_PATH = "test_data/fscore_data/vdd.txt"
        NCD_PATH = "test_data/fscore_data/ncd.txt"
        EXPECTED_PATH = "test_data/fscore_data/expected.txt"
        fscore = FScore.from_file(EXPECTED_PATH, VDD_PATH)
        fscore.build()
        vdd = fscore.calculate()
        print("VDD:", vdd)
        print("Precision:", fscore.precision)
        print("returned count:", fscore.returned_res_count)
        print("Recall:", fscore.recall)
        print()
        fscore = FScore.from_file(EXPECTED_PATH, NCD_PATH)
        fscore.build()
        ncd = fscore.calculate()
        
        print("NCD:", ncd)
        print("Precision:", fscore.precision)
        print("Recall:", fscore.recall)
        self.assertEqual(ncd, 0.625)
        self.assertEqual(vdd, 0.5)
        self.assertEqual(fscore.count_expected, 8)
        
        
    def test_perfect_model(self):
        path = "test_data/fscore-test.txt"
        fscore = FScore.from_file(EXPECTED_ENGLISH_PATH, EXPECTED_ENGLISH_PATH)
        fscore.build()
        print("Precision:", fscore.precision)
        print("Returned Count:", fscore.returned_res_count)
        print("Test Corpus Token", fscore.count_expected)
        print("Correct Count:", fscore.correct_res_count)
        print("Recall:", fscore.recall)
        print("Token Count", fscore.count_expected)
        print(fscore.correct_res_count)
        actual = fscore.calculate()
        expected = 1
        self.assertEqual(expected, actual)
        
        
    def test_number_of_expected_tokens(self):
        with open(EXPECTED_ENGLISH_PATH, encoding="latin-1") as fp:
            token_count = fp.read()
            token_count = len(token_count.split(" "))
        self.assertEqual(token_count, 477712)
        
    

if __name__ == "__main__":
    unittest.main()