#!/usr/bin/env python
# encoding: utf-8
"""
File:        search.py
Created:     Saturday,  3 October 2015
Description:
"""

from __future__ import print_function, division


import argparse

parser = argparse.ArgumentParser(
    description = "Take pdf and a word, produce all paragraphs that mention this word")

parser.add_argument("-w", "--word", dest="word", required=True,
                    help="word to search for")
parser.add_argument("-p", "--pdf", dest="pdf_file", required=True,
                    help="pdf file to search in")
parser.add_argument("-d", "--debug", required=False, action="store_true", default=False,
                    help="run in verbose debug mode")

args = parser.parse_args()

if args.debug:
    print("Searching for {} in {}".format(args.word, args.pdf_file))


print("Done")
