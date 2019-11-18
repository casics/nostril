#!/usr/bin/env python3
'''Find parameter values for Nostril.

Introduction
------------

This uses a multiobjective optimization approach to tune the parameter values
for the arguments of `generate_nonsense_detector()`.  It uses the Python
package Platypus, specifically its implementation of the multiobjective
optimization algorithm NSGA-II ("Non-dominated Sorting Genetic Algorithm").
The objective functions minimize by this script are the errors on a
combination of positive and negative examples of nonsense strings.

The nature of the optimization problem is such that it is not possible to
find an optimal behavior for the nonsense string evaluator: the evaluator
will always produce some number of false positives on real identifier strings
and some number of false negatives on random text strings, and pushing one
number lower will push the other one higher.  The optimization process here
will do its best, but will ultimately only result in a surface and we have to
pick what matters to us subjectively.  The result of running this
optimization script will be a file containing a list of lines of values.
Each line will have a set of false positive and false negative values and the
parameter values that led to those particular results.  In the final usage of
this optimization script, I sorted these results and then picked a
(subjective) balance of very low false positives and some not-too-high false
negatives.

Usage
-----

This is a simple script that you run by executing it on the command line:

  ./optimize.py

The output is written to a file named `optimization-output.txt`.  You have to
sort the lines of the file, then look at the results and decide which
combination of false positives and false negatives you're willing to accept,
and finally, read off the corresponding parameter values.

Authors
-------

Michael Hucka <mhucka@caltech.edu>

Copyright
---------

Copyright (c) 2017-2019 by the California Institute of Technology.  This
software was developed as part of the CASICS project, the Comprehensive and
Automated Software Inventory Creation System. For more, visit http://casics.org.
'''

from   contextlib import redirect_stdout
import humanize
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
from nostril import *


# Objective function
# .............................................................................

ngram_freq = dataset_from_pickle('ngram_data.pklz')

def find_parameters(vars):
    var_min_score       = vars[0]
    var_len_penalty_exp = vars[1]
    var_rep_penalty_exp = vars[2]
    var_len_threshold   = vars[3]

    tester = generate_nonsense_detector(min_score=var_min_score,
                                        score_len_threshold=var_len_threshold,
                                        score_len_penalty_exp=var_len_penalty_exp,
                                        score_rep_penalty_exp=var_rep_penalty_exp)

    false_pos1, _, _, _, _ = test_strings('/usr/share/dict/web2', tester,
                                          trace_scores=False)

    false_pos2, _, _, _, _ = test_strings('tests/unlabeled-cases/loyola-u-ids-cleaned.txt',
                                          tester, trace_scores=False)

    false_pos3, false_neg1, _, _, _ = test_labeled('tests/labeled-cases/real-not-real.csv',
                                                   tester, trace_scores=False)
    # test_labeled returns a list of items, not counts, so turn them into counts
    false_pos3 = len(false_pos3)
    false_neg1 = len(false_neg1)

    false_neg2, _, _, _, _ = test_strings('tests/unlabeled-cases/random-by-hand.txt',
                                          tester, sense='invalid', trace_scores=False)

    return [false_pos1, false_pos2, false_pos3, false_neg1, false_neg2]


# Platypus hacks.
# .............................................................................

# This is a cheat to allow mixing Real and Integer types for the variables.
# Platypus's definition of Real is very simple and Integer can be made quite
# compatible with it, but Platypus' default definition of Integer is not, and
# if you mix Real and Integer in the variables list, you will get an error.
# The hack below relies on the fact that Platypus checks all the other
# variables against the type of the first one.  So, we make an Integer type
# that is based on Real and use that type as a variable other than the first
# variable in the list.  (Hey, don't judge me for this, okay?)

class MyInteger(Real):
    def __init__(self, range_min, range_max):
        super(Type, self).__init__()
        self.elements = range(range_min, range_max)
        self.min_value = range_min
        self.max_value = range_max - 1

    def rand(self):
        indices = list(range(1, len(self.elements)))
        random.shuffle(indices)
        return self.elements[indices[0]]

    def __str__(self):
        return "MyInteger(%d, %d)" % (len(self.elements), self.size)


# Code to run the optimization.
# .............................................................................

# Define our problem: 4 variables and 5 objectives.

problem = Problem(4, 5)
problem.function = find_parameters
problem.types[:] = [Real(7.0, 10.0),    # min_score
                    Real(0.75, 1.75),   # len_penalty_exponent
                    Real(0.75, 1.75),   # rep_penalty_exponent
                    MyInteger(25, 41)]  # len_threshold

msg('Running NSGAII')
start = time()
with ProcessPoolEvaluator(6) as evaluator:
    algorithm = NSGAII(problem, evaluator=evaluator)
    algorithm.run(50000)
msg('Done after {}s'.format(time() - start))

with open('optimize-results.txt', "w") as f:
    with redirect_stdout(f):
        for solution in algorithm.result:
            v = solution.variables
            f = solution.objectives
            msg('fp1 = {:05d}, fp2 = {:05d}, fp3 = {:05d}, fn1 = {:05d}, fn2 = {:05d} => min_score = {}, len_penalty_exp = {}, rep_penalty_exp = {}, len_threshold = {}'.
                format(f[0], f[1], f[2], f[3], f[4], v[0], v[1], v[2], v[3]))
