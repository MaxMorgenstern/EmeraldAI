#!/usr/bin/python
# -*- coding: utf-8 -*-
from EmeraldAI.Logic.Modules.Database import SQlite3

class Thesaurus(object):
  database = None

  def __init__(self):
    self.database = SQlite3.GetDB("thesaurus_DE")


  def GetSynonymsAndCategory(self, word, normalized=False):
    queryWordCol = "word"
    if(normalized):
        queryWordCol = "normalized_word"

    query = """SELECT term.normalized_word, term.word, term2.word, category.category_name
            FROM term, synset, term term2, category_link, category
            WHERE synset.is_visible = 1
            AND synset.id = term.synset_id
            AND term2.synset_id = synset.id
            AND (term2.{col} = '{lowerword}' OR term2.{col} = '{titleword}')
            AND category_link.synset_id = synset.id
            AND category_link.category_id = category.id
            ORDER BY term.word;"""
    return SQlite3.Fetchall(self.database, query.format(col=queryWordCol, lowerword=word.lower(), titleword=word.decode('utf8').title()))


  def GetSynonyms(self, word, normalized=False):
    queryWordCol = "word"
    if(normalized):
        queryWordCol = "normalized_word"

    query = """SELECT term.normalized_word, term.word, term2.word
            FROM term, synset, term term2
            WHERE synset.is_visible = 1
            AND synset.id = term.synset_id
            AND term.synset_id
            AND term2.synset_id = synset.id
            AND (term2.{col} = '{lowerword}' OR term2.{col} = '{titleword}')
            ORDER BY term.word;"""
    return SQlite3.Fetchall(self.database, query.format(col=queryWordCol, lowerword=word.lower(), titleword=word.decode('utf8').title()))


  def GetCategory(self, word, normalized=False):
    queryWordCol = "word"
    if(normalized):
        queryWordCol = "normalized_word"

    query = """SELECT term.normalized_word, term.word, category.category_name
            FROM term, synset, category_link, category
            WHERE synset.is_visible = 1
            AND synset.id = term.synset_id
            AND (term.{col} = '{lowerword}' OR term.{col} = '{titleword}')
            AND category_link.synset_id = synset.id
            AND category_link.category_id = category.id;"""
    return SQlite3.Fetchall(self.database, query.format(col=queryWordCol, lowerword=word.lower(), titleword=word.decode('utf8').title()))


  def GetOpposite(self, word, normalized=False):
    queryWordCol = "word"
    if(normalized):
        queryWordCol = "normalized_word"

    query = """SELECT term.word, term2.word
            FROM term, term_link, term term2
            AND (term.{col} = '{lowerword}' OR term.{col} = '{titleword}')
            AND (
              (term.id = term_link.term_id AND term_link.target_term_id = term2.id)
              OR (term.id = term_link.target_term_id AND term_link.term_id = term2.id)
            );"""
    return SQlite3.Fetchall(self.database, query.format(col=queryWordCol, lowerword=word.lower(), titleword=word.decode('utf8').title()))
