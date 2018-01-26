#!/usr/bin/env python3

import os
import pytest
import sys
from   time import time

try:
    thisdir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.join(thisdir, '..'))
except:
    sys.path.append('..')

from nostril import *

assert nonsense('lakdfqtajaklj')
assert nonsense('AaBbCcDdEeFGgHhIiJjKkLlMmNnOoPpQqRrSsTtU')
assert nonsense('AcoGQMJyIapivScpnfuXUDMtgTtvAACYdAyABnSLpoABhzZWAAVvAYAAAnqUAFTPo')
assert nonsense('BCDEFGHIJKLMNOPQRSTUVWXYZ')
assert nonsense('CDjjiJJTbvFWaSdEtUygGMoGl')
assert nonsense('CQgHAwIDFQIDAxYCAQIeAQIXgAAKCRC')
assert nonsense('CgKDQpPUkdBTklaSUHIENPTUJVFRFRQKLStLStLStLStLStLStLStLStLStLSt')
assert nonsense('aoaoesuouooeueooeuoaeuoeou')
assert nonsense('iuewrofahgalkfgaufpiupqrjf')
assert nonsense('ieeoienkjadfakj')
assert nonsense('lalalaalkjuogaajfajlfal')

print('')
print('Testing all words in /usr/share/dict/web2 -- expect 22 failures (99.99% correct):')
test_strings('/usr/share/dict/web2', nonsense, trace_scores=True)

print('')
print('Testing against Ludiso cases -- expect 2 failures:')
test_strings('unlabeled-cases/ludiso.txt', nonsense, trace_scores=True)

print('')
print('Testing real-not-real -- expect 5 false positives, 9 false negatives:')
result = test_labeled('labeled-cases/real-not-real.csv', nonsense, trace_scores=True)

print('')
print('Testing against real OSX identifiers -- expect 5 failures:')
test_strings('unlabeled-cases/select-identifiers-from-osx-frameworks.txt', nonsense, trace_scores=True)

print('')
print('Testing against hand-written random strings -- expect 70% correct:')
test_strings('unlabeled-cases/random-by-hand.txt', nonsense, sense='invalid', trace_scores=True) 

print('')
print('Recall test: all of these are believed to be real -- expect 6 failures:')
(failures, successes, count, skipped, elapsed_time) = test_strings('../nostril/training/identifier-corpora/random-identifiers-from-github.txt', nonsense, trace_scores=True)
print('Recall = {:.6f}'.format(successes/count))

print('')
print('Recall test: all of these are truly random strings -- expect 85.75% correct:')
random_strings = dataset_from_pickle('unlabeled-cases/random_set.pklz')
(failures, successes, count, skipped, elapsed_time) = test_strings(random_strings[:1000000], nonsense, trace_scores=True, sense='nonsense')
print('Recall = {:.6f}'.format(successes/count))
