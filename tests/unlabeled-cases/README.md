About this directory
====================

The contents of the file [loyola-u-ids-cleaned.txt](loyola-u-ids-cleaned.txt) consists of fragments of the identifiers from the Loyola University of Delaware Identifier Splitting Oracle (see http://www.cs.loyola.edu/~binkley/ludiso).  It was generated using the small program [utils/extract-loyola-ids-clean.py](utils/extract-loyola-ids-clean.py) in the subdirectory named [utils](utils).

The contents of the file [random-by-hand.txt](random-by-hand.txt) is a list of (semi) random strings typed by me (M. Hucka) at a keyboard.  These are as random as I could make them, but they are surely not truly random because of how keyboards are layed out and how humans tend to hit the keys. They are here because strings like these are the most difficult for the nonsense detector to classify correctly. To a human, they _look_ like random junk, but statistically speaking, I strongly suspect they are not.

The contents of the file [random_set.pklz](random_set.pklz) is a pickled list of truly random strings, generated using the code in [../../training_set.py](../../training_set.py).  The text is generated using a uniform random distribution.

The contents of the file [select-identifiers-from-osx-frameworks.txt](select-identifiers-from-osx-frameworks.txt) is a set of identifiers from Xcode developer frameworks for Mac OS X 10.12.  They were produced with the help of the utilities [../../utils/extract-symbols](../../utils/extract-symbols) and [../../utils/keep-some-symbols](../../utils/keep-some-symbols), and the following steps (here shown using `csh` shell syntax):

    foreach f (`find /Applications/Xcode.app/Contents/Developer/Platforms/ -name '*.h'`)
        extract-symbols "$f" >> /tmp/symbols
    end
    keep-some-symbols /tmp/symbols > /tmp/subset
    sort -u /tmp/subset > /tmp/sorted
