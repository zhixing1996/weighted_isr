#!/usr/bin/env python
#-*- coding: utf-8 -*-

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>, inspired by Lianjin WU <wulj@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING, Lianjin WU"
__created__ = "[2020-11-06 Fri 23:18]"

from sys import *
from ROOT import *
from math import *
from array import *
import sys

def set_pub_style():
    gStyle.SetPaperSize(20, 26)
    gStyle.SetPadColor(0)
    gStyle.SetPadBorderMode(0)
    gStyle.SetPadTopMargin(0.03)
    gStyle.SetPadRightMargin(0.05)
    gStyle.SetPadBottomMargin(0.22)
    gStyle.SetPadLeftMargin(0.12)
    gStyle.SetTitleFillColor(0)
    gStyle.SetTitleFont(22, 'xyz') 
    gStyle.SetTitleFont(22, ' ')
    gStyle.SetTitleSize(0.06, 'xyz') 
    gStyle.SetTitleSize(0.06, ' ')
    gStyle.SetLabelFont(22, 'xyz')
    gStyle.SetLabelSize(0.05, 'xyz')
    gStyle.SetTextFont(22)
    gStyle.SetTextSize(0.08)
    gStyle.SetStatFont(22)
    gStyle.SetFrameBorderMode(0)
    gStyle.SetCanvasBorderMode(0)
    gStyle.SetCanvasColor(0)
    gStyle.SetStatColor(0)
    gStyle.SetMarkerStyle(8)
    gStyle.SetHistFillColor(0)
    gStyle.SetLineWidth(2)
    gStyle.SetLineStyleString(2, '[12 12]')
    gStyle.SetErrorX(0.001)
    gStyle.SetOptTitle(0)
    gStyle.SetOptStat(0)
    gStyle.SetOptFit(0)
    gStyle.SetPadTickX(0)
    gStyle.SetPadTickY(0)

def set_graph_style(gr, xtitle, ytitle):
    gr.GetXaxis().SetNdivisions(509)
    gr.GetYaxis().SetNdivisions(504)
    gr.SetLineWidth(2)
    gr.GetXaxis().SetTitleSize(0.06)
    gr.GetXaxis().SetTitleOffset(1.05)
    gr.GetXaxis().SetLabelOffset(0.01)
    gr.GetYaxis().SetTitleSize(0.06)
    gr.GetYaxis().SetTitleOffset(1.05)
    gr.GetYaxis().SetLabelOffset(0.01)
    gr.GetXaxis().SetTitle(xtitle)
    gr.GetXaxis().CenterTitle()
    gr.GetYaxis().SetTitle(ytitle)
    gr.GetYaxis().CenterTitle()
    gr.SetMarkerColor(1)
    gr.SetMarkerStyle(21)

def set_pad_style(pad):
    pad.SetLeftMargin(0.35)
    pad.SetRightMargin(0.15)
    pad.SetTopMargin(0.1)
    pad.SetBottomMargin(0.15)
    pad.SetFrameLineColor(kBlack)

def set_canvas_style(mbc):
    mbc.SetFillColor(0)
    mbc.SetLeftMargin(0.15)
    mbc.SetRightMargin(0.15)
    mbc.SetTopMargin(0.1)
    mbc.SetBottomMargin(0.15)
    mbc.SetGrid()

def set_pavetext(pt):
    pt.SetFillStyle(0)
    pt.SetBorderSize(0)
    pt.SetTextAlign(10)
    pt.SetTextSize(0.04)
    pt.SetTextSize(0.05)

def set_frame_style(frame, xtitle, ytitle):
    frame.GetXaxis().SetTitle(xtitle)
    frame.GetXaxis().SetTitleSize(0.06)
    frame.GetXaxis().SetLabelSize(0.04)
    frame.GetXaxis().SetTitleOffset(1.0)
    frame.GetXaxis().SetLabelOffset(0.008)
    frame.GetXaxis().SetNdivisions(508)
    frame.GetXaxis().CenterTitle()
    frame.GetYaxis().SetNdivisions(504)
    frame.GetYaxis().SetTitleSize(0.06)
    frame.GetYaxis().SetLabelSize(0.04)
    frame.GetYaxis().SetTitleOffset(1.0)
    frame.GetYaxis().SetLabelOffset(0.008)
    frame.GetYaxis().SetTitle(ytitle)
    frame.GetYaxis().CenterTitle()
