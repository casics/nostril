Notes about the files here
==========================

This directory contains corpora used as training sets for the nonsense detector.  When re-training the detector, the files in this directory are read by the code in the functions `english_word_list()` and `identifier_list()` in the `training_set` module in the parent directory.

*Important*: [training_set.pklz](training_set.pklz) contains a pickled version of the training set that was used to produce the frequency table in the file [ngram_frequencies.pklz](../ngram_frequencies.pklz) in the parent directory.  To reproduce exactly the frequencies that were stored in [ngram_frequencies.pklz](../ngram_frequencies.pklz), it is important to use [training_set.pklz](training_set.pklz) and not simply generate a new training set.  The reason is that the training set process creates a large set of random word combinations, and this affects the statistics of n-grams.

Origins of the files in this directory
--------------------------------------

* [training_set.pklz](training_set.pklz): A pickled version of the training set used to produce the frequency table in the file [ngram_frequencies.pklz](../ngram_frequencies.pklz) in the parent directory.

* [real-ids.txt](real-ids.txt): Real identifiers extracted from crawling random GitHub repositories with Python and/or Java code (and possibly other languages) in them.

* [word-corpora](word-corpora): Lists of words from different sources.  See the [README.md](word-corpora/README.md) file in the subdirectory for more information.

* [identifier-corpora](identifier-corpora): Identifiers extracted from real software.
