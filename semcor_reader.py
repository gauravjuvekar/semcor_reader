#!/usr/bin/env python

import nltk
import bs4
wordnet = nltk.wordnet.wordnet
wordnet.ensure_loaded()

def readsemcor(f):
    soup = bs4.BeautifulSoup(f.read(), 'html.parser')
    context = soup.find('context')
    output = []
    for para in context.findAll('p'):
        sents = []
        for sentence in para.findAll('s'):
            tokens = []
            for token in  sentence.children:
                if token == '\n':
                    continue
                if token.get('lemma') is not None:
                    lemma = token['lemma']
                    lexsn = token['lexsn']
                    lemma_key = lemma + '%' + lexsn
                    try:
                        lemma = wordnet.lemma_from_key(lemma_key)
                    except nltk.corpus.reader.wordnet.WordNetError:
                        lemma = lemma_key
                else:
                    lemma = None
                tokens.append((token.string, lemma))
            else:
                sents.append(tokens)
        else:
            output.append(sents)
    return output


if __name__ == '__main__':
    output = readsemcor(open('../datasets/semcor3.0/brownv/tagfiles/br-a06'))
    import pdb
    pdb.set_trace()
    output = output

