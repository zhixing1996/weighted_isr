#!/usr/bin/env python
"""
Fit cross section
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>, inspired by Lianjin WU <wulj@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING, Lianjin WU"
__created__ = "[2020-11-06 Fri 23:18]"

import sys, os
import logging
from math import *
from ROOT import TF1, TGraphAsymmErrors, TGraphErrors, TCanvas

def fit(label, iter, xs_file, tfunc, xmin, xmax, is_fit = True):
    ''' ARGUE: 1. label of your input
               2. iter name
               3. data source file path and its name
               4. fit function
               5. minimum of tfunc
               6. maximum of tfunc
               7. is fit or not
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
        path_user = './txts/xs_user_' + label + '_' + iter + '.dat'
        f_user = open(path_user, 'w')
        for i in xrange(int((xmax - xmin)/0.001)):
            ecm = xmin + i * 0.001
            xs_ecm = tfunc.Eval(ecm)
            out = str(ecm) + ' ' + str(xs_ecm) + '\n'
            f_user.write(out)
        f_user.close()
    return gaexs, geeff, tfunc

def fit_xs(label_list, iter, xs_list, tfunc_list, par_list, par_range_list, xmin, xmax, is_fit = True):
    ''' ARGUE: 1. label of your input
               2. iter name
               3. data source file path and its name
               4. TF1 fit function
               5. initial parameters for fit function
               6. parameterrange
               7. minimum of tfunc
               8. maximum of tfunc
               9. is fit or not
    '''
    if not len(label_list) == len(tfunc_list) == len(xs_list) == len(par_list) == len(par_range_list):
        print 'WRONG: please add necessary info in weighted_isr.conf or main.py (array size of tfunc_list, xs_list, par_list and par_range_list should be the same)!'
        exit(-1)
    gaexs_list, geeff_list, func_list = [], [], []
    for label, xs, tfunc, par, par_range in zip(label_list, xs_list, tfunc_list, par_list, par_range_list):
        if is_fit:
            tfunc.SetParameters(par)
            for ilimit, low, high in par_range:
                tfunc.SetParLimits(ilimit, low, high)
            tfunc.SetLineColor(2)
        igaexs, igeeff, itfunc = fit(label, iter, xs, tfunc, xmin, xmax, is_fit)
        gaexs_list.append(igaexs)
        geeff_list.append(igeeff)
        func_list.append(itfunc)
    return gaexs_list, geeff_list, func_list
