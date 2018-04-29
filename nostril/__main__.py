#!/usr/bin/env python3
# =============================================================================
# @file    __main__.py
# @brief   Interface to run Nostril from the command line
# @author  Michael Hucka <mhucka@caltech.edu>
# @license Please see the file named LICENSE in the project directory
# @website https://github.com/casics/nostril
# =============================================================================

import os
import plac
import sys

import nostril
from nostril import *


# Main program.
# .............................................................................

@plac.annotations(
    file     = ('read input from a file',       'option', 'f'),
    trace    = ('trace scoring',                'flag',   't'),
    version  = ('print version info and exit',  'flag',   'V'),
    strings  = 'text string to test'
)

def main(file=None, trace=False, version=False, *strings):
    '''Nostril is the Nonsense String Evaluator.  It uses heuristics and
statistical methods to infer whether a given text string is likely to be
meaningful text or nonsense.  Nostril is a Python library primarily intended
to be used for identifying whether strings of characters may or may not
be program identifiers.  This command-line program provides a very simple
interface to run Nostril, for testing and exploration.

The input to this program can be a string on the command line, or (using the
-f argument) a file of strings.  If given a file of strings, it will
analyze each line in the file separately.

The optional argument --version will make this program display version
information and exit without doing anything more.

Note that Nostril has to load a large data file when it first starts up.  In
normal use, within an application program, this would only happen once.
However, in this interactive program, every time you run this program, the
data is (re)loaded, which means that startup is slow, which means that this
interactive interface will make it seem that Nostril itself is slow.  It is
not; loading the data file is normally a one-time startup cost that you would
not repeatedly incur in practice the way Nostril is normally used.

Nostril is not perfect; it will generate some false positive and false
negatives.  This is an unavoidable consequence of the problem domain: without
direct knowledge, even a human cannot recognize a real text string in all
cases.  Note that Nostril is trained on program identifiers, and performs
best with real-life program identifiers.
'''
    # Process arguments
    if version:
        print('{} version {}'.format(nostril.__title__, nostril.__version__))
        print('Author: {}'.format(nostril.__author__))
        print('URL: {}'.format(nostril.__url__))
        print('License: {}'.format(nostril.__license__))
        sys.exit()
    if not file and not strings:
        raise SystemExit('Need a file or list of strings as input argument')
    if strings and strings[0].startswith('-'):
        # If it starts with a dash and we get to this point, it's not an arg
        # recognized by plac and it's probably not input meant to be analyzed.
        raise SystemExit('Unrecognized argument "{}". (Hint: use -h to get help.)'
                         .format(strings[0]))

    # Let's do this thing.
    if file:
        if os.path.exists(file):
            with open(file) as f:
                analyze(f.readlines(), trace)
        elif os.path.exists(os.path.join(os.getcwd(), file)):
            with open(os.path.join(os.getcwd(), file)) as f:
                analyze(f.readlines(), trace)
        else:
            raise ValueError('Cannot find file "{}"'.format(file))
    else:
        analyze(strings, trace)


def analyze(string_list, trace):
    if trace:
        nonsense = generate_nonsense_detector(trace=trace)
    else:
        nonsense = generate_nonsense_detector()
    padding = max(len(s) for s in string_list)
    for s in [string.rstrip() for string in string_list]:
        if len(sanitize_string(s)) >= 6:
            print('{}  [{}]'.format(s.ljust(padding),
                                      'nonsense' if nonsense(s) else 'real'))
        else:
            print('{}  [too short to test]'.format(s.ljust(padding)))


# Main entry point.
# .............................................................................

if __name__ == '__main__':
    plac.call(main)



# Please leave the following for Emacs users.
# ......................................................................
# Local Variables:
# mode: python
# python-indent-offset: 4
# End:
