#!/usr/bin/python
# -*- coding: utf-8 -*-
from cachetools import cached
from EmeraldAI.Config.Config import *
from EmeraldAI.Logic.Singleton import Singleton

if(Config().Get("Database", "ThesaurusDatabaseType").lower() == "sqlite"):
    from EmeraldAI.Logic.Database.SQlite3 import SQlite3 as db
elif(Config().Get("Database", "ThesaurusDatabaseType").lower() == "mysql"):
    from EmeraldAI.Logic.Database.MySQL import MySQL as db


class Thesaurus(object):
    __metaclass__ = Singleton

    def __executePragma(self):
        db().Fetchall("PRAGMA automatic_index=OFF;")

    def __executeQuery(self, query, word):
        return db().Fetchall(query.format(lowerword=word.lower()))

    @cached(cache={})
    def GetSynonymsAndCategory(self, word):
        self.__executePragma();
        query = """SELECT term.normalized_word, term.word, category.category_name
            FROM Thesaurus_Term term, Thesaurus_Category_Link category_link, Thesaurus_Category category
            WHERE term.synset_id IN (
                SELECT synset_id
                FROM Thesaurus_Term term2, Thesaurus_Synset synset
                WHERE (term2.word = '{lowerword}' OR term2.normalized_word = '{lowerword}')
                and synset.id = term2.synset_id
                and synset.is_visible = 1
            )
            AND category_link.synset_id = term.synset_id
            AND category_link.category_id = category.id
            ORDER BY term.word"""
        return self.__executeQuery(query, word)

    #@cached(cache={})
    #def GetSynonymsAndCategory(self, word):
    #    query = """SELECT term.normalized_word, term.word, term2.word, category.category_name
    #        FROM Thesaurus_Term term, Thesaurus_Synset synset, Thesaurus_Term term2, Thesaurus_Category_Link category_link, Thesaurus_Category category
    #        WHERE synset.is_visible = 1
    #        AND synset.id = term.synset_id
    #        AND term2.synset_id = synset.id
    #        AND (term2.word = '{lowerword}' OR term2.normalized_word = '{lowerword}')
    #        AND category_link.synset_id = synset.id
    #        AND category_link.category_id = category.id
    #        ORDER BY term.word"""
    #    return self.__executeQuery(query, word)

    @cached(cache={})
    def GetSynonyms(self, word):
        self.__executePragma();
        query = """SELECT term.normalized_word, term.word
            FROM Thesaurus_Term term
            WHERE term.synset_id IN (
                SELECT synset_id
                FROM Thesaurus_Term term2, Thesaurus_Synset synset
                WHERE (term2.word = '{lowerword}' OR term2.normalized_word = '{lowerword}')
                and synset.id = term2.synset_id
                and synset.is_visible = 1
            )
            ORDER BY term.word"""
        return self.__executeQuery(query, word)

    #@cached(cache={})
    #def GetSynonyms(self, word):
    #    query = """SELECT term.normalized_word, term.word, term2.word
    #        FROM Thesaurus_Term term, Thesaurus_Synset synset, Thesaurus_Term term2
    #        WHERE synset.is_visible = 1
    #        AND synset.id = term.synset_id
    #        AND term2.synset_id = synset.id
    #        AND (term2.word = '{lowerword}' OR term2.normalized_word = '{lowerword}')
    #        ORDER BY term.word"""
    #    return self.__executeQuery(query, word)

    @cached(cache={})
    def GetCategory(self, word):
        self.__executePragma();
        query = """SELECT category.category_name
            FROM Thesaurus_Category_Link category_link, Thesaurus_Category category
            WHERE category_link.synset_id IN (
                SELECT synset_id
                FROM Thesaurus_Term term2, Thesaurus_Synset synset
                WHERE (term2.word = '{lowerword}' OR term2.normalized_word = '{lowerword}')
                and synset.id = term2.synset_id
                and synset.is_visible = 1
            )
            AND category_link.category_id = category.id"""
        return self.__executeQuery(query, word)

    #@cached(cache={})
    #def GetCategory(self, word):
    #    query = """SELECT term.normalized_word, term.word, category.category_name
    #        FROM Thesaurus_Term term,  Thesaurus_Category_Link category_link, Thesaurus_Synset synset, Thesaurus_Category category
    #        WHERE synset.is_visible = 1
    #        AND synset.id = term.synset_id
    #        AND (term.word = '{lowerword}' OR term.normalized_word = '{lowerword}')
    #        AND category_link.synset_id = synset.id
    #        AND category_link.category_id = category.id"""
    #    return self.__executeQuery(query, word)

    @cached(cache={})
    def GetOpposite(self, word):
        query = """SELECT term.word, term2.word as opposite
            FROM Thesaurus_Term term, Thesaurus_Term_Link term_link, Thesaurus_Term term2
            WHERE (term.word = '{lowerword}' OR term.normalized_word = '{lowerword}')
            AND (
            term.id = term_link.term_id AND term_link.target_term_id = term2.id
            OR term.id = term_link.target_term_id AND term_link.term_id = term2.id
            )"""
        return self.__executeQuery(query, word)
