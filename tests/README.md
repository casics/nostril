Notes about the tests here
==========================

This doesn't use `pytest` because I couldn't resolve a problem with pickled `defaultdict` data structures.  It seems that when running in `pytest`, the dictionary unpickled by `generate_nonsense_detector` ends up having the Python data type `tuple` instead of `defauldict`.  I gave up trying to solve that problem, and decided to create a simple test function instead.  This is the file `test.py`.

Simply run `test.py` and it will execute a number of tests and print the results, along with information about the expected values.  Here is an example at the time of this writing, but note that evolution of the code may cause the exact output to change from what is shown here:

```csh
# python3 -m test
Testing labeled cases -- expect 6 false positives, 5 false negatives:
4,625 tested in 0.38s, 0 skipped -- 98.36% precision, 98.63% recall, 359 true pos, 4,255 true neg, 6 false pos, 5 false neg

Testing against valid Ludiso cases -- expect 6 false positives:
99.76% accuracy (2,540 tested in 0.10s, 0 true pos, 2,534 true neg, 6 false pos, 0 false neg, 123 skipped)

Testing against valid OSX identifiers -- expect 5 false positives:
99.98% accuracy (25,941 tested in 1.34s, 0 true pos, 25,936 true neg, 5 false pos, 0 false neg, 234 skipped)

Testing against hand-written random strings -- expect 79.50% accuracy:
79.50% accuracy (1,000 tested in 0.03s, 795 true pos, 0 true neg, 0 false pos, 205 false neg, 0 skipped)

Recall test: /usr/share/dict/web2 -- expect 89 false positives positives (99.96% correct):
99.96% accuracy (218,752 tested in 5.35s, 0 true pos, 218,663 true neg, 89 false pos, 0 false neg, 17,134 skipped)

Recall test: valid identifiers from source code -- expect 7 false positives:
99.83% accuracy (4,020 tested in 0.27s, 0 true pos, 4,013 true neg, 7 false pos, 0 false neg, 0 skipped)

Testing against machine-generated random strings -- expect 91.70% accuracy:
91.70% accuracy (997,636 tested in 36.22s, 914,882 true pos, 0 true neg, 0 false pos, 82,754 false neg, 2,364 skipped)
```
