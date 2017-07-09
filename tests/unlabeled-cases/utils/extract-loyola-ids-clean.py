#!/usr/bin/env python3
#
# @file    extract-loyola-ids-clean.py
# @brief   Extract id's from Loyola University of Delaware Identifier corpus
# @author  Michael Hucka
#
# <!---------------------------------------------------------------------------
# Copyright (C) 2015 by the California Institute of Technology.
# This software is part of CASICS, the Comprehensive and Automated Software
# Inventory Creation System.  For more information, visit http://casics.org.
# ------------------------------------------------------------------------- -->
#
# The purpose of this script is to take the identifier corpus from the
# Loyola University of Delaware Identifier Splitting Oracle (see
# http://www.cs.loyola.edu/~binkley/ludiso) and extract just the identifiers.
#
# Here's an example of an input line in the Loyola U. oracle file:
#    2692 windowspan cpp cinelerra-2.0-src windowspan 1 window-span 3 2 2 2
#
# This utility keeps only the 2nd item in each line ("windowspan").  It also
# applies a mild amount of cleaning to the identifiers, and splits identifier
# strings at hard delimiters (underscores, periods, colons) and numbers.
# Examples:
#
#   ::CreateProcess           --> CreateProcess
#   ~WaveEffect               --> WaveEffect
#   AAS_FreeAASLinkedEntities --> AAS, FreeAASLinkedEntities
#   ASTRewrite.TYPE           --> ASTRewrite, TYPE

import os
import plac
import string
import sys

def run(input=None, output=None, min_length=6):
    if not output and not input:
        raise SystemExit('Need both input and output arguments')
    input_file = os.path.join(os.getcwd(), input)
    output_file = os.path.join(os.getcwd(), output)
    id_list = set()
    delchars = str.maketrans('', '', ':~')
    replacechars = str.maketrans('_.', '  ')
    with open(input_file, 'r') as input:
        print('Reading {}'.format(input_file))
        for line in input.readlines():
            id = line.split(' ')[1]
            id = id.translate(delchars)
            id = id.translate(replacechars)
            id_list.update(id.split(' '))
    id_list = [id for id in id_list if id]
    with open(output_file, 'w') as output:
        print('Writing {}'.format(output_file))
        for id in id_list:
            output.write(id)
            output.write('\n')
    print('Done')


run.__annotations__ = dict(
    input  = ('the corpus (input) file', 'option', 'i'),
    output = ('file where to write the results', 'option', 'o'),
)

if __name__ == '__main__':
    plac.call(run)
