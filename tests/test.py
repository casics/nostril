#!/usr/bin/env python3

import os
import pytest
import sys
from   time import time

thisdir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(thisdir, '..'))

from nostril import *

assert is_nonsense('lakdfqtajaklj')
assert is_nonsense('AaBbCcDdEeFGgHhIiJjKkLlMmNnOoPpQqRrSsTtU')
assert is_nonsense('AcoGQMJyIapivScpnfuXUDMtgTtvAACYdAyABnSLpoABhzZWAAVvAYAAAnqUAFTPo')
assert is_nonsense('BCDEFGHIJKLMNOPQRSTUVWXYZ')
assert is_nonsense('CDjjiJJTbvFWaSdEtUygGMoGl')
assert is_nonsense('CQgHAwIDFQIDAxYCAQIeAQIXgAAKCRC')
assert is_nonsense('CgKDQpPUkdBTklaSUHIENPTUJVFRFRQKLStLStLStLStLStLStLStLStLStLSt')
assert is_nonsense('aoaoesuouooeueooeuoaeuoeou')
assert is_nonsense('iuewrofahgalkfgaufpiupqrjf')
assert is_nonsense('ieeoienkjadfakj')
assert is_nonsense('lalalaalkjuogaajfajlfal')

is_nonsense = generate_nonsense_detector()

print('')
print('Testing all words in /usr/share/dict/web2 -- expect 22 failures (99.99% correct):')
test_strings('/usr/share/dict/web2', is_nonsense, trace_scores=True)

print('')
print('Testing against Loyola cases -- expect 2 failures:')
test_strings('unlabeled-cases/loyola-u-ids-cleaned.txt', is_nonsense, trace_scores=True) 

print('')
print('Testing real-not-real -- expect 5 false positives, 9 false negatives:')
result = test_labeled('labeled-cases/real-not-real.csv', is_nonsense, trace_scores=True)

print('')
print('Testing against real OSX identifiers -- expect 5 failures:')
test_strings('unlabeled-cases/select-identifiers-from-osx-frameworks.txt', is_nonsense, trace_scores=True)

print('')
print('Testing against hand-written random strings -- expect 70% correct:')
test_strings('unlabeled-cases/random-by-hand.txt', is_nonsense, sense='invalid', trace_scores=True) 

print('')
print('Recall test: all of these are believed to be real -- expect 6 failures:')
(failures, successes, count, skipped, elapsed_time) = test_strings('../nostril/training/identifier-corpora/random-identifiers-from-github.txt', is_nonsense, trace_scores=True)
print('Recall = {:.6f}'.format(successes/count))

print('')
print('Recall test: all of these are truly random strings -- expect 85.75% correct:')
random_strings = dataset_from_pickle('unlabeled-cases/random_set.pklz')
(failures, successes, count, skipped, elapsed_time) = test_strings(random_strings[:1000000], is_nonsense, trace_scores=True, sense='nonsense')
print('Recall = {:.6f}'.format(successes/count))
