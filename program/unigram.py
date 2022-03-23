
import os
import math
from typing import List


def get_token_count(dictionary):
    return sum(dictionary.values())


def get_likelihood(test_dictionary, training_dictionary, token_count, alpha):
    """This function is a unigram language model as a distribution over
        documents

        Args:
            dictionary (dict): a dictionary containing all the types and

        Returns:
            (int):

    5.2918617392170534e-05
    0.06387069595245211
    """
    log_likelihood = 0
    for word in test_dictionary:

        theta = get_theta(word, training_dictionary, token_count, alpha)
        # if (theta == 0)
        log_theta = math.log(theta, 10) * test_dictionary[word]

        log_likelihood = log_likelihood + log_theta

    return log_likelihood


def get_theta(word, training_dictionary, token_count, alpha):
    """This functions like a unigram model dictionary that is trained by the
    training data. It's as if we are getting the value of a key from the
    dictionary representing a model. It follows the exact formula for theta on
    the writeup.

    Args:
        word (str): the word for which we are calculating theta.
        training_dictionary (dict[str: int]): this is all the words in the
        training corpus and their respective frequency.
        token_count (int): all the tokens in the training corpus.
        alpha (int): the value for alpha

    Returns:
        int: the respective theta for the word.
    """
    # Because when word doesn't exist in training dictionary, we get a key
    # error.
    if word not in training_dictionary:
        return (0 + alpha) / (token_count + alpha * len(training_dictionary))

    theta = (training_dictionary[word] + alpha) / (
        token_count + alpha * len(training_dictionary)
    )

    return theta


def gss(f, a, b, tol, development_dictionary, training_dictionary):
    """
    Golden-section search
    to find the maximum of f on [a,b]
    f: a strictly unimodal function on [a,b]

    Example:
    >>> f = lambda x: (x-2)**2
    >>> x = gss(f, 1, 5)
    >>> print("%.15f" % x)
    2.000009644875678
    """
    gr = (math.sqrt(5) + 1) / 2

    c = b - (b - a) / gr
    d = a + (b - a) / gr
    while abs(b - a) > tol:
        if f(
            development_dictionary,
            training_dictionary,
            get_token_count(training_dictionary),
            c,
        ) > f(
            development_dictionary,
            training_dictionary,
            get_token_count(training_dictionary),
            d,
        ):
            b = d
        else:
            a = c

        # We recompute both c and d here to avoid loss of precision
        # which may lead to incorrect results or infinite loop
        c = b - (b - a) / gr
        d = a + (b - a) / gr

    return (b + a) / 2


def make_dictionary(lst_of_words):
    """
    Args:
        lst_of_words (list): a list of words in text.

    Returns:
        dict: a dictionary with the word as the key and the freq. as
        the value.
    """
    dict = {}
    for word in lst_of_words:
        if word in dict:
            dict[word] += 1
        else:
            dict[word] = 1
    return dict


def main():

    ##creating the three text files###
    directory = "langmod/hansard/"
    files = os.listdir(directory)
    infile = open(
        os.path.join(directory, "english-senate-0.txt"), "r", encoding="latin1"
    )
    training_data = infile.read()
    training_data_lst = training_data.split(" ")
    infile.close()

    infile = open(
        os.path.join(directory, "english-senate-1.txt"), "r", encoding="latin1"
    )
    development_data = infile.read()
    development_data_lst = development_data.split(" ")
    infile.close()

    infile = open(
        os.path.join(directory, "english-senate-2.txt"), "r", encoding="latin1"
    )
    test_data = infile.read()
    test_data_lst = test_data.split(" ")
    infile.close()

    infile = open(
        os.path.join(directory, "good-bad-split.txt"), "r", encoding="latin1"
    )
    good_bad = infile.read()
    good_bad_lst = good_bad.split(" ")
    infile.close()
    ## creating the dictionary for all types

    training_dictionary = make_dictionary(training_data_lst)
    development_dictionary = make_dictionary(development_data_lst)
    test_dictionary = make_dictionary(test_data_lst)
    good_bad_dictionary = make_dictionary(good_bad_lst)
    test_token_count = len(test_data_lst)
    training_token_count = len(training_data_lst)
    dev_token_count = len(development_data_lst)

    # Assertions
    ## Asserting dictionaries have all the contents
    assert len(training_data_lst) == get_token_count(training_dictionary)
    assert len(test_data_lst) == get_token_count(test_dictionary)
    assert len(development_data_lst) == get_token_count(development_dictionary)

    alpha = 1

    chance = get_likelihood(
        test_dictionary, training_dictionary, training_token_count, alpha
    )
    print("The likelihood of the test corpus for when Alpha is 1: ", chance)

    alpha = gss(
        get_likelihood, 1, 5, 1e-5, development_dictionary, training_dictionary
    )

    print("Alpha value after smoothing: ", alpha)

    ## Testing with good-bad-split

    infile = open(
        os.path.join(directory, "good-bad-split.txt"), "r", encoding="latin1"
    )
    good_bad_lst = infile.readlines()
    infile.close()

    good_lst = []
    bad_lst = []
    for i in range(0, len(good_bad_lst), 3):
        good_lst.append(good_bad_lst[i].strip())
        bad_lst.append(good_bad_lst[i + 1].strip())

    ## Asserting the lists have the same number of lengths
    assert len(good_lst) == len(bad_lst)

    count = 0
    examples = 0
    for i in range(len(bad_lst)):
        good_sentence = good_lst[i]
        bad_sentence = bad_lst[i]

        good_sentence_lst = good_sentence.split(" ")
        bad_sentence_lst = bad_sentence.split(" ")

        good_sentence_dictionary = make_dictionary(good_sentence_lst)
        bad_sentence_dictionary = make_dictionary(bad_sentence_lst)

        good_chance = get_likelihood(
            good_sentence_dictionary,
            training_dictionary,
            len(training_data_lst),
            alpha,
        )
        bad_chance = get_likelihood(
            bad_sentence_dictionary,
            training_dictionary,
            len(training_data_lst),
            alpha,
        )

        if good_chance > bad_chance:
            count += 1
        else:
            if examples < 3:
                examples += 1
                print(f"Example {examples}: ")
                print("Good Sentence: ", good_sentence)
                print("Bad Sentence: ", bad_sentence)
                print()

    percentage = round(count / len(bad_lst) * 100)
    print(f"Percent Score on Good-Bad data: {percentage}%")


if __name__ == "__main__":
    main()