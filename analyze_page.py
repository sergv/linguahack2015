#!/usr/bin/env python
# encoding: utf-8
"""
File:        analyze_page.py
Created:     Saturday,  3 October 2015
Author:      Sergey Vinokurov
Description:
"""

from __future__ import print_function, division

import Document

pdf_file = "/home/sergey/projects/hackaton/linguahack2015/pdfs/Кобозева-И.М.-Лингвистическая-семантика-2000.pdf"

doc = Document.Document(pdf_file, 49, 59)
doc.print_pages()
