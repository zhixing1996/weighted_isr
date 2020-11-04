#!/usr/bin/env python
"""
Simultaneous fit of recoiling mass of D and Dmiss and recoiling mass of tagged piplus and piminus
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-12-19 Thu 15:02]"

import math
from array import array
import sys, os
import logging
from math import *
from tools import *
from ROOT import *
from setup import set_pub_style, set_pavetext, set_frame_style
set_pub_style()
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')

def simul_fit(ecms, path, patch):
    try:
        data_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/data/'+str(ecms)+'/data_'+str(ecms)+'_after.root'
        f_data = TFile(data_path, 'READ')
        t_data = f_data.Get('save')
        entries_data = t_data.GetEntries()
        logging.info('data('+str(ecms)+') entries :'+str(entries_data))

        sideband_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/data/'+str(ecms)+'/data_'+str(ecms)+'_sideband.root'
        f_sideband = TFile(sideband_path, 'READ')
        t_sideband = f_sideband.Get('save')
        entries_sideband = t_sideband.GetEntries()
        logging.info('sideband('+str(ecms)+') entries :'+str(entries_sideband))

        for ipath in path:
            if 'psipp' in ipath:
                h_psipp_rm_D = TFile(ipath, 'READ').Get('h_rm_D_'+label+'_'+str(int(ecms)))
                h_psipp_rm_Dmiss = TFile(ipath, 'READ').Get('h_rm_Dmiss_'+label+'_'+str(int(ecms)))
                h_psipp_rm_pipi = TFile(ipath, 'READ').Get('h_rm_pipi_'+label+'_'+str(int(ecms)))

            if 'DDPIPI' in ipath:
                h_DDPIPI_rm_D = TFile(ipath, 'READ').Get('h_rm_D_'+label+'_'+str(int(ecms)))
                h_DDPIPI_rm_Dmiss = TFile(ipath, 'READ').Get('h_rm_Dmiss_'+label+'_'+str(int(ecms)))
                h_DDPIPI_rm_pipi = TFile(ipath, 'READ').Get('h_rm_pipi_'+label+'_'+str(int(ecms)))

            if 'D1_2420' in ipath:
                h_D1_2420_rm_D = TFile(ipath, 'READ').Get('h_rm_D_'+label+'_'+str(int(ecms)))
                h_D1_2420_rm_Dmiss = TFile(ipath, 'READ').Get('h_rm_Dmiss_'+label+'_'+str(int(ecms)))
                h_D1_2420_rm_pipi = TFile(ipath, 'READ').Get('h_rm_pipi_'+label+'_'+str(int(ecms)))
    except:
        logging.error('Files are invalid!')
        sys.exit()
    
    N_D1_2420, N_PSIPP, N_DDPIPI = num_rm_D(ecms)
    if ecms > 4311:
        n2420 = RooRealVar('n2420', 'n2420', 500, 0, N_D1_2420)
    nsideband = RooRealVar('nsideband', 'nsideband', int(entries_sideband/2.))
    npsipp = RooRealVar('npsipp', 'npsipp', 0, N_PSIPP)
    nDDPIPI = RooRealVar('nDDPIPI', 'nDDPIPI', 0, N_DDPIPI)

    # model for RM(D)
    xmin_rm_D, xmax_rm_D, temp = param_rm_D(ecms)
    xbins_rm_D = int((xmax_rm_D - xmin_rm_D)/0.005)
    rm_D = RooRealVar('rm_D', 'rm_D', xmin_rm_D, xmax_rm_D)
    rm_D.setRange('signal', xmin_rm_D, xmax_rm_D)
    h_sideband_rm_D = TH1F('h_sideband_rm_D', '', xbins_rm_D, xmin_rm_D, xmax_rm_D)

    cut = ''
    t_sideband.Project('h_sideband_rm_D', 'rm_D', cut)

    set_data_rm_D = RooDataSet('set_data_rm_D', ' set_data_rm_D', t_data, RooArgSet(rm_D))
    hist_sideband_rm_D = RooDataHist('hist_sideband_rm_D', 'hist_sideband_rm_D', RooArgList(rm_D), h_sideband_rm_D)
    hist_psipp_rm_D = RooDataHist('hist_psipp_rm_D', 'hist_psipp_rm_D', RooArgList(rm_D), h_psipp_rm_D)
    hist_DDPIPI_rm_D = RooDataHist('hist_DDPIPI_rm_D', 'hist_DDPIPI_rm_D', RooArgList(rm_D), h_DDPIPI_rm_D)

    pdf_sideband_rm_D = RooHistPdf('pdf_sideband_rm_D', 'pdf_sideband_rm_D', RooArgSet(rm_D), hist_sideband_rm_D, 0)
    pdf_psipp_rm_D = RooHistPdf('pdf_psipp_rm_D', 'pdf_psipp_rm_D', RooArgSet(rm_D), hist_psipp_rm_D, 2)
    pdf_DDPIPI_rm_D = RooHistPdf('pdf_DDPIPI_rm_D', 'pdf_DDPIPI_rm_D', RooArgSet(rm_D), hist_DDPIPI_rm_D, 2)

    # model for RM(Dmiss)
    xmin_rm_Dmiss, xmax_rm_Dmiss, temp = param_rm_D(ecms)
    xbins_rm_Dmiss = int((xmax_rm_Dmiss - xmin_rm_Dmiss)/0.005)
    rm_Dmiss = RooRealVar('rm_Dmiss', 'rm_Dmiss', xmin_rm_Dmiss, xmax_rm_Dmiss)
    rm_Dmiss.setRange('signal', xmin_rm_Dmiss, xmax_rm_Dmiss)
    h_sideband_rm_Dmiss = TH1F('h_sideband_rm_Dmiss', '', xbins_rm_Dmiss, xmin_rm_Dmiss, xmax_rm_Dmiss)

    cut = ''
    t_sideband.Project('h_sideband_rm_Dmiss', 'rm_Dmiss', cut)

    set_data_rm_Dmiss = RooDataSet('set_data_rm_Dmiss', ' set_data_rm_Dmiss', t_data, RooArgSet(rm_Dmiss))
    hist_sideband_rm_Dmiss = RooDataHist('hist_sideband_rm_Dmiss', 'hist_sideband_rm_Dmiss', RooArgList(rm_Dmiss), h_sideband_rm_Dmiss)
    hist_psipp_rm_Dmiss = RooDataHist('hist_psipp_rm_Dmiss', 'hist_psipp_rm_Dmiss', RooArgList(rm_Dmiss), h_psipp_rm_Dmiss)
    hist_DDPIPI_rm_Dmiss = RooDataHist('hist_DDPIPI_rm_Dmiss', 'hist_DDPIPI_rm_Dmiss', RooArgList(rm_Dmiss), h_DDPIPI_rm_Dmiss)

    pdf_sideband_rm_Dmiss = RooHistPdf('pdf_sideband_rm_Dmiss', 'pdf_sideband_rm_Dmiss', RooArgSet(rm_Dmiss), hist_sideband_rm_Dmiss, 0)
    pdf_psipp_rm_Dmiss = RooHistPdf('pdf_psipp_rm_Dmiss', 'pdf_psipp_rm_Dmiss', RooArgSet(rm_Dmiss), hist_psipp_rm_Dmiss, 2)
    pdf_DDPIPI_rm_Dmiss = RooHistPdf('pdf_DDPIPI_rm_Dmiss', 'pdf_DDPIPI_rm_Dmiss', RooArgSet(rm_Dmiss), hist_DDPIPI_rm_Dmiss, 2)

    # model for RM(pipi)
    xmin_rm_pipi, xmax_rm_pipi = param_rm_pipi(ecms)
    xbins_rm_pipi = int((xmax_rm_pipi - xmin_rm_pipi)/0.005)
    rm_pipi = RooRealVar('rm_pipi', 'rm_pipi', xmin_rm_pipi, xmax_rm_pipi)
    rm_pipi.setRange('signal', xmin_rm_pipi, xmax_rm_pipi)
    h_sideband_rm_pipi = TH1F('h_sideband_rm_pipi', '', xbins_rm_pipi, xmin_rm_pipi, xmax_rm_pipi)

    cut = ''
    t_sideband.Project('h_sideband_rm_pipi', 'rm_pipi', cut)

    set_data_rm_pipi = RooDataSet('set_data_rm_pipi', ' set_data_rm_pipi', t_data, RooArgSet(rm_pipi))
    hist_sideband_rm_pipi = RooDataHist('hist_sideband_rm_pipi', 'hist_sideband_rm_pipi', RooArgList(rm_pipi), h_sideband_rm_pipi)
    hist_psipp_rm_pipi = RooDataHist('hist_psipp_rm_pipi', 'hist_psipp_rm_pipi', RooArgList(rm_pipi), h_psipp_rm_pipi)
    hist_DDPIPI_rm_pipi = RooDataHist('hist_DDPIPI_rm_pipi', 'hist_DDPIPI_rm_pipi', RooArgList(rm_pipi), h_DDPIPI_rm_pipi)

    pdf_psipp_rm_pipi = RooHistPdf('pdf_psipp_rm_pipi', 'pdf_psipp_rm_pipi', RooArgSet(rm_pipi), hist_psipp_rm_pipi, 2)
    pdf_sideband_rm_pipi = RooHistPdf('pdf_sideband_rm_pipi', 'pdf_sideband_rm_pipi', RooArgSet(rm_pipi), hist_sideband_rm_pipi, 0)
    pdf_DDPIPI_rm_pipi = RooHistPdf('pdf_DDPIPI_rm_pipi', 'pdf_DDPIPI_rm_pipi', RooArgSet(rm_pipi), hist_DDPIPI_rm_pipi, 2)

    mean_rm_pipi = RooRealVar('mean_rm_pipi', 'mean_rm_pipi', 0, -0.01, 0.01)
    sigma_rm_pipi = RooRealVar('sigma_rm_pipi', 'sigma_rm_pipi', 0.00123, 0., 0.02)
    gauss_rm_pipi = RooGaussian('gaus_rm_pipi', 'guass_rm_pipi', rm_pipi, mean_rm_pipi, sigma_rm_pipi)
    rm_pipi.setBins(xbins_rm_pipi, 'cache')
    covpdf_psipp = RooFFTConvPdf('covpdf_psipp', 'covpdf_psipp', rm_pipi, pdf_psipp_rm_pipi, gauss_rm_pipi)

    # model for RM(D)
    if ecms > 4311:
        hist_D1_2420_rm_D = RooDataHist('hist_D1_2420_rm_D', 'hist_D1_2420_rm_D', RooArgList(rm_D), h_D1_2420_rm_D)
        pdf_D1_2420_rm_D = RooHistPdf('pdf_D1_2420_rm_D', 'pdf_D1_2420_rm_D', RooArgSet(rm_D), hist_D1_2420_rm_D, 2)
        mean_rm_D = RooRealVar('mean_rm_D', 'mean_rm_D', 0, -0.01, 0.01)
        sigma_rm_D = RooRealVar('sigma_rm_D', 'sigma_rm_D', 0.00123, 0., 0.02)
        gauss_rm_D = RooGaussian('gaus_rm_D', 'guass_rm_D', rm_D, mean_rm_D, sigma_rm_D)
        rm_D.setBins(xbins_rm_D, 'cache')
        covpdf_D1_2420_D = RooFFTConvPdf('covpdf_D1_2420_D', 'covpdf_D1_2420_D', rm_D, pdf_D1_2420_rm_D, gauss_rm_D)
        model_rm_D = RooAddPdf('model_rm_D', 'model_rm_D', RooArgList(covpdf_D1_2420_D, pdf_sideband_rm_D, pdf_psipp_rm_D, pdf_DDPIPI_rm_D), RooArgList(n2420, nsideband, npsipp, nDDPIPI))
    else:
        model_rm_D = RooAddPdf('model_rm_D', 'model_rm_D', RooArgList(pdf_sideband_rm_D, pdf_psipp_rm_D, pdf_DDPIPI_rm_D), RooArgList(nsideband, npsipp, nDDPIPI))

    # model for RM(Dmiss)
    if ecms > 4311:
        cut = ''
        h_D1_2420_rm_Dmiss = TH1F('h_D1_2420_rm_Dmiss', '', xbins_rm_Dmiss, xmin_rm_Dmiss, xmax_rm_Dmiss)
        t_D1_2420.Project('h_D1_2420_rm_Dmiss', 'rm_Dmiss', cut)
        hist_D1_2420_rm_Dmiss = RooDataHist('hist_D1_2420_rm_Dmiss', 'hist_D1_2420_rm_Dmiss', RooArgList(rm_Dmiss), h_D1_2420_rm_Dmiss)
        pdf_D1_2420_rm_Dmiss = RooHistPdf('pdf_D1_2420_rm_Dmiss', 'pdf_D1_2420_rm_Dmiss', RooArgSet(rm_Dmiss), hist_D1_2420_rm_Dmiss, 2)
        mean_rm_Dmiss = RooRealVar('mean_rm_Dmiss', 'mean_rm_Dmiss', 0, -0.01, 0.01)
        sigma_rm_Dmiss = RooRealVar('sigma_rm_Dmiss', 'sigma_rm_Dmiss', 0.00123, 0., 0.02)
        gauss_rm_Dmiss = RooGaussian('gaus_rm_Dmiss', 'guass_rm_Dmiss', rm_Dmiss, mean_rm_Dmiss, sigma_rm_Dmiss)
        rm_Dmiss.setBins(xbins_rm_Dmiss, 'cache')
        covpdf_D1_2420_Dmiss = RooFFTConvPdf('covpdf_D1_2420_D', 'covpdf_D1_2420_D', rm_Dmiss, pdf_D1_2420_rm_Dmiss, gauss_rm_Dmiss)
        model_rm_Dmiss = RooAddPdf('model_rm_Dmiss', 'model_rm_Dmiss', RooArgList(covpdf_D1_2420_Dmiss, pdf_sideband_rm_Dmiss, pdf_psipp_rm_Dmiss, pdf_DDPIPI_rm_Dmiss), RooArgList(n2420, nsideband, npsipp, nDDPIPI))
    else:
        model_rm_Dmiss = RooAddPdf('model_rm_Dmiss', 'model_rm_Dmiss', RooArgList(pdf_sideband_rm_Dmiss, pdf_psipp_rm_Dmiss, pdf_DDPIPI_rm_Dmiss), RooArgList(nsideband, npsipp, nDDPIPI))

    # model for RM(pipi)
    if ecms > 4311:
        cut = ''
        h_D1_2420_rm_pipi = TH1F('h_D1_2420_rm_pipi', '', xbins_rm_pipi, xmin_rm_pipi, xmax_rm_pipi)
        t_D1_2420.Project('h_D1_2420_rm_pipi', 'rm_pipi', cut)
        hist_D1_2420_rm_pipi = RooDataHist('hist_D1_2420_rm_pipi', 'hist_D1_2420_rm_pipi', RooArgList(rm_pipi), h_D1_2420_rm_pipi)
        pdf_D1_2420_rm_pipi = RooHistPdf('pdf_D1_2420_rm_pipi', 'pdf_D1_2420_rm_pipi', RooArgSet(rm_pipi), hist_D1_2420_rm_pipi, 2)
        model_rm_pipi = RooAddPdf('model_rm_pipi', 'model_rm_pipi', RooArgList(pdf_D1_2420_rm_pipi, pdf_sideband_rm_pipi, covpdf_psipp, pdf_DDPIPI_rm_pipi), RooArgList(n2420, nsideband, npsipp, nDDPIPI))
    else:
        model_rm_pipi = RooAddPdf('model_rm_pipi', 'model_rm_pipi', RooArgList(pdf_sideband_rm_pipi, covpdf_psipp, pdf_DDPIPI_rm_pipi), RooArgList(nsideband, npsipp, nDDPIPI))

    # simultaneous fit
    sample = RooCategory('sample', 'sample')
    sample.defineType('rm_D')
    sample.defineType('rm_Dmiss')
    sample.defineType('rm_pipi')
    combData = RooDataSet('combData', 'combined data', RooArgSet(rm_D, rm_Dmiss, rm_pipi), 
        RooFit.Index(sample), RooFit.Import('rm_D', set_data_rm_D), RooFit.Import('rm_Dmiss', set_data_rm_Dmiss), RooFit.Import('rm_pipi', set_data_rm_pipi))
    sim_pdf = RooSimultaneous('sim_pdf', 'simultaneous pdf', sample)
    sim_pdf.addPdf(model_rm_D, 'rm_D')
    sim_pdf.addPdf(model_rm_Dmiss, 'rm_Dmiss')
    sim_pdf.addPdf(model_rm_pipi, 'rm_pipi')
    fit_result = sim_pdf.fitTo(combData, RooFit.Extended(kTRUE), RooFit.Save(kTRUE))

    # Write necessary info
    if not os.path.exists('./txts/'):
        os.makedirs('./txts/')

    Br = 0.0938
    lum = luminosity(ecms)

    eff_D1_2420 = 0.
    ISR_D1_2420 = 1.
    VP_D1_2420 = 1.
    xs_D1_2420 = 0.
    xserr_D1_2420 = 0.
    if ecms > 4311:
        if ecms == 4420 or ecms == 4680:
            eff_D1_2420 = float(t_D1_2420.GetEntries('m_rm_D > %.5f && m_rm_D < %.5f && m_rm_Dmiss > %.5f && m_rm_Dmiss < %.5f && rm_pipi > %.5f && rm_pipi < %.5f' %(xmin_rm_D, xmax_rm_D, xmin_rm_Dmiss, xmax_rm_Dmiss, xmin_rm_pipi, xmax_rm_pipi)))/100000.
        else:
            eff_D1_2420 = float(t_D1_2420.GetEntries('m_rm_D > %.5f && m_rm_D < %.5f && m_rm_Dmiss > %.5f && m_rm_Dmiss < %.5f && rm_pipi > %.5f && rm_pipi < %.5f' %(xmin_rm_D, xmax_rm_D, xmin_rm_Dmiss, xmax_rm_Dmiss, xmin_rm_pipi, xmax_rm_pipi)))/50000.
        f_D1_2420_factor = open('./txts/factor_info_' + str(ecms) + '_D1_2420_' + patch + '.txt', 'r')
        lines_D1_2420 = f_D1_2420_factor.readlines()
        for line_D1_2420 in lines_D1_2420:
            rs_D1_2420 = line_D1_2420.rstrip('\n')
            rs_D1_2420 = filter(None, rs_D1_2420.split(" "))
            ISR_D1_2420 = float(rs_D1_2420[0])
            VP_D1_2420 = float(rs_D1_2420[1])
        xs_D1_2420 = n2420.getVal()/2./Br/eff_D1_2420/lum/ISR_D1_2420/VP_D1_2420
        xserr_D1_2420 = n2420.getError()/2./Br/eff_D1_2420/lum/ISR_D1_2420/VP_D1_2420

    n_psipp = 0.
    eff_psipp = 0.
    ISR_psipp = 1.
    VP_psipp = 1.
    xs_psipp = 0.
    xserr_psipp = 0.
    if ecms == 4190 or ecms == 4210 or ecms == 4220 or ecms == 4230 or ecms == 4260 or ecms == 4420 or ecms == 4680:
        eff_psipp = float(t_psipp.GetEntries('m_rm_D > %.5f && m_rm_D < %.5f && m_rm_Dmiss > %.5f && m_rm_Dmiss < %.5f && rm_pipi > %.5f && rm_pipi < %.5f' %(xmin_rm_D, xmax_rm_D, xmin_rm_Dmiss, xmax_rm_Dmiss, xmin_rm_pipi, xmax_rm_pipi)))/100000.
    else:
        eff_psipp = float(t_psipp.GetEntries('m_rm_D > %.5f && m_rm_D < %.5f && m_rm_Dmiss > %.5f && m_rm_Dmiss < %.5f && rm_pipi > %.5f && rm_pipi < %.5f' %(xmin_rm_D, xmax_rm_D, xmin_rm_Dmiss, xmax_rm_Dmiss, xmin_rm_pipi, xmax_rm_pipi)))/50000.
    f_psipp_factor = open('./txts/factor_info_' + str(ecms) + '_psipp_' + patch + '.txt', 'r')
    lines_psipp = f_psipp_factor.readlines()
    for line_psipp in lines_psipp:
        rs_psipp = line_psipp.rstrip('\n')
        rs_psipp = filter(None, rs_psipp.split(" "))
        ISR_psipp = float(rs_psipp[0])
        VP_psipp = float(rs_psipp[1])
    xs_psipp = npsipp.getVal()/2./Br/eff_psipp/lum/ISR_psipp/VP_psipp
    xserr_psipp = npsipp.getError()/2./Br/eff_psipp/lum/ISR_psipp/VP_psipp

    n_DDPIPI = 0.
    eff_DDPIPI = 0.
    ISR_DDPIPI = 1.
    VP_DDPIPI = 1.
    xs_DDPIPI = 0.
    xserr_DDPIPI = 0.
    if ecms == 4190 or ecms == 4210 or ecms == 4220 or ecms == 4230 or ecms == 4260 or ecms == 4420 or ecms == 4680:
        eff_DDPIPI = float(t_DDPIPI.GetEntries('m_rm_D > %.5f && m_rm_D < %.5f && m_rm_Dmiss > %.5f && m_rm_Dmiss < %.5f && rm_pipi > %.5f && rm_pipi < %.5f' %(xmin_rm_D, xmax_rm_D, xmin_rm_Dmiss, xmax_rm_Dmiss, xmin_rm_pipi, xmax_rm_pipi)))/100000.
    else:
        eff_DDPIPI = float(t_DDPIPI.GetEntries('m_rm_D > %.5f && m_rm_D < %.5f && m_rm_Dmiss > %.5f && m_rm_Dmiss < %.5f && rm_pipi > %.5f && rm_pipi < %.5f' %(xmin_rm_D, xmax_rm_D, xmin_rm_Dmiss, xmax_rm_Dmiss, xmin_rm_pipi, xmax_rm_pipi)))/50000.
    f_DDPIPI_factor = open('./txts/factor_info_' + str(ecms) + '_DDPIPI_' + patch + '.txt', 'r')
    lines_DDPIPI = f_DDPIPI_factor.readlines()
    for line_DDPIPI in lines_DDPIPI:
        rs_DDPIPI = line_DDPIPI.rstrip('\n')
        rs_DDPIPI = filter(None, rs_DDPIPI.split(" "))
        ISR_DDPIPI = float(rs_DDPIPI[0])
        VP_DDPIPI = float(rs_DDPIPI[1])
    xs_DDPIPI = nDDPIPI.getVal()/2./Br/eff_DDPIPI/lum/ISR_DDPIPI/VP_DDPIPI
    xserr_DDPIPI = nDDPIPI.getError()/2./Br/eff_DDPIPI/lum/ISR_DDPIPI/VP_DDPIPI

    if ecms > 4311:
        path_xs_D1_2420 = './txts/xs_D1_2420_'+ patch +'.txt'
        if ecms == 4315 and os.path.isfile(path_xs_D1_2420): os.remove(path_xs_D1_2420)
        f_xs_D1_2420 = open(path_xs_D1_2420, 'a')
        if ecms == 4315: f_xs_D1_2420.write('sample energy luminosity br     nsignal nserrl nserrh eff    isr   vp   N0\n')
        if ecms == 4420 or ecms == 4680:
            f_xs_D1_2420.write('{:.0f}    {:<10.3f}{:<10.2f}{:<10.4f}{:<10.1f}{:<10.1f}{:<10.1f}{:<10.5f}{:<10.3f}{:<10.3f}{:<10.1f}'.format(ecms, ecms/1000., lum, 0.0938, n2420.getVal(), n2420.getError(), n2420.getError(), eff_D1_2420, ISR_D1_2420, VP_D1_2420, 100000))
            f_xs_D1_2420.write('\n')
        else:
            f_xs_D1_2420.write('{:.0f}    {:<10.3f}{:<10.2f}{:<10.4f}{:<10.1f}{:<10.1f}{:<10.1f}{:<10.5f}{:<10.3f}{:<10.3f}{:<10.1f}'.format(ecms, ecms/1000., lum, 0.0938, n2420.getVal(), n2420.getError(), n2420.getError(), eff_D1_2420, ISR_D1_2420, VP_D1_2420, 50000))
            f_xs_D1_2420.write('\n')
        f_xs_D1_2420.close()

    path_xs_psipp = './txts/xs_psipp_'+ patch +'.txt'
    if ecms == 4190 and os.path.isfile(path_xs_psipp): os.remove(path_xs_psipp)
    f_xs_psipp = open(path_xs_psipp, 'a')
    if ecms == 4190: f_xs_psipp.write('sample energy luminosity br     nsignal nserrl nserrh eff    isr   vp   N0\n')
    if ecms == 4190 or ecms == 4210 or ecms == 4220 or ecms == 4230 or ecms == 4260 or ecms == 4420 or ecms == 4680:
        f_xs_psipp.write('{:.0f}    {:<10.3f}{:<10.2f}{:<10.4f}{:<10.1f}{:<10.1f}{:<10.1f}{:<10.5f}{:<10.3f}{:<10.3f}{:<10.1f}'.format(ecms, ecms/1000., lum, 0.0938, npsipp.getVal(), npsipp.getError(), npsipp.getError(), eff_psipp, ISR_psipp, VP_psipp, 100000))
        f_xs_psipp.write('\n')
    else:
        f_xs_psipp.write('{:.0f}    {:<10.3f}{:<10.2f}{:<10.4f}{:<10.1f}{:<10.1f}{:<10.1f}{:<10.5f}{:<10.3f}{:<10.3f}{:<10.1f}'.format(ecms, ecms/1000., lum, 0.0938, npsipp.getVal(), npsipp.getError(), npsipp.getError(), eff_psipp, ISR_psipp, VP_psipp, 50000))
        f_xs_psipp.write('\n')
    f_xs_psipp.close()

    path_xs_DDPIPI = './txts/xs_DDPIPI_'+ patch +'.txt'
    if ecms == 4190 and os.path.isfile(path_xs_DDPIPI): os.remove(path_xs_DDPIPI)
    f_xs_DDPIPI = open(path_xs_DDPIPI, 'a')
    if ecms == 4190: f_xs_DDPIPI.write('sample energy luminosity br     nsignal nserrl nserrh eff    isr   vp   N0\n')
    if ecms == 4190 or ecms == 4210 or ecms == 4220 or ecms == 4230 or ecms == 4260 or ecms == 4420 or ecms == 4680:
        f_xs_DDPIPI.write('{:.0f}    {:<10.3f}{:<10.2f}{:<10.4f}{:<10.1f}{:<10.1f}{:<10.1f}{:<10.5f}{:<10.3f}{:<10.3f}{:<10.1f}'.format(ecms, ecms/1000., lum, 0.0938, nDDPIPI.getVal(), nDDPIPI.getError(), nDDPIPI.getError(), eff_DDPIPI, ISR_DDPIPI, VP_DDPIPI, 100000))
        f_xs_DDPIPI.write('\n')
    else:
        f_xs_DDPIPI.write('{:.0f}    {:<10.3f}{:<10.2f}{:<10.4f}{:<10.1f}{:<10.1f}{:<10.1f}{:<10.5f}{:<10.3f}{:<10.3f}{:<10.1f}'.format(ecms, ecms/1000., lum, 0.0938, nDDPIPI.getVal(), nDDPIPI.getError(), nDDPIPI.getError(), eff_DDPIPI, ISR_DDPIPI, VP_DDPIPI, 50000))
        f_xs_DDPIPI.write('\n')
    f_xs_DDPIPI.close()

    # Draw fitting results
    c = TCanvas('c', 'c', 1700, 600)
    set_canvas_style(c)
    c.Divide(3, 1)

    c.cd(1)
    frame_rm_D = rm_D.frame(RooFit.Bins(xbins_rm_D), RooFit.Title('rm_D'))
    xtitle_rm_D = 'RM(D^{+}) (GeV)'
    content_rm_D = (xmax_rm_D - xmin_rm_D)/xbins_rm_D * 1000
    ytitle_rm_D = 'Entries/%.1f MeV'%int(content_rm_D )
    set_frame_style(frame_rm_D, xtitle_rm_D, ytitle_rm_D)
    combData.plotOn(frame_rm_D, RooFit.Cut('sample==sample::rm_D'), RooFit.Name('data'))
    sim_pdf.plotOn(frame_rm_D, RooFit.Slice(sample, 'rm_D'), RooFit.Components('pdf_sideband_rm_D'), RooFit.ProjWData(RooArgSet(sample), combData), RooFit.LineColor(kGreen), RooFit.FillStyle(1001), RooFit.FillColor(3), RooFit.LineColor(3), RooFit.VLines(), RooFit.DrawOption('F'))
    if ecms > 4311:
        sim_pdf.plotOn(frame_rm_D, RooFit.Slice(sample, 'rm_D'), RooFit.Components('covpdf_D1_2420_D'), RooFit.ProjWData(RooArgSet(sample), combData), RooFit.LineColor(kRed), RooFit.LineWidth(2), RooFit.LineStyle(kDashed))
    sim_pdf.plotOn(frame_rm_D, RooFit.Slice(sample, 'rm_D'), RooFit.Components('pdf_psipp_rm_D'), RooFit.ProjWData(RooArgSet(sample), combData), RooFit.LineColor(kBlue), RooFit.LineWidth(2), RooFit.LineStyle(kDashed))
    sim_pdf.plotOn(frame_rm_D, RooFit.Slice(sample, 'rm_D'), RooFit.Components('pdf_DDPIPI_rm_D'), RooFit.ProjWData(RooArgSet(sample), combData), RooFit.LineColor(37), RooFit.LineWidth(2), RooFit.LineStyle(kDashed))
    sim_pdf.plotOn(frame_rm_D, RooFit.Slice(sample, 'rm_D'), RooFit.ProjWData(RooArgSet(sample), combData), RooFit.LineColor(kBlack), RooFit.LineWidth(3), RooFit.Name('TotFit'))
    combData.plotOn(frame_rm_D, RooFit.Cut('sample==sample::rm_D'))

    name = []
    name.append('Data')
    name.append('Backgrounds')
    if ecms > 4311:
        name.append('D_{1}(2420)^{+}D^{-}')
    name.append('#psi(3770)#pi^{+}#pi^{-}')
    name.append('D^{+}D^{-}#pi^{+}#pi^{-}')
    name.append('Total Fit')

    lg_rm_D = TLegend(.15, .65, .35, .95)
    for m in xrange(len(name)):
        objName = frame_rm_D.nameOf(m)
        obj = frame_rm_D.findObject(objName)
        if objName == 'model_rm_D_Norm[rm_D]_Comp[pdf_sideband_rm_D]':
            lg_rm_D.AddEntry(obj, name[m], 'F')
        else:
            lg_rm_D.AddEntry(obj, name[m], 'PL')
        lg_rm_D.SetTextFont(42)
        lg_rm_D.SetTextSize(0.06)
    lg_rm_D.SetBorderSize(1)
    lg_rm_D.SetLineColor(0)
    lg_rm_D.SetFillColor(0)
    lg_rm_D.SetHeader(str(ecms) + ' MeV')
    frame_rm_D.Draw()
    lg_rm_D.Draw()

    curve = frame_rm_D.findObject('TotFit')
    histo = frame_rm_D.findObject('data')
    chi2_tot, nbin, ytot, avg, eyl, eyh = 0, 0, 0, 0, 0, 0
    x = array('d', 999*[0])
    y = array('d', 999*[0])
    for i in xrange(xbins_rm_D):
        histo.GetPoint(i, x, y)
        exl = histo.GetEXlow()[i]
        exh = histo.GetEXhigh()[i]
        avg += curve.average(x[0] - exl, x[0] + exh)
        ytot += y[0]
        eyl += histo.GetEYlow()[i]  * histo.GetEYlow()[i]
        eyh += histo.GetEYhigh()[i] * histo.GetEYhigh()[i]
        if ytot >= 7:
            if ytot > avg:
                pull = (ytot - avg)/sqrt(eyl)
            else:
                pull = (ytot - avg)/sqrt(eyh)
            chi2_tot += pull * pull
            nbin += 1
            ytot, avg, eyl, eyh = 0, 0, 0, 0
    pt_rm_D = TPaveText(0.15, 0.5, 0.25, 0.6, "BRNDC")
    set_pavetext(pt_rm_D)
    pt_rm_D.Draw()
    n_param = fit_result.floatParsFinal().getSize()
    pt_title = '#chi^{2}/ndf = '
    pt_rm_D.AddText(pt_title)
    if not (nbin - n_param -1) == 0: pt_title = str(round(chi2_tot, 2)) + '/' + str(nbin - n_param -1) + '=' + str(round(chi2_tot/(nbin - n_param -1), 2))
    else: pt_title = str(round(chi2_tot, 2)) + '/' + str(nbin - n_param -1)
    pt_rm_D.AddText(pt_title)

    c.cd(2)
    frame_rm_Dmiss = rm_Dmiss.frame(RooFit.Bins(xbins_rm_Dmiss), RooFit.Title('rm_Dmiss'))
    xtitle_rm_Dmiss = 'RM(D^{-}_{miss}) (GeV)'
    content_rm_Dmiss = (xmax_rm_Dmiss - xmin_rm_Dmiss)/xbins_rm_Dmiss * 1000
    ytitle_rm_Dmiss = 'Entries/%.1f MeV'%int(content_rm_Dmiss)
    set_frame_style(frame_rm_Dmiss, xtitle_rm_Dmiss, ytitle_rm_Dmiss)
    combData.plotOn(frame_rm_Dmiss, RooFit.Cut('sample==sample::rm_Dmiss'), RooFit.Name('data'))
    sim_pdf.plotOn(frame_rm_Dmiss, RooFit.Slice(sample, 'rm_Dmiss'), RooFit.Components('pdf_sideband_rm_Dmiss'), RooFit.ProjWData(RooArgSet(sample), combData), RooFit.LineColor(kGreen), RooFit.FillStyle(1001), RooFit.FillColor(3), RooFit.LineColor(3), RooFit.VLines(), RooFit.DrawOption('F'))
    if ecms > 4311:
        sim_pdf.plotOn(frame_rm_Dmiss, RooFit.Slice(sample, 'rm_Dmiss'), RooFit.Components('covpdf_D1_2420_D'), RooFit.ProjWData(RooArgSet(sample), combData), RooFit.LineColor(kRed), RooFit.LineWidth(2), RooFit.LineStyle(kDashed))
    sim_pdf.plotOn(frame_rm_Dmiss, RooFit.Slice(sample, 'rm_Dmiss'), RooFit.Components('pdf_psipp_rm_Dmiss'), RooFit.ProjWData(RooArgSet(sample), combData), RooFit.LineColor(kBlue), RooFit.LineWidth(2), RooFit.LineStyle(kDashed))
    sim_pdf.plotOn(frame_rm_Dmiss, RooFit.Slice(sample, 'rm_Dmiss'), RooFit.Components('pdf_DDPIPI_rm_Dmiss'), RooFit.ProjWData(RooArgSet(sample), combData), RooFit.LineColor(37), RooFit.LineWidth(2), RooFit.LineStyle(kDashed))
    sim_pdf.plotOn(frame_rm_Dmiss, RooFit.Slice(sample, 'rm_Dmiss'), RooFit.ProjWData(RooArgSet(sample), combData), RooFit.LineColor(kBlack), RooFit.LineWidth(3), RooFit.Name('TotFit'))
    combData.plotOn(frame_rm_Dmiss, RooFit.Cut('sample==sample::rm_Dmiss'))

    name = []
    name.append('Data')
    name.append('Backgrounds')
    if ecms > 4311:
        name.append('D_{1}(2420)^{+}D^{-}')
    name.append('#psi(3770)#pi^{+}#pi^{-}')
    name.append('D^{+}D^{-}#pi^{+}#pi^{-}')
    name.append('Total Fit')

    lg_rm_Dmiss = TLegend(.15, .65, .35, .95)
    for m in xrange(len(name)):
        objName = frame_rm_Dmiss.nameOf(m)
        obj = frame_rm_Dmiss.findObject(objName)
        if objName == 'model_rm_Dmiss_Norm[rm_D]_Comp[pdf_sideband_rm_Dmiss]':
            lg_rm_Dmiss.AddEntry(obj, name[m], 'F')
        else:
            lg_rm_Dmiss.AddEntry(obj, name[m], 'PL')
        lg_rm_Dmiss.SetTextFont(42)
        lg_rm_Dmiss.SetTextSize(0.06)
    lg_rm_Dmiss.SetBorderSize(1)
    lg_rm_Dmiss.SetLineColor(0)
    lg_rm_Dmiss.SetFillColor(0)
    lg_rm_Dmiss.SetHeader(str(ecms) + ' MeV')
    frame_rm_Dmiss.Draw()
    lg_rm_Dmiss.Draw()

    curve = frame_rm_Dmiss.findObject('TotFit')
    histo = frame_rm_Dmiss.findObject('data')
    chi2_tot, nbin, ytot, avg, eyl, eyh = 0, 0, 0, 0, 0, 0
    x = array('d', 999*[0])
    y = array('d', 999*[0])
    for i in xrange(xbins_rm_Dmiss):
        histo.GetPoint(i, x, y)
        exl = histo.GetEXlow()[i]
        exh = histo.GetEXhigh()[i]
        avg += curve.average(x[0] - exl, x[0] + exh)
        ytot += y[0]
        eyl += histo.GetEYlow()[i]  * histo.GetEYlow()[i]
        eyh += histo.GetEYhigh()[i] * histo.GetEYhigh()[i]
        if ytot >= 7:
            if ytot > avg:
                pull = (ytot - avg)/sqrt(eyl)
            else:
                pull = (ytot - avg)/sqrt(eyh)
            chi2_tot += pull * pull
            nbin += 1
            ytot, avg, eyl, eyh = 0, 0, 0, 0
    pt_rm_Dmiss = TPaveText(0.15, 0.5, 0.25, 0.6, "BRNDC")
    set_pavetext(pt_rm_Dmiss)
    pt_rm_Dmiss.Draw()
    n_param = fit_result.floatParsFinal().getSize()
    pt_title = '#chi^{2}/ndf = '
    pt_rm_Dmiss.AddText(pt_title)
    if not (nbin - n_param -1) == 0: pt_title = str(round(chi2_tot, 2)) + '/' + str(nbin - n_param -1) + '=' + str(round(chi2_tot/(nbin - n_param -1), 2))
    else: pt_title = str(round(chi2_tot, 2)) + '/' + str(nbin - n_param -1)
    pt_rm_Dmiss.AddText(pt_title)

    c.cd(3)
    frame_rm_pipi = rm_pipi.frame(RooFit.Bins(xbins_rm_pipi), RooFit.Title('rm_pipi'))
    xtitle_rm_pipi = 'RM(#pi_{0}^{+}#pi_{0}^{-})(GeV)'
    content_rm_pipi = (xmax_rm_pipi - xmin_rm_pipi)/xbins_rm_pipi * 1000
    ytitle_rm_pipi = 'Entries/%.1f MeV'%int(content_rm_pipi)
    set_frame_style(frame_rm_pipi, xtitle_rm_pipi, ytitle_rm_pipi)
    combData.plotOn(frame_rm_pipi, RooFit.Cut('sample==sample::rm_pipi'), RooFit.Name('data'))
    sim_pdf.plotOn(frame_rm_pipi, RooFit.Slice(sample, 'rm_pipi'), RooFit.Components('pdf_sideband_rm_pipi'), RooFit.ProjWData(RooArgSet(sample), combData), RooFit.LineColor(kGreen), RooFit.FillStyle(1001), RooFit.FillColor(3), RooFit.LineColor(3), RooFit.VLines(), RooFit.DrawOption('F'))
    if ecms > 4311:
        sim_pdf.plotOn(frame_rm_pipi, RooFit.Slice(sample, 'rm_pipi'), RooFit.Components('pdf_D1_2420_rm_pipi'), RooFit.ProjWData(RooArgSet(sample), combData), RooFit.LineColor(kRed), RooFit.LineWidth(2), RooFit.LineStyle(kDashed))
    sim_pdf.plotOn(frame_rm_pipi, RooFit.Slice(sample, 'rm_pipi'), RooFit.Components('covpdf_psipp'), RooFit.ProjWData(RooArgSet(sample), combData), RooFit.LineColor(kBlue), RooFit.LineWidth(2), RooFit.LineStyle(kDashed))
    sim_pdf.plotOn(frame_rm_pipi, RooFit.Slice(sample, 'rm_pipi'), RooFit.Components('pdf_DDPIPI_rm_pipi'), RooFit.ProjWData(RooArgSet(sample), combData), RooFit.LineColor(37), RooFit.LineWidth(2), RooFit.LineStyle(kDashed))
    sim_pdf.plotOn(frame_rm_pipi, RooFit.Slice(sample, 'rm_pipi'), RooFit.ProjWData(RooArgSet(sample), combData), RooFit.LineColor(kBlack), RooFit.LineWidth(3), RooFit.Name('TotFit'))
    combData.plotOn(frame_rm_pipi, RooFit.Cut('sample==sample::rm_pipi'))

    name = []
    name.append('Data')
    name.append('Backgrounds')
    if ecms > 4311:
        name.append('D_{1}(2420)^{+}D^{-}')
    name.append('#psi(3770)#pi^{+}#pi^{-}')
    name.append('D^{+}D^{-}#pi^{+}#pi^{-}')
    name.append('Total Fit')

    lg_rm_pipi = TLegend(.55, .65, .75, .95)
    for m in xrange(len(name)):
        objName = frame_rm_pipi.nameOf(m)
        obj = frame_rm_pipi.findObject(objName)
        if objName == 'model_rm_pipi_Norm[rm_pipi]_Comp[pdf_sideband_rm_pipi]':
            lg_rm_pipi.AddEntry(obj, name[m], 'F')
        else:
            lg_rm_pipi.AddEntry(obj, name[m], 'PL')
        lg_rm_pipi.SetTextFont(42)
        lg_rm_pipi.SetTextSize(0.06)
    lg_rm_pipi.SetBorderSize(1)
    lg_rm_pipi.SetLineColor(0)
    lg_rm_pipi.SetFillColor(0)
    lg_rm_pipi.SetHeader(str(ecms) + ' MeV')
    frame_rm_pipi.Draw()
    lg_rm_pipi.Draw()

    curve = frame_rm_pipi.findObject('TotFit')
    histo = frame_rm_pipi.findObject('data')
    chi2_tot, nbin, ytot, avg, eyl, eyh = 0, 0, 0, 0, 0, 0
    x = array('d', 999*[0])
    y = array('d', 999*[0])
    for i in xrange(xbins_rm_pipi):
        histo.GetPoint(i, x, y)
        exl = histo.GetEXlow()[i]
        exh = histo.GetEXhigh()[i]
        avg += curve.average(x[0] - exl, x[0] + exh)
        ytot += y[0]
        eyl += histo.GetEYlow()[i]  * histo.GetEYlow()[i]
        eyh += histo.GetEYhigh()[i] * histo.GetEYhigh()[i]
        if ytot >= 7:
            if ytot > avg:
                pull = (ytot - avg)/sqrt(eyl)
            else:
                pull = (ytot - avg)/sqrt(eyh)
            chi2_tot += pull * pull
            nbin += 1
            ytot, avg, eyl, eyh = 0, 0, 0, 0
    pt_rm_pipi = TPaveText(0.6, 0.5, 0.65, 0.6, "BRNDC")
    set_pavetext(pt_rm_pipi)
    pt_rm_pipi.Draw()
    n_param = fit_result.floatParsFinal().getSize()
    pt_title = '#chi^{2}/ndf = '
    pt_rm_pipi.AddText(pt_title)
    if not (nbin - n_param -1) == 0: pt_title = str(round(chi2_tot, 2)) + '/' + str(nbin - n_param -1) + '=' + str(round(chi2_tot/(nbin - n_param -1), 2))
    else: pt_title = str(round(chi2_tot, 2)) + '/' + str(nbin - n_param -1)
    pt_rm_pipi.AddText(pt_title)

    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')
    canvas_name = './figs/simul_fit_' + str(ecms) + '.pdf'
    c.SaveAs(canvas_name)

    # raw_input('Enter anything to end...')
