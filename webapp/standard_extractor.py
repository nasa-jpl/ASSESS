# -*- coding: utf-8 -*-

import re


standard_orgs={}
for line in open('standards/data/standard_orgs.txt','r').readlines():
    line=line.strip()
    abbr=line.split(' — ')[0]
    name=line.split(' — ')[1]
    standard_orgs[abbr]=name


def find_standard_ref(text):
    refs=[]
    # match abbreviations in upper case
    words=text.split()
    for i, word in enumerate(words):
        for k in standard_orgs.keys():
            if k in word:
                # check one word before and after for alphanumeric
                if i<len(words):
                    word_after=words[i+1]
                    if bool(re.search(r'\d', word_after)):
                        standard_ref=word + ' ' + word_after
                        # clean a bit
                        if standard_ref[-1]=='.' or standard_ref[-1]==',':
                            standard_ref=standard_ref[:-1]
                        standard_ref=standard_ref.replace('\\n','')
                        refs.append(standard_ref)
                elif i>=0:
                    word_before=words[i+1]
                    if bool(re.search(r'\d', word_before)):
                        refs.append(word_before+' '+word)

    return list(set(refs))

# print(find_standard_ref('(IEC) sdd67'))