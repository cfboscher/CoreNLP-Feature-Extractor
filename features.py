#!/usr/bin/env python
# -*- coding: utf-8 -*-

def removeArticles(text):
    stopwords = ['the','a','an','this','that','these','those']
    textwords = text.split()

    resultwords  = [word for word in textwords if word.lower() not in stopwords]
    result = ' '.join(resultwords)

    return result


def getSENTENCEDIST(i, j):
    """
        Sentence distance between i and j
    """
    return i.sentence - j.sentence


def getMENTIONDIST(i, j):
    """
        Mention distance between i and j
    """
    return 0
    #TODO Implement this


def getWORDDIST(i, j):
    """
        Word distance between i and j
    """
    return 0
    #TODO Implement this


def getPRONOUN(i):
    """
        True if i is a Pronoun
    """
    return (i.pos=="PRP")


def getSTRMATCH(i, j):
    """
        The two mentions are the same if we remove articles from both
    """
    return (removeArticles(i.mention) == removeArticles(j.mention))


def getSUBSTRING(i, j):
    """
        One mention is a part of the other
    """
    return (i in j.mention.split() or j in i.mention.split())


def getDEF_NP(j):
    """
        j is a definite noun phrase (begins by "The")
    """
    return (j.mention.split()[0].lower() == "the")


def getDEM_NP(j):
    """
        j is a definite noun phrase (begins by "The")
    """
    words = ["this", "that", "those", "these"]
    return (j.mention.split()[0].lower() in words)


def getHEADMATCH(i, j):
    """
        The two mentions have the same head word
    """
    return (i.head == j.head)


def getNUMBER(i, j):
    """
        The two mentions have the same number
    """
    return 0
    #TODO Implement this


def getSEMCLASS(i, j):
    """
        The two mentions have the same semantic class
    """
    return (i.semantic == j.semantic)


def getGENDER(i, j):
    """
        The two mentions have the same gender
    """
    return 0
    #TODO Implement this


def getPROPERNAME(i, j):
    """
        Both mentions are proper names
    """
    return (i.pos=="NNP" and j.pos=="NNP")


def getALIAS(i,j):
    """
        One mention is an alias of the other
    """
    #TODO Implement this
    return 0


def getAPPOSITIVE(i,j):
    """
        One mention is an apposition of the other
    """
    #TODO Implement this
    return 0
