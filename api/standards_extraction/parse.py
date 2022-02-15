# -*- coding: utf-8 -*-

import re
import io
import os
import pdfplumber


def parse_pdf(pdf, cache=False):
    filepath = "./data/" + pdf.filename
    if cache and os.path.exists(filepath + "_parsed.txt"):
        return str(open(filepath + "_parsed.txt", "r").read())
    # Below should throw an "PDFSyntaxError" error if this is an invalid pdf. FastAPI should already catch this.
    with pdfplumber.open(pdf) as pdf:
        text = [page.extract_text() for page in pdf.pages]
        full_str = (" ".join(text))
    if cache:
        pdf.write(filepath)
        file = open(filepath + "_parsed.txt", "wb")
        file.write(full_str)
        file.close()
    return(full_str)


def find_standard_ref(text):
    standard_orgs = {}
    for line in io.open("standards_extraction/standard_orgs.txt", mode="r", encoding="utf-8").readlines():
        line = line.strip()
        abbr = line.split(' — ')[0]
        name = line.split(' — ')[1]
        standard_orgs[abbr] = name
    refs = []
    # match abbreviations in upper case
    words = text.split()
    for i, word in enumerate(words):
        for k in standard_orgs.keys():
            if k in word:
                # check one word before and after for alphanumeric
                if i < len(words):
                    word_after = words[i+1]
                    if bool(re.search(r'\d', word_after)):
                        standard_ref = word + ' ' + word_after
                        # clean a bit
                        if standard_ref[-1] == '.' or standard_ref[-1] == ',':
                            standard_ref = standard_ref[:-1]
                        standard_ref = standard_ref.replace('\\n', '')
                        refs.append(standard_ref)
                elif i >= 0:
                    word_before = words[i+1]
                    if bool(re.search(r'\d', word_before)):
                        refs.append(word_before+' '+word)

    return list(set(refs))

# print(find_standard_ref('(IEC) sdd67'))
