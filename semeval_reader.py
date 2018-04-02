#!/usr/bin/env python
import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.WARNING)

import nltk
import bs4
wordnet = nltk.wordnet.wordnet
wordnet.ensure_loaded()


def sepos2morphy(sepostag):
    morphy_tag = {'N':wordnet.NOUN, 'J':wordnet.ADJ,
                  'V':wordnet.VERB, 'R':wordnet.ADV,
                  'X':None}
    return morphy_tag[sepostag[:1]]


def read_para(para):
    sents = []
    for sentence in para.findAll('sentence'):
        tokens = []
        for token in  sentence.children:
            if token == '\n':
                continue
            if token.get('lemma') is not None:
                disambiguate = True
                lemma = token['lemma']
                pos = token['pos'].upper()
                pos = sepos2morphy(pos)
            else:
                disambiguate = False
                lemma = None
                pos = None
            string = token.string
            words = nltk.tokenize.word_tokenize(string.replace('_', ' '))
            tokens.append({'words': words,
                           'lemma': lemma,
                           'pos': pos,
                           'disambiguate?': disambiguate,
                           'id': token['id']})
        else:
            sents.append(tokens)
    return sents


def read_semeval15_13(f):
    soup = bs4.BeautifulSoup(f.read(), 'html.parser')
    context = soup.find('corpus')
    output = []
    for para in context.findAll('text'):
        sents = read_para(para)
        output.append(sents)
    return output


if __name__ == '__main__':
    output = read_semeval15_13(open('../data/datasets/semeval15/data/semeval-2015-task-13-en.xml'))
    import pdb
    pdb.set_trace()
    output = output

