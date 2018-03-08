#!/usr/bin/env python
import nltk
import bs4
wordnet = nltk.wordnet.wordnet
wordnet.ensure_loaded()


def read_para(para):
    sents = []
    for sentence in para.findAll('s'):
        tokens = []
        for token in  sentence.children:
            if token == '\n':
                continue
            if token.get('lemma') is not None:
                lemma = token['lemma']
                lexsn = token['lexsn']
                pos = token['pos'][0].lower()
                if pos not in ('a', 'n', 'v'):
                    pos = None
                lemma_key = lemma + '%' + lexsn
                try:
                    wn_lemma = wordnet.lemma_from_key(lemma_key)
                except nltk.corpus.reader.wordnet.WordNetError:
                    wn_lemma = lemma_key
            else:
                wn_lemma = None
                lemma = None
                pos = None
            string = token.string
            words = nltk.tokenize.word_tokenize(string.replace('_', ' '))
            tokens.append({'words': words,
                           'true_sense': wn_lemma,
                           'lemma': lemma,
                           'pos': pos})
        else:
            sents.append(tokens)
    return sents


def read_semcor(f):
    soup = bs4.BeautifulSoup(f.read(), 'html.parser')
    context = soup.find('context')
    output = []
    for para in context.findAll('p'):
        sents = read_para(para)
        output.append(sents)
    return output


if __name__ == '__main__':
    output = read_semcor(open('../datasets/semcor3.0/brownv/tagfiles/br-a06'))
    import pdb
    pdb.set_trace()
    output = output

