#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Markable:

    def __init__(self, mention, word_begin, word_end, head, sentence, lemma, pos, semantic):

        self.mention = mention
        self.word_begin = word_begin
        self.word_end = word_end
        self.head = head
        self.sentence = sentence
        self.lemma = lemma
        self.pos = pos
        self.semantic = semantic





    def show(self):
        print("Mention = ", self.mention)
        print("Begin = ", self.word_begin)
        print("End = " , self.word_end)
        print("Sentence = ", self.sentence)
        print("Head = ", self.head)
        print("Lemma = ", self.lemma)
        print("Part of Speech = ", self.pos)
        print("Semantic Class = ", self.semantic)
        print("Number = ", self.semantic)
        print("Gender = ", self.gender)
