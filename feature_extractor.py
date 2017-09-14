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
                                        head.find("word"),
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
    for coreference in mention_tree.xpath("/root/document/coreference/coreference"):
        for mention in coreference.getchildren():
            markable = createMarkable(mention_tree, mention)
            markables.append(markable)

    return markables


def writeCSV_featureVector(markables, document):
    """
        Create features vectors from markables and write them in a CSV
    """
    with open(('Output/'+document.replace('.xml', '' )+'.csv'), 'w') as csvfile:
        fieldnames=['I', 'J', 'SENTENCEDIST', 'IPRONOUN', 'JPRONOUN', 'STRMATCH',
                    'SUBSTRING', 'DEF_NP', 'DEM_NP', 'HEADMATCH', 'NUMBER',
                    'SEMCLASS', 'GENDER', 'PROPERNAME', 'ALIAS', 'APPOSITIVE','COREF']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(len(markables)-1):
            for j in range(i+1, len(markables)):
                vector = FeatureVector(markables[i], markables[j])
                writer.writerow({'I':vector.i.mention,
                                 'J':vector.j.mention,
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
                                 'COREF':vector.coref})


#Reading XML file as an argument
#TODO : implementer la lecture d'argument correctement

def main():

    dir_path = r"../../data/WikiCoref/Output/Dcoref/XML-Post Processing/"
    documents = os.listdir(dir_path)

    for document in documents:
        print("Extracting " + document)
        mention_tree = etree.parse(dir_path + document)
        markables = extractMarkables(mention_tree)
        # markables = markables.sort
        writeCSV_featureVector(markables,document)


main()
