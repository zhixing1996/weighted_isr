#!/usr/bin/env python
"""
main file of weighted_isr package
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>, inspired by Lianjin Wu <wulj@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING, Lianjin WU"
__created__ = "[2020-11-06 Fri 23:18]"

import ConfigParser
import sys, os
from array import array
sys.dont_write_bytecode = True
from tools.setup import set_pub_style, set_graph_style, set_pad_style, set_canvas_style
import tools.xs_func as xs_func
set_pub_style()
from tools.fit_xs import fit_xs
from tools.update import update
from tools.fill_xs import fill_xs
from ROOT import TCanvas, TMath, TF1, TChain
from math import *

if not os.path.exists('./figs/'):
    os.makedirs('./figs/')

if not os.path.exists('./weights/'):
    os.makedirs('./weights/')

if not os.path.exists('./txts/'):
    os.makedirs('./txts/')

'''
Config file parser
'''
cp = ConfigParser.SafeConfigParser()
cp.read('weighted_isr.conf')
label_list = cp.get('patch', 'label').strip('[').strip(']').replace(' ', '').split(',')
iter_old = cp.get('patch', 'iter_old')
iter_new = cp.get('patch', 'iter_new')
old_xs_list = [xs.replace('iter_old', iter_old) for xs in cp.get('path', 'xs_old').strip('[').strip(']').replace(' ', '').split(',')]
new_xs_list = [xs.replace('iter_new', iter_new)for xs in cp.get('path', 'xs_new').strip('[').strip(']').replace(' ', '').split(',')]
ini_isr_list = cp.get('path', 'ini_isr').strip('[').strip(']').replace(' ', '').split(',')
xtitle_list = cp.get('draw', 'xtitle').strip('[').strip(']').replace(' ', '').replace('\'', '').split(',')
xs_ytitle_list = cp.get('draw', 'xs_ytitle').strip('[').strip(']').replace(' ', '').replace('\'', '').split(',')
eff_ytitle_list = cp.get('draw', 'eff_ytitle').strip('[').strip(']').replace(' ', '').replace('\'', '').split(',')
shape_dep_str = cp.get('weight', 'shape_dep')
if shape_dep_str == 'True' or shape_dep_str == 'true':
    shape_dep = True
elif shape_dep_str == 'False' or shape_dep_str == 'false':
    shape_dep = False
else:
    print("WRONG: shape_dep in weighted_isr.conf must be 'True'/'true' or 'False'/'false', now is " + cp.get('weight', 'shape_dep'))
    exit(-1)
root_path_list = cp.get('weight', 'root_path').strip('[').strip(']').replace(' ', '').split(',')
truth_root_list = cp.get('weight', 'truth_root').strip('[').strip(']').replace(' ', '').split(',')
event_root_list = cp.get('weight', 'event_root').strip('[').strip(']').replace(' ', '').split(',')
cut_weight = cp.get('weight', 'cut_weight').replace('\'', '')
pyroot_fit_str = cp.get('weight', 'pyroot_fit')
if pyroot_fit_str == 'True' or pyroot_fit_str == 'true':
    pyroot_fit = True
elif pyroot_fit_str == 'False' or pyroot_fit_str == 'false':
    pyroot_fit = False
else:
    print("WRONG: pyroot_fit in weighted_isr.conf must be 'True'/'true' or 'False'/'false', now is " + cp.get('weight', 'pyroot_fit'))
    exit(-1)
manual_update_str = cp.get('weight', 'manual_update')
if manual_update_str == 'True' or manual_update_str == 'true':
    manual_update = True
elif manual_update_str == 'False' or manual_update_str == 'false':
    manual_update = False
else:
    print("WRONG: manual_update in weighted_isr.conf must be 'True'/'true' or 'False'/'false', now is " + cp.get('weight', 'manual_update'))
    exit(-1)
truth_tree = cp.get('weight', 'truth_tree')
event_tree = cp.get('weight', 'event_tree')

'''
USER DEFINE SECTION{ : fit functions for input cross sections
'''
# formula of fit functions
xmin, xmax = 4.2, 4.8
func = xs_func.xs_func(100, xmin, xmax)
def func_D1_2420(x, par):
    ''' function for correlated breit wigner: e+e- --> D1D'''
    xx = x[0]
    resonances = []
    resonances.append((4.410, 0.082, par[0], par[1]))
    resonances.append((4.520, 0.064, par[0], par[2]))
    bw = func.getCorrelatedBreitWigners(xx, resonances, xmin)
    return pow(abs(bw), 2) + func.getPHSPFactor(xx) * par[3] + par[4] * xx + par[5]
def func_psipp(x, par):
    ''' function for correlated breit wigner: e+e- --> psipp pipi '''
    xx = x[0]
    resonances = []
    resonances.append((4.350, 0.060, par[0], par[1]))
    resonances.append((4.421, 0.058, par[0], par[2]))
    resonances.append((4.520, 0.064, par[0], par[3]))
    bw = func.getCorrelatedBreitWigners(xx, resonances, xmin)
    return pow(abs(bw), 2) + func.getPHSPFactor(xx) * par[4] + par[5] * xx + par[6]
def func_DDPIPI(x, par):
    ''' function for correlated breit wigner: e+e- --> DDpipi '''
    xx = x[0]
    return par[0] * pow(xx, -2) * TMath.Exp(-1 * par[1] * (xx - 4.015))
# initial parameters of fit functions
par_D1_2420 = array('d', [1.0, 0.1, 0.1, 1.0, 0, 0])
par_psipp = array('d', [1.0, 0.1, 0.1, 0.1, 1.0, .0, .0])
par_DDPIPI = array('d', [1.0, 1.0])
par_list = [par_D1_2420, par_psipp, par_DDPIPI]
# parameters range of fit functions
par_range_D1_2420 = [
    [0, -50.0, 50.0],
    [1, -50.0, 50.0],
    [2, -50.0, 50.0],
    [3, -10.0, 10.0],
    [4, -10.0, 10.0],
    [5, -10.0, 10.0]
]
par_range_psipp = [
    [0, -50.0, 50.0],
    [1, -50.0, 50.0],
    [2, -50.0, 50.0],
    [3, -10.0, 10.0],
    [4, -10.0, 10.0],
    [5, -50.0, 50.0]
]
par_range_DDPIPI = [
    [0, -100.0, 100.0],
    [1, -100.0, 100.0]
]
par_range_list = [par_range_D1_2420, par_range_psipp, par_range_DDPIPI]
# list of TF1 fit functions
tfunc_D1_2420 = TF1('tfunc_D1_2420', func_D1_2420, xmin, xmax, len(par_D1_2420))
tfunc_psipp = TF1('tfunc_psipp', func_psipp, xmin, xmax, len(par_psipp))
tfunc_DDPIPI = TF1('tfunc_DDPIPI', func_DDPIPI, xmin, xmax, len(par_DDPIPI))
tfunc_list = [tfunc_D1_2420, tfunc_psipp, tfunc_DDPIPI]
'''
} USER DEFINE SECTION
'''

'''
fitting of input cross sections
'''
is_fit = True
gaexs_list_fit, geeff_list_fit, func_list = fit_xs(old_xs_list, tfunc_list, par_list, par_range_list, is_fit)
for label, gaexs, geeff, xtitle, xs_ytitle, eff_ytitle in zip(label_list, gaexs_list_fit, geeff_list_fit, xtitle_list, xs_ytitle_list, eff_ytitle_list):
    xs_mbc = TCanvas('xs_mbc_' + label + '_' + iter_old + '_fit', '', 700, 600)
    set_canvas_style(xs_mbc)
    xs_mbc.cd()
    set_graph_style(gaexs, xtitle, xs_ytitle)
    gaexs.Draw('ap')
    xs_mbc.SaveAs('./figs/xs_' + label + '_' + iter_old + '_fit.pdf')
    eff_mbc = TCanvas('eff_mbc_' + label + '_' + iter_old + '_fit', '', 700, 600)
    set_canvas_style(eff_mbc)
    eff_mbc.cd()
    set_graph_style(geeff, xtitle, eff_ytitle)
    geeff.Draw('ap')
    eff_mbc.SaveAs('./figs/eff_' + label + '_' + iter_old + '_fit.pdf')
is_continue = raw_input('Do you want to continue? (Yes/No)')
if is_continue == 'No':
    exit(-1)
elif is_continue == 'Yes':
    pass
else:
    print('you have enetred an unwanted string, now exiting...')
    exit(-1)

'''
update cross sections
'''
if not manual_update:
    update(label_list, iter_new, old_xs_list, new_xs_list, ini_isr_list, func_list, root_path_list, truth_root_list, event_root_list, truth_tree, event_tree, shape_dep, cut_weight, pyroot_fit)
if not ((shape_dep and not pyroot_fit and manual_update) or (shape_dep and pyroot_fit) or (not shape_dep)):
    print("INFO: please update new xs files manually and continue, after updating, please set manual_update in weighted_isr.conf to be 'True' or 'true'")
    exit(-1)

'''
draw updated cross sections
'''
gaexs_list, geeff_list = fill_xs(label_list, new_xs_list, iter_new)
for label, gaexs, geeff, xtitle, xs_ytitle, eff_ytitle in zip(label_list, gaexs_list, geeff_list, xtitle_list, xs_ytitle_list, eff_ytitle_list):
    xs_mbc = TCanvas('xs_mbc_' + label + '_' + iter_new, '', 700, 600)
    set_canvas_style(xs_mbc)
    xs_mbc.cd()
    set_graph_style(gaexs, xtitle, xs_ytitle)
    gaexs.Draw('ap')
    xs_mbc.SaveAs('./figs/xs_' + label + '_' + iter_new + '.pdf')
    eff_mbc = TCanvas('eff_mbc_' + label + '_' + iter_new, '', 700, 600)
    set_canvas_style(eff_mbc)
    eff_mbc.cd()
    set_graph_style(geeff, xtitle, eff_ytitle)
    geeff.Draw('ap')
    eff_mbc.SaveAs('./figs/eff_' + label + '_' + iter_new + '.pdf')
 
raw_input('Press <Enter> to end...')
