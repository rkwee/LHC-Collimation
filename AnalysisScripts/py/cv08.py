#!/usr/bin/python
#
#
# Nov  2013, rkwee
## -------------------------------------------------------------------------------
import ROOT, sys, glob, os
from ROOT import *
from helpers import workpath
## -------------------------------------------------------------------------------
def cv08():

    rfBGac = TFile.Open('~/Documents/RHUL/work/runs/TCT/HL/results_BGac.root')
    rfBGst = TFile.Open('~/Documents/RHUL/work/runs/TCT/HL/results_BGst.root')

    hname = 'EkinAll'
    hN = hname + '_BGst'
    hD = hname + '_BGac'

    hNumerator = rfBGst.Get(hN)
    hDenominator = rfBGac.Get(hD)

    print hNumerator
    print hDenominator

    cv = TCanvas( 'cv', 'cv', 1200, 900)

    x1, y1, x2, y2 = 0.2, 0.8, 0.9, 0.9
    mlegend = TLegend( x1, y1, x2, y2)
    mlegend.SetFillColor(0)
    mlegend.SetFillStyle(0)
    mlegend.SetLineColor(0)
    mlegend.SetTextSize(0.035)
    mlegend.SetShadowColor(0)
    mlegend.SetBorderSize(0)
    
    hNumerator.GetXaxis().SetTitle('E [GeV]')
    hNumerator.GetYaxis().SetTitle('ratio')

    hNumerator.Divide(hNumerator, hDenominator, 1, 1, 'B')
    mlegend.AddEntry(hNumerator, 'EkinAll BG startup over BG after conditioning', "l")
    gPad.SetLogx(1)
    gPad.SetLogy(0)
    gPad.SetGridy(1)
    hNumerator.GetYaxis().SetRangeUser(86,114)
    hNumerator.Draw('HIST')
    mlegend.Draw()
    pname =  '/Users/rkwee/Documents/RHUL/work/results/www/TCT/HL/nominalSettings/comp/ratio_stOverac.pdf'
    cv.SaveAs(pname)
