#!/usr/bin/env python
# encoding: utf-8
"""
File:        analyze_page.py
Created:     Saturday,  3 October 2015
Author:      Sergey Vinokurov
Description:
"""

from __future__ import print_function, division


from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice

from pdfminer.layout import LAParams, LTTextBoxHorizontal
from pdfminer.converter import PDFPageAggregator

import pdfminer.layout as layout

pdf_file = "/home/sergey/projects/hackaton/linguahack2015/pdfs/Кобозева-И.М.-Лингвистическая-семантика-2000.pdf"

# Open a PDF file.
fp = open(pdf_file, 'rb')
# Create a PDF parser object associated with the file object.
parser = PDFParser(fp)
# Create a PDF document object that stores the document structure.
# Supply the password for initialization.
document = PDFDocument(parser)
# Check if the document allows text extraction. If not, abort.
if not document.is_extractable:
    raise PDFTextExtractionNotAllowed
# Create a PDF resource manager object that stores shared resources.
rsrcmgr = PDFResourceManager()

# Set parameters for analysis.
laparams = LAParams()
# Create a PDF page aggregator object.
device = PDFPageAggregator(rsrcmgr, laparams=laparams)
interpreter = PDFPageInterpreter(rsrcmgr, device)

# with list(PDFPage.create_pages(document))[i] as pageNumber, page:
i = 50
for pageNumber, page in enumerate(PDFPage.create_pages(document)):
    if pageNumber == i:
        interpreter.process_page(page)
        # receive the LTPage object for the page.
        layout = device.get_result()
        print("page #{}, layout = {}".format(pageNumber, layout))
        xs = [ x.get_text() for x in layout if type(x) is LTTextBoxHorizontal ]
        for i, x in enumerate(xs):
            print(i)
            print(x)
