'''Nostril: Nonsense String Evaluator

Introduction
------------

This package implements a mechanism to infer whether text string is likely to
be meaningful text or simply nonsense.  The main use case is to decide
whether strings returned by source code mining methods are likely to be
(e.g.) program identifiers, or likely to be random characters or other
non-identifier strings.

Modules
-------

`nonsense_detector.py`: This is the core of this module; it exports the
    function `is_nonsense()` as well as some others such as
    `generate_nonsense_detector()`.  The function `is_nonsense()` takes a
    text string as a single argument and returns `True` if the string appears
    to be nonsense, `False` otherwise.  The function
    `generate_nonsense_detector()` can be used to create a different test
    function (actually, a closure) with different tunable parameter values.
    (Internally, `is_nonsense()` is created using
    `generate_nonsense_detector()` with default paramater values.)

`training.py`: Functions to create a training set of real program identifiers
    or pseudo-real program identifiers, as well as to create a set of random
    text strings.  This was used to generate n-gram statistics used by
    default by `generate_nonsense_detector()`.  It can be used to retrain the
    system.

`ng.py`: Definition of a named tuple for storing n-gram statistics.

`optimize.py`: Script to perform parameter optimization.

Usage
-----

The basic usage is very simple.  Nostril provides a single function,
`is_nonsense()`, that takes a text string as an argument and returns a
Boolean value as a result.  Here is an example:

    from nostril import is_nonsense
    result = is_nonsense('yoursinglestringhere')

Please see the documentation in nonsense_detector.py for more information.

Authors
-------

Michael Hucka <mhucka@caltech.edu>

Copyright
---------

Copyright (c) 2017 by the California Institute of Technology.  This software
was developed as part of the CASICS project, the Comprehensive and Automated
Software Inventory Creation System.  For more, visit http://casics.org.

'''

__version__ = '1.0'
__author__  = 'Michael Hucka <mhucka@caltech.edu>'
__email__   = 'mhucka@caltech.edu'
__license__ = 'GPL'

from .ng import (
    NGramData
)

from .nonsense_detector import (
    is_nonsense, generate_nonsense_detector, test_strings, test_labeled,
    ngrams, dataset_from_pickle
)
