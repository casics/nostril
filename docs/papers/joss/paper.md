---
title: 'Nostril: A nonsense string evaluator written in Python'
tags:
- mining source repositories
- identifiers
- text processing
- inference
authors:
- name: Michael Hucka
  orcid: 0000-0001-9105-5960
  affiliation: 1
affiliations:
- name: Department of Computing and Mathematical Sciences, California Institute of Technology, Pasadena, CA 91125, USA
  index: 1
date: 6 February 2018
bibliography: paper.bib
---

# Summary

Nostril (_Nonsense String Evaluator_) is a Python 3 module that can infer whether a given word or text string is likely to be nonsense or meaningful text.  Nostril takes a text string as input and returns `True` if it is probably nonsense, `False` otherwise.  A "meaningful" string of characters is one constructed from real or real-looking English words or fragments of real words (even if the words are _runtogetherlikethis_).  The main use case is to decide whether short strings returned by source code mining methods are likely to be program identifiers (of classes, functions, variables, etc.), or random or other non-identifier strings.

Discerning real identifiers from nonsense is a surprisingly difficult problem, because program identifiers often consist of words, acronyms and word fragments jammed together (e.g., `ioFlXFndrInfo`) and the result can challenge even humans.  Out of the box, Nostril is tuned to reduce false positives &ndash; it is more likely to say something is _not_ gibberish when it really might be.  This bias is motivated by its original purpose of filtering source code identifiers for machine-learning applications, where false positives would cause real identifiers to be filtered out and potentially useful features to be missed.

Internally, Nostril uses a combination of (1) a prefilter that detects simple cases using heuristic rules and (2) a custom TF-IDF  [@manning2009introduction] scoring scheme that uses letter 4-grams as features.  Nostril includes a precomputed table of n-gram weights that were derived by training the system on a large set of strings constructed from concatenated American English words, real text corpora, and other inputs.  Parameter values were optimized using the evolutionary algorithm NSGA-II [@deb2000fast].  Nostril works out of the box, but it can also be retrained if applications require it.

Nostril is reasonably fast: once the package is loaded,  a string evaluation takes 30&ndash;50 microseconds on average on a 4 Ghz Apple macOS computer.  Nostril is accurate: it achieves 99.76% on the the Ludiso identifier oracle [@binkley2013dataset] and 91.70% on a test set of 1,000,000 machine-generated random strings.


# References
