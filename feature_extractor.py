#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import os
import pandas as pd
from Markable import *
from FeatureVector import *


from lxml import etree


def createMarkable(tree, mention):
    """
        Extract Mention information from the XML file to create a Markable
    """
    for sentence in tree.xpath("/root/document/sentences/sentence"):

        if sentence.get("id") == mention.find("sentence").text:

            for head in sentence.getchildren()[0].getchildren():
                if head.get("id") == mention.find("head").text:
                    head_token = head

            for begin in sentence.getchildren()[0].getchildren():
                if begin.get("id") == mention.find("start").text:
                    begin_token = begin

            for end in sentence.getchildren()[0].getchildren():
                if end.get("id") == mention.find("end").text:
                    end_token = end
                else:
                    end_token = begin_token

            # for end in sentence.getchildren()[0].getchildren()

            markable = Markable(mention.find("text").text,
                                int(mention.find("start").text),
                                begin_token.find("word").text,
                                int(mention.find("sentence").text),
                                end_token.find("word").text,
                                head_token.find("word").text,
                                int(mention.find("sentence").text),
                                head_token.find("lemma").text,
                                head_token.find("POS").text,
                                head_token.find("NER").text)
            markable.number = getNumber(markable)
            markable.gender = getGender(markable)

            if (markable.semantic == "DATE"):
                markable.normalized_NER = head_token.find("NormalizedNER").text

            return markable


def extractMarkables(mention_tree):
    """
        Extract markables from mentions with attributes
    """
    markables = []
    coref_index = 0
    for coreference in mention_tree.xpath("/root/document/coreference/coreference"):
        for mention in coreference.getchildren():
            markable = createMarkable(mention_tree, mention)
            markable.coref_group = coref_index
            markables.append(markable)
        coref_index += 1
    return markables


def extractVectors(markables):
    """
        Extract feature vectors for pairs of markables
    """
    vectors = []
    for i in range(len(markables)-1):
        for j in range(i+1, len(markables)):
            vectors.append(FeatureVector(markables[i], markables[j]))
    return vectors


def writeCSV_featureVector(vectors, document):
    """
        Create features vectors from markables and write them in a CSV
    """

    directory = 'Output/Documents/'

    with open((directory+document.replace('.xml', '')+'.csv'), 'w') as csvfile:
        fieldnames = ['LABEL', 'I', 'I_SENTENCE', 'J', 'SENTENCEDIST',
                      'J_SENTENCE', 'IPRONOUN', 'JPRONOUN', 'STRMATCH',
                      'SUBSTRING', 'DEF_NP', 'DEM_NP', 'HEADMATCH', 'NUMBER',
                      'SEMCLASS', 'GENDER', 'PROPERNAME', 'ALIAS',
                      'APPOSITIVE', 'COREF']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        # writer.writeheader()

        for vector in vectors:
            writer.writerow({
                             'LABEL': vector.i.mention + ' | ' +
                                                         vector.j.mention,
                             'I': vector.i.mention,
                             'I_SENTENCE': vector.i.sentence,
                             'J': vector.j.mention,
                             'J_SENTENCE': vector.j.sentence,
                             'SENTENCEDIST': vector.SENTENCEDIST,
                             'IPRONOUN': vector.IPRONOUN,
                             'JPRONOUN': vector.JPRONOUN,
                             'STRMATCH': vector.STRMATCH,
                             'SUBSTRING': vector.SUBSTRING,
                             'DEF_NP': vector.DEF_NP,
                             'DEM_NP': vector.DEM_NP,
                             'HEADMATCH': vector.HEADMATCH,
                             'NUMBER': vector.NUMBER,
                             'SEMCLASS': vector.SEMCLASS,
                             'GENDER': vector.GENDER,
                             'PROPERNAME': vector.PROPERNAME,
                             'ALIAS': vector.ALIAS,
                             'APPOSITIVE': vector.APPOSITIVE,
                             'COREF': vector.COREF})


def writeCSV_Markables(markables, document):
    """
        Write Markables in a CSV File
    """

    directory = 'Output/Markables/'
    with open((directory+document.replace('.xml', '')+'_Markables.csv'), 'w') as csvfile:

        fieldnames = ['LABEL', 'SENTENCE', 'BEGIN', 'END', 'HEAD', 'SENTENCE',
                      'LEMMA', 'POS', 'SEMANTIC', 'NORMALIZED_NER', 'GENDER',
                      'NUMBER']

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for markable in markables:
            writer.writerow({'LABEL': markable.mention,
                             'SENTENCE': markable.sentence,
                             'BEGIN': markable.word_begin,
                             'END': markable.word_end,
                             'HEAD': markable.head,
                             'LEMMA': markable.lemma,
                             'POS': markable.pos,
                             'SEMANTIC': markable.semantic,
                             'NORMALIZED_NER': markable.normalized_NER,
                             'GENDER': markable.gender,
                             'NUMBER': markable.number})


def mergeCSV_Corpus():
    path = 'Output/Documents/'
    documents = os.listdir(path)

    merged = pd.read_csv(path + documents[0])
    for i in range(1, len(documents)):
        b = pd.read_csv(path + documents[i])
        merged = merged.merge(b, on='SENTENCEDIST')

    merged.to_csv("output.csv", index=False)


def main():

    dir_path = r"../../data/WikiCoref/Output/Dcoref/XML-Post Processing/"
    documents = os.listdir(dir_path)

    for document in documents:
        # Reading XML Files
        print("Extracting " + document)
        mention_tree = etree.parse(dir_path + document)

        # Extract Markables from XML file
        markables = extractMarkables(mention_tree)
        writeCSV_Markables(markables, document)

        # Create Feature vectors from markables
        vectors = extractVectors(markables)
        writeCSV_featureVector(vectors, document)


main()
