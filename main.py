#!/usr/bin/env python
import ConfigParser
import sys, os
from array import array
sys.dont_write_bytecode = True
from tools.setup import set_pub_style, set_graph_style, set_pad_style, set_canvas_style
import tools.xs_func as xs_func
set_pub_style()
from tools.fit_xs import fit_xs
from tools.update import update
from ROOT import TCanvas, TMath, TF1, TChain
from math import *

if not os.path.exists('./figs/'):
    os.makedirs('./figs/')
    
if not os.path.exists('./weights/'):
    os.makedirs('./weights/')

cp = ConfigParser.SafeConfigParser()
cp.read('example.conf')
old_xs_list = cp.get('general', 'xs_old').strip('[').strip(']').replace(' ', '').split(',')
new_xs_list = cp.get('general', 'xs_new').strip('[').strip(']').replace(' ', '').split(',')
ini_isr_list = cp.get('general', 'ini_isr').strip('[').strip(']').replace(' ', '').split(',')
xtitle_list = cp.get('general', 'xtitle').strip('[').strip(']').replace(' ', '').replace('\'', '').split(',')
xs_ytitle_list = cp.get('general', 'xs_ytitle').strip('[').strip(']').replace(' ', '').replace('\'', '').split(',')
eff_ytitle_list = cp.get('general', 'eff_ytitle').strip('[').strip(']').replace(' ', '').replace('\'', '').split(',')
root_path_list = cp.get('general', 'root_path').strip('[').strip(']').replace(' ', '').split(',')
truth_root_list = cp.get('general', 'truth_root').strip('[').strip(']').replace(' ', '').split(',')
event_root_list = cp.get('general', 'event_root').strip('[').strip(']').replace(' ', '').split(',')
truth_tree = cp.get('general', 'truth_tree').strip('[').strip(']').replace(' ', '').split(',')[0]
event_tree = cp.get('general', 'event_tree').strip('[').strip(']').replace(' ', '').split(',')[0]
func = xs_func.xs_func(100, 4.2, 4.8)

def func_D1_2420(x, par):
    ''' function for correlated breit wigner: e+e- --> D1D'''
    xx = x[0]
    resonances = []
    resonances.append((4.410, 0.082, par[0], par[1]))
    resonances.append((4.520, 0.064, par[0], par[2]))
    bw = func.getCorrelatedBreitWigners(xx, resonances, 4.200)
    return pow(abs(bw), 2) + func.getPHSPFactor(xx) * par[3] + par[4] * xx + par[5]
def func_psipp(x, par):
    ''' function for correlated breit wigner: e+e- --> psipp pipi '''
    xx = x[0]
    resonances = []
    resonances.append((4.360, 0.064, par[0], par[1]))
    resonances.append((4.421, 0.062, par[0], par[2]))
    resonances.append((4.520, 0.064, par[0], par[3]))
    bw = func.getCorrelatedBreitWigners(xx, resonances, 4.2)
    return pow(abs(bw), 2) + func.getPHSPFactor(xx) * par[4] + par[5] * xx + par[6]
def func_DDPIPI(x, par):
    ''' function for correlated breit wigner: e+e- --> DDpipi '''
    xx = x[0]
    # return par[0] * TMath.Exp(par[1] * xx) + par[2]
    # return par[0] * xx * xx * xx + par[2] * xx *xx + par[3] * xx + par[4]
    return par[0] * pow(xx, -2) * TMath.Exp(-1 * par[1] * (xx - 4.015))

par_D1_2420 = array('d', [1.0, 0.1, 0.1, 1.0, 0, 0])
par_psipp = array('d', [1.0, 0.1, 0.1, 0.1, 1.0, .0, .0])
par_DDPIPI = array('d', [1.0, 1.0])
par_list = [par_D1_2420, par_psipp, par_DDPIPI]

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
    [1, -100.0, 100.0],
]
par_range_list = [par_range_D1_2420, par_range_psipp, par_range_DDPIPI]

tfunc_D1_2420 = TF1('tfunc_D1_2420', func_D1_2420, 4.200, 4.800, len(par_D1_2420))
tfunc_psipp = TF1('tfunc_psipp', func_psipp, 4.200, 4.800, len(par_psipp))
tfunc_DDPIPI = TF1('tfunc_DDPIPI', func_DDPIPI, 4.200, 4.800, len(par_DDPIPI))
tfunc_list = [tfunc_D1_2420, tfunc_psipp, tfunc_DDPIPI]

gaexs_list, geeff_list, func_list = fit_xs(old_xs_list, tfunc_list, par_list, par_range_list, cp.get('general', 'cut'), True)
# for gaexs, geeff, xtitle, xs_ytitle, eff_ytitle, tfunc, i in zip(gaexs_list, geeff_list, xtitle_list, xs_ytitle_list, eff_ytitle_list, func_list, xrange(len(gaexs_list))):
#     xs_mbc = TCanvas('xs_mbc_' + str(i), '', 700, 600)
#     set_canvas_style(xs_mbc)
#     xs_mbc.cd()
#     set_graph_style(gaexs, xtitle, xs_ytitle)
#     gaexs.Draw('ap')
#     xs_mbc.SaveAs('./figs/xs_'+str(i)+'.pdf')
#     eff_mbc = TCanvas('eff_mbc_' + str(i), '', 700, 600)
#     set_canvas_style(eff_mbc)
#     eff_mbc.cd()
#     set_graph_style(geeff, xtitle, eff_ytitle)
#     geeff.Draw('ap')
#     eff_mbc.SaveAs('./figs/eff_'+str(i)+'.pdf')

update(old_xs_list, new_xs_list, ini_isr_list, func_list, root_path_list, truth_root_list, event_root_list, truth_tree, event_tree, cp.get('general', 'cut'), True)
 
raw_input('Press <Enter> to end...')
