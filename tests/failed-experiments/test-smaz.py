#!/usr/bin/env python3

import sys
import operator
from time import time

sys.path.append('../common')
sys.path.append('../splitters')
sys.path.append('../extractor')

from training_set import *
from nonsense_detector import *

import smaz

def test(data):
    count_40 = 0
    count_50 = 0
    count_60 = 0
    c = {}
    start = time()
    for s in data:
        c[s] = len(smaz.compress(s))/len(s)
        if c[s] < 0.4:
            count_40 += 1
        if c[s] < 0.5:
            count_50 += 1
        if c[s] < 0.6:
            count_60 += 1
    duration = time() - start
    msg('{} strings'.format(len(data)))
    msg('40%: {}. {:.4f}s elapsed'.format(count_40, duration))
    msg('50%: {}. {:.4f}s elapsed'.format(count_50, duration))
    msg('60%: {}. {:.4f}s elapsed'.format(count_60, duration))
    for s, v in sorted(c.items(), key=operator.itemgetter(1)):
        msg('{:.2f}% -- {}'.format(v, s))


msg('-'*70)
msg('random')
test(dataset_from_pickle('tests/random_set.pickle'))

msg('-'*70)
msg('real')
test(dataset_from_pickle('training/training_set.pickle'))

# with open('real-not-real.csv', 'r') as f:
#     ids = f.read().strip().splitlines()
#     ids = [x.split(',')[1] for x in ids if x.split(',')[0] == 'y']
# test(ids)
