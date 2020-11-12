#!/usr/bin/env python
"""
Update isr factor and efficiency
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>, inspired by Lianjin Wu <wulj@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING, Lianjin WU"
__created__ = "[2020-11-06 Fri 23:18]"

import sys, os
import logging
from math import *
from ROOT import TF1, TChain, TH1D, TFile, TTree
import operator
from array import array

def cal_weight(sample, ecms, chain, tfunc, shape_dep = False, label = '', iter_new = '', sample_type = 'truth', cut = '', weights_out = './weights'):
    ''' ARGUE: 1. input data sample
               2. input data ecms
               3. input TChain/TTree
               4. input defined TF1
               5. shape depended or not
               6. label of input data
               7. patch number of input data
               8. sample type
               9. cut
               10. output path of weight files
    '''
    if (sample_type == 'event' and shape_dep):
        wf = weights_out + '/weighted_' + label + '_' + str(int(sample)) + '_' + iter_new + '.root'
        f_weight = TFile(wf, 'RECREATE')
        t_weight = TTree('weight', 'weight')
        m_weight = array('d', [0])
        t_weight.Branch('m_weight', m_weight, 'm_weightl/D')
    wsumtotal, sumtotal = 0., 0.
    tree = chain.CopyTree(cut)
    for evt in tree:
        winvm = float(tfunc.Eval(evt.m_m_truthall))
        wecms = float(tfunc.Eval(ecms))
        w = winvm / wecms
        if (sample_type == 'event' and shape_dep):
            m_weight[0] = w
            t_weight.Fill()
        if not wecms == 0:
            wsumtotal += w
        sumtotal += 1
    if (sample_type == 'event' and shape_dep):
        f_weight.cd()
        t_weight.Write()
        f_weight.Close()
        return wf, float(wsumtotal), float(sumtotal)
    else: return float(wsumtotal), float(sumtotal)

def weight(sample, ecms, chtruth, chevent, tfunc, shape_dep = False, label = '', iter_new = '', cut = '', weights_out = './weights_out'):
    ''' ARGUE: 1. input data sample
               2. input data ecms
               3. input TChain/TTree for truth
               4. input TChain/TTree for reconstruct MC (events)
               5. whether mc shape dependent or not
               6. input defined TF1
               7. label of input data
               8. patch number of input data (next)
               9. cut
               10. output path of weight files
    '''
    if shape_dep:
        wsumtru, sumtru = cal_weight(sample, ecms, chtruth, tfunc, shape_dep, label, iter_new, 'truth', '', '')
        wf, wsumsig, sumsig = cal_weight(sample, ecms, chevent, tfunc, shape_dep, label, iter_new, 'event', cut, weights_out)
        weff, eff = wsumsig/wsumtru, sumsig/sumtru
        print('wntru:{:<10.2f}wnsig:{:<10.2f}weff:{:<10.5f} --   ntru:{:<10.2f}nsig:{:<10.2f}eff:{:<10.5f}'.format(wsumtru, wsumsig, weff, sumtru, sumsig, eff))
        return wf, wsumtru, weff, sumtru, eff
    else:
        wsumtru, sumtru = cal_weight(sample, ecms, chtruth, tfunc, shape_dep, label, iter_new, 'truth', '', '')
        wsumsig, sumsig = cal_weight(sample, ecms, chevent, tfunc, shape_dep, label, iter_new, 'event', cut, '')
        weff, eff = wsumsig/wsumtru, sumsig/sumtru
        print('wntru:{:<10.2f}wnsig:{:<10.2f}weff:{:<10.5f} --   ntru:{:<10.2f}nsig:{:<10.2f}eff:{:<10.5f}'.format(wsumtru, wsumsig, weff, sumtru, sumsig, eff))
        return wsumtru, weff, sumtru, eff

def update(label_list, iter_new, old_xs_list, new_xs_list, ini_isr_list, tfunc_list, root_path_list, truth_root_list, event_root_list, truth_tree, event_tree, shape_dep = False, cut = '', pyroot_fit = False, weights_out = './weights'):
    ''' ARGUE: 1. label list
               2. new iteration tag
               3. old data source file path and name
               4. new data file path and its name, used to store productions
               5. initial parameters for fit function
               6. defined TF1 list
               7. root path
               8. root name of truth
               9. root name of evnets after selecting
               10. tree name of truth
               11. tree name of evnets after selecting
               12. whether mc shape dependent or not
               13. cut
               14. using dedicted pyroot fit or not
               15. output path of weight files
    '''
    if not len(label_list) == len(old_xs_list) == len(new_xs_list) == len(ini_isr_list) == len(tfunc_list) == len(root_path_list) == len(truth_root_list) == len(event_root_list):
        print('WRONG: array size of label_list, old_xs, new_xs, ini_isr, tfunc, root_path, truth_path, truth_root and event_root should be the same')
        exit(-1)
    if shape_dep: wf_list = []
    for label, old_xs, new_xs, ini_isr, tfunc, root_path, truth_root, event_root in zip(label_list, old_xs_list, new_xs_list, ini_isr_list, tfunc_list, root_path_list, truth_root_list, event_root_list):
        if os.path.isfile(new_xs):
            os.remove(new_xs)
        lines_out = []
        for line, iniisr in zip(open(old_xs), open(ini_isr)):
            if '#' in line: line = line.replace('#', '')
            try:
                fargs = map(float, line.strip().strip('\n').split())
                fisrs = map(float, iniisr.strip().strip('\n').split())
                sample, ecms, lum, br, nsig, nsigerrl, nsigerrh, isr_old, vp, N0 = fargs[0], fargs[1], fargs[2], fargs[3], fargs[4], fargs[5], fargs[6], fargs[8], fargs[9], fargs[10]
                truthroot, eventroot = root_path + '/' + str(int(sample)) + '/' + truth_root.replace('ECMS', str(int(sample))), root_path + '/' + str(int(sample)) + '/' + event_root.replace('ECMS', str(int(sample)))
                if not os.path.exists(root_path + '/' + str(int(sample))):
                    wsumtru, wsumeff, sumtru, sumeff, wisr = 0., 0., 0., 0., 0.
                else:
                    chtruth, chevent = TChain(truth_tree), TChain(event_tree)
                    chtruth.Add(truthroot)
                    chevent.Add(eventroot)
                    print('executing {0} -- {1} -- {2}'.format(label, iter_new, str(int(sample))))
                    if shape_dep:
                        wf, wsumtru, wsumeff, sumtru, sumeff = weight(sample, ecms, chtruth, chevent, tfunc, shape_dep, label, iter_new, cut, weights_out)
                        wf_list.append(wf)
                    else: wsumtru, wsumeff, sumtru, sumeff = weight(sample, ecms, chtruth, chevent, tfunc, shape_dep, label, iter_new, cut, weights_out)
                    wisr = float(fisrs[1]) * wsumtru * pow(sumtru, -1)
                    print('wisr:{:<10.5f}, old isr:{:<10.5f}'.format(wisr, isr_old))
                    lines_out.append('{:<7.0f}{:<10.5f}{:<10.2f}{:<10.5f}{:<10.3f}{:<10.3f}{:<10.3f}{:<10.3f}{:<10.5f}{:<10.5f}{:<10.5f}\n'.format(sample, ecms, lum, br, nsig, nsigerrl, nsigerrh, wsumeff, wisr, vp, N0))
            except Exception as e:
                lines_out.append(line)
        with open(new_xs, 'w') as f:
            for line_out in lines_out:
                f.write(line_out)
    '''
    USER DEFINE SECTION { pyroot fit -------- Optional
    '''
    if shape_dep and pyroot_fit:
        from simul_fit import simul_fit
        wf_dic_temp = {}
        wf_dic = {}
        for wf in wf_list:
            sample = wf.split('/')[-1].split('.')[0].split('_')[-2]
            wf_dic_temp[wf] = sample
        for k1, v1 in wf_dic_temp.items():
            path = []
            for k2, v2 in wf_dic_temp.items():
                if v1 == v2:
                    path.append(k2)
            wf_dic[v1] = path
        wf_sourted = sorted(wf_dic.items(), key = operator.itemgetter(0))
        for WF in wf_sourted:
            simul_fit(int(WF[0]), WF[1], iter_new, new_xs_list, cut)
    '''
    } USER DEFINE SECTION
    '''
