#!/usr/bin/env python3
'''Naive Bayes variations tested for Nostril.
'''

from collections import defaultdict, Counter, namedtuple
from math import pow, log, ceil
import humanize
import os
import plac
import re
import string
import sys

if '__file__' in globals():
    thisdir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.join(thisdir, '../common'))
else:
    sys.path.append('../common')

from utils import msg, full_path
from nonsense_detector import *
from training_set import *


# Global data structures.
# .............................................................................

NGramWeight = namedtuple('NGramWeight', 'log_real, log_nonsense, ts_real, ts_nonsense')
'''
The conditional parameter term for an n-gram, used in the Naive Bayes
formula.  'ts_real' and 'ts_nonsense' are Boolean values indicating whether
the n-gram was encountered in the real and/nor nonsense training sets,
respectively.
'''

NGramFactor = namedtuple('NGramFactor', 'real_term, nonsense_term')


# Training sets for multinomial Naive Bayes.
# .............................................................................

def mnb_training_set(min_length=4):
    raw = set()
    raw.update(_words_from_nltk())
    raw.update(_words_from_file('wordfrequency-unique-from-100k.txt'))
    raw.update(_words_from_file('nltk-linux-problem-reports.txt'))
    raw.update(_words_from_file('nltk-apache-problem-reports.txt'))
    raw.update(_identifiers_from_file('random-identifiers-from-github.txt'))
    raw.update(_identifiers_from_file('selected-linux-symbols.txt'))
    # Remove words shorter than the threshold.
    semi_final = [w for w in raw if len(w) >= min_length]
    return semi_final


# Functions to calculate statistics for Multinomial Naive Bayes (MNB).
# .............................................................................

def relative_frequency(count_x, total_count, total_ngrams, smoothing=1):
    '''
    This calculates the probability term for an n-gram for a single class.
    Note that this doesn't need the actual n-gram as a parameter; it only
    needs to know the various counts.  It also doesn't take the class as a
    parameter.  The question of which n-gram and class are at stake is
    something assumed to be dealt with by the caller.

    The formula used is:
                                   count_x + smoothing
    Probability(x|class) = ----------------------------------------
                           total_count + (total_ngrams * smoothing)
    where:
      count_x      = total count of ngram x in strings of the class
      total_count  = total count of all ngrams across all strings of the class
      total_ngrams = total number of ngrams

    When the value of "smoothing" is 1, this is known as Laplace smoothing.
    When the value is < 1, it's Lidstone smoothing.
    '''
    return (count_x + smoothing)/(total_count + (total_ngrams * smoothing))


def mnb_ngram_weights(real_strings, nonsense_strings, n, smoothing=1):
    # This actually stores the logarithm of the probabilities, because that's
    # the quantity used when applying the Bayes formula and it's more efficient
    # to precompute the log than to have to compute it over and over again.

    occurrences_real     = defaultdict(int)
    occurrences_nonsense = defaultdict(int)
    for string in real_strings:
        for ngram in ngrams(string.lower(), n):
            occurrences_real[ngram] += 1
    for string in nonsense_strings:
        for ngram in ngrams(string.lower(), n):
            occurrences_nonsense[ngram] += 1

    real_sum = sum(occurrences_real.values())
    nonsense_sum = sum(occurrences_nonsense.values())

    all_ngrams = all_possible_ngrams(n)
    num_ngrams = len(all_ngrams)

    # Initialize all n-gram values to the value that would come from zero
    # occurrences of an n-gram in a given training set.
    missing_real = log(relative_frequency(0, real_sum, num_ngrams, smoothing))
    missing_nonsense = log(relative_frequency(0, nonsense_sum, num_ngrams, smoothing))
    weights = defaultdict.fromkeys(all_ngrams,
                                   NGramWeight(log_real=missing_real,
                                               log_nonsense=missing_nonsense,
                                               ts_real=False, ts_nonsense=False))
    for ngram in all_ngrams:
        real = log(relative_frequency(occurrences_real[ngram], real_sum,
                                      num_ngrams, smoothing))
        nonsense = log(relative_frequency(occurrences_nonsense[ngram],
                                          nonsense_sum, num_ngrams, smoothing))
        weights[ngram] = NGramWeight(log_real=real, log_nonsense=nonsense,
                                     ts_real=bool(occurrences_real[ngram]),
                                     ts_nonsense=bool(occurrences_nonsense[ngram]))
    return weights


def mnb_score_function(ngram_weights, real_multiplier=1):
    # A smaller real_multiplier will actually raise the real score, because the
    # score numbers are negative.
    ngram_length = len(next(iter(ngram_weights.keys())))
    def naive_bayes_score(string):
        # This the algorithm in Manning et al.  It is also equivalent to
        # their variant in equation 13.15 that uses term frequency: their
        # term frequency appears to be just raw unadjusted frequency of an
        # n-gram in a given document, and the formula below is the same as
        # doing the sum of tf_i * P(term_i | c) but by simply counting up
        # P(term_i | c) multiple times (namely, number tf_i times).

        real_score = 0
        nonsense_score = 0
        for ngram in ngrams(string, ngram_length):
            real_score += ngram_weights[ngram].log_real
            nonsense_score += ngram_weights[ngram].log_nonsense
        real_score = real_multiplier * real_score
        return (nonsense_score > real_score, real_score, nonsense_score)
    return naive_bayes_score

        # Generate list of n-grams for the given string.
        # string_ngrams = ngrams(string, ngram_length)
        # Count up occurrences of each n-gram in the string.
        # ngram_counts = defaultdict(int)
        # for ngram in string_ngrams:
        #     ngram_counts[ngram] += 1
        # real_score = sum(weights[ngram].log_real for ngram in ngram_counts.keys())
        # nonsense_score = sum(weights[ngram].log_nonsense for ngram in ngram_counts.keys())


def generate_mnb_detector(ngram_weights, min_length=6, trace=False,
                          real_multiplier=1):
    string_score = mnb_score_function(ngram_weights, real_multiplier=real_multiplier)
    if trace:
        def is_nonsense(string, show=trace):
            # Lower-case the string & remove non-letters before checking length.
            string = string.lower().translate(_delchars)
            if len(string) < min_length:
                raise ValueError('Too short to test')
            is_nonsense, real_score, nonsense_score = string_score(string)
            if show:
                msg('"{}": {} (real score {:.4f}, nonsense score {:.4f})'
                    .format(string, 'y' if is_nonsense else 'n',
                            real_score, nonsense_score))
            return is_nonsense
    else:
        def is_nonsense(string, show=trace):
            # Lower-case the string & remove non-letters before checking length.
            string = string.lower().translate(_delchars)
            if len(string) < min_length:
                raise ValueError('Too short to test')
            is_nonsense, real_score, nonsense_score = string_score(string)
            return is_nonsense
    return is_nonsense


# Functions to calculate statistics for generalized Multinomial Naive Bayes (GMNB).
# .............................................................................

def gmnb_ngram_factors(real_strings, nonsense_strings, n, theta=0):
    # This actually stores the logarithm of the probabilities, because that's
    # the quantity used when applying the Bayes formula and it's more efficient
    # to precompute the log than to have to compute it over and over again.

    occurrences_real     = defaultdict(int)
    occurrences_nonsense = defaultdict(int)
    for string in real_strings:
        for ngram in ngrams(string.lower(), n):
            occurrences_real[ngram] += 1
    for string in nonsense_strings:
        for ngram in ngrams(string.lower(), n):
            occurrences_nonsense[ngram] += 1

    real_sum = sum(occurrences_real.values())
    nonsense_sum = sum(occurrences_nonsense.values())

    all_ngrams = all_possible_ngrams(n)
    num_ngrams = len(all_ngrams)
    num_real_strings = len(real_strings)
    num_nonsense_strings = len(nonsense_strings)

    # In this generalized version of tf-idf, if the tf for a given document
    # is 0, then the whole term is 0.  So our default is simple:
    # weights = defaultdict.fromkeys(all_ngrams, NGramFactor(real_term=0, nonsense_term=0))

    missing_real = log(relative_frequency(0, real_sum, num_ngrams, 1))
    missing_nonsense = log(relative_frequency(0, nonsense_sum, num_ngrams, 1))
    weights = defaultdict.fromkeys(all_ngrams,
                                   NGramFactor(real_term=missing_real,
                                               nonsense_term=missing_nonsense))

    # We store everything that is constant for a given n-gram.
    # theta_over_N = theta/num_ngrams
    # for ngram in all_ngrams:
    #     real_term = missing_real
    #     nonsense_term = missing_nonsense
    #     if occurrences_real[ngram] > 0:
    #         idf = log(num_real_strings/occurrences_real[ngram])
    #         real = relative_frequency(occurrences_real[ngram], real_sum, num_ngrams)
    #         real_term = idf*log((1 - theta)*real + theta_over_N)
    #     if occurrences_nonsense[ngram] > 0:
    #         idf = log(num_nonsense_strings/occurrences_nonsense[ngram])
    #         nonsense = relative_frequency(occurrences_nonsense[ngram], nonsense_sum, num_ngrams)
    #         nonsense_term = idf*log((1 - theta)*nonsense + theta_over_N)
    #     weights[ngram] = NGramFactor(real_term=real_term, nonsense_term=nonsense_term)

    theta_over_N = theta/num_ngrams
    for ngram in all_ngrams:
        real = relative_frequency(occurrences_real[ngram], real_sum, num_ngrams)
        real_term = log((1 - theta)*real + theta_over_N)
        nonsense = relative_frequency(occurrences_nonsense[ngram], nonsense_sum, num_ngrams)
        nonsense_term = log((1 - theta)*nonsense + theta_over_N)
        weights[ngram] = NGramFactor(real_term=real_term, nonsense_term=nonsense_term)

    return weights


def gmnb_score_function(ngram_factors, real_multiplier=1, theta=0, phi=1, rho=1):
    ngram_length = len(next(iter(ngram_factors.keys())))
    def generalized_naive_bayes_score(string):
        string_ngrams = ngrams(string.lower(), ngram_length)

        ngram_occurrences = defaultdict(int)
        unique_ngrams = set()
        for ngram in string_ngrams:
            ngram_occurrences[ngram] += 1
            unique_ngrams.add(ngram)

        unique_phi = pow(len(unique_ngrams), phi)
        unique_one_minus_phi = pow(len(unique_ngrams), 1 - phi)
        real_score = 0
        nonsense_score = 0
        for ngram in string_ngrams:
            tf = log(1 + ngram_occurrences[ngram]/unique_phi) / unique_one_minus_phi
            real_score += tf * ngram_factors[ngram].real_term
            nonsense_score += tf * ngram_factors[ngram].nonsense_term
        real_score = real_multiplier * real_score
        return (nonsense_score > real_score, real_score, nonsense_score)
    return generalized_naive_bayes_score


def generate_gmnb_detector(ngram_factors, min_length=6, trace=False,
                           theta=0, phi=1, rho=1, real_multiplier=1):
    string_score = gmnb_score_function(ngram_factors, real_multiplier=real_multiplier,
                                       theta=theta, phi=phi, rho=rho)
    if trace:
        def is_nonsense(string, show=trace):
            # Lower-case the string & remove non-letters before checking length.
            string = string.lower().translate(_delchars)
            if len(string) < min_length:
                raise ValueError('Too short to test')
            is_nonsense, real_score, nonsense_score = string_score(string)
            if show:
                msg('"{}": {} (real score {:.4f}, nonsense score {:.4f})'
                    .format(string, 'y' if is_nonsense else 'n',
                            real_score, nonsense_score))
            return is_nonsense
    else:
        def is_nonsense(string, show=trace):
            # Lower-case the string & remove non-letters before checking length.
            string = string.lower().translate(_delchars)
            if len(string) < min_length:
                raise ValueError('Too short to test')
            is_nonsense, real_score, nonsense_score = string_score(string)
            return is_nonsense
    return is_nonsense


# Functions to calculate statistics for Bernoulli Naive Bayes (BNB).
# .............................................................................
#
# This follows the algorithm given in Figure 13.3 of the book "Introduction
# to information retrieval" by Manning, C. D., Raghavan, P., & Schütze,
# H. (2009, Online edition ed., Cambridge University Press).
#
# In my limited testing, this produced better results than MNB on the Loyola
# id subset, but slightly worse results for the real-not-real.csv set.
# Unfortunately, this is too slow to be practical, at least when using
# 4-grams.  This is due to the fact that it scales with the number of terms
# in the vocabulary (i.e., the number of all possible n-grams).  The
# iteration over the possible vocabulary terms in the scoring function is
# unavoidable, and though I've tried to optimize the loop in
# bnb_score_function() as much as possible, it is still slow.  (For 4-grams,
# it iterates over 456,976 terms and adds 2 * 456,976 floating point
# numbers.)  Due to the unusably slow nature of this algorithm, and the lack
# of apparent improvement in performance over MNB, I gave up on further work
# on Bernoulli Naive Bayes.  I'm leaving the code here for reference.
#
# The code below uses a modified version of the NGramWeight tuple:
#
#  NGramWeight = namedtuple('NGramWeight', 'found_in_ts, log_real, log_nonsense,
#  log_one_minus_real, log_one_minus_nonsense')
#

def bnb_ngram_weights(real_strings, nonsense_strings, n):
    # Count the number of strings in which each n-gram occurs.  Note this is
    # not the same as all occurrences of the n-gram, which would entail
    # counting cases when an n-gram appears more than once in a string.)
    occurrences_real     = defaultdict(set)
    occurrences_nonsense = defaultdict(set)
    for string in real_strings:
        for ngram in ngrams(string.lower(), n):
            # Using a set so that if the n-gram appears more than once in a
            # given string, we only count it once.
            occurrences_real[ngram].update(string)
    for string in nonsense_strings:
        for ngram in ngrams(string.lower(), n):
            occurrences_nonsense[ngram].update(string)

    # Initialize all n-gram values to the value that would come from zero
    # occurrences of an n-gram in a given training set.
    missing_real = 1/(len(real_strings) + 2)
    missing_nonsense = 1/(len(nonsense_strings) + 2)
    all_ngrams = all_possible_ngrams(n)
    weights = defaultdict.fromkeys(all_ngrams,
                                   NGramWeight(found_in_ts=False,
                                               log_real=log(missing_real),
                                               log_nonsense=log(missing_nonsense),
                                               log_one_minus_real=log(1 - log(missing_real)),
                                               log_one_minus_nonsense=log(1 - missing_nonsense)))
    num_real_strings = len(real_strings)
    num_nonsense_strings = len(nonsense_strings)
    for ngram in all_ngrams:
        num_occurrences_real = len(occurrences_real[ngram])
        num_occurrences_nonsense = len(occurrences_nonsense[ngram])
        real = (num_occurrences_real + 1)/(num_real_strings + 2)
        nonsense = (num_occurrences_nonsense + 1)/(num_nonsense_strings + 2)
        found = (num_occurrences_real + num_occurrences_nonsense) > 0
        weights[ngram] = NGramWeight(found_in_ts=found,
                                     log_real=log(real),
                                     log_nonsense=log(nonsense),
                                     log_one_minus_real=log(1 - real),
                                     log_one_minus_nonsense=log(1 - nonsense))
    return weights


def bnb_score_function(weights, ngram_length=4):
    all_ngrams = set(all_possible_ngrams(ngram_length))

    def bernoulli_nb_score(string, show=False):
        string_ngrams = ngrams(string, ngram_length)
        real_score = 0
        nonsense_score = 0
        for ngram in string_ngrams:
            real_score += weights[ngram].log_real
            nonsense_score += weights[ngram].log_nonsense
        for ngram in all_ngrams - set(string_ngrams):
            real_score += weights[ngram].log_one_minus_real
            nonsense_score += weights[ngram].log_one_minus_nonsense
        return nonsense_score > real_score
    return bernoulli_nb_score

