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
print('Testing valid words in /usr/share/dict/web2 -- expect 22 false positives positives (99.99% correct):')
test_unlabeled('/usr/share/dict/web2', nonsense, trace_scores=True)

print('')
print('Testing against valid Ludiso cases -- expect 2 false positives:')
test_unlabeled('unlabeled-cases/ludiso.txt', nonsense, trace_scores=True)

print('')
print('Testing labeled cases -- expect 5 false positives, 9 false negatives:')
result = test_labeled('labeled-cases/real-not-real.csv', nonsense, trace_scores=True)

print('')
print('Testing against valid OSX identifiers -- expect 5 false positives:')
test_unlabeled('unlabeled-cases/select-identifiers-from-osx-frameworks.txt', nonsense, trace_scores=True)

print('')
print('Testing against hand-written random strings -- expect 70% true positives:')
test_unlabeled('unlabeled-cases/random-by-hand.txt', nonsense, sense='invalid', trace_scores=True)

print('')
print('Recall test: valid identifiers from source code -- expect 6 false positives:')
test_unlabeled('../nostril/training/identifier-corpora/random-identifiers-from-github.txt', nonsense, trace_scores=True)

print('')
print('Recall test: machine-generated random strings -- expect 85.75% true positives:')
random_strings = dataset_from_pickle('unlabeled-cases/random_set.pklz')
test_unlabeled(random_strings[:1000000], nonsense, trace_scores=True, sense='nonsense')
