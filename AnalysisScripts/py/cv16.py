#!/usr/bin/python
#
#
# Nov  2013, rkwee
## -------------------------------------------------------------------------------
import ROOT, sys, glob, os
from ROOT import *
from helpers import workpath, mylabel
from createTTree import treeName
from fillTTree_dict import generate_sDict
## -------------------------------------------------------------------------------
def cv16():

    # need one file to generate sDict
    bbgFile = workpath + 'results/results_ir1_4TeV_settings_from_TWISS_20MeV_b1_nprim6971000_66.root'
    print "Opening...", bbgFile
    tag = '_BH_4TeV_B1'
    norm = float(bbgFile.split('nprim')[-1].split('_')[0])
    tBBG = TFile.Open(bbgFile).Get(treeName)
    yrel = '/TCT hit'
    sDict = generate_sDict(tag, norm, tBBG, yrel)

    fNum   = workpath + 'results/results_ir1_4TeV_settings_from_TWISS_20MeV_b1_nprim6971000_66.root'
    fDenom = workpath + 'results/results_ir1_4TeV_settings_from_TWISS_b2_nprim7825000_66.root'
    subfolder = '4TeV/compB1B2/'
    lTextNum = 'B1'
    lTextDenom = 'B2'
    tagNum, tagDenom = 'BH_4TeV_B1', 'BH_4TeV_B2'

    rfNum = TFile.Open(fNum)
    rfDenom = TFile.Open(fDenom)
    print 'opening as numerator', fNum
    print 'opening as denominator', fDenom

    nColor, dColor = kOrange-3, kPink-7
    msize = 0.05
    for skey in sDict.keys():

        if skey.count('XY'): continue

        cv = TCanvas( 'cv'+skey, 'cv'+skey, 100, 120, 600, 600 )

        x1, y1, x2, y2 = 0.73,0.75,0.98,0.9
        mlegend = TLegend( x1, y1, x2, y2)
        mlegend.SetFillColor(0)
        mlegend.SetFillStyle(0)
        mlegend.SetLineColor(0)
        mlegend.SetTextSize(0.035)
        mlegend.SetShadowColor(0)
        mlegend.SetBorderSize(0)

        p1 = TPad('p1'+skey,'p1'+skey,0.01,0.35,0.99,0.99)

        ymax = 2.
        if skey.count('Ekin'): 
            p1.SetLogx(1)
            p1.SetLogy(1)
            ymax = 3.

        if skey.count('En'): 
            p1.SetLogy(1)
            ymax = 3.

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

        histNum.SetLineColor(nColor)
        histDenom.SetLineColor(dColor)
        histNum.SetMarkerColor(nColor)
        histDenom.SetMarkerColor(dColor)
        histNum.SetMarkerStyle(21)
        histDenom.SetMarkerStyle(20)
        histDenom.SetMarkerSize(msize)
        histNum.SetMarkerSize(msize)

        histNum.SetMaximum(ymax * histNum.GetMaximum())
        histNum.Draw('h')
        histDenom.Draw('hsame')

        mlegend.AddEntry(histNum, lTextNum, "l")
        mlegend.AddEntry(histDenom, lTextDenom, "l")
        mlegend.Draw()

        lab = mylabel(42)
        lab.DrawLatex(0.56, 0.82, sDict[skey][6])

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

        hRatio.GetXaxis().SetLabelSize(0.1)
        hRatio.GetYaxis().SetLabelSize(0.08)
        hRatio.GetYaxis().SetTitleOffset(0.6)
        hRatio.GetYaxis().SetTitleSize(0.08)
        hRatio.GetXaxis().SetTitleSize(0.08)
        hRatio.Draw('pe')
        hRatio.GetYaxis().SetTitle('ratio ' + lTextNum + '/' + lTextDenom + " ")
        l.DrawLine(XurMin,1,XurMax,1)
        pname =  '/Users/rkwee/Documents/RHUL/work/results/www/TCT/'+subfolder+hnameRatio.split('_')[0]+'.pdf'

        print pname
        cv.SaveAs(pname)
