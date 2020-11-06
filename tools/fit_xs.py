#!/usr/bin/env python
"""
Fit cross section
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2020-01-04 Sat 15:08]"

import sys, os
import logging
from math import *
from ROOT import TF1, TGraphAsymmErrors, TGraphErrors, TCanvas

def fit(xs_file, tfunc, is_fit = True):
    ''' ARGUE: 1. data source file path and its name
               2. fit function
               3. is fit or not
    '''
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
    if is_fit:
        gaexs.Fit(tfunc)
    return gaexs, geeff, tfunc

def fit_xs(xs_list, tfunc_list, par_list, par_range_list, is_fit = True):
    ''' ARGUE: 1. data source file path and its name
               2. TF1 fit function
               3. initial parameters for fit function
               4. parameterrange
               5. is fit or not
    '''
    if not len(tfunc_list) == len(xs_list) == len(par_list) == len(par_range_list):
        print 'WRONG: please add necessary info in example.conf or main.py (array size of tfunc_list, xs_list, par_list and par_range_list should be the same)!'
        exit(-1)
    gaexs_list, geeff_list, func_list = [], [], []
    for xs, tfunc, par, par_range in zip(xs_list, tfunc_list, par_list, par_range_list):
        if is_fit:
            tfunc.SetParameters(par)
            for ilimit, low, high in par_range:
                tfunc.SetParLimits(ilimit, low, high)
            tfunc.SetLineColor(2)
        igaexs, igeeff, itfunc = fit(xs, tfunc, is_fit)
        gaexs_list.append(igaexs)
        geeff_list.append(igeeff)
        func_list.append(itfunc)
    return gaexs_list, geeff_list, func_list
