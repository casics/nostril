Nostril<img align="right" src=".graphics/nostril.png">
=======

Nostril is the _Nonsense String Evaluator_: a Python module that infers whether a given short string of characters is likely to be random gibberish or something meaningful.

[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg?style=flat-square)](https://www.gnu.org/licenses/gpl-3.0)
[![Python](https://img.shields.io/badge/Python-3.4+-brightgreen.svg?style=flat-square)](http://shields.io)
[![Latest release](https://img.shields.io/badge/Latest_release-1.1.1-b44e88.svg?style=flat-square)](http://shields.io)
[![DOI](http://img.shields.io/badge/DOI-10.22002%20%2F%20D1.935-blue.svg?style=flat-square)](https://data.caltech.edu/records/935)
[![DOI](http://img.shields.io/badge/JOSS-10.21105%20%2f%20joss.00596-brightgreen.svg?style=flat-square)](https://doi.org/10.21105/joss.00596)

*Author*:       [Michael Hucka](http://github.com/mhucka)<br>
*Code repository*:   [https://github.com/casics/nostril](https://github.com/casics/nostril)<br>
*License*:      Unless otherwise noted, this content is licensed under the [GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html) license.

🏁 Recent news and activities
------------------------------

_May 2018_: The [JOSS paper](http://joss.theoj.org/papers/10.21105/joss.00596) has been published.  Also, Nostril release 1.1.1 has a citable DOI: [10.22002/D1.935](https://data.caltech.edu/records/935).

_April 2018_: Version 1.1.1 fixes the `requirements.txt` file so that instead of doing exact version comparisons, it only requires minimum versions.  The release also updates the documentation in [docs/explanations](docs/explanations).  Other changes (which were in release 1.1.0) include a fix to `setup.py` to make automatic installation of depencies work properly, updated installation instructions [below](#-installing-nostril), improvements to the [JOSS paper](docs/papers/joss/paper.pdf), a change to the command-line program to use the more conventional `-V` instead of `-v` for printing the version, and internal code refactoring.

Table of contents
-----------------

* [Introduction](#-introduction)
* [Please cite the paper](#%EF%B8%8F-please-cite-the-spiral-paper-and-the-version-you-use)
* [Installation instructions](#-installation-instructions)
* [Using Nostril](#-using-nostril)
* [Performance](#-performance)
* [Limitations](#️-limitations)
* [More information](#-more-information)
* [Getting help and support](#-getting-help-and-support)
* [Contributing — info for developers](#-contributing--info-for-developers)
* [Acknowledgments](#️-acknowledgments)

☀ Introduction
-----------------------------

A number of research efforts have investigated extracting and analyzing textual information contained in software artifacts.  However, source code files can contain meaningless text, such as random text used as markers or test cases, and code extraction methods can also sometimes make mistakes and produce garbled text.  When used in processing pipelines without human intervention, it is often important to include a data cleaning step before passing tokens extracted from source code to subsequent analysis or machine learning algorithms.  Thus, a basic (and often unmentioned) step is to filter out nonsense tokens.

_Nostril_ is a Python 3 module that can be used to infer whether a given word or text string is likely to be nonsense or meaningful text.  Nostril takes a text string and returns `True` if it is probably nonsense, `False` otherwise.  _Meaningful_ in this case means a string of characters that is probably constructed from real or real-looking English words or fragments of real words (even if the words are run togetherlikethis).  The main use case is to decide whether short strings returned by source code mining methods are likely to be program identifiers (of classes, functions, variables, etc.), or random characters or other non-identifier strings.  To illustrate, the following example code,

```python
from nostril import nonsense
real_test = ['bunchofwords', 'getint', 'xywinlist', 'ioFlXFndrInfo',
             'DMEcalPreshowerDigis', 'httpredaksikatakamiwordpresscom']
junk_test = ['faiwtlwexu', 'asfgtqwafazfyiur', 'zxcvbnmlkjhgfdsaqwerty']
for s in real_test + junk_test:
    print('{}: {}'.format(s, 'nonsense' if nonsense(s) else 'real'))
```
produces the following output:

```
bunchofwords: real
getint: real
xywinlist: real
ioFlXFndrInfo: real
DMEcalPreshowerDigis: real
httpredaksikatakamiwordpresscom: real
faiwtlwexu: nonsense
asfgtqwafazfyiur: nonsense
zxcvbnmlkjhgfdsaqwerty: nonsense
```

Nostril uses a combination of heuristic rules and a probabilistic assessment.  It is not always correct (see below).  It is tuned to reduce false positives: it is more likely to say something is _not_ gibberish when it really might be.  This is suitable for its intended purpose of filtering source code identifiers &ndash; a difficult problem, incidentally, because program identifiers often consist of acronyms and word fragments jammed together (e.g., "kBoPoMoFoOrderIdCID", "ioFlXFndrInfo", etc.), which can challenge even humans.  Nevertheless, on the identifier strings from the [Loyola University of Delaware Identifier Splitting Oracle](http://www.cs.loyola.edu/~binkley/ludiso), Nostril classifies over 99% correctly.

Nostril is reasonably fast: once the module is loaded, on a 4 Ghz Apple OS X 10.12 computer, calling the evaluation function returns a result in 30&ndash;50 microseconds per string on average.

♥️ Please cite the Spiral paper and the version you use
------------------------------------------------------

Article citations are **critical** for academic developers.  If you use Nostril and you publish papers about work that uses Nostril, **please cite the Nostril paper**:

<dl>
<dd>
Hucka, M. (2018). Nostril: A nonsense string evaluator written in Python. <i>Journal of Open Source Software</i>, 3(25), 596, <a href="https://doi.org/10.21105/joss.00596">https://doi.org/10.21105/joss.00596</a>
</dd>
</dl>

Please also use the DOI to indicate the specific version you use, to improve other people's ability to reproduce your results:

* Nostril release 1.1.0 &rArr; [10.22002/D1.935](https://data.caltech.edu/records/935)

✺ Installation instructions
--------------------------

The following is probably the simplest and most direct way to install Nostril on your computer:
```
sudo pip3 install git+https://github.com/casics/nostril.git
```

Alternatively, you can clone this repository and then run `setup.py`:
```
git clone https://github.com/casics/nostril.git
cd nostril
sudo python3 -m pip install .
```

Both of these installation approaches should automatically install some Python dependencies that Nostril relies upon, namely [plac](https://micheles.github.io/plac/), [tabulate](https://pypi.org/project/tabulate/), [humanize](https://pypi.org/project/humanize/), and [pytest](https://pypi.org/project/pytest/).

► Using Nostril
---------------

The basic usage is very simple.  Nostril provides a Python function named `nonsense()`.  This function takes a single text string as an argument and returns a Boolean value as a result.  Here is an example:

```python
from nostril import nonsense
if nonsense('yoursinglestringhere'):
   print("nonsense")
else:
   print("real")
```

The Nostril source code distribution also comes with a command-line program called `nostril`.  You can invoke the `nostril` command-line interface in two ways:

1. Using the Python interpreter:
    ```
    python3 -m nostril
    ```
2. On Linux and macOS systems, using the program `nostril`, which should be installed automatically by `setup.py` in a `bin` directory on your shell's command search path.  Thus, you should be able to run it normally:
    ```
    nostril
    ```

The command-line program can take strings on the command line or (with the `-f` option) in a file, and will return nonsense-or-not assessments for each string.  It can be useful for interactive testing and experimentation.  For example:

```sh
# nostril bunchofwords xywinlist ioFlXFndrInfo lasaakldfalakj
xywinlist       [real]
ioFlXFndrInfo   [real]
lasaakldfalakj  [nonsense]
xyxyxyx         [nonsense]
```


_Beware that the Nostril module takes a noticeable amount of time to load, and since the command-line program must reload the module anew each time, it is relatively slow as a means of using Nostril._  (In normal usage, your program would only load the Python module once and not incur the loading time on every call.)

Nostril ignores numbers, spaces and punctuation characters embedded in the input string.  This was a design decision made for practicality &ndash; it makes Nostril a bit easier to use.  If, for your application, non-letter characters indicates a string that is definitely nonsense, then you may wish to test for that separately before passing the string to Nostril.

Please see the [docs](docs/explanations/README.md) subdirectory for more information about Nostril and its operation.

🎯 Performance
--------------

You can verify the following results yourself by running the small test program `tests/test.py`.  The following are the results on sets of strings that are all either real identifiers or all random/gibberish text:

<table>
  <tr>
    <th></th>
    <th colspan="2"><i>Type of content</i></th>
    <th colspan="3"><i>Results</i></th>
  </tr>
  <tr>
    <th>Test case</th>
    <th>Meaningful</th>
    <th>Gibberish</th>
    <th>False pos.</th>
    <th>False neg.</th>
    <th>Accuracy</th>
  </tr>
  <tr>
    <td>/usr/share/dict/web2</td>
    <td align="right">218,752</td>
    <td align="right">0</td>
    <td align="right">89</td>
    <td align="right">0</td>
    <td align="right">99.96%</td>
  </tr>
  <tr>
    <td><a href="http://www.cs.loyola.edu/~binkley/ludiso">Ludiso oracle</a></td>
    <td align="right">2,540</td>
    <td align="right">0</td>
    <td align="right">6</td>
    <td align="right">0</td>
    <td align="right">99.76%</td>
  </tr>
  <tr>
    <td>Auto-generated random strings</td>
    <td align="right">0</td>
    <td align="right">997,636</td>
    <td align="right">0</td>
    <td align="right">82,754</td>
    <td align="right">91.70%</td>
  </tr>
  <tr>
    <td>Hand-written random strings</td>
    <td align="right">0</td>
    <td align="right">1,000</td>
    <td align="right">0</td>
    <td align="right">205</td>
    <td align="right">79.50%</td>
  </tr>
</table>

In tests on real identifiers extracted from actual software source code mined by the author in another project, Nostril's performance is as follows:

<table>
  <tr>
    <th></th>
    <th colspan="2"><i>Type of content</i></th>
    <th colspan="4"><i>Results</i></th>
  </tr>
  <tr>
    <th>Test case</th>
    <th>Meaningful</th>
    <th>Gibberish</th>
    <th>False pos.</th>
    <th>False neg.</th>
    <th>Precision</th>
    <th>Recall</th>
  </tr>
  <tr>
    <td>Strings mined from real code</td>
    <td align="right">4,261</td>
    <td align="right">364</td>
    <td align="right">6</td>
    <td align="right">5</td>
    <td align="right">98.36%</td>
    <td align="right">98.63%</td>
  </tr>
</table>

⚠️ Limitations
--------------

Nostril is not fool-proof; **it _will_ generate some false positive and false negatives**.  This is an unavoidable consequence of the problem domain: without direct knowledge, even a human cannot recognize a real text string in all cases.  Nostril's default trained system puts emphasis on reducing false positives (i.e., reducing how often it mistakenly labels something as nonsense) rather than false negatives, so it will sometimes report that something is not nonsense when it really is.

A vexing result is that this system does more poorly on supposedly "random" strings typed by a human.  I hypothesize this is because those strings may be less random than they seem: if someone is asked to type junk at random on a QWERTY keyboard, they are likely to use a lot of characters from the home row (a-s-d-f-g-h-j-k-l), and those actually turn out to be rather common in English words.  In other words, what we think of a strings "typed at random" on a keyboard are actually not that random, and probably have statistical properties similar to those of real words.  These cases are hard for Nostril, but thankfully, in real-world situations, they are rare.  This view is supported by the fact that Nostril's performance is much better on statistically random text strings generated by software.

Nostril has been trained using American English words, and is unlikely to work for other languages unchanged.  However, the underlying framework may work if it were retrained on different sample inputs.  Nostril uses uses [n-grams](https://en.wikipedia.org/wiki/N-gram) coupled with a custom [TF-IDF](https://en.wikipedia.org/wiki/Tf–idf) weighting scheme.  See the subdirectory `training` for the code used to train the system.

Finally, the algorithm does not perform well on very short text, and by default Nostril imposes a lower length limit of 6 characters &ndash; strings must be longer than 6 characters or else it will raise an exception.


📚 More information
-----------------

Please see the [docs](docs/explanations/README.md) subdirectory for more information.

⁇ Getting help and support
--------------------------

If you find an issue, please submit it in [the GitHub issue tracker](https://github.com/casics/nostril/issues) for this repository.

♬ Contributing &mdash; info for developers
------------------------------------------

Any constructive contributions &ndash; bug reports, pull requests (code or documentation), suggestions for improvements, and more &ndash; are welcome.  Please feel free to contact me directly, or even better, jump right in and use the standard GitHub approach of forking the repo and creating a pull request.

Everyone is asked to read and respect the [code of conduct](CONDUCT.md) when participating in this project.

❤️ Acknowledgments
------------------

This material is based upon work supported by the [National Science Foundation](https://nsf.gov) under Grant Number 1533792 (Principal Investigator: Michael Hucka).  Any opinions, findings, and conclusions or recommendations expressed in this material are those of the author(s) and do not necessarily reflect the views of the National Science Foundation.
    
<br>
<div align="center">
  <a href="https://www.nsf.gov">
    <img width="105" height="105" src=".graphics/NSF.svg">
  </a>
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <a href="https://www.caltech.edu">
    <img width="100" height="100" src=".graphics/caltech-round.svg">
  </a>
</div>
