#!/usr/bin/python
#
#
# Nov  2013, rkwee
## -------------------------------------------------------------------------------
import ROOT, sys, glob, os
from ROOT import *
from helpers import workpath, mylabel
from array import array
## -------------------------------------------------------------------------------
def cv12():


    subfolder = 'comp/'
    hname = 'compMu'

    # 0.01	5.3e-21
    # 0.0125893	5.3e-21
    # 0.0125893	5.3e-21

    muHalo3p5TeV = '/Users/rkwee/Documents/RHUL/work/runs/TCT/muon_rate_enLog_halo.dat'
    muBgas3p5TeV = '/Users/rkwee/Documents/RHUL/work/runs/TCT/muon_rate_enLog_localBG.dat'
    rf = TFile.Open('/Users/rkwee/Documents/RHUL/work/runs/TCT/HL/save/results_comp.root')
    muHaloHLop = rf.Get('EkinMuBHop')
    muHaloHLds = rf.Get('EkinMuBHds')
    muBgasHLst = rf.Get('EkinMuBGst')
    muBgasHLac = rf.Get('EkinMuBGac')
    muHaloHLop.SetLineColor(kGreen+2)
    muHaloHLds.SetLineColor(kPink-9)
    muBgasHLst.SetLineColor(kBlue-1)
    muBgasHLac.SetLineColor(kAzure-3)

    axis, yval = [],[]
    with open(muHalo3p5TeV) as mf:
        for i,line in enumerate(mf):
            # use only every second entry of file
            if not i%2:
                axis += [ float(line.split()[0]) ]
                yval += [ float(line.split()[1]) ]

    yvalBG = []
    with open(muBgas3p5TeV) as mf:
        for i,line in enumerate(mf):
            # use only every second entry of file
            if not i%2:
                yvalBG += [ float(line.split()[1]) ]

    axis += [10000.]
    cv = TCanvas( 'cv', 'cv', 10, 10, 1200, 900 )
    gPad.SetLogx(1)
    # gPad.SetLogy(1)
    histBH = TH1F(hname, hname, len(axis)-1, array('d', axis) )
    histBG = TH1F(hname+'BG', hname+'BG', len(axis)-1, array('d', axis) )
    histBG.SetLineColor(kOrange)
    histBH.SetLineColor(kViolet)

    for i,y in enumerate(yval): 
        histBH.SetBinContent(i+1,y)
    for i,y in enumerate(yvalBG): 
        histBG.SetBinContent(i+1,y)

    histBH.Draw('hist')
    histBG.Draw('histsame')
    XurMin, XurMax, YurMin, YurMax = 2e-2,9e3,1e-1,8e9
    histBH.GetXaxis().SetRangeUser(XurMin, XurMax)
    histBH.GetYaxis().SetRangeUser(YurMin, YurMax)

    xtitle, ytitle = 'E [GeV]', '#frac{dN(counts/s)}{dlog E}'
    histBH.GetXaxis().SetTitle(xtitle)
    histBH.GetYaxis().SetTitle(ytitle)
    muHaloHLop.Draw('histsame')
    muHaloHLds.Draw('histsame')
    muBgasHLst.Draw('histsame')
    muBgasHLac.Draw('histsame')

    x1, y1, x2, y2 = 0.63,0.7,0.95,0.92
    mlegend = TLegend( x1, y1, x2, y2)
    mlegend.SetFillColor(0)
    mlegend.SetFillStyle(0)
    mlegend.SetLineColor(0)
    mlegend.SetTextSize(0.035)
    mlegend.SetShadowColor(0)
    mlegend.SetBorderSize(0)
    mlegend.AddEntry(muBgasHLst, 'BG start-up', "l")
    mlegend.AddEntry(muBgasHLac, 'BG after cond.', "l")
    mlegend.AddEntry(histBG, 'BG at 3.5 TeV', "l")

    mlegend.AddEntry(muHaloHLds, 'BH 12 min loss', "l")
    mlegend.AddEntry(muHaloHLop, 'BH 100h loss', "l")
    mlegend.AddEntry(histBH, 'BH at 3.5 TeV', "l")

    mlegend.Draw()
    lab = mylabel(42)
    lab.DrawLatex(0.45, 0.85, '#mu^{#pm}')
    
    gPad.RedrawAxis()

    pname =  '/Users/rkwee/Documents/RHUL/work/results/www/TCT/HL/nominalSettings/'+subfolder+'/EkinMuComp3p5.pdf'
    #cv.SaveAs(pname)

    histRatioBG = histBG.Clone('cloon')
    histRatioBH = histBH.Clone('cloony')

    #    hNumerator.Divide(hNumerator, hDenominator, 1, 1, 'B')
    histRatioBG.Divide(histRatioBG, muBgasHLac, 1, 1, 'B')
    XurMin, XurMax, YurMin, YurMax = 2e-2,9e3,0,4
    histRatioBG.GetXaxis().SetRangeUser(XurMin, XurMax)
    histRatioBG.GetYaxis().SetRangeUser(YurMin, YurMax)

    histRatioBG.Draw('hist')
    mlabBH = mylabel(42)
    l = TLine()
    l.SetLineWidth(1)
    l.SetLineColor(1)
    l.DrawLine(XurMin,2.5,XurMax,2.5)
    l.DrawLine(XurMin,1,XurMax,1)
    mlabBH.DrawLatex(0.45, 0.85, 'BG 3.5 TeV/BG a.c. HL')
    pname =  '/Users/rkwee/Documents/RHUL/work/results/www/TCT/HL/nominalSettings/'+subfolder+'/compMuBG.pdf'
    cv.SaveAs(pname)
    
    histRatioBH.Divide(histRatioBH, muHaloHLop, 1, 1, 'B')
    XurMin, XurMax, YurMin, YurMax = 2e-2,9e3,1e-5,1
    histRatioBH.GetXaxis().SetRangeUser(XurMin, XurMax)
    histRatioBH.GetYaxis().SetRangeUser(YurMin, YurMax)

    histRatioBH.Draw('hist')

    mlab = mylabel(42)
    mlab.DrawLatex(0.45, 0.85, 'BH 3.5 TeV/BH #tau_{beam} = 100h')

    l = TLine()
    l.SetLineWidth(1)
    l.SetLineColor(1)
    l.DrawLine(XurMin,0.1,XurMax,0.1)
    pname =  '/Users/rkwee/Documents/RHUL/work/results/www/TCT/HL/nominalSettings/'+subfolder+'/compMuBH.pdf'
    cv.SaveAs(pname)
