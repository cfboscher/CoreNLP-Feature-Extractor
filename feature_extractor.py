#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import csv
from lxml import etree

from Markable import *
from FeatureVector import *


def createMarkable(tree, mention):
    """
        Extract Mention information from the XML file to create a Markable Object
    """
    for sentence in tree.xpath("/root/document/sentences/sentence"):
        if sentence.get("id") == mention.find("sentence").text :

            for head in sentence.getchildren()[0].getchildren():
                if head.get("id") == mention.find("head").text:

                    markable = Markable(mention.find("text").text,
                                        int(mention.find("start").text),
                                        int(mention.find("end").text),
                                        head.find("word").text,
                                        int(mention.find("sentence").text),
                                        head.find("lemma").text,
                                        head.find("POS").text, head.find("NER").text)
                    markable.number = getNumber(markable)
                    markable.gender = getGender(markable)

                    if (markable.semantic == "DATE"):
                        markable.normalized_NER = head.find("NormalizedNER").text

                    return markable


def extractMarkables(mention_tree):
    """
        Extract markables from mentions with attributes
    """
    markables = []
    coref_index=0
    for coreference in mention_tree.xpath("/root/document/coreference/coreference"):
        for mention in coreference.getchildren():
            markable = createMarkable(mention_tree, mention)
            markable.coref_group = coref_index
            markables.append(markable)
        coref_index+=1
    return markables


def writeCSV_featureVector(vectors, document):
    """
        Create features vectors from markables and write them in a CSV
    """

    if len(sys.argv) > 1 and sys.argv[1]=='train':
        directory = 'Output/Train/'
        word = '_Train'
    else:
        directory = 'Output/Test/'
        word = '_Test'
    with open((directory+document.replace('.xml', '' )+'.csv'), 'w') as csvfile:
        fieldnames=['I', 'I_SENTENCE', 'I_BEGIN', 'I_END',
                    'J', 'J_SENTENCE', 'J_BEGIN', 'J_END',
                    'SENTENCEDIST', 'IPRONOUN', 'JPRONOUN', 'STRMATCH',
                    'SUBSTRING', 'DEF_NP', 'DEM_NP', 'HEADMATCH', 'NUMBER',
                    'SEMCLASS', 'GENDER', 'PROPERNAME', 'ALIAS', 'APPOSITIVE','COREF']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for vector in vectors:
            writer.writerow({'I':vector.i.mention,
                             'I_SENTENCE':vector.i.sentence,
                             'I_BEGIN':vector.i.word_begin,
                             'I_END':vector.i.word_end,
                             'J':vector.j.mention,
                             'J_SENTENCE':vector.j.sentence,
                             'J_BEGIN':vector.j.word_begin,
                             'J_END':vector.j.word_end,
                             'SENTENCEDIST':vector.SENTENCEDIST,
                             'IPRONOUN':vector.IPRONOUN,
                             'JPRONOUN':vector.JPRONOUN,
                             'STRMATCH':vector.STRMATCH,
                             'SUBSTRING':vector.SUBSTRING,
                             'DEF_NP':vector.DEF_NP,
                             'DEM_NP':vector.DEM_NP,
                             'HEADMATCH':vector.HEADMATCH,
                             'NUMBER':vector.NUMBER,
                             'SEMCLASS':vector.SEMCLASS,
                             'GENDER':vector.GENDER,
                             'PROPERNAME':vector.PROPERNAME,
                             'ALIAS':vector.ALIAS,
                             'APPOSITIVE':vector.APPOSITIVE,
                             'COREF':vector.COREF})


def writeCSV_Markables(markables, document):
    """
        Write Markables in a CSV File
    """

    directory = 'Output/Markables/'
    with open((directory+document.replace('.xml', '' )+'_Markables.csv'), 'w') as csvfile:

        fieldnames=['I', 'I_SENTENCE', 'BEGIN', 'END', 'HEAD', 'SENTENCE',
                    'LEMMA', 'POS', 'SEMANTIC', 'NORMALIZED_NER', 'GENDER', 'NUMBER']

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for markable in markables:
            writer.writerow({'I': markable.mention,
                             'SENTENCE': markable.sentence,
                             'BEGIN': markable.word_begin,
                             'END': markable.word_end,
                             'HEAD': markable.head,
                             'SENTENCE': markable.sentence,
                             'LEMMA': markable.lemma,
                             'POS': markable.pos,
                             'SEMANTIC': markable.semantic,
                             'NORMALIZED_NER': markable.normalized_NER,
                             'GENDER': markable.gender,
                             'NUMBER': markable.number})


def main():

    dir_path = r"../../data/WikiCoref/Output/Dcoref/XML-Post Processing/"
    documents = os.listdir(dir_path)

    for document in documents:
        print("Extracting " + document)
        mention_tree = etree.parse(dir_path + document)
        markables = extractMarkables(mention_tree)
        writeCSV_Markables(markables, document)

        vectors = []
        for i in range(len(markables)-1):
            for j in range(i+1, len(markables)):
                vectors.append(FeatureVector(markables[i], markables[j]))

        writeCSV_featureVector(vectors, document)


main()
