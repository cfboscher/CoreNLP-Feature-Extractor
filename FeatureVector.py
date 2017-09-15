#!/usr/bin/env python
# -*- coding: utf-8 -*-

from features import *
import sys

class FeatureVector:
    """
        Feature vector between 2 markables
    """

    def __init__(self,i,j):
        self.i = i
        self.j = j
        self.SENTENCEDIST = getSENTENCEDIST(i, j)
        self.IPRONOUN = getPRONOUN(i)
        self.JPRONOUN = getPRONOUN(j)
        self.STRMATCH = getSTRMATCH(i, j)
        self.SUBSTRING = getSUBSTRING(i, j)
        self.DEF_NP = getDEF_NP(j)
        self.DEM_NP = getDEM_NP(j)
        self.HEADMATCH = getHEADMATCH(i, j)
        self.NUMBER = getNUMBER(i, j)
        self.SEMCLASS = getSEMCLASS(i, j)
        self.GENDER = getGENDER(i, j)
        self.PROPERNAME = getPROPERNAME(i, j)
        self.ALIAS = getALIAS(i, j)
        self.APPOSITIVE = getAPPOSITIVE(i,j)

        if sys.argv[1] == 'train':
            self.COREF = getCOREF(i,j)
        else:
            self.COREF =''
