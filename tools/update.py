#!/usr/bin/env python
"""
Update isr factor and efficiency
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2020-01-04 Sat 15:08]"

import sys, os
import logging
from math import *
from ROOT import TF1, TChain, TH1D, TFile, TTree
import operator
from simul_fit import simul_fit

def calc_weight(sample, ecms, chain, cut, shape_dep, tfunc, label = '', patch = 'round1'):
    ''' ARGUE: 1. input data ecms
               2. input TChain/TTree
               3. cut
               4. shape depended or not
               5. input defined TF1
    '''
    if (cut != '' and shape_dep):
        wf = './weights/weighted_' + label + '_' + str(int(sample)) + '_' + patch + '.root'
        f_weight = TFile(wf, 'RECREATE')
        h_rm_D_w = TH1D('h_rm_D_'+label+'_'+str(int(sample)), 'h_rm_D_'+label+'_'+str(int(sample)), 200, 2.1, 2.9)
        h_rm_Dmiss_w = TH1D('h_rm_Dmiss_'+label+'_'+str(int(sample)), 'h_rm_Dmiss_'+label+'_'+str(int(sample)), 200, 2.1, 2.9)
        h_rm_pipi_w = TH1D('h_rm_pipi_'+label+'_'+str(int(sample)), 'h_rm_pipi_'+label+'_'+str(int(sample)), 200, 3.7, 4.4)
    wsumtotal, sumtotal = 0., 0.
    tree = chain.CopyTree(cut)
    for evt in tree:
        winvm = float(tfunc.Eval(evt.m_m_truthall))
        wecms = float(tfunc.Eval(ecms))
        w = winvm / wecms
        if (cut != '' and shape_dep):
            h_rm_D_w.Fill(evt.m_rm_D, w)
            h_rm_Dmiss_w.Fill(evt.m_rm_Dmiss, w)
            h_rm_pipi_w.Fill(evt.m_rm_pipi, w)
        if not wecms == 0:
            wsumtotal += w
        sumtotal += 1
    if (cut != '' and shape_dep):
        h_rm_D_w.Write()
        h_rm_Dmiss_w.Write()
        h_rm_pipi_w.Write()
        return wf, float(wsumtotal), float(sumtotal)
    else: return float(wsumtotal), float(sumtotal)

def weight(sample, ecms, chtruth, chevent, cut, shape_dep, tfunc, label, patch):
    ''' ARGUE: 1. input data ecms
               2. input TChain/TTree for truth
               3. input TChain/TTree for reconstruct MC
               4. cut
               5. whether mc shape dependent or not
               6. input defined TF1
    '''
    if shape_dep:
        wsumtru, sumtru = calc_weight(sample, ecms, chtruth, '', shape_dep, tfunc)
        wf, wsumsig, sumsig = calc_weight(sample, ecms, chevent, cut, shape_dep, tfunc, label, patch)
        weff, eff = wsumsig/wsumtru, sumsig/sumtru
        print('wntru:{:<10.2f}wnsig:{:<10.2f}weff:{:<10.5f} --   ntru:{:<10.2f}nsig:{:<10.2f}eff:{:<10.5f}'.format(wsumtru, wsumsig, weff, sumtru, sumsig, eff))
        return wf, wsumtru, weff, sumtru, eff
    else:
        wsumtru, sumtru = calc_weight(sample, ecms, chtruth, '', shape_dep, tfunc)
        wsumsig, sumsig = calc_weight(sample, ecms, chevent, cut, shape_dep, tfunc, label, patch)
        weff, eff = wsumsig/wsumtru, sumsig/sumtru
        print('wntru:{:<10.2f}wnsig:{:<10.2f}weff:{:<10.5f} --   ntru:{:<10.2f}nsig:{:<10.2f}eff:{:<10.5f}'.format(wsumtru, wsumsig, weff, sumtru, sumsig, eff))
        return wsumtru, weff, sumtru, eff

def update(old_xs_list, new_xs_list, ini_isr_list, tfunc_list, root_path_list, truth_root_list, event_root_list, truth_tree, event_tree, cut, shape_dep = False):
    ''' ARGUE: 1. old data source file path and name
               2. new data file path and its name, used to store productions
               3. initial parameters for fit function
               4. defined TF1
               5. root path
               6. root name of truth
               7. root name of evnets after selecting
               8. tree name of truth
               9. tree name of evnets after selecting
               10. cut
               11. whether mc shape dependent or not
    '''
    if not len(old_xs_list) == len(new_xs_list) == len(ini_isr_list) == len(tfunc_list) == len(root_path_list) == len(truth_root_list) == len(event_root_list):
        print('WRONG: array size for chains, cutsignals, cutsides, scalefactors are not same')
        exit(-1)
    if shape_dep: wf_list = []
    for old_xs, new_xs, ini_isr, tfunc, root_path, truth_root, event_root in zip(old_xs_list, new_xs_list, ini_isr_list, tfunc_list, root_path_list, truth_root_list, event_root_list):
        if os.path.isfile(new_xs):
            os.remove(new_xs)
        label = ''
        patch = ''
        lines_out = []
        for line, iniisr in zip(open(old_xs), open(ini_isr)):
            if '#' in line: line = line.replace('#', '')
            try:
                fargs = map(float, line.strip().strip('\n').split())
                fisrs = map(float, iniisr.strip().strip('\n').split())
                sample, ecms, lum, br, nsig, nsigerrl, nsigerrh, vp, N0 = fargs[0], fargs[1], fargs[2], fargs[3], fargs[4], fargs[5], fargs[6], fargs[9], fargs[10]
                truthroot, eventroot = root_path + '/' + str(int(sample)) + '/' + truth_root.replace('ECMS', str(int(sample))), root_path + '/' + str(int(sample)) + '/' + event_root.replace('ECMS', str(int(sample)))
                if not os.path.exists(root_path + '/' + str(int(sample))):
                    wsumtru, wsumeff, sumtru, sumeff, wisr = 0., 0., 0., 0., 0.
                else:
                    chtruth, chevent = TChain(truth_tree), TChain(event_tree)
                    chtruth.Add(truthroot)
                    chevent.Add(eventroot)
                    if label == '' or patch == '':
                        print('WRONG: please add a label and patch number in the head of %s'.format(old_xs))
                        exit(-1)
                    print('executing {0} -- {1} -- {2}'.format(label, patch, str(int(sample))))
                    if shape_dep:
                        wf, wsumtru, wsumeff, sumtru, sumeff = weight(sample, ecms, chtruth, chevent, cut, shape_dep, tfunc, label, patch)
                        wf_list.append(wf)
                    else: wsumtru, wsumeff, sumtru, sumeff = weight(sample, ecms, chtruth, chevent, cut, shape_dep, tfunc, label, patch)
                    wisr = float(fisrs[1]) * wsumtru * pow(sumtru, -1)
                    print('wisr:{:<10.5f}iniisr:{:<10.5f}'.format(wisr, float(fisrs[1])))
                    lines_out.append('{:<7.0f}{:<10.5f}{:<10.2f}{:<10.5f}{:<10.3f}{:<10.3f}{:<10.3f}{:<10.3f}{:<10.5f}{:<10.5f}{:<10.5f}\n'.format(sample, ecms, lum, br, nsig, nsigerrl, nsigerrh, wsumeff, wisr, vp, N0))
            except Exception as e:
                lines_out.append(line)
                strings = map(str, line.strip().split())
                if len(strings) == 2:
                    label, patch = strings[0], strings[1]
        with open(new_xs, 'w') as f:
            for line_out in lines_out:
                f.write(line_out)
    if shape_dep:
        wf_dic_temp = {}
        wf_dic = {}
        for wf in wf_list:
            sample = wf.split('.')[1].split('/')[2].strip('weighted_').strip(patch).split('_')[-2]
            wf_dic_temp[wf] = sample
        for k1, v1 in wf_dic_temp.items():
            path = []
            for k2, v2 in wf_dic_temp.items():
                if v1 == v2:
                    path.append(k2)
            wf_dic[v1] = path
        wf_sourted = sorted(wf_dic.items(), key = operator.itemgetter(0))
        for WF in wf_sourted:
            simul_fit(int(WF[0]), WF[1], patch, new_xs_list)
