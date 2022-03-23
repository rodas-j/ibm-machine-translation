from itertools import combinations
import sys
from unittest import TestCase
import unittest
sys.path.append("..")
from ibm_estimator import *
import pandas as pd


ENGLISH_PATH = "../../mt/english-senate-0.txt"
FRENCH_PATH = "../../mt/french-senate-0.txt"

english_path = "test_data/test_english-senate-0.txt"
french_path = "test_data/test_french-senate-0.txt"
french_sentence = "Elle mange du pain"
english_sentence = "She eats bread"
sentence_taus = {
                            "mange":{
                                "She": 1,
                                "eats": 1,
                                "bread": 1
                                
                                    
                            },
                            "elle": {
                                "She": 1,
                                "eats": 1,
                                "bread": 1,
                            },
                            "du": {
                                "She": 1,
                                "eats": 1,
                                "bread": 1,
                            },
                            "pain": {
                                "She": 1,
                                "eats": 1,
                                "bread": 1,
                            }
                            
                        }

class TestIBMEstimator(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestIBMEstimator, self).__init__(*args, **kwargs)
    
    @classmethod
    def setUp(self):
        self.sentence_pair = SentencePair.from_sentences(french_sentence, english_sentence)
        self.ibm_estimator = IBMEstimator()
        
        
    def test_get_all_possible_alignments(self):
        expected = [('a', 1), ('a', 2), ('a', 3), ('a', 4), ('b', 1), ('b', 2), ('b', 3), ('b', 4)]
        lst1 = ['a', 'b']
        lst2 = [1, 2, 3, 4]
        combinations = IBMEstimator.get_all_possible_alignments(lst1, lst2)
        self.assertCountEqual(combinations, expected)
    
    def test_from_file(self):
        ibm_estimator = IBMEstimator.from_file(french_path, english_path)
        sentence_pair_lst = ibm_estimator.sentence_pair_lst
        expected_pair_count = 5000
        self.assertEqual(expected_pair_count, len(sentence_pair_lst))
        
    def test_get_probability(self):
        word = "mange"
        expected = 3
        self.ibm_estimator.taus.taus = sentence_taus
        probability = self.ibm_estimator.get_probability(word, self.sentence_pair)
        self.assertEqual(probability, expected)
        
    def test_one_sentence_pair_buid(self):
 
        self.ibm_estimator.sentence_pair_lst = [self.sentence_pair]
        self.ibm_estimator.build()
        pair = ("eats", "mange")
        expected_n_value = 1/3
        actual_n_value = self.ibm_estimator.n_values.get_n_value_from_pair(pair)
        self.assertEqual(expected_n_value, actual_n_value)
        
        
        
    def test_two_sentence_pair_buid(self):
        mock_french_sentence = "Il mange du boef"
        mock_english_sentence = "He eats beef"
        mock_sentence_pair = SentencePair.from_sentences(mock_french_sentence, mock_english_sentence)
        two_sentence_pair_lst = [self.sentence_pair, mock_sentence_pair]
        self.ibm_estimator = IBMEstimator()
        self.ibm_estimator.sentence_pair_lst = two_sentence_pair_lst
        self.ibm_estimator.build()
        

        expected = {'Elle': {'She': 0.25, 'eats': 0.125, 'bread': 0.25}, 'mange': {'She': 0.25, 'eats': 0.25, 'bread': 0.25, 'He': 0.25, 'beef': 0.25}, 'du': {'She': 0.25, 'eats': 0.25, 'bread': 0.25, 'He': 0.25, 'beef': 0.25}, 'pain': {'She': 0.25, 'eats': 0.125, 'bread': 0.25}, 'Il': {'He': 0.25, 'eats': 0.125, 'beef': 0.25}, 'boef': {'He': 0.25, 'eats': 0.125, 'beef': 0.25}}  
        actual = self.ibm_estimator.get_taus().to_dict()
        
        
        self.assertEqual(expected, actual)
        
        expected = {'She': {'Elle': 0.3333333333333333, 'mange': 0.3333333333333333, 'du': 0.3333333333333333, 'pain': 0.3333333333333333}, 'eats': {'Elle': 0.3333333333333333, 'mange': 0.6666666666666666, 'du': 0.6666666666666666, 'pain': 0.3333333333333333, 'Il': 0.3333333333333333, 'boef': 0.3333333333333333}, 'bread': {'Elle': 0.3333333333333333, 'mange': 0.3333333333333333, 'du': 0.3333333333333333, 'pain': 0.3333333333333333}, 'He': {'Il': 0.3333333333333333, 'mange': 0.3333333333333333, 'du': 0.3333333333333333, 'boef': 0.3333333333333333}, 'beef': {'Il': 0.3333333333333333, 'mange': 0.3333333333333333, 'du': 0.3333333333333333, 'boef': 0.3333333333333333}}
        actual = self.ibm_estimator.get_n_values().to_dict()
        # df = pd.DataFrame.from_dict(actual)
        # print(df.T)
        self.assertEqual(expected, actual)
           
        
            
    def test_iterate(self):
        mock_french_sentence = "Il mange du boef"
        mock_english_sentence = "He eats beef"
        mock_sentence_pair = SentencePair.from_sentences(mock_french_sentence, mock_english_sentence)
        two_sentence_pair_lst = [self.sentence_pair, mock_sentence_pair]
        self.ibm_estimator = IBMEstimator()
        self.ibm_estimator.sentence_pair_lst = two_sentence_pair_lst
        
        self.ibm_estimator.train(2)
        
        actual = self.ibm_estimator.get_n_values().to_dict()
        expected = {'She': {'Elle': 0.4, 'mange': 0.3333333333333333, 'du': 0.3333333333333333, 'pain': 0.4}, 'eats': {'Elle': 0.2, 'mange': 0.6666666666666666, 'du': 0.6666666666666666, 'pain': 0.2, 'Il': 0.2, 'boef': 0.2}, 'bread': {'Elle': 0.4, 'mange': 0.3333333333333333, 'du': 0.3333333333333333, 'pain': 0.4}, 'He': {'Il': 0.4, 'mange': 0.3333333333333333, 'du': 0.3333333333333333, 'boef': 0.4}, 'beef': {'Il': 0.4, 'mange': 0.3333333333333333, 'du': 0.3333333333333333, 'boef': 0.4}}
        
        
        self.assertEqual(actual, expected)
        
        actual = self.ibm_estimator.get_taus().to_dict()
        expected = {'Elle': {'She': 0.2727272727272727, 'eats': 0.09375, 'bread': 0.2727272727272727}, 'mange': {'She': 0.22727272727272724, 'eats': 0.3125, 'bread': 0.22727272727272724, 'He': 0.22727272727272724, 'beef': 0.22727272727272724}, 'du': {'She': 0.22727272727272724, 'eats': 0.3125, 'bread': 0.22727272727272724, 'He': 0.22727272727272724, 'beef': 0.22727272727272724}, 'pain': {'She': 0.2727272727272727, 'eats': 0.09375, 'bread': 0.2727272727272727}, 'Il': {'He': 0.2727272727272727, 'eats': 0.09375, 'beef': 0.2727272727272727}, 'boef': {'He': 0.2727272727272727, 'eats': 0.09375, 'beef': 0.2727272727272727}}
        
        self.assertEqual(actual, expected)

    def test_train_with_files(self):
        mock_estimator = IBMEstimator.from_file(FRENCH_PATH, ENGLISH_PATH)
        mock_estimator.train(3)
        translated_word = mock_estimator.translate("débats")
        expected = "debates"
        self.assertEqual(expected, translated_word)  
        
    def test_to_json(self):
        mock_estimator = IBMEstimator.from_file(FRENCH_PATH, ENGLISH_PATH)
        mock_estimator.train(3)
        expected = "debates"
        mock_estimator.taus.to_json("test_model/french_to_english.json")
        new_ibm_estimator = IBMEstimator.from_json("test_model/french_to_english.json")
        actual = new_ibm_estimator.translate("débats")
        self.assertEqual(expected, actual)
        
        
        

    
class TestSentencePair(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestSentencePair, self).__init__(*args, **kwargs)
        
    @classmethod
    def setUpClass(self):
        self.sentence_pair = SentencePair.from_sentences(french_sentence, english_sentence)
        
    def test_from_file(self):
        sentence_pair_lst = SentencePair.from_file(english_path, french_path)
        expected_pair_count = 5000
        self.assertEqual(expected_pair_count, len(sentence_pair_lst))    
        
    def test_from_sentences(self):
        self.assertEqual(self.sentence_pair.src_sentence, french_sentence)
        self.assertEqual(self.sentence_pair.dest_sentence, english_sentence)
    
    def test_tokenize(self):
        expected_token_count = 3
        actual_token_count = len(SentencePair.tokenize(english_sentence))
        self.assertEqual(actual_token_count, expected_token_count)
       
    def test_get_probability_pairs(self):
        # TODO: THERE'S A LOGIC ERROR IN THIS FUNCTION
        word = "mange"
        probability_pairs = self.sentence_pair.get_probability_pairs(word)
        expected_output = [("mange", "She"), ("mange", "eats"), ("mange", "bread")]
        # self.assertCountEqual(expected_output, probability_pairs)
    # TODO: WRITE TESTS FOR THE STATIC METHODS
    
    
class TestTaus(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestTaus, self).__init__(*args, **kwargs)
    
    @classmethod
    def setUpClass(self):
        self.taus = Taus()
        self.mock_taus = {
                            "mange":{
                                "She": 2,
                                "eats": 2,
                                "bread": 2
                                
                                    
                            },
                            "elle": {
                                "She": 2,
                                "eats": 2,
                                "bread": 2,
                            },
                            "du": {
                                "She": 2,
                                "eats": 2,
                                "bread": 2,
                            },
                            "pain": {
                                "She": 2,
                                "eats": 2,
                                "bread": 2,
                            }
                            
                        }
        
        self.taus.taus = self.mock_taus
        self.mock_pairs = [("She", "mange"), ("eats", "mange"), ("bread", "mange")]
        
        
    def test_get_tau_from_pair(self):
        #NOTE: WHEN IT'S EMPTY IT SHOULD BE AN EMPTY DICTIONARY
        
        for i in range(len(self.mock_pairs)):
            pair = self.mock_pairs[i]
            actual = self.taus.get_tau_from_pair(pair)
            self.assertEqual(2, actual)
            
    def test_set_tau_from_pair(self):
        new_tau = 5
        pair = ("She", "mange")
        self.taus.set_tau_from_pair(pair, new_tau)
        actual = self.taus.get_tau_from_pair(pair)
        self.assertEqual(actual, new_tau)
    
    def reset_taus(self, num=1):
        for f in self.taus.taus:
            for e in self.taus.taus[f]:
               self.taus.taus[f][e] = num
               
    def test_to_json_from_json(self):
        tau_path = "test_data/taus.json"
        self.taus.to_json(tau_path)
        test_taus = Taus.from_json(tau_path)
        self.assertEqual(test_taus.to_dict(), self.taus.to_dict())
               
    
        
class TestNValues(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestNValues, self).__init__(*args, **kwargs)
    
    @classmethod        
    def setUp(self):
        self.test_n_values = NValues()
        self.test_n_values.n_values = {
                "She":{
                    "mange":1.0,
                    "elle":1.0,
                    "du":4.0,
                    "pain":6.0
                },
                "eats":{
                    "mange":6.0,
                    "elle":1.0,
                    "du":1.0,
                    "pain":1.0
                },
                "bread":{
                    "mange":1.0,
                    "elle":1.0,
                    "du":1.0,
                    "pain":1.0
                }
        }
        
    def test_add_to_n_values_from_pair(self):
        self.test_n_values.n_values  = {}
        eng_lst = ["She", "eats", "bread"]
        for eng in eng_lst:
            pair_lst = [(eng, "mange"), (eng, "elle"), (eng, "du"), (eng, "pain")]
            new_n_v = 1/3
            for pair in pair_lst:
                self.test_n_values.add_to_n_values_from_pair(pair, new_n_v)
        
        for eng in eng_lst:
            pair_lst = [(eng, "mange"), (eng, "elle"), (eng, "du"), (eng, "pain")]
            new_n_v = 2/3
            for pair in pair_lst:
                self.test_n_values.add_to_n_values_from_pair(pair, new_n_v)
                
        result = {
                "She":{
                    "mange":1.0,
                    "elle":1.0,
                    "du":1.0,
                    "pain":1.0
                },
                "eats":{
                    "mange":1.0,
                    "elle":1.0,
                    "du":1.0,
                    "pain":1.0
                },
                "bread":{
                    "mange":1.0,
                    "elle":1.0,
                    "du":1.0,
                    "pain":1.0
                }
        }
        self.assertEqual(result, self.test_n_values.to_dict())
        
    def test_get_n_value_from_pair(self):
        test_pair = ("eats", "mange")
        actual = self.test_n_values.get_n_value_from_pair(test_pair)
        expected = 6.0
        self.assertEqual(actual, expected)
        
    
    def test_get_n_word_align_everything(self):
        self.test_n_values.n_values  = {}
        eng_lst = ["She", "eats", "bread"]
        for eng in eng_lst:
            pair_lst = [(eng, "mange"), (eng, "elle"), (eng, "du"), (eng, "pain")]
            new_n_v = 1/3
            for pair in pair_lst:
                self.test_n_values.add_to_n_values_from_pair(pair, new_n_v)
        
        test_word = "eats"
        actual = self.test_n_values.get_n_word_align_everything(test_word)
        expected = 4/3
        self.assertEqual(expected, actual)
        
        
if __name__ == "__main__":
    unittest.main()