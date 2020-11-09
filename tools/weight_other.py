#!/usr/bin/env python
"""
weight other distributions or root files
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>, inspired by Lianjin Wu <wulj@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING, Lianjin WU"
__created__ = "[2020-11-10 Tue 00:50]"

import sys, os
sys.dont_write_bytecode = True
from setup import set_pub_style, set_graph_style, set_pad_style, set_canvas_style
set_pub_style()
from fit_xs import fit_xs
from update import cal_weight
from ROOT import TCanvas, TMath, TChain
from math import *

def weight_other(label_list, iter, xs_list, tfunc_list, par_list, par_range_list, xtitle_list, xs_ytitle_list, eff_ytitle_list, root_path_list, event_root_list, event_tree, cut):
    gaexs_list_fit, geeff_list_fit, func_list = fit_xs(xs_list, tfunc_list, par_list, par_range_list, True)
    for label, gaexs, geeff, xtitle, xs_ytitle, eff_ytitle in zip(label_list, gaexs_list_fit, geeff_list_fit, xtitle_list, xs_ytitle_list, eff_ytitle_list):
        xs_mbc = TCanvas('xs_mbc_' + label + '_' + iter + '_fit', '', 700, 600)
        set_canvas_style(xs_mbc)
        xs_mbc.cd()
        set_graph_style(gaexs, xtitle, xs_ytitle)
        gaexs.Draw('ap')
        xs_mbc.SaveAs('./figs/xs_' + label + '_' + iter + '_fit.pdf')
        eff_mbc = TCanvas('eff_mbc_' + label + '_' + iter + '_fit', '', 700, 600)
        set_canvas_style(eff_mbc)
        eff_mbc.cd()
        set_graph_style(geeff, xtitle, eff_ytitle)
        geeff.Draw('ap')
        eff_mbc.SaveAs('./figs/eff_' + label + '_' + iter + '_fit.pdf')
    is_continue = raw_input('Do you want to continue? (Yes/No)')
    if is_continue == 'No':
        exit(-1)
    elif is_continue == 'Yes':
        pass
    else:
        print('you have enetred an unwanted string, now exiting...')
        exit(-1)
    if not len(label_list) == len(xs_list) == len(func_list) == len(root_path_list) == len(event_root_list):
        print('WRONG: [weight_other] array size of label_list, xs, func, root_path, and event_root should be the same')
        exit(-1)
    for label, xs, func, root_path, event_root in zip(label_list, xs_list, func_list, root_path_list, event_root_list):
            for line in open(xs):
                if '#' in line: line = line.replace('#', '')
                try:
                    fargs = map(float, line.strip().strip('\n').split())
                    sample, ecms, isr, vp = fargs[0], fargs[1], fargs[8], fargs[9]
                    eventroot = root_path + '/' + str(int(sample)) + '/' + event_root.replace('ECMS', str(int(sample)))
                    chevent = TChain(event_tree)
                    chevent.Add(eventroot)
                    print('executing {0} -- {1} -- {2}'.format(label, iter, str(int(sample))))
                    temp1, temp2, temp3 = cal_weight(sample, ecms, chevent, func, True, label, iter, 'event', cut)
                except Exception as e:
                    '''
                    '''
