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

Nostril (_Nonsense String Evaluator_) is a Python 3 module that can infer whether a given word or text string is likely to be nonsense or meaningful text.  A "meaningful" string of characters is one constructed from real or real-looking English words or fragments of real words (even if the words are _runtogetherlikethis_).  The main use case for Nostril is to decide whether short strings returned by source code mining methods are likely to be program identifiers (of classes, functions, variables, etc.), or random or other non-identifier strings.

Nostril is easy to use.  It provides a Python function named `nonsense()`; this function takes a single text string as an argument and returns a Boolean value as a result.  Here is an example of its use.  The following code,

```python
    from nostril import nonsense
    for s in ['bunchofwords', 'xywinlist', 'faiwtlwexu', 'asfgtqwafazfy']:
        if nonsense(s):
           print("{} is nonsense".format(s))
        else:
           print("{} is real".format(s))
```
produces the following output:

```
    bunchofwords is real
    xywinlist is real
    faiwtlwexu is nonsense
    asfgtqwafazfy is nonsense
```

Nostril also includes a command-line program named `nostril`; it will evaluate strings provided on the command line or in a file, and is useful for experimenting with Nostril or using it in command-oriented workflows.

# The need for detecting nonsense

A number of research efforts have investigated extracting and analyzing textual information contained in software artifacts [e.g., @Dit2011-fz; @Linstead2009-ky].  However, source code files can contain meaningless text, such as random text used as markers or test cases, and code extraction methods can also sometimes make mistakes and produce garbled text.  When used in processing pipelines without human intervention, it is often important to include a data cleaning step before passing tokens extracted from source code to subsequent analysis or machine learning algorithms.  Thus, a basic (and often unmentioned) step is to filter out nonsense tokens.

Discerning real identifiers from nonsense is a surprisingly difficult problem, because program identifiers often consist of words, acronyms and word fragments jammed together (e.g., `ioFlXFndrInfo`).  The resulting strings can challenge even humans.  Nostril uses a combination of (1) a prefilter that detects simple positive and negative cases using heuristic rules and (2) a custom TF-IDF [@manning2009introduction] scoring scheme that uses letter 4-grams as features.  The software includes a precomputed table of n-gram weights derived by training the system on a large set of strings constructed from concatenated American English words, real text corpora, and other inputs.  Parameter values were optimized using the evolutionary algorithm NSGA-II [@deb2000fast].

By default, Nostril is tuned to reduce false positives &ndash; it is more likely to say something is _not_ gibberish when it really might be.  This bias is motivated by Nostril's original purpose of filtering source code identifiers for machine-learning applications, where false positives would cause real identifiers to be filtered out and potentially-useful features to be missed.  However, the bias and other parameters (and the table of n-grams) can also be retrained if applications require it.

Nostril is reasonably fast: once the package is loaded,  a string evaluation takes 30&ndash;50 microseconds on average on a 4 Ghz Apple macOS computer.  Nostril is accurate: it achieves 99.76% on the the Ludiso identifier oracle [@binkley2013dataset] and 91.70% on a test set of 1,000,000 machine-generated random strings.


# Acknowledgments

This material is based upon work supported by the [National Science Foundation](https://nsf.gov) under Grant Number 1533792.  Any opinions, findings, and conclusions or recommendations expressed in this material are those of the author(s) and do not necessarily reflect the views of the National Science Foundation.


# References
