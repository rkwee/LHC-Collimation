#!/usr/bin/python
# # fluka output TCT hits
#
# R Kwee-Hinzmann, Mar 2015
# ---------------------------------------------------------------------------------
import ROOT, sys, glob, os, math, helpers
from ROOT import *
from helpers import *
from array import array
# ---------------------------------------------------------------------------------
def doTCTs(var, mt, hname, nbins, xmin, xmax, ynbins, ymin, ymax, tct, s):

    hist = TH2F(hname, hname, nbins, xmin, xmax, ynbins, ymin, ymax)
    cuts = []
    debug = 1

    # store sum of squares of weights 
    hist.Sumw2()

    zB = 100*fabs(s-length_LHC)
    zA = 100*fabs(s-length_LHC+1.)

    cuts += [ 'z_interact <= ' + str(zB) + " && z_interact > " + str(zA)]

    if debug: print 'INFO: will fill these variables ', var, 'into', hname

    if cuts: cut = 'weight * (' + ' && '.join(cuts) + ')'
    else: cut = 'weight'

    if debug: print 'INFO: will apply a cut of ', cut, 'to', hname
    mt.Project(hname, var, cut)
    if debug: print 'INFO: Have ', hist.GetEntries(), ' entries in', hname

    return hist
# ---------------------------------------------------------------------------------
def resultFile(bbgFile):
    k=bbgFile
    n='/'.join(k.split('/')[:-1]) + '/orig_' + k.split('/')[-1]
    return  n
# ---------------------------------------------------------------------------------
def cv33():
    # histname+entrie
    #gStyle.SetOptStat(0111)

    # name, entries, mean, rms
    # gStyle.SetOptStat(1111)
    #gStyle.SetOptStat(111111)
    # only entries!
    #gStyle.SetOptStat(10)
    gStyle.SetPalette(1)
    gStyle.SetStatX(0.90)
    gStyle.SetStatY(0.95)
    gStyle.SetTitleX(0.1)
    gStyle.SetTitleY(.955)

    bbgFile = workpath + 'runs/FL_TCT5IN_roundthin/hilumi_ir1_hybrid_b1_20MeV_exp_nprim1635000_30.root'

    print "Opening...", bbgFile
    norm = float(bbgFile.split('nprim')[-1].split('_')[0])

    rf   = TFile.Open(bbgFile)
    mt   = rf.Get('particle')

    yrel = '/TCT hit'

    tcts = [
        ( 52    ,'TCTH.4L1.B1',  26525.36),
        ( 53   ,'TCTVA.4L1.B1',  26527.04),
        ( 54    ,'TCTH.5L1.B1',  26445.00),
        ( 55   ,'TCTVA.5L1.B1',  26446.70),
        ]

    # histograms which should be written one to rootfile
    rHists = []

    # rootfile with results
    rfoutname = resultFile(bbgFile)

    print 'writing ','.'*20, rfoutname
    rfile = TFile.Open(rfoutname, "RECREATE")

    hists = []
    cnt = 0

    for collid,tct,s in tcts:

        cv = TCanvas( 'cv'+tct, 'cv'+tct, 900, 900)

        gStyle.SetPalette(1)
        cv.SetRightMargin(0.15)
        gPad.SetLeftMargin(-0.1)

        xnbins, xmin, xmax, ynbins, ymin, ymax = 200, -12., -2, 100, -5., 5
        hname = "OrigXYNAll" + tct.replace('.','_') + tag_BH_7TeV
        var = 'y_interact:x_interact'
        xtitle, ytitle = 'x [cm]', 'y [cm]'
        hist  = doTCTs(var, mt, hname, xnbins, xmin, xmax, ynbins, ymin, ymax, tct, s) 
        hist.GetZaxis().SetLabelSize(0.035)
        hist.GetXaxis().SetLabelSize(0.035)
        hist.GetYaxis().SetLabelSize(0.035)
        hist.GetZaxis().SetTitleSize(0.035)
        hist.GetXaxis().SetTitleSize(0.035)
        hist.GetYaxis().SetTitleSize(0.035)
        hist.GetXaxis().SetTitle(xtitle)
        hist.GetYaxis().SetTitle(ytitle)

        if norm != 1.: print 'normalising by ', norm
        hist.Scale(1./norm)

        hist.Draw("COLZ")
        x1, y1, x2, y2 = 0.2, 0.98, 0.84, 0.9
        lab = mylabel(60)
        lab.DrawLatex(x1, y1-0.1, tct)

        subfolder= 'TCT/HL/relaxedColl/newScatt/fluka/tcthits/'
        pname = wwwpath + subfolder + hname + '.pdf'
        cv.SaveAs(pname)

        # ......................................................................

        cv = TCanvas( 'cvv'+tct, 'cvv'+tct, 1200, 900)
        cv.SetRightMargin(0.15)
        zB = 100*fabs(s-length_LHC)
        zA = 100*fabs(s-length_LHC+1.)

        xnbins, xmin, xmax, ynbins, ymin, ymax = 200, zA, zB, 100, -12., -2.
        hname = "OrigZXNAll" + tct.replace('.','_') + tag_BH_7TeV
        var = 'x_interact:z_interact'
        xtitle, ytitle = 'z [cm]', 'x [cm]'
        hist  = doTCTs(var, mt, hname, xnbins, xmin, xmax, ynbins, ymin, ymax, tct, s) 
        hist.GetZaxis().SetLabelSize(0.035)
        hist.GetXaxis().SetLabelSize(0.035)
        hist.GetYaxis().SetLabelSize(0.035)
        hist.GetZaxis().SetTitleSize(0.035)
        hist.GetXaxis().SetTitleSize(0.035)
        hist.GetYaxis().SetTitleSize(0.035)
        hist.GetXaxis().SetTitle(xtitle)
        hist.GetYaxis().SetTitle(ytitle)
        
        if norm != 1.: print 'normalising by ', norm
        hist.Scale(1./norm)

        hist.Draw("COLZ")
        x1, y1, x2, y2 = 0.2, 0.98, 0.84, 0.9
        lab = mylabel(60)
        lab.DrawLatex(x1, y1-0.1, tct)

        subfolder= 'TCT/HL/relaxedColl/newScatt/fluka/tcthits/'
        pname = wwwpath + subfolder + hname + '.pdf'
        cv.SaveAs(pname)

        # ......................................................................

        cv = TCanvas( 'cvvr'+tct, 'cvvr'+tct, 1200, 900)
        cv.SetRightMargin(0.15)

        xnbins, xmin, xmax, ynbins, ymin, ymax = 200, zA, zB, 100, -5, 5.
        hname = "OrigZYNAll" + tct.replace('.','_') + tag_BH_7TeV
        var = 'y_interact:z_interact'
        xtitle, ytitle = 'z [cm]', 'y [cm]'
        hist  = doTCTs(var, mt, hname, xnbins, xmin, xmax, ynbins, ymin, ymax, tct, s) 
        hist.GetZaxis().SetLabelSize(0.035)
        hist.GetXaxis().SetLabelSize(0.035)
        hist.GetYaxis().SetLabelSize(0.035)
        hist.GetZaxis().SetTitleSize(0.035)
        hist.GetXaxis().SetTitleSize(0.035)
        hist.GetYaxis().SetTitleSize(0.035)
        hist.GetXaxis().SetTitle(xtitle)
        hist.GetYaxis().SetTitle(ytitle)
        
        if norm != 1.: print 'normalising by ', norm
        hist.Scale(1./norm)

        hist.Draw("COLZ")
        x1, y1, x2, y2 = 0.2, 0.98, 0.84, 0.9
        lab = mylabel(60)
        lab.DrawLatex(x1, y1-0.1, tct)

        subfolder= 'TCT/HL/relaxedColl/newScatt/fluka/tcthits/'
        pname = wwwpath + subfolder + hname + '.pdf'
        cv.SaveAs(pname)
                
