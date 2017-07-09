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

from nonsense_detector import *
from training_set import *

words = mnb_training_set()
rs = random_set(words)
weights = mnb_ngram_weights(words, rs, 4)

real     = sum(1 for w in weights.values() if w.ts_real)
nonsense = sum(1 for w in weights.values() if w.ts_nonsense)
neither  = sum(1 for w in weights.values() if not w.ts_real and not w.ts_nonsense)
msg('4-gram: real = {}, nonsense = {}, neither = {}'.format(real, nonsense, neither))

weights = mnb_ngram_weights(words, rs, 3)

real     = sum(1 for w in weights.values() if w.ts_real)
nonsense = sum(1 for w in weights.values() if w.ts_nonsense)
neither  = sum(1 for w in weights.values() if not w.ts_real and not w.ts_nonsense)
msg('3-gram: real = {}, nonsense = {}, neither = {}'.format(real, nonsense, neither))

weights = mnb_ngram_weights(words, rs, 2)

real     = sum(1 for w in weights.values() if w.ts_real)
nonsense = sum(1 for w in weights.values() if w.ts_nonsense)
neither  = sum(1 for w in weights.values() if not w.ts_real and not w.ts_nonsense)
msg('2-gram: real = {}, nonsense = {}, neither = {}'.format(real, nonsense, neither))
