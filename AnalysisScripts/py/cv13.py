#!/usr/bin/python
#
#
# Nov  2013, rkwee
## -------------------------------------------------------------------------------
import ROOT, sys, glob, os
from ROOT import *
from helpers import workpath, mylabel
from array import array
from fillTTree_dict import sDict_HL_BGac,sDict_HL_BGst,sDict_BH_3p5TeV,sDict_BH_4TeV
## -------------------------------------------------------------------------------
def cv13():

    # ratio BGac to BGst

    # fNum   = workpath + 'results/results_BGst.root'
    # fDenom = workpath + 'results/results_BGac.root'
    # subfolder = 'HL/compBG/'
    # lTextNum = 'BG start-up'
    # lTextDenom = 'BG after cond.'
    # tagNum, tagDenom = 'BGst', 'BGac'
    # sDict = sDict_BH_4TeV

    fNum   = workpath + 'results/results_beam-halo_3.5TeV-R1_D1.root'
    fDenom = workpath + 'results/results_ir1_4TeV_settings_from_TWISS_b2_nprim7825000_66.root'
    subfolder = '4TeV/compBH/'
    lTextNum = 'BH 3.5 TeV '
    lTextDenom = 'BH 4 TeV'
    tagNum, tagDenom = 'BH_3p5TeV', 'BH_4TeV'
    # tagNum, tagDenom = 'BH_4TeV', 'BH_4TeV'
    sDict = sDict_BH_3p5TeV

    # fNum   = workpath + 'results/results_BH_3p5TeV.root'
    # fDenom = workpath + 'results/results_BH.root'
    # subfolder = 'compBH_HLvs3p5/'
    # lTextNum = 'BH HL TeV'
    # lTextDenom = 'BH 3.5 TeV'
    # tagNum, tagDenom = 'BH_3p5TeV', 'BH'
    # sDict = sDict_BH_3p5TeV

    # fNum   = workpath + 'results/results_BH_3p5TeV.root'
    # fDenom = workpath + 'results/results_BH_3p5TeV_v2.root'
    # subfolder = 'compBH_3p5vs3p5_v2/'
    # lTextNum = 'BH 3.5 TeV'
    # lTextDenom = 'BH 3.5 TeV analytic magnf'
    # tagNum, tagDenom = 'BH_3p5TeV', 'BH_3p5TeV_v2'
    # sDict = sDict_BH_3p5TeV

    rfNum = TFile.Open(fNum)
    rfDenom = TFile.Open(fDenom)
    print 'opening as numerator', fNum
    print 'opening as denominator', fDenom

    msize = 0.05
    for skey in sDict.keys():

        if skey.count('XY'): continue

        cv = TCanvas( 'cv'+skey, 'cv'+skey, 10, 10, 80, 80 )

        x1, y1, x2, y2 = 0.63,0.7,0.95,0.92
        mlegend = TLegend( x1, y1, x2, y2)
        mlegend.SetFillColor(0)
        mlegend.SetFillStyle(0)
        mlegend.SetLineColor(0)
        mlegend.SetTextSize(0.035)
        mlegend.SetShadowColor(0)
        mlegend.SetBorderSize(0)

        p1 = TPad('p1'+skey,'p1'+skey,0.01,0.35,0.99,0.99)
        if skey.count('Ekin'): 
            p1.SetLogx(1)
            p1.SetLogy(1)

        if skey.count('En'): p1.SetLogy(1)

        p1.Draw()
        p1.SetBottomMargin(0.00)

        p2 = TPad('p2'+skey,'p2'+skey,0.01,0.01,0.99,.35)
        if skey.count('Ekin'):
            p2.SetLogx(1)

        p2.Draw()
        p2.SetTopMargin(0.00)
        p2.SetBottomMargin(0.25)

        p1.cd()
        hnameNum = skey
        hnameDenom = hnameNum.replace(tagNum, tagDenom)
        print 'plotting ratio of ', hnameNum, 'and', hnameDenom

        xtitle, ytitle = sDict[skey][9], sDict[skey][10]
        histNum  = rfNum.Get(hnameNum)
        histDenom  = rfDenom.Get(hnameDenom)

        if hnameNum.count('Rad'):
            histNum.Rebin()
            histDenom.Rebin()


        histNum.GetXaxis().SetTitle(xtitle)
        histNum.GetYaxis().SetTitle(ytitle)

        histNum.SetLineColor(kAzure-2)
        histDenom.SetLineColor(kOrange-2)
        histNum.SetMarkerColor(kAzure-2)
        histDenom.SetMarkerColor(kOrange-2)
        histNum.SetMarkerStyle(21)
        histDenom.SetMarkerStyle(20)
        histDenom.SetMarkerSize(msize)
        histNum.SetMarkerSize(msize)

        histNum.Draw('h')
        histDenom.Draw('hsame')

        mlegend.AddEntry(histNum, lTextNum, "l")
        mlegend.AddEntry(histDenom, lTextDenom, "l")
        mlegend.Draw()

        lab = mylabel(42)
        lab.DrawLatex(0.45, 0.85, sDict[skey][6])

        hnameRatio = 'ratio'+hnameNum
        hRatio = histNum.Clone(hnameRatio)

        hRatio.Divide(histNum, histDenom, 1, 1)
        hRatio.SetLineColor(kRed)
        hRatio.SetMarkerColor(kRed)
        hRatio.SetMarkerStyle(22)
        hRatio.SetMarkerSize(msize)

        l = TLine()
        l.SetLineWidth(1)
        l.SetLineColor(kSpring)
        XurMin = hRatio.GetBinLowEdge(1)
        XurMax = hRatio.GetBinLowEdge( hRatio.GetNbinsX()+1 )

        p2.cd()

        if hnameNum.count('Rad') or hRatio.GetMaximum()>200:
            hRatio.GetYaxis().SetRangeUser(-2,2)
        hRatio.GetYaxis().SetTitle('ratio ' + lTextNum + '/' + lTextDenom)
        hRatio.Draw('pe')
        l.DrawLine(XurMin,1,XurMax,1)
        pname =  '/Users/rkwee/Documents/RHUL/work/results/www/TCT/'+subfolder+hnameRatio.split('_')[0]+'.pdf'

        print pname
        cv.SaveAs(pname)
