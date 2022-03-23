
import os
import math
from unigram import get_theta


def tokenize(lst_of_sentences):
    """This funciton, given a list of strings, returns a list of words that come
    from each sentence.

    Args:
        lst_of_sentences (list): list of strings. For our situation, they are
        sentences.

    Returns:
        list: list of words from all the sentences.
    """
    tokenized_lst = []
    for sentence in lst_of_sentences:
        for word in sentence.split(" "):
            tokenized_lst.append(word)
    return tokenized_lst


def add_padding_and_tokenize(lines):
    """this function puts together the add_padding function and the tokenize
    function and returns a list. It is meant to make our code look cleaner with
    less blocks.

    Args:
        lines (list): list of strings. lines that we get from readlines()

    Returns:
        list: a list of words from all the sentences including the paddings.
    """
    result = add_padding(lines)
    result = tokenize(result)
    return result


def add_padding(lines):
    """This function takes in an entire corpus as a string and adds padding to
    it. The padding should be *START* and *END*. It uses regular expression to
    achieve this. It's going to return the entire corpus but with paddings for
    each sentence

    Args:
        lines ([str]): Should be a string that contains no paddings. It should
        be a one sentence per line with \n to separate the sentences.
    """
    assert type(lines) == list
    padded_lines = []
    for sentence in lines:

        item = "*START* " + sentence.strip() + " *END*"
        padded_lines.append(item)
    return padded_lines


def get_token_count(dictionary):
    """Calculates the number of tokens from a dictionary that has counts as
    values

    Args:
        dictionary (tuple:int): This dictionary most likely comes from the
        bigram dictionary which contains all the bigrams and their respective
        frequencies.

    Returns:
        int: sum of all the frequencies. Total count.
    """
    return sum(dictionary.values())


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


def create_bigram_dictionary(corpus_token_lst):
    """Creates a dictionary of tuples with (word, word') as keys and their
    frequency as values. This can help us determine the big_theta for each
    bigram. This function creates the dictionary by iterating through the entire
    list and creating pairs by accessing the current element using the index and
    the value that follows the current element.

    Args:
        corpus_token_lst (list): This list is a padded list of tokens from which
        we can create the bigram dictionary.

    Returns:
        dict: a dictionary of tuples with (word, word') and int for frequency.
    """
    lst_of_bigrams = []
    for i in range(len(corpus_token_lst) - 1):
        lst_of_bigrams.append((corpus_token_lst[i], corpus_token_lst[i + 1]))

    bigram_dictionary = make_dictionary(lst_of_bigrams)
    return bigram_dictionary


def get_big_theta(
    word1: str,
    word2,
    bigram_dictionary,
    corpus_dictionary,
    token_count,
    alpha,
    beta,
):
    """This functions like our theta model from the training. It's like we are
    getting values from a big_theta dictionary, our language model. It is
    a direct implementation of the formula in the writeup.

    Args:
        word1 (str): the word the comes first.
        word2 (str): the word that comes second.
        bigram_dictionary (dict[tuple: int]): the training bigram dictionary, which
        should be similar to every other data that is fed to this function.
        corpus_dictionary (dict[str : int]): the non-bigram version of the
        dictionary.
        token_count (int): number of tokens in the training data.
        alpha (int): the alpha value
        beta (int): the beta value Θ

    Returns:
        int: the big theta value.
    """
    bigram = (word1, word2)
    total_word1_count = corpus_dictionary.get(
        word1, 0
    )  # TODO: CREATE ONE HUGE WORD COUNT
    bigram_count = bigram_dictionary.get(bigram, 0)
    theta_of_word2 = get_theta(word2, corpus_dictionary, token_count, alpha)
    big_theta = (bigram_count + (beta * theta_of_word2)) / (
        total_word1_count + beta
    )
    return big_theta


def get_likelihood_bigram(
    training_corpus_dictionary,
    training_corpus_token_lst,
    training_bigram_dictionary,
    test_bigram_dictionary,
    alpha,
    beta,
):
    """This function

    Args:
        training_corpus_dictionary (_type_): _description_
        training_corpus_token_lst (_type_): _description_
        training_bigram_dictionary (_type_): _description_
        test_bigram_dictionary (_type_): _description_
        alpha (_type_): _description_
        beta (_type_): _description_

    Returns:
        _type_: _description_
    """
    log_likelihood_bigram = 0
    for pair in test_bigram_dictionary:
        word1 = pair[0]
        word2 = pair[1]

        big_theta = get_big_theta(
            word1,
            word2,
            training_bigram_dictionary,
            training_corpus_dictionary,
            len(training_corpus_token_lst),
            alpha,
            beta,
        )
        log_big_theta = math.log(big_theta, 10) * test_bigram_dictionary[pair]
        log_likelihood_bigram = log_big_theta + log_likelihood_bigram

    return log_likelihood_bigram


def run_good_bad_test(
    padded_training_data_lst,
    training_bigram_dictionary,
    good_bad_lst,
    alpha,
    beta,
):
    """This function is designed to modularize our test for the performance of
    our model. It is supposed to return the percentage of tests from the
    good-bad data that we got correct.

    Args:
        padded_training_data_lst (list[str]): The string data for the training
        dataset tokenized and including the padded elements.
        training_bigram_dictionary (dict[tulpe: int]): the same training data
        but turned into a bigram dictionary
        good_bad_lst (list[str]): list of strings alternating between a good &
        a bad sentence.
        alpha (int): the alpha value
        beta (int): the beta value

    Returns:
        int: percentage value of our score.
    """
    good_lst = []
    bad_lst = []
    for i in range(0, len(good_bad_lst), 3):
        good_lst.append(good_bad_lst[i].strip())
        bad_lst.append(good_bad_lst[i + 1].strip())

    ## Asserting the lists have the same number of lengths
    assert len(good_lst) == len(bad_lst)
    padded_good_sentence = add_padding(good_lst)
    padded_bad_sentence = add_padding(bad_lst)
    training_corpus_dictionary = make_dictionary(padded_training_data_lst)

    count = 0
    examples = 0
    length = len(bad_lst)
    for i in range(length):
        good_sentence = padded_good_sentence[i]
        bad_sentence = padded_bad_sentence[i]
        assert type(good_sentence) == str
        good_sentence_lst = good_sentence.split(" ")
        bad_sentence_lst = bad_sentence.split(" ")

        good_sentence_bigram_dictionary = create_bigram_dictionary(
            good_sentence_lst
        )
        bad_sentence_bigram_dictionary = create_bigram_dictionary(
            bad_sentence_lst
        )

        good_chance = get_likelihood_bigram(
            training_corpus_dictionary,
            padded_training_data_lst,
            training_bigram_dictionary,
            good_sentence_bigram_dictionary,
            alpha,
            beta,
        )
        bad_chance = get_likelihood_bigram(
            training_corpus_dictionary,
            padded_training_data_lst,
            training_bigram_dictionary,
            bad_sentence_bigram_dictionary,
            alpha,
            beta,
        )

        if good_chance >= bad_chance:
            count += 1
        else:
            if examples < 3:
                examples += 1
                print(f"Example {examples}: ")
                print("Good Sentence: ", good_sentence)
                print("Bad Sentence: ", bad_sentence)
                print()
    percentage = count / length * 100
    return percentage


def gss(
    f,
    a,
    b,
    tol,
    training_corpus_dictionary,
    padded_training_data_lst,
    training_bigram_dictionary,
    test_bigram_dictionary,
    alpha,
):
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
            training_corpus_dictionary,
            padded_training_data_lst,
            training_bigram_dictionary,
            test_bigram_dictionary,
            alpha,
            c,
        ) > f(
            training_corpus_dictionary,
            padded_training_data_lst,
            training_bigram_dictionary,
            test_bigram_dictionary,
            alpha,
            d,
        ):
            b = d
        else:
            a = c

        # We recompute both c and d here to avoid loss of precision which may lead to incorrect results or infinite loop
        c = b - (b - a) / gr
        d = a + (b - a) / gr
    beta = (b + a) / 2
    # print(beta)
    return (b + a) / 2


def main():
    ALPHA = 1.595977110540115
    # Opening all files into variables
    directory = "langmod/hansard/"
    files = os.listdir(directory)
    infile = open(
        os.path.join(directory, "english-senate-0.txt"), "r", encoding="latin1"
    )
    training_data_lst = infile.readlines()
    infile.close()

    infile = open(
        os.path.join(directory, "english-senate-1.txt"), "r", encoding="latin1"
    )
    development_data_lst = infile.readlines()
    infile.close()

    infile = open(
        os.path.join(directory, "english-senate-2.txt"), "r", encoding="latin1"
    )
    test_data_lst = infile.readlines()
    infile.close()

    infile = open(
        os.path.join(directory, "good-bad-split.txt"), "r", encoding="latin1"
    )
    good_bad_lst = infile.readlines()
    infile.close()

    # Clean the data
    ## Add padding
    padded_training_data_lst = add_padding_and_tokenize(training_data_lst)
    padded_development_data_lst = add_padding_and_tokenize(development_data_lst)
    padded_test_data_lst = add_padding_and_tokenize(test_data_lst)

    training_bigram_dictionary = create_bigram_dictionary(
        padded_training_data_lst
    )
    development_bigram_dictionary = create_bigram_dictionary(
        padded_development_data_lst
    )
    test_bigram_dictionary = create_bigram_dictionary(padded_test_data_lst)

    training_corpus_dictionary = make_dictionary(padded_training_data_lst)
    BETA = 1
    log_likelihood_bigram = get_likelihood_bigram(
        training_corpus_dictionary,
        padded_training_data_lst,
        training_bigram_dictionary,
        test_bigram_dictionary,
        ALPHA,
        BETA,
    )
    BETA = gss(
        get_likelihood_bigram,
        1,
        200,
        1e-5,
        training_corpus_dictionary,
        padded_training_data_lst,
        training_bigram_dictionary,
        development_bigram_dictionary,
        ALPHA,
    )
    percentage = run_good_bad_test(
        padded_training_data_lst,
        training_bigram_dictionary,
        good_bad_lst,
        ALPHA,
        BETA,
    )
    print("Likelihood of our Test Data when Beta = 1: ", log_likelihood_bigram)
    print(
        "Our estimated Beta after using the development data for smoothing: ",
        BETA,
    )
    print(f"Percent Score on Good-Bad data: {round(percentage)}%")


if __name__ == "__main__":
    main()