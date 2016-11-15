#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
reload(sys)
sys.setdefaultencoding('utf-8')



from EmeraldAI.Logic.Modules.Database import MySQL
from EmeraldAI.Logic.Modules.Database import SQlite3
"""
db = MySQL.GetDB("thesaurus")
result = MySQL.Execute(db, "SELECT term.normalized_word, term.word, term2.word FROM term, synset, term term2 WHERE synset.is_visible = 1 AND synset.id = term.synset_id AND term.synset_id AND term2.synset_id = synset.id AND term2.word = 'Bank';")
for row in result.fetchall():
    print row
MySQL.Disconnect(db)

print "-----"

litedb = SQlite3.GetDB("thesaurus_DE")
literesult = SQlite3.Execute(litedb, "SELECT term.normalized_word, term.word, term2.word FROM term, synset, term term2 WHERE synset.is_visible = 1 AND synset.id = term.synset_id AND term.synset_id AND term2.synset_id = synset.id AND term2.word = 'Bank';")
for row2 in literesult.fetchall():
    print row2
SQlite3.Disconnect(litedb)
"""

litedb = SQlite3.GetDB("thesaurus_DE")


literesult = SQlite3.Fetchall(litedb, "SELECT term.normalized_word, term.word, term2.word FROM term, synset, term term2 WHERE synset.is_visible = 1 AND synset.id = term.synset_id AND term.synset_id AND term2.synset_id = synset.id AND term2.word = 'Bank';")
print literesult

literesult = SQlite3.Fetchall(litedb, "SELECT term.normalized_word, term.word, term2.word FROM term, synset, term term2 WHERE synset.is_visible = 1 AND synset.id = term.synset_id AND term.synset_id AND term2.synset_id = synset.id AND term2.word = 'bank';")
print literesult

literesult = SQlite3.Fetchall(litedb, "SELECT term.normalized_word, term.word, term2.word FROM term, synset, term term2 WHERE synset.is_visible = 1 AND synset.id = term.synset_id AND term.synset_id AND term2.synset_id = synset.id AND term2.word  = 'bank' COLLATE NOCASE;")
print literesult

literesult = SQlite3.Fetchall(litedb, "SELECT term.normalized_word, term.word, term2.word FROM term, synset, term term2 WHERE synset.is_visible = 1 AND synset.id = term.synset_id AND term.synset_id AND term2.synset_id = synset.id AND UPPER(term2.word) = UPPER('bank');")
print literesult
SQlite3.Disconnect(litedb)


print "-----"
print "-----"
print "-----"

from EmeraldAI.Logic.Thesaurus import Thesaurus

t = Thesaurus()

print "-----"
res = t.GetSynonyms("Bank")
for x in res:
  print x

print " "

res = t.GetCategory("Bank")
for x in res:
  print x

print " "

res = t.GetOpposite("schwarz")
for x in res:
  print x

print " "

res = t.GetSynonymsAndCategory("Bank")
for x in res:
  print x



"""
Synonym + Category
SELECT term.normalized_word, term.word, term2.word, category.category_name
FROM term, synset, term term2, category_link, category
WHERE synset.is_visible = 1
AND synset.id = term.synset_id
AND term2.synset_id = synset.id
AND term2.word = 'Auge'
AND category_link.synset_id = synset.id
AND category_link.category_id = category.id;


cat:
SELECT term.normalized_word, term.word, category.category_name
FROM term, synset, category_link, category
WHERE synset.is_visible = 1
AND synset.id = term.synset_id
AND term.word = 'Auge'
AND category_link.synset_id = synset.id
AND category_link.category_id = category.id;


oppisite:
SELECT *
FROM term, term_link, term term2
WHERE term.word = 'schwarz'
AND (
(term.id = term_link.term_id
AND term_link.target_term_id = term2.id)
OR (term.id = term_link.target_term_id
AND term_link.term_id = term2.id)
);


Description of the important tables:

synset: each concept listed in the thesaurus has a row in this table. Note that
  concepts never get deleted but their is_visible column is set to 0 instead.

synset_link: connections between synsets (e.g. hypernym/hyponym). Also see link_type.

term: a word belonging to a synset. Words with more than one meaning thus have
  as many entries in this table as they have meanings. Words are not deleted in
  this table, so always do a JOIN with the synset table to check the is_visible
  column.

term_level: a term can optionally have a level like 'colloquial', 'vulgar' etc.

term_link: similar to synset_link, but represents a connection between terms
   of different synsets. Use term_link_type to find which kind of relation is
   described.

category: each synset can be in any number of categories. Use category_link for
  connecting 'synset' and 'category' tables.

word_grammar: optional term information, referenced from term.word_grammar_id
  (not used for openthesaurus.de)

"""
