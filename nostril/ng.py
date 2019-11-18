#!/usr/bin/env python3
'''N-gram named tuple for Nostril.

N-gram statistics in Nostril are stored as a Python defaultdict, whose keys
are the n-gram strings themselves and whose values are lightweight tuples.
The named tuple type is `NGramData` and it has fields for frequency
statistics and a computed IDF (inverse document frequency) measure derived
from training on example data.

Authors
-------

Michael Hucka <mhucka@caltech.edu>

Copyright
---------

Copyright (c) 2017-2019 by the California Institute of Technology.  This
software was developed as part of the CASICS project, the Comprehensive and
Automated Software Inventory Creation System. For more, visit http://casics.org.
'''

from collections import namedtuple


# Global data structures.
# .............................................................................

NGramData = namedtuple('NGramData', 'string_frequency, total_frequency, idf')
'''
In analogy to typical applications of IDF, a "document" in our case is a
text string, and the "corpus" of documents is the set of all strings used
for training.  With this in mind, the fields of NGramData are as follows:

  string_frequency = number of strings in the corpus that contain this n-gram
  total_frequency = total # of occurrences of the n-gram across all strings
  idf = IDF value for this n-gram

The difference between string_frequency and total_frequency results from
the fact that a given string may have more than one occurrence of a
particular n-gram.  Thus, string_frequency is the number of strings in the
corpus that contain the n-gram, regardless of whether the strings have more
than one instance of the n-gram, whereas total_frequency counts all n-gram
occurrences everywhere.

Note that IDF values can be precomputed based on a training set, and do
not reply on a particular string being tested during classification.  The IDF
values depend only on the frequency characteristics of a particular training
corpus.
'''
