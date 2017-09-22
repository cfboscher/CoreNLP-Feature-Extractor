#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Markable:

    def __init__(self, mention, nb_begin, word_begin, nb_end, word_end, head,
                 sentence, lemma, pos, semantic):

        self.mention = mention
        self.nb_begin = nb_begin
        self.word_begin = word_begin
        self.nb_end = nb_end
        self.word_end = word_end
        self.head = head
        self.sentence = sentence
        self.lemma = lemma
        self.pos = pos
        self.semantic = semantic
        self.normalized_NER = self.semantic
        self.number = 'UNKNOWN'
        self.gender = 'UNKNOWN'

    def __lt__(self, other):
        return (self.sentence < other.sentence and
                self.word_begin < other.word_begin)

    def show(self):
        print("Mention = ", self.mention)
        print("Begin = ", self.word_begin)
        print("End = ", self.word_end)
        print("Sentence = ", self.sentence)
        print("Head = ", self.head)
        print("Lemma = ", self.lemma)
        print("Part of Speech = ", self.pos)
        print("Semantic Class = ", self.semantic)
        print("Number = ", self.semantic)
        print("Gender = ", self.gender)
