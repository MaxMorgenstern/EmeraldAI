#!/usr/bin/python
# -*- coding: utf-8 -*-

import nltk

print "jojo"
#nltk.download('all')

def extract_entities(text):
    for sent in nltk.sent_tokenize(text):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            if hasattr(chunk, 'node'):
                print chunk.node, ' '.join(c[0] for c in chunk.leaves())


#extract_entities("Hallo Martin, Was mach deine Tochter Zoé heute?")


sentence = "hallo martin was macht deine tochter bernadett heute zu essen ich habe hunger"
tokens = nltk.word_tokenize(sentence)
print tokens
postag =  nltk.pos_tag(tokens)
print postag
chunk = nltk.ne_chunk(postag)
for c in chunk:
    print c

extract_entities(sentence)


