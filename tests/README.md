Notes about the tests here
==========================

This doesn't use `pytest` because I couldn't resolve a problem with pickled `defaultdict` data structures.  It seems that when running in `pytest`, the dictionary unpickled by `generate_nonsense_detector` ends up having the Python data type `tuple` instead of `defauldict`.

I gave up trying to solve that problem, and decided to create a simple test function instead.  This is the file `test.py`.  Simply run it on the command line and it will execute a number of tests.
