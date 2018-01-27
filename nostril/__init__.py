'''Nostril: Nonsense String Evaluator

Introduction
------------

This package implements a mechanism to infer whether text string is likely to
be meaningful text or simply nonsense.  "Meaningful" in this case is not
strictly defined; for Nostril, it refers to a string of characters that is
probably constructed from real or real-looking English words or fragments of
real words (even if the words are run togetherlikethis).  The main use case
is to decide whether strings returned by source code mining methods are
likely to be (e.g.) program identifiers, or random characters or other
non-identifier strings.  Nostril makes a probabilistic assessment and is not
always correct -- see below for more information.

Usage
-----

The basic usage is very simple.  Nostril provides a single function,
`nonsense()`, that takes a text string as an argument and returns a Boolean
value as a result.  Here is an example:

    from nostril import nonsense
    if nonsense('yoursinglestringhere'):
       print("nonsense")
    else:
       print("real")

Nostril ignores numbers and spaces embedded in the input string.  This was a
design decision made for practicality -- it simply makes Nostril a bit easier
to use.  If, in your application, the presence of numbers indicates a string
is definitely nonsense, then you may wish to test for that separately before
passing the string to Nostril.

The function used to clean up strings before they are assessed is called
`sanitize_string()` and is exported so that users of the Nostril module can
call it themselves if needed.

Limitations
-----------

Nostril is not fool-proof; it WILL generate some false positive and false
negatives.  This is an unavoidable consequence of the problem domain: without
direct knowledge, even a human cannot recognize a real text string in all
cases.  Nostril's default trained system puts emphasis on reducing false
positives (i.e., reducing how often it mistakenly labels something as
nonsense) rather than false negatives, so it will sometimes report that
something is not nonsense when it really is.

Nostril has been trained using American English words, and is unlikely to
work for other languages unchanged.  However, the underlying framework may
work if it were retrained to create a new table of the n-gram frequencies.

Finally, the algorithm does not perform well on very short text, and by
default Nostril imposes a lower length limit of 6 characters -- strings must
be longer than 6 characters or else it will raise an exception.

Modules
-------

`nonsense_detector`: This is the core of this module; it exports the
    function `nonsense()` as well as some others such as
    `generate_nonsense_detector()`.  The function `nonsense()` takes a
    text string as a single argument and returns `True` if the string appears
    to be nonsense, `False` otherwise.  The function
    `generate_nonsense_detector()` can be used to create a different test
    function (actually, a closure) with different tunable parameter values.
    (Internally, `nonsense()` is created using
    `generate_nonsense_detector()` with default paramater values.)

`ng`: Definition of a named tuple for storing n-gram statistics.

Authors
-------

Michael Hucka <mhucka@caltech.edu>

Copyright
---------

Copyright (c) 2017 by the California Institute of Technology.  This software
was developed as part of the CASICS project, the Comprehensive and Automated
Software Inventory Creation System.  For more, visit http://casics.org.
'''

from .__version__ import *
from .ng import NGramData
from .nonsense_detector import (
    nonsense, generate_nonsense_detector, test_unlabeled, test_labeled,
    ngrams, dataset_from_pickle, sanitize_string
)
