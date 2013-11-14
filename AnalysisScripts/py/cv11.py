#!/usr/bin/python
#
#
# Nov  2013, rkwee
## -------------------------------------------------------------------------------
import ROOT, sys, glob, os
from ROOT import *
from helpers import workpath, mylabel
## -------------------------------------------------------------------------------
def cv11():

    rfname = 'results_HL_BH.root'
    tag = '_BH'
    norm = 7330000.
    lText = 'beamhalo'
    subfolder = 'beamhalo/'
    XurMin, XurMax = 2e-2,1e4
    YurMin, YurMax = 1e-6,9
    ytitle = '#frac{dN(counts/TCT hit)}{dlog E}'

    rfname = 'results_BGac.root'
    tag = '_BGac'
    norm = 1.
    lText = 'BG after cond'
    subfolder = 'beamgas/'
    XurMin, XurMax = 2e-2,1e4
    YurMin, YurMax = 1e2,9e7
    ytitle = '#frac{dN(counts/s)}{dlog E}'

    rf = TFile.Open('~/Documents/RHUL/work/runs/TCT/HL/' + rfname)
    # pions char
    hPins = 'EkinPiPlusRInBP'+tag
    hMins = 'EkinPiMinusRInBP'+tag
    hPout = 'EkinPiPlusROutBP'+tag
    hMout = 'EkinPiMinusROutBP'+tag
    histPins = rf.Get(hPins)
    histMins = rf.Get(hMins)
    histPout = rf.Get(hPout)
    histMout = rf.Get(hMout)
    histPionIns = histPins.Clone('cloony'+hPins)
    histPionIns.Add(histMins)
    histPionOut = histPout.Clone('cloony'+hPout)
    histPionOut.Add(histMout)

    # neutrons
    histNeutIns = rf.Get('EkinNeutronsRInBP'+tag)
    histNeutOut = rf.Get('EkinNeutronsROutBP'+tag)

    # all ins/out
    histAllIns = rf.Get('EkinAllRInBP'+tag)
    histAllOut = rf.Get('EkinAllROutBP'+tag)

    cv = TCanvas( 'cv', 'cv', 1200, 900)

    x1, y1, x2, y2 = 0.7, 0.65, 0.9, 0.9
    mlegend = TLegend( x1, y1, x2, y2)
    mlegend.SetFillColor(0)
    mlegend.SetFillStyle(0)
    mlegend.SetLineColor(0)
    mlegend.SetTextSize(0.035)
    mlegend.SetShadowColor(0)
    mlegend.SetBorderSize(0)
    
    leg= [
        ('all, r < r_{bp}', "l"),
        ('#pi^{#pm}, r < r_{bp}', "l"),
        ('n, r < r_{bp}', "l"),
        ('all, r #geq r_{bp}', "l"),
        ('#pi^{#pm}, r #geq r_{bp}', "l"),
        ('n, r #geq r_{bp}', "l"),

    ]

    gPad.SetLogx(1)
    gPad.SetLogy(1)
    gPad.SetGridy(0)

    hists = [
        histAllIns,
        histPionIns,
        histNeutIns,
        histAllOut,
        histPionOut,
        histNeutOut,
    ]

    hcol = [
        kBlack,
        kCyan,
        kAzure-3, 
        kRed,
        kViolet,
        kOrange,
    ]

    for i,hist in enumerate(hists):

        hist.SetLineColor(hcol[i])        
        hist.Scale(1./norm)
        hist.GetXaxis().SetRangeUser(XurMin, XurMax)
        hist.GetYaxis().SetRangeUser(YurMin, YurMax)
        hist.GetXaxis().SetTitle('E [GeV]')
        hist.GetYaxis().SetTitle(ytitle)

        if not i: hist.Draw('HIST')
        else: hist.Draw('HISTSAME')
        mlegend.AddEntry(hist, leg[i][0], "l")

    mlegend.Draw()
    lab = mylabel(42)
    lab.DrawLatex(0.45, 0.85, lText)
    
    gPad.RedrawAxis()

    pname =  '/Users/rkwee/Documents/RHUL/work/results/www/TCT/HL/nominalSettings/'+subfolder+'/EkinBp2'+tag+'.pdf'
    cv.SaveAs(pname)
