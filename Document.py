#!/usr/bin/env python
# encoding: utf-8
"""
File:        Document.py
Created:     Saturday,  3 October 2015
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

from pdfminer.layout import LTPage, LTContainer, LAParams, LTTextContainer
from pdfminer.converter import PDFPageAggregator

import pdfminer.layout as layout

class Paragraph(object):
    """Paragraph object containing list of words and the actual text."""

    def __init__(self, text, total_number_of_pages_so_far):
        super(Paragraph, self).__init__()
        assert type(text) in [str, unicode], "Expected text of type str or unicode but got text of type {}".format(type(text))
        self.text    = text
        self.words   = text.split()
        self.numbers = set()
        for w in self.words:
            if w.isdigit():
                n = int(w)
                if n <= total_number_of_pages_so_far:
                    self.numbers.add(n)

# TODO: add convenient iteration over paragraphs
class Page(object):
    """Page object"""

    def __init__(self, layout, total_number_of_pages_so_far):
        super(Page, self).__init__()
        assert type(layout) is LTPage
        self.paragraphs = []
        self.numbers    = set()
        for container in get_all_nodes_of_type(layout, LTTextContainer):
            par = Paragraph(container.get_text(), total_number_of_pages_so_far)
            self.paragraphs.append(par)
            self.numbers = self.numbers.union(par.numbers)

        # xs = [ x.get_text() for x in ]
        # # xs = [ x.get_text() for x in layout if type(x) is LTTextBoxHorizontal ]
        # for i, words in enumerate(xs):
        #     print(i)
        #     print(" ".join(words))

class Document(object):
    """Document object"""

    def __init__(self, pdf_file, start_page = 0, last_page = None):
        super(Document, self).__init__()
        # dictionary mapping *real* page numbers to actual pages
        self.pages_dict = dict()
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

        pages = []
        for page_number, page in enumerate(PDFPage.create_pages(document)):
            if start_page <= page_number and \
               (last_page is None or page_number <= last_page):
                interpreter.process_page(page)
                # receive the LTPage object for the page.
                layout = device.get_result()
                # TODO: we're assuming that page_number is strictly greater than
                # the "real" page number mentioned of the page. This is not
                # always the case.
                pages.append(Page(layout, start_page + page_number))
        if len(pages) == 0:
            raise RuntimeError("No pages collected from {}".format(pdf_file))

        all_numbers_of_pages = map(lambda page: page.numbers, pages)
        page_offset = infer_page_offset(all_numbers_of_pages, 2)
        if page_offset is None:
            for pageno, page in enumerate(pages):
                print_page(start_page + pageno, page)
            raise RuntimeError("failed to infer page offset from numbers {}".format(all_numbers_of_pages))
        real_page_offset = page_offset
        for i, p in enumerate(pages):
            real_page_number = i + real_page_offset
            self.pages_dict[real_page_number] = p
        # # if len(pages) == 0:
        # #     raise RuntimeError("No pages collected from {}".format(pdf_file))
        # page_offset_candidates = set()
        # i = 0
        # while i < len(pages):
        #     next_candidates = set([ x + 1 for x in page_offset_candidates ])
        #     next_candidates.intersect(pages[i].numbers)

    def print_pages(self):
        for real_pageno, page in self.pages_dict.iteritems():
            print_page(real_pageno, page)

def print_page(pageno, page):
    # print("Page #{}".format(real_pageno))
    # # for par in page.paragraphs:
    # #     print("    {}".format(par.text.encode("utf8")))
    print("Page #{} of type {}".format(pageno, type(page)))
    print("  Numbers")
    print("    {}".format(page.numbers))
    for j, par in enumerate(page.paragraphs):
        # print("  Words {}".format(j))
        # print("    {}".format(par.words))
        print("  Paragraph {}".format(j))
        print("    {}".format(par.text.encode("utf8")))
        print("  Paragraph {} lines".format(j))
        for line in par.text.encode("utf8").split("\n"):
            print("    {}".format(line))

# Parameters:
# accuracy - how many consecutive pages should contain increasing sequence
# in order to consider it a page numbers.
def infer_page_offset(page_number_sets, accuracy):
    candidates = set()
    i = 0
    while i < len(page_number_sets) and len(candidates) == 0:
        candidates = page_number_sets[i]
        i          += 1
    consecutive_increases = 0
    while i < len(page_number_sets):
        next_candidates = set([ x + 1 for x in candidates ])
        number_set      = page_number_sets[i]
        candidates      = next_candidates.intersection(number_set)
        if len(candidates) == 0:
            candidates = number_set
        if len(candidates) == 1:
            consecutive_increases += 1
            if consecutive_increases == accuracy:
                real_page_number = candidates.pop()
                return real_page_number - i
        i += 1
    return None

def get_all_nodes_of_type(page, type_to_find):
    assert type(page) is LTPage
    def go(node, result):
        if issubclass(type(node), type_to_find):
            result.append(node)
        elif issubclass(type(node), LTContainer):
            for child in node:
                go(child, result)
        return result
    return go(page, [])

if __name__ == "__main__":
    pdf_file = "/home/sergey/projects/hackaton/linguahack2015/pdfs/Кобозева-И.М.-Лингвистическая-семантика-2000.pdf"

    # doc = Document(pdf_file, 49, 59)
    # doc.print_pages()

    index = Document(pdf_file, 331, 332)
    index.print_pages()

    # # with list(PDFPage.create_pages(document))[i] as page_number, page:
    # i = 50
    # for page_number, page in enumerate(PDFPage.create_pages(document)):
    #     if page_number == i:
    #         interpreter.process_page(page)
    #         # receive the LTPage object for the page.
    #         layout = device.get_result()
    #         print("page #{}, layout = {}".format(page_number, layout))
    #         xs = [ x.get_text() for x in get_all_nodes_of_type(layout, LTTextContainer) ]
    #         # xs = [ x.get_text() for x in layout if type(x) is LTTextBoxHorizontal ]
    #         for i, words in enumerate(xs):
    #             print(i)
    #             print(" ".join(words))

