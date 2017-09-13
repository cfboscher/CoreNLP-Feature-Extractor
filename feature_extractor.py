#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import csv
from lxml import etree

from Markable import *
from FeatureVector import *

def getNumber(markable):
    if(markable.lemma.lower() in ["I", "me","he", "she", "it", "him", "her"]):
        return "SINGULAR"

    elif(markable.lemma.lower() in ["we","us", "they", "them"]):
        return "PLURAL"

    elif(markable.mention == markable.lemma):
        return "SINGULAR"

    elif(markable.mention.replace(markable.lemma,'') in ["s", "es"]):
        return "PLURAL"

    else:
        return "UNKNOWN"


def getGender(markable):
    if (markable.lemma.lower() == "she"):
        return "FEMALE"
    elif (markable.lemma.lower()=="he"):
        return "MALE"
    elif (markable.lemma.lower()=="it"):
        return "NEUTRAL"
    elif (markable.semantic == "PERSON"):
        if markable.mention.split()[0].lower() in ["mr.", "sir", "mister", "sr.", "lord"]:
            return "MALE"
        elif markable.mention.split()[0].lower() in ["mrs.", "miss", "lady", "ms."] :
            return "FEMALE"
        else:
            return "NEUTRAL"
    elif (markable.semantic == "0"):
        return "UNKNOWN"
    else:
        return "NEUTRAL"

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
                                        int(mention.find("head").text),
                                        int(mention.find("sentence").text),
                                        head.find("lemma"),
                                        head.find("POS").text, head.find("NER").text)
                    markable.number = getNumber(markable)
                    markable.gender = getGender(markable)

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


def writeCSV_featureVector(markables):
    """
        Create features vectors from markables and write them in a CSV
    """
    with open('Barack_Obama.csv', 'w') as csvfile:
        fieldnames=['I', 'J', 'SENTENCEDIST', 'IPRONOUN', 'JPRONOUN', 'STRMATCH',
                    'SUBSTRING', 'DEF_NP', 'DEM_NP', 'HEADMATCH', 'NUMBER',
                    'SEMCLASS', 'GENDER', 'PROPERNAME', 'ALIAS', 'APPOSITIVE','COREF']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(len(markables)-1):
            for j in range(i+1, len(markables)):
                vector = FeatureVector(markables[i], markables[j])
                writer.writerow({'I':vector.i.mention, 'J':vector.j.mention,
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

    file = "Barack Obama"
    path = r"../../data/WikiCoref/Output/Dcoref/XML-Post Processing/"+file+".xml"
    mention_tree = etree.parse(path)
    markables = getMarkables(mention_tree)
    writeCSV_featureVector(markables)



main()
