Labeled test cases
==================

`real-not-real.csv` was derived from the strings returned by an early version of the CASICS word extractor.  The "words" included many strings that were obviously random or garbage, but their origin were unclear.  (This lead to the need to develop a tester in the first place, in fact.)

`real-not-real.csv` is a set of nearly 5000 strings that have been hand-labeled to indicate whether they should be considered junk/random, or human-generated strings (most likely identifiers in source code).  The strings may be multiple words concatenated together, as often happens when programmers create identifiers.

Update 2017-02-22
-----------------

`real-not-real.csv` started off with several strings that were all of the form `AxxxxBHelloWorldAxxxxBHelloWorld`, `AxxxxBHelloWorldAxxxxBHelloWorldAxxxxBHelloWorldAxxxxB`, etc.  It's unclear whether they _should_ be considered real identifiers or random strings. I finally removed them from the test set because I could not decide, and couldn't decide on the appropriate label.

