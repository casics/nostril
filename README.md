Nostril
=======

<img align="right" src=".graphics/nostril.png">

Nostril is the _Nonsense String Evaluator_: a Python module that infers whether a given medium-length string of characters is likely to be random gibberish or something meaningful.

*Author*:       [Michael Hucka](http://github.com/mhucka)<br>
*Repository*:   [https://github.com/casics/nostril](https://github.com/casics/nostril)<br>
*License*:      Unless otherwise noted, this content is licensed under the [GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html) license.

☀ Introduction
-----------------------------

_Nostril_ is a Python 3 module that can be used to infer whether a given word or text string is likely to be nonsense or meaningful text.  Nostril takes a text string and returns `True` if it is probably nonsense, `False` otherwise.  _Meaningful_ in this case is not strictly defined; for Nostril, it refers to a string of characters that is probably constructed from real or real-looking English words or fragments of real words (even if the words are run togetherlikethis).  The main use case is to decide whether strings returned by source code mining methods are likely to be (e.g.) program identifiers, or random characters or other non-identifier strings.  Here are some example input strings and Nostril's assement of them:

```
getinteger: real
xywinlist: real
bunchofwords: real
whataboutthis: real
blahblahblah: real
faiwtlwex: nonsense
lksklgaiui: nonsense
```

Nostril makes a probabilistic assessment and is not always correct &ndash; see below for more information.  The approach implemented uses [n-grams](https://en.wikipedia.org/wiki/N-gram) coupled with a custom [TF-IDF](https://en.wikipedia.org/wiki/Tf–idf) weighting scheme.  Nostril is reasonably fast: once the module is loaded, on a 4 Ghz Apple OS X 10.12 computer, calling the evaluation function returns a result in 20-35 microseconds on average.

✺ Installing Nostril
-------------------

The following is probably the simplest and most direct way to install Nostril on your computer:
```
pip3 install git+https://github.com/casics/nostril.git
```

Alternatively, you can clone this repository and then run `setup.py`:
```
git clone https://github.com/casics/nostril.git
cd nostril
sudo python3 setup.py install
```

► Using Nostril
---------------

The basic usage is very simple.  Nostril provides a function named `nonsense()`.  This function takes a single text string as an argument and returns a Boolean value as a result.  Here is an example:

```python
from nostril import nonsense
if nonsense('yoursinglestringhere'):
   print("nonsense")
else:
   print("real")
```

The Nostril source code distribution also comes with a command-line program called (unsurprisingly) `nostril`.  This command-line program can take strings on the command line or (with the `-f` option) in a file, and will return nonsense-or-not assessments for each string.  It can be useful for interactive testing and experimentation.   Beware that the Nostril module takes a noticeable amount of time to load, and since the command-line program must reload the module anew each time, it is relatively slow as a means of using Nostril.  (In normal usage, your program would only load the Python module once and not incur the loading time on every call.)

Nostril ignores numbers and spaces embedded in the input string.  This was a design decision made for practicality &ndash; it simply makes Nostril a bit easier to use.  If, in your application, the presence of numbers indicates a string is definitely nonsense, then you may wish to test for that separately before passing the string to Nostril.


⚠️ Limitations
--------------

Nostril is not fool-proof; **it _will_ generate some false positive and false negatives**.  This is an unavoidable consequence of the problem domain: without direct knowledge, even a human cannot recognize a real text string in all cases.  Nostril's default trained system puts emphasis on reducing false positives (i.e., reducing how often it mistakenly labels something as nonsense) rather than false negatives, so it will sometimes report that something is not nonsense when it really is.  With its default parameter values, on dictionary words (specifically, 218,752 words from `/usr/share/dict/web2`), the default version of `nonsense()` achieves greater than 99.99% accuracy.  In tests on real identifiers extracted from actual software source code, it achieves 99.94% to 99.96% accuracy; on truly random strings, it achieves 86% accuracy.  Inspecting the errors shows that most false positives really are quite ambiguous, to the point where most false positives are random-looking, and many false negatives could be plausible identifiers.

Nostril has been trained using American English words, and is unlikely to work for other languages unchanged.  However, the underlying framework may work if it were retrained to create a new table of the n-gram frequencies.

Finally, the algorithm does not perform well on very short text, and by default Nostril imposes a lower length limit of 6 characters &ndash; strings must be longer than 6 characters or else it will raise an exception.


📚 More information
-----------------

Please see the [docs](docs/README.md) subdirectory for more information.

⁇ Getting help and support
--------------------------

If you find an issue, please submit it in [the GitHub issue tracker](https://github.com/casics/nostril/issues) for this repository.

♬ Contributing &mdash; info for developers
------------------------------------------

It may be possible to improve Nostril's performance.  I would be happy to receive your help and participation if you are interested.  Please feel free to contact me directly, or jump right in and use the standard GitHub approach of forking the repo and creating a pull request.

Everyone is asked to read and respect the [code of conduct](CONDUCT.md) when participating in this project.

❤️ Acknowledgments
------------------

Funding for this and other CASICS work has come from the [National Science Foundation](https://nsf.gov) via grant NSF EAGER #1533792 (Principal Investigator: Michael Hucka).
