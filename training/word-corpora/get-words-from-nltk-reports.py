#!/usr/bin/env python3
#
# @file    get-words-from-nltk-reports.py
# @brief   Extract words from the NLTK "problem reports" corpora files
# @author  Michael Hucka
#
# <!---------------------------------------------------------------------------
# Copyright (C) 2015 by the California Institute of Technology.
# This software is part of CASICS, the Comprehensive and Automated Software
# Inventory Creation System.  For more information, visit http://casics.org.
# ------------------------------------------------------------------------- -->
#
# The purpose of this script is to take the identifier corpus from one of the
# NLTK corpora of problem reports and generate a set of unique words.  It
# discards things that have non-alphabetic characters in them (e.g., "foo.c",
# "64gb", etc.) and outputs a file containing unique words, one per line.

import os
import plac
import string
import sys

def run(input=None, output=None, min_length=6):
    if not output and not input:
        raise SystemExit('Need both input and output arguments')
    input_file = os.path.join(os.getcwd(), input)
    output_file = os.path.join(os.getcwd(), output)
    string_list = set()
    with open(input_file, 'r', errors='replace') as input:
        print('Reading {}'.format(input_file))
        for line in input.readlines():
            tokens = line.split(' ')
            strings = [x[:x.find('/')] for x in tokens]
            strings = [x for x in strings if x.isalpha()]
            string_list.update(strings)
    with open(output_file, 'w') as output:
        print('Writing {}'.format(output_file))
        for s in string_list:
            output.write(s)
            output.write('\n')
    print('Done')


run.__annotations__ = dict(
    input  = ('the corpus (input) file', 'option', 'i'),
    output = ('file where to write the results', 'option', 'o'),
)

if __name__ == '__main__':
    plac.call(run)
