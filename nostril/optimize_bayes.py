#!/usr/bin/env python3
'''Find parameter values for the nonsense detector.

Introduction
------------

This uses optimization to tune the parameter values for the arguments of
`generate_score_function()` and `generate_nonsense_detector()`.  It uses
scipy.optimize with the Nelder-Mead algorithm in combination with a
simplistic iteration scheme to deal with an integer parameter in
`generate_score_function()`.  The output is written to a bunch of files
named `run-NN.txt`, where the NN is the value of the integer parameter
(which is the value for `len_threshold` in `generate_score_function()`).

Usage
-----

This is a simple script that you run by executing it on the command line:
  ./optimize.py

After it's done, there will be a bunch of files named `run-NN.txt`.  Look
at them all and find which one had the best combination of false positive
and false negative scores.

Authors
-------

Michael Hucka <mhucka@caltech.edu>

Copyright
---------

Copyright (c) 2017 by the California Institute of Technology.  This software
was developed as part of the CASICS project, the Comprehensive and Automated
Software Inventory Creation System.  For more, visit http://casics.org.

'''

from   collections import defaultdict, Counter, namedtuple
from   contextlib import redirect_stdout
import humanize
from   multiprocessing import Pool
import numpy as np
import os
from   platypus import *
import re
import string
import sys
from   time import time

if '__file__' in globals():
    thisdir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.join(thisdir, '../'))
    sys.path.append(os.path.join(thisdir, '../common'))
else:
    sys.path.append('../')
    sys.path.append('../common')

from utils import msg, full_path
from nonsense_detector import *
from training_set import *

msg('Creating word lists')
words = mnb_training_set()
rs = random_set(words)

msg('Setting up problem')

def find_parameters(vars):
    theta        = vars[0]
    phi          = vars[1]
    multiplier   = vars[2]

    factors = gmnb_ngram_factors(words, rs, 4, theta=theta)
    is_nonsense = generate_gmnb_detector(ngram_factors=factors,
                                         theta=theta, phi=phi,
                                         real_multiplier=multiplier)

    false_pos1, _, _, _, _ = test_strings('/usr/share/dict/web2', is_nonsense,
                                          trace_scores=False)
    # false_pos2, _, _, _, _ = test_strings('tests/unlabeled-cases/loyola-u-ids-cleaned.txt',
    #                                       is_nonsense, trace_scores=False)
    # false_pos3, false_neg1, _, _, _ = test_labeled('tests/labeled-cases/real-not-real.csv',
    #                                                is_nonsense, trace_scores=False)
    # false_pos3 = len(false_pos3)
    # false_neg1 = len(false_neg1)
    false_neg2, _, _, _, _ = test_strings('tests/unlabeled-cases/random-by-hand.txt',
                                          is_nonsense, sense='invalid', trace_scores=False)

    # return [false_pos1, false_pos2, false_pos3, false_neg1, false_neg2]
    return [false_pos1, false_neg2]

# problem = Problem(3, 5)
problem = Problem(3, 2)
problem.types[:] = [Real(0.0, 0.9), Real(-1.0, 2.0), Real(0.1, 2.0)]
problem.function = find_parameters

msg('Running NSGAII')
start = time()
with ProcessPoolEvaluator(7) as evaluator:
    algorithm = NSGAII(problem, evaluator=evaluator)
    algorithm.run(10000)
msg('Done after {}s'.format(time() - start))

for solution in algorithm.result:
    v = solution.variables
    f = solution.objectives
    # msg('theta = {}, phi = {}, mult = {} => fp1 = {}, fp2 = {}, fp3 = {}, fn1 = {}, fn2 = {}'.
    #     format(v[0], v[1], v[2], f[0], f[1], f[2], f[3], f[4]))
    msg('fp1 = {:06d}, fn2 = {:06d} => theta = {}, phi = {}, mult = {}'.
        format(f[0], f[1], v[0], v[1], v[2]))
