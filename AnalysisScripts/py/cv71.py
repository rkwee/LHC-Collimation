#!/usr/bin/python
#
# reads histograms with reweights
# Sept 16
#
# R Kwee, 2016
# 
# ---------------------------------------------------------------------------------
import ROOT, sys, glob, os, math, helpers
from ROOT import *
from array import array
# get function to read the data if 14 columns are present 
from cv32 import getdata14c
from helpers import makeTGraph, mylabel, wwwpath
from fillTTree_dict import generate_sDict
# --------------------------------------------------------------------------------
def doEkin(hist,nbins):
    for bin in range(1,nbins+1):
        content = hist.GetBinContent(bin)
        width   = hist.GetBinWidth(bin)
        bcenter = hist.GetXaxis().GetBinCenterLog(bin)
        hist.SetBinContent(bin,bcenter*content/width)
    return hist

def doPhi(hist,nbins):
    for i in range(1,nbins+1):
        content = hist.GetBinContent(i)
        binWidth = hist.GetBinWidth(i)
        hist.SetBinContent(i,content/binWidth)
        hist.SetBinError(i,hist.GetBinError(i)/binWidth)
    return hist

def doRad(hist,nbins):
    for i in range(1,nbins+1):
        binArea = math.pi * (xaxis[i+1]**2 - xaxis[i]**2)
        content = hist.GetBinContent(i)
        hist.SetBinContent(i,content/binArea)
        hist.SetBinError(i,hist.GetBinError(i)/binArea)
    return hist

# --------------------------------------------------------------------------------
def resultFileBG(k,rel):
    n = os.path.join(os.path.dirname(k),"results_pressure2012_"+rel+k.split('/')[-1])
    return  n
# --------------------------------------------------------------------------------
def cv71():

    datafile = '/afs/cern.ch/project/lhc_mib/valBG4TeV/ir1_BG_bs_4TeV_20MeV_b1_nprim5925000_67'
    bbgFile = datafile + ".root"
    print "Opening", bbgFile
    tag = '_BG_4TeV_20MeV_bs'
    norm = float(bbgFile.split('nprim')[-1].split('_')[0])
    rfile = TFile.Open(bbgFile, "READ")
    tBBG = rfile.Get("particle")
    yrel = ''
    print tBBG
    sDict = generate_sDict(tag, norm, tBBG, yrel)

    # -- small version of plotSpectra
    beamintensity = 2e14    
    Trev  = 2*math.pi/112450
    kT = 1.38e-23*300

    # rootfile with results
    rfoutname = resultFileBG(bbgFile,'')
    rf = TFile.Open(rfoutname, "READ")

    for i,skey in enumerate(sDict.keys()):

        if skey.count("Sel"): continue
        elif skey.count("Neg"): continue
        elif skey.count("Pos"): continue
        elif skey.count("Z"): continue
        #elif skey.count("Rad"): continue
        elif skey.count("Char"): continue
        elif skey.count("Plus") or skey.count("Minus"): continue
        elif skey.split(tag)[0].endswith("0") or skey.count("XY"): continue
        elif skey.count("Pio") or skey.count("Kao"): continue

        cv = TCanvas( 'cv', 'cv', 1400, 900)

        x1, y1, x2, y2 = 0.7, 0.75, 0.9, 0.88
        mlegend = TLegend( x1, y1, x2, y2)
        mlegend.SetFillColor(0)
        mlegend.SetFillStyle(0)
        mlegend.SetLineColor(0)
        mlegend.SetTextSize(0.035)
        mlegend.SetShadowColor(0)
        mlegend.SetBorderSize(0)

        twoDhname_flat = skey + '_flat'
        twoDhname_reweighted = skey + '_reweighted'
        twoDhist_flat = rf.Get(twoDhname_flat)
        twoDhist_reweighted = rf.Get(twoDhname_reweighted)

        hist_flat = twoDhist_flat.ProjectionX(skey + "makeit1d_flat")
        hist_reweighted = twoDhist_reweighted.ProjectionX(skey + "makeit1d_reweighted")
        nbins = hist_reweighted.GetNbinsX()

        doLogx, doLogy = 0, 0
        if skey.count("Ekin"):
            hist_flat = doEkin(hist_flat,nbins)
            hist_reweighted = doEkin(hist_reweighted,nbins)
            doLogx, doLogy = 1,1
        elif skey.count("Phi"):
            hist_flat = doPhi(hist_flat,nbins)
            hist_reweighted = doPhi(hist_reweighted,nbins)
            doLogx, doLogy = 0,1
            
        hname = skey
        xtitle = sDict[hname][9]
        ytitle = sDict[hname][10]

        hist_flat.Scale(1./hist_flat.Integral())
        hist_flat.GetXaxis().SetTitle(xtitle)
        hist_flat.GetYaxis().SetTitle(ytitle)
        hist_flat.Draw("h")
        lg, lm = "flat", 'l'
        mlegend.AddEntry(hist_flat, lg, lm)

        hist_reweighted.SetLineColor(kPink-3)
        hist_reweighted.Scale(1./hist_reweighted.Integral())
        hist_reweighted.GetYaxis().SetTitle(ytitle)
        hist_reweighted.Draw("hsame")
        lg, lm = "reweighted", 'l'
        mlegend.AddEntry(hist_reweighted, lg, lm)
        #twoDhist_reweighted.Draw("colz")
    #    hist_pint.Draw("hist")
        cv.SetLogx(doLogx)
        cv.SetLogy(doLogy)
        gPad.RedrawAxis()

    #     lab = mylabel(42)
    #     lab.DrawLatex(0.45, 0.9, '4 TeV beam-gas' )
    # #    lab.DrawLatex(0.7, 0.82, '#mu^{#pm}' )

        mlegend.Draw()

        pname = wwwpath + 'TCT/4TeV/beamgas/fluka/bs/reweighted/'+skey+'.pdf'
        print('Saving file as ' + pname ) 
        cv.Print(pname)

