#!/usr/bin/env python
"""
Simultaneous fit of recoiling mass of D and Dmiss and recoiling mass of tagged piplus and piminus
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-12-19 Thu 15:02]"

import math
from array import array
import sys, os, re
sys.dont_write_bytecode = True
import logging
from math import *
from params import *
from ROOT import *
from setup import set_pub_style, set_pavetext, set_frame_style, set_canvas_style
set_pub_style()
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')

def usage():
    sys.stdout.write('''
NAME
    simul_fit_cal.py

SYNOPSIS
    ./simul_fit_cal.py [ecms] [patch]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    December 2019
\n''')

def fit(sample, patch, path):
    xmin_rm_D, xmax_rm_D, temp = param_rm_D(sample)
    xbins_rm_D = int((xmax_rm_D - xmin_rm_D)/0.005)
    xmin_rm_Dmiss, xmax_rm_Dmiss, temp = param_rm_D(sample)
    xbins_rm_Dmiss = int((xmax_rm_Dmiss - xmin_rm_Dmiss)/0.005)
    xmin_rm_pipi, xmax_rm_pipi = param_rm_pipi(sample)
    xbins_rm_pipi = int((xmax_rm_pipi - xmin_rm_pipi)/0.005)
    try:
        data_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/data/'+str(sample)+'/data_'+str(sample)+'_after.root'
        f_data = TFile(data_path, 'READ')
        t_data = f_data.Get('save')
        entries_data = t_data.GetEntries()
        logging.info('data('+str(sample)+') entries :'+str(entries_data))

        sideband_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/data/'+str(sample)+'/data_'+str(sample)+'_sideband.root'
        f_sideband = TFile(sideband_path, 'READ')
        t_sideband = f_sideband.Get('save')
        entries_sideband = t_sideband.GetEntries()
        logging.info('sideband('+str(sample)+') entries :'+str(entries_sideband))

        for ipath in path:
            if 'psipp' in ipath:
                psipp_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/'+str(sample)+'/sigMC_psipp_'+str(sample)+'_after.root'
                f_psipp = TFile(psipp_path, 'READ')
                t_psipp = f_psipp.Get('save')
                f_psipp_w = TFile(ipath, 'READ')
                t_psipp_w = f_psipp_w.Get('weight')
                entries_psipp = t_psipp.GetEntries()
                entries_psipp_w = t_psipp_w.GetEntries()
                if entries_psipp == entries_psipp_w: logging.info('psipp('+str(sample)+') entries :'+str(entries_psipp))
                else:
                    print('WRONG: entries_psipp and entries_psipp_w are not equal, please check cut')
                    exit(-1)
                h_psipp_rm_D = TH1D('h_rm_D_psipp', 'h_rm_D_psipp', xbins_rm_D, xmin_rm_D, xmax_rm_D)
                h_psipp_rm_Dmiss = TH1D('h_rm_Dmiss_psipp', 'h_rm_Dmiss_psipp', xbins_rm_Dmiss, xmin_rm_Dmiss, xmax_rm_Dmiss)
                h_psipp_rm_pipi = TH1D('h_rm_pipi_psipp', 'h_rm_pipi_psipp', xbins_rm_pipi, xmin_rm_pipi, xmax_rm_pipi)
                for ientry in xrange(int(t_psipp.GetEntries())):
                    t_psipp.GetEntry(ientry)
                    t_psipp_w.GetEntry(ientry)
                    h_psipp_rm_D.Fill(t_psipp.m_rm_D, t_psipp_w.m_weight)
                    h_psipp_rm_Dmiss.Fill(t_psipp.m_rm_Dmiss, t_psipp_w.m_weight)
                    h_psipp_rm_pipi.Fill(t_psipp.m_rm_pipi, t_psipp_w.m_weight)

            if 'DDPIPI' in ipath:
                DDPIPI_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/'+str(sample)+'/sigMC_D_D_PI_PI_'+str(sample)+'_after.root'
                f_DDPIPI = TFile(DDPIPI_path, 'READ')
                t_DDPIPI = f_DDPIPI.Get('save')
                f_DDPIPI_w = TFile(ipath, 'READ')
                t_DDPIPI_w = f_DDPIPI_w.Get('weight')
                entries_DDPIPI = t_DDPIPI.GetEntries()
                entries_DDPIPI_w = t_DDPIPI_w.GetEntries()
                if entries_DDPIPI == entries_DDPIPI_w: logging.info('DDPIPI('+str(sample)+') entries :'+str(entries_DDPIPI))
                else:
                    print('WRONG: entries_DDPIPI and entries_DDPIPI_w are not equal, please check cut')
                    exit(-1)
                h_DDPIPI_rm_D = TH1D('h_rm_D_DDPIPI', 'h_rm_D_DDPIPI', xbins_rm_D, xmin_rm_D, xmax_rm_D)
                h_DDPIPI_rm_Dmiss = TH1D('h_rm_Dmiss_DDPIPI', 'h_rm_Dmiss_DDPIPI', xbins_rm_Dmiss, xmin_rm_Dmiss, xmax_rm_Dmiss)
                h_DDPIPI_rm_pipi = TH1D('h_rm_pipi_DDPIPI', 'h_rm_pipi_DDPIPI', xbins_rm_pipi, xmin_rm_pipi, xmax_rm_pipi)
                for ientry in xrange(int(t_DDPIPI.GetEntries())):
                    t_DDPIPI.GetEntry(ientry)
                    t_DDPIPI_w.GetEntry(ientry)
                    h_DDPIPI_rm_D.Fill(t_DDPIPI.m_rm_D, t_DDPIPI_w.m_weight)
                    h_DDPIPI_rm_Dmiss.Fill(t_DDPIPI.m_rm_Dmiss, t_DDPIPI_w.m_weight)
                    h_DDPIPI_rm_pipi.Fill(t_DDPIPI.m_rm_pipi, t_DDPIPI_w.m_weight)

            if 'D1_2420' in ipath:
                D1_2420_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/'+str(sample)+'/sigMC_D1_2420_'+str(sample)+'_after.root'
                f_D1_2420 = TFile(D1_2420_path, 'READ')
                t_D1_2420 = f_D1_2420.Get('save')
                f_D1_2420_w = TFile(ipath, 'READ')
                t_D1_2420_w = f_D1_2420_w.Get('weight')
                entries_D1_2420 = t_D1_2420.GetEntries()
                entries_D1_2420_w = t_D1_2420_w.GetEntries()
                if entries_D1_2420 == entries_D1_2420_w: logging.info('D1_2420('+str(sample)+') entries :'+str(entries_D1_2420))
                else:
                    print('WRONG: entries_D1_2420 and entries_D1_2420_w are not equal, please check cut')
                    exit(-1)
                h_D1_2420_rm_D = TH1D('h_rm_D_D1_2420', 'h_rm_D_D1_2420', xbins_rm_D, xmin_rm_D, xmax_rm_D)
                h_D1_2420_rm_Dmiss = TH1D('h_rm_Dmiss_D1_2420', 'h_rm_Dmiss_D1_2420', xbins_rm_Dmiss, xmin_rm_Dmiss, xmax_rm_Dmiss)
                h_D1_2420_rm_pipi = TH1D('h_rm_pipi_D1_2420', 'h_rm_pipi_D1_2420', xbins_rm_pipi, xmin_rm_pipi, xmax_rm_pipi)
                for ientry in xrange(int(t_D1_2420.GetEntries())):
                    t_D1_2420.GetEntry(ientry)
                    t_D1_2420_w.GetEntry(ientry)
                    h_D1_2420_rm_D.Fill(t_D1_2420.m_rm_D, t_D1_2420_w.m_weight)
                    h_D1_2420_rm_Dmiss.Fill(t_D1_2420.m_rm_Dmiss, t_D1_2420_w.m_weight)
                    h_D1_2420_rm_pipi.Fill(t_D1_2420.m_rm_pipi, t_D1_2420_w.m_weight)
    except Exception as e:
        print(str(e))
        logging.error('Files are invalid!')
        sys.exit()
    
    N_D1_2420, N_PSIPP, N_DDPIPI = num_rm_D(sample)
    if sample > 4311:
        n2420 = RooRealVar('n2420', 'n2420', 500, 0, N_D1_2420)
    nsideband = RooRealVar('nsideband', 'nsideband', int(entries_sideband/2.))
    npsipp = RooRealVar('npsipp', 'npsipp', 0, N_PSIPP)
    nDDPIPI = RooRealVar('nDDPIPI', 'nDDPIPI', 0, N_DDPIPI)

    # model for RM(D)
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
    if sample > 4311:
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
    if sample > 4311:
        cut = ''
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
    if sample > 4311:
        cut = ''
        hist_D1_2420_rm_pipi = RooDataHist('hist_D1_2420_rm_pipi', 'hist_D1_2420_rm_pipi', RooArgList(rm_pipi), h_D1_2420_rm_pipi)
        pdf_D1_2420_rm_pipi = RooHistPdf('pdf_D1_2420_rm_pipi', 'pdf_D1_2420_rm_pipi', RooArgSet(rm_pipi), hist_D1_2420_rm_pipi, 2)
        model_rm_pipi = RooAddPdf('model_rm_pipi', 'model_rm_pipi', RooArgList(pdf_D1_2420_rm_pipi, pdf_sideband_rm_pipi, covpdf_psipp, pdf_DDPIPI_rm_pipi), RooArgList(n2420, nsideband, npsipp, nDDPIPI))
    else:
        model_rm_pipi = RooAddPdf('model_rm_pipi', 'model_rm_pipi', RooArgList(pdf_sideband_rm_pipi, covpdf_psipp, pdf_DDPIPI_rm_pipi), RooArgList(nsideband, npsipp, nDDPIPI))

    # simultaneous fit
    SAMPLE = RooCategory('SAMPLE', 'SAMPLE')
    SAMPLE.defineType('rm_D')
    SAMPLE.defineType('rm_Dmiss')
    SAMPLE.defineType('rm_pipi')
    combData = RooDataSet('combData', 'combined data', RooArgSet(rm_D, rm_Dmiss, rm_pipi), 
        RooFit.Index(SAMPLE), RooFit.Import('rm_D', set_data_rm_D), RooFit.Import('rm_Dmiss', set_data_rm_Dmiss), RooFit.Import('rm_pipi', set_data_rm_pipi))
    sim_pdf = RooSimultaneous('sim_pdf', 'simultaneous pdf', SAMPLE)
    sim_pdf.addPdf(model_rm_D, 'rm_D')
    sim_pdf.addPdf(model_rm_Dmiss, 'rm_Dmiss')
    sim_pdf.addPdf(model_rm_pipi, 'rm_pipi')
    fit_result = sim_pdf.fitTo(combData, RooFit.Extended(kTRUE), RooFit.Save(kTRUE))

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
    combData.plotOn(frame_rm_D, RooFit.Cut('SAMPLE==SAMPLE::rm_D'), RooFit.Name('data'))
    sim_pdf.plotOn(frame_rm_D, RooFit.Slice(SAMPLE, 'rm_D'), RooFit.Components('pdf_sideband_rm_D'), RooFit.ProjWData(RooArgSet(SAMPLE), combData), RooFit.LineColor(kGreen), RooFit.FillStyle(1001), RooFit.FillColor(3), RooFit.LineColor(3), RooFit.VLines(), RooFit.DrawOption('F'))
    if sample > 4311:
        sim_pdf.plotOn(frame_rm_D, RooFit.Slice(SAMPLE, 'rm_D'), RooFit.Components('covpdf_D1_2420_D'), RooFit.ProjWData(RooArgSet(SAMPLE), combData), RooFit.LineColor(kRed), RooFit.LineWidth(2), RooFit.LineStyle(kDashed))
    sim_pdf.plotOn(frame_rm_D, RooFit.Slice(SAMPLE, 'rm_D'), RooFit.Components('pdf_psipp_rm_D'), RooFit.ProjWData(RooArgSet(SAMPLE), combData), RooFit.LineColor(kBlue), RooFit.LineWidth(2), RooFit.LineStyle(kDashed))
    sim_pdf.plotOn(frame_rm_D, RooFit.Slice(SAMPLE, 'rm_D'), RooFit.Components('pdf_DDPIPI_rm_D'), RooFit.ProjWData(RooArgSet(SAMPLE), combData), RooFit.LineColor(37), RooFit.LineWidth(2), RooFit.LineStyle(kDashed))
    sim_pdf.plotOn(frame_rm_D, RooFit.Slice(SAMPLE, 'rm_D'), RooFit.ProjWData(RooArgSet(SAMPLE), combData), RooFit.LineColor(kBlack), RooFit.LineWidth(3), RooFit.Name('TotFit'))
    combData.plotOn(frame_rm_D, RooFit.Cut('SAMPLE==SAMPLE::rm_D'))

    name = []
    name.append('Data')
    name.append('Backgrounds')
    if sample > 4311:
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
    lg_rm_D.SetHeader(str(sample) + ' MeV')
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
    combData.plotOn(frame_rm_Dmiss, RooFit.Cut('SAMPLE==SAMPLE::rm_Dmiss'), RooFit.Name('data'))
    sim_pdf.plotOn(frame_rm_Dmiss, RooFit.Slice(SAMPLE, 'rm_Dmiss'), RooFit.Components('pdf_sideband_rm_Dmiss'), RooFit.ProjWData(RooArgSet(SAMPLE), combData), RooFit.LineColor(kGreen), RooFit.FillStyle(1001), RooFit.FillColor(3), RooFit.LineColor(3), RooFit.VLines(), RooFit.DrawOption('F'))
    if sample > 4311:
        sim_pdf.plotOn(frame_rm_Dmiss, RooFit.Slice(SAMPLE, 'rm_Dmiss'), RooFit.Components('covpdf_D1_2420_D'), RooFit.ProjWData(RooArgSet(SAMPLE), combData), RooFit.LineColor(kRed), RooFit.LineWidth(2), RooFit.LineStyle(kDashed))
    sim_pdf.plotOn(frame_rm_Dmiss, RooFit.Slice(SAMPLE, 'rm_Dmiss'), RooFit.Components('pdf_psipp_rm_Dmiss'), RooFit.ProjWData(RooArgSet(SAMPLE), combData), RooFit.LineColor(kBlue), RooFit.LineWidth(2), RooFit.LineStyle(kDashed))
    sim_pdf.plotOn(frame_rm_Dmiss, RooFit.Slice(SAMPLE, 'rm_Dmiss'), RooFit.Components('pdf_DDPIPI_rm_Dmiss'), RooFit.ProjWData(RooArgSet(SAMPLE), combData), RooFit.LineColor(37), RooFit.LineWidth(2), RooFit.LineStyle(kDashed))
    sim_pdf.plotOn(frame_rm_Dmiss, RooFit.Slice(SAMPLE, 'rm_Dmiss'), RooFit.ProjWData(RooArgSet(SAMPLE), combData), RooFit.LineColor(kBlack), RooFit.LineWidth(3), RooFit.Name('TotFit'))
    combData.plotOn(frame_rm_Dmiss, RooFit.Cut('SAMPLE==SAMPLE::rm_Dmiss'))

    name = []
    name.append('Data')
    name.append('Backgrounds')
    if sample > 4311:
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
    lg_rm_Dmiss.SetHeader(str(sample) + ' MeV')
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
    combData.plotOn(frame_rm_pipi, RooFit.Cut('SAMPLE==SAMPLE::rm_pipi'), RooFit.Name('data'))
    sim_pdf.plotOn(frame_rm_pipi, RooFit.Slice(SAMPLE, 'rm_pipi'), RooFit.Components('pdf_sideband_rm_pipi'), RooFit.ProjWData(RooArgSet(SAMPLE), combData), RooFit.LineColor(kGreen), RooFit.FillStyle(1001), RooFit.FillColor(3), RooFit.LineColor(3), RooFit.VLines(), RooFit.DrawOption('F'))
    if sample > 4311:
        sim_pdf.plotOn(frame_rm_pipi, RooFit.Slice(SAMPLE, 'rm_pipi'), RooFit.Components('pdf_D1_2420_rm_pipi'), RooFit.ProjWData(RooArgSet(SAMPLE), combData), RooFit.LineColor(kRed), RooFit.LineWidth(2), RooFit.LineStyle(kDashed))
    sim_pdf.plotOn(frame_rm_pipi, RooFit.Slice(SAMPLE, 'rm_pipi'), RooFit.Components('covpdf_psipp'), RooFit.ProjWData(RooArgSet(SAMPLE), combData), RooFit.LineColor(kBlue), RooFit.LineWidth(2), RooFit.LineStyle(kDashed))
    sim_pdf.plotOn(frame_rm_pipi, RooFit.Slice(SAMPLE, 'rm_pipi'), RooFit.Components('pdf_DDPIPI_rm_pipi'), RooFit.ProjWData(RooArgSet(SAMPLE), combData), RooFit.LineColor(37), RooFit.LineWidth(2), RooFit.LineStyle(kDashed))
    sim_pdf.plotOn(frame_rm_pipi, RooFit.Slice(SAMPLE, 'rm_pipi'), RooFit.ProjWData(RooArgSet(SAMPLE), combData), RooFit.LineColor(kBlack), RooFit.LineWidth(3), RooFit.Name('TotFit'))
    combData.plotOn(frame_rm_pipi, RooFit.Cut('SAMPLE==SAMPLE::rm_pipi'))

    name = []
    name.append('Data')
    name.append('Backgrounds')
    if sample > 4311:
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
    lg_rm_pipi.SetHeader(str(sample) + ' MeV')
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

    raw_input('Press <Enter> to continue...')

def main():
    args = sys.argv[1:]
    if len(args)<2:
        return usage()
    sample = int(args[0])
    patch = args[1]

    path = []
    if sample > 4311:
        path.append('../weights/weighted_psipp_'+str(sample)+'_'+patch+'.root')
        path.append('../weights/weighted_DDPIPI_'+str(sample)+'_'+patch+'.root')
        path.append('../weights/weighted_D1_2420_'+str(sample)+'_'+patch+'.root')
        fit(sample, patch, path)

    if sample <= 4311:
        path.append('../weights/weighted_psipp_'+str(sample)+'_'+patch+'.root')
        path.append('../weights/weighted_DDPIPI_'+str(sample)+'_'+patch+'.root')
        fit(sample, patch, path)

if __name__ == '__main__':
    main()
