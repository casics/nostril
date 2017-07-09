#!/usr/bin/env python3

import os
import pytest
import sys
from   time import time

thisdir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(thisdir, '..'))
sys.path.append(os.path.join(thisdir, '../../common'))
sys.path.append(os.path.join(thisdir, '../../cataloguer'))
sys.path.append(os.path.join(thisdir, '../../detector'))
sys.path.append(os.path.join(thisdir, '../../splitters'))

from nonsense_detector import *
from training_set import *

start = time()

words = training_set()
rs = random_set()
weights = mnb_ngram_weights(words, rs, 4)
is_nonsense = generate_mnb_detector(weights, real_multiplier=0.865)
print('time to generate test function: {:.6f}s'.format(time() - start))

start = time()
# assert is_nonsense('lakdfqtajaklj')
print('time for first test: {:.6f}s'.format(time() - start))

start = time()
# assert is_nonsense('AaBbCcDdEeFGgHhIiJjKkLlMmNnOoPpQqRrSsTtU')
# assert is_nonsense('AcoGQMJyIapivScpnfuXUDMtgTtvAACYdAyABnSLpoABhzZWAAVvAYAAAnqUAFTPo')
# assert is_nonsense('BCDEFGHIJKLMNOPQRSTUVWXYZ')
# assert is_nonsense('CDjjiJJTbvFWaSdEtUygGMoGl')
# assert is_nonsense('CQgHAwIDFQIDAxYCAQIeAQIXgAAKCRC')
# assert is_nonsense('CgKDQpPUkdBTklaSUHIENPTUJVFRFRQKLStLStLStLStLStLStLStLStLStLSt')
# assert is_nonsense('aoaoesuouooeueooeuoaeuoeou')
# assert is_nonsense('aoprqoadoahhag')
# assert is_nonsense('ieeoienkjadfakj')
# assert is_nonsense('lalalaalkjuogaajfajlfal')
elapsed = time() - start
print('time for 10 tests: {:.6f}s => {:.6f}s per test'.format(
      elapsed, elapsed/10.0))

print('')
print('Testing all words in /usr/share/dict/web2 -- expect 18 failures:')
test_strings('/usr/share/dict/web2', is_nonsense, trace_scores=True)

print('')
print('Testing against Loyola cases -- expect 1 failure:')
test_strings('unlabeled-cases/loyola-u-ids-cleaned.txt', is_nonsense, trace_scores=True) 

print('')
print('Testing real-not-real -- expect 2 false positives, 7 false negatives:')
result = test_labeled('labeled-cases/real-not-real.csv', is_nonsense, trace_scores=True)

print('')
print('Testing against real OSX identifiers:')
test_strings('unlabeled-cases/select-identifiers-from-osx-frameworks.txt', is_nonsense, trace_scores=True)

print('')
print('Testing against hand-written random strings:')
test_strings('unlabeled-cases/random-by-hand.txt', is_nonsense, sense='invalid', trace_scores=True) 

print('')
print('Recall test: all of these are believed to be real:') 
(failures, successes, count, skipped, elapsed_time) = test_strings('../training/identifier-corpora/random-identifiers-from-github.txt', is_nonsense, trace_scores=True)
print('Recall = {:.6f}'.format(successes/count))

print('')
print('Recall test: all of these are truly random strings:') 
random_strings = dataset_from_pickle('unlabeled-cases/random_set.pklz')
(failures, successes, count, skipped, elapsed_time) = test_strings(random_strings[:1000000], is_nonsense, trace_scores=True, sense='nonsense')
print('Recall = {:.6f}'.format(successes/count))
