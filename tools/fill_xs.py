#!/usr/bin/env python
"""
Plot cross section
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-12-20 Fri 23:27]"

from ROOT import TGraphAsymmErrors, TGraphErrors
import sys, os
import logging
from math import *
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')

def fill_xs(xs_list):
    ''' ARGUE: 1. data source file path and its name
    '''
    gaexs_list, geeff_list = [], []
    for xs_file in xs_list:
        ipoint, gaexs, geeff = 0, TGraphAsymmErrors(0), TGraphErrors(0)
        for line in open(xs_file):
            try:
                fargs = map(float, line.strip().split())
                sample, ecms, lum, br, nsig, nsigerrl, nsigerrh = fargs[0], fargs[1], fargs[2], fargs[3], fargs[4], fargs[5], fargs[6]
                eff, isr, vp, N0 = fargs[7],  fargs[8],  fargs[9], fargs[10]
                '''
                USER DEFINE SECTION { formula of cross section
                '''
                xs = nsig/(2*lum*eff*br*isr*vp)
                xserrl = nsigerrl/(2*lum*eff*br*isr*vp)
                xserrh = nsigerrh/(2*lum*eff*br*isr*vp)
                '''
                } USER DEFINE SECTION
                '''
                gaexs.Set(ipoint + 1)
                gaexs.SetPoint(ipoint, ecms, xs)
                gaexs.SetPointError(ipoint, 0.0, 0.0, xserrl, xserrh)
                geeff.Set(ipoint + 1)
                geeff.SetPoint(ipoint, ecms, eff*isr)
                geeff.SetPointError(ipoint, 0.0, sqrt(isr*eff*(1.00 - eff)/N0))
                ipoint += 1
            except:
                '''
                '''
        gaexs_list.append(gaexs)
        geeff_list.append(geeff)
    return gaexs_list, geeff_list
