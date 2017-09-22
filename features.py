#!/usr/bin/env python
# -*- coding: utf-8 -*-


def removeArticles(text):
    stopwords = ['the', 'a', 'an', 'this', 'that', 'these', 'those']
    textwords = text.split()

    resultwords = [word for word in textwords if word.lower() not in stopwords]
    result = ' '.join(resultwords)

    return result


def getAcronym(text):
    """
        Returns the acronym of an Organization name
    """

    removables = ["corp.", "ltd."]
    text = text.split()
    text = [word for word in text if word.lower() not in removables]

    acronym = [word[0].upper() for word in text]

    acronym = ''.join(acronym)
    period_acronym = '.'.join(acronym) + '.'

    return acronym, period_acronym


def getNumber(markable):
    """
        Returns the number of a markable
    """
    if(markable.lemma.lower() in ["I", "me", "he", "she", "it", "him", "her"]):
        return "SINGULAR"
    elif(markable.lemma.lower() in ["we", "us", "they", "them"]):
        return "PLURAL"
    elif(markable.mention == markable.lemma):
        return "SINGULAR"
    elif(markable.mention.replace(markable.lemma, '') in ["s", "es"]):
        return "PLURAL"
    else:
        return "UNKNOWN"


def getGender(markable):
    """
        Returns the gender of a markable
    """
    if (markable.lemma.lower() == "she"):
        return "FEMALE"

    elif (markable.lemma.lower() == "he"):
        return "MALE"

    elif (markable.lemma.lower() == "it"):
        return "NEUTRAL"

    elif (markable.semantic == "PERSON"):
        if markable.mention.split()[0].lower() in ["mr.", "sir", "mister",
                                                   "sr.", "lord"]:
            return "MALE"

        elif markable.mention.split()[0].lower() in ["mrs.", "miss", "lady",
                                                     "ms."]:
            return "FEMALE"

        else:
            return "NEUTRAL"

    elif (markable.semantic == "0"):
        return "UNKNOWN"

    else:
        return "NEUTRAL"


def getSENTENCEDIST(i, j):
    """
        Sentence distance between i and j
    """
    return abs(i.sentence - j.sentence)


def getPRONOUN(i):
    """
        True if i is a Pronoun
    """
    return (i.pos == "PRP")


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
    return (i.number == j.number and i.number != "UNKNOWN")


def getSEMCLASS(i, j):
    """
        The two mentions have the same semantic class
    """
    return (i.semantic == j.semantic)


def getGENDER(i, j):
    """
        The two mentions have the same gender
    """
    return (i.gender == j.gender and i.gender != "UNKNOWN")


def getPROPERNAME(i, j):
    """
        Both mentions are proper names
    """
    return (i.pos == "NNP" and j.pos == "NNP")


def getALIAS(i, j):
    """
        One mention is an alias of the other
    """
    if (i.semantic == j.semantic):
        if (i.semantic == "DATE"):
            return (i.normalized_NER == j.normalized_NER)
        elif(i.semantic == "PERSON"):
            return (i.head == j.head)
        elif (i.semantic == "ORGANIZATION"):
            return (i.mention in getAcronym(j.mention) or
                    j.mention in getAcronym(i.mention))
        else:
            return False
    else:
        return False


def getAPPOSITIVE(i, j):
    """
        One mention is an apposition of the other
    """

    return (i.word_end == ',' and i.nb_end+1 == j.nb_begin)


def getCOREF(i, j):
    """
        Both mentions are coreferent
    """
    if i.coref_group == j.coref_group:
        return 'COREF'
    else:
        return 'NO COREF'
