#!/usr/bin/python
# -*- coding: utf-8 -*-
import nltk
#nltk.download()

sentence = """Guten Morgen. Die Katze liegt auf der Matte."""

tokens = nltk.word_tokenize(sentence)
print tokens

tagged = nltk.pos_tag(tokens)
print tagged


from nltk.stem.snowball import GermanStemmer

wordnet_lemmatizer = GermanStemmer()
print wordnet_lemmatizer.stem("Hunde")
print wordnet_lemmatizer.stem("hattest")
print wordnet_lemmatizer.stem("hatten")
print wordnet_lemmatizer.stem("schwimmen")

"""
from nltk.stem.porter import PorterStemmer
porter_stemmer = PorterStemmer()
print porter_stemmer.stem("hattest")
print porter_stemmer.stem("hatten")
print porter_stemmer.stem("schwimmen")


from nltk.stem.lancaster import LancasterStemmer
lancaster_stemmer = LancasterStemmer()
print lancaster_stemmer.stem("hattest")
print lancaster_stemmer.stem("hatten")
print lancaster_stemmer.stem("schwimmen")

from nltk.stem import SnowballStemmer
snowball_stemmer = SnowballStemmer("german")
print snowball_stemmer.stem("hattest")
print snowball_stemmer.stem("hatten")
print snowball_stemmer.stem("schwimmen")


from nltk.stem import WordNetLemmatizer
wordnet_lemmatizer = WordNetLemmatizer()
print wordnet_lemmatizer.lemmatize("Hunde")
print wordnet_lemmatizer.lemmatize("hattest")
print wordnet_lemmatizer.lemmatize("hatten")
print wordnet_lemmatizer.lemmatize("schwimmen")


from nltk import wordpunct_tokenize
from nltk.corpus import stopwords

#stopwords.fileids()
def _calculate_languages_ratios(text):
    languages_ratios = {}

    tokens = wordpunct_tokenize(text)
    words = [word.lower() for word in tokens]

    # Compute per language included in nltk number of unique stopwords appearing in analyzed text
    for language in stopwords.fileids():
        stopwords_set = set(stopwords.words(language))
        words_set = set(words)
        common_elements = words_set.intersection(stopwords_set)

        languages_ratios[language] = len(common_elements) # language "score"

    return languages_ratios

def detect_language(text):
    ratios = _calculate_languages_ratios(text)

    most_rated_language = max(ratios, key=ratios.get)

    return most_rated_language

print detect_language("Das ist ein Test")
print detect_language("This is a test")
print detect_language("Hola que tal")
"""



"""
Die/DT/B-NP/O
Katze/NN/I-NP/O
liegt/VB/B-VP/O
auf/IN/B-PP/B-PNP
der/DT/B-NP/I-PNP
Matte/NN/I-NP/I-PNP
"""

"""
Alphabetical list of part-of-speech tags used in the Penn Treebank Project:

Number
Tag
Description
1.	CC	Coordinating conjunction
2.	CD	Cardinal number
3.	DT	Determiner
4.	EX	Existential there
5.	FW	Foreign word
6.	IN	Preposition or subordinating conjunction
7.	JJ	Adjective
8.	JJR	Adjective, comparative
9.	JJS	Adjective, superlative
10.	LS	List item marker
11.	MD	Modal
12.	NN	Noun, singular or mass
13.	NNS	Noun, plural
14.	NNP	Proper noun, singular
15.	NNPS	Proper noun, plural
16.	PDT	Predeterminer
17.	POS	Possessive ending
18.	PRP	Personal pronoun
19.	PRP$	Possessive pronoun
20.	RB	Adverb
21.	RBR	Adverb, comparative
22.	RBS	Adverb, superlative
23.	RP	Particle
24.	SYM	Symbol
25.	TO	to
26.	UH	Interjection
27.	VB	Verb, base form
28.	VBD	Verb, past tense
29.	VBG	Verb, gerund or present participle
30.	VBN	Verb, past participle
31.	VBP	Verb, non-3rd person singular present
32.	VBZ	Verb, 3rd person singular present
33.	WDT	Wh-determiner
34.	WP	Wh-pronoun
35.	WP$	Possessive wh-pronoun
36.	WRB	Wh-adverb
"""
