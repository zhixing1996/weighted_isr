#!/usr/bin/env python
"""
Plot cross section
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2020-11-06 Fri 23:18]"

from ROOT import TGraphAsymmErrors, TGraphErrors
import sys, os
import logging
from math import *
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')

def fill_xs(label_list, xs_list, iter_new):
    ''' ARGUE: 1. data source file path and its name
               2. name of new iteration
    '''
    gaexs_list, geeff_list = [], []
    for label, xs_file in zip(label_list, xs_list):
        ipoint, gaexs, geeff = 0, TGraphAsymmErrors(0), TGraphErrors(0)
        lines_out = []
        for line in open(xs_file):
            if '#' in line: line = line.replace('#', '')
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
                lines_out.append('{:<7.0f}{:<10.5f}{:<10.2f}{:<10.5f}{:<10.3f}{:<10.3f}{:<10.3f}{:<10.3f}{:<10.5f}{:<10.5f}{:<10.5f}\n'.format(sample, ecms, lum, br, xs, xserrl, xserrh, eff, isr, vp, N0))
            except Exception as e:
                lines_out.append(line.replace('nsignal', 'xs').replace('nserrl', 'xserrl').replace('nserrh', 'xserrh'))
        with open('./txts/xs_' + label + '_' + iter_new + '.txt', 'w') as f:
            for line_out in lines_out:
                f.write(line_out)
        gaexs_list.append(gaexs)
        geeff_list.append(geeff)
    return gaexs_list, geeff_list
