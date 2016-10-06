#!/usr/bin/python
#
# reads histograms with reweights
# Oct 16
#
# R Kwee, 2016
# 
# ---------------------------------------------------------------------------------
import ROOT, sys, glob, os, math, helpers
from ROOT import *
from array import array
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
    xaxis = hist.GetXaxis()
    for i in range(1,nbins+1):
        binArea = math.pi * (xaxis.GetBinUpEdge(i)**2 - xaxis.GetBinUpEdge(i-1)**2)
        content = hist.GetBinContent(i)
        hist.SetBinContent(i,content/binArea)
        hist.SetBinError(i,hist.GetBinError(i)/binArea)
    return hist

# --------------------------------------------------------------------------------
def resultFileBG(k,rel):
    n = os.path.join(os.path.dirname(k),"results_pressure2015_"+rel+k.split('/')[-1])
    return  n
# --------------------------------------------------------------------------------
def cv81():

    energy = "4 TeV"
    datafile = '/afs/cern.ch/project/lhc_mib/valBG4TeV/ir1_BG_bs_4TeV_20MeV_b1_nprim5925000_67'
    datafile = '/Users/rkwee/Documents/RHUL/work/HL-LHC/runs/TCT/ir1_BG_bs_4TeV_20MeV_b1_nprim5925000_67'
    tag = '_BG_4TeV_20MeV_bs'
    beamintensity = 2e14
    bgcl = kAzure-3
    bgcl = kPink-3
    

    energy = "6.5 TeV"
    datafile = '/Users/rkwee/Documents/RHUL/work/HL-LHC/runs/TCT/ir1_BG_bs_6500GeV_b1_20MeV_nprim3198000_67'
    tag = '_BG_6500GeV_flat_20MeV_bs' #!! MMMeV NOT GeV
    bgcl = kYellow-2
    beamintensity = 2.29e14 ## https://acc-stats.web.cern.ch/acc-stats/#lhc/fill-details 4536, ring 1.
    
    bbgFile = datafile + ".root"
    print "Opening", bbgFile
    norm = float(bbgFile.split('nprim')[-1].split('_')[0])
    rfile = TFile.Open(bbgFile, "READ")
    tBBG = rfile.Get("particle")
    yrel = ''
    sDict = generate_sDict(tag, norm, tBBG, yrel)

    # -- small version of plotSpectra    
    Trev  = 2*math.pi/112450
    kT = 1.38e-23*300

    # rootfile with results
    rfoutname = resultFileBG(bbgFile,'')
    print "Opening", "."*30,bbgFile
    rf = TFile.Open(rfoutname, "READ")

    for i,skey in enumerate(sDict.keys()):

        if skey.count("Sel"): continue
        elif skey.count("Neg"): continue
        elif skey.count("Pos"): continue
        elif skey.count("Z"): continue
        elif skey.count("Neu_"): continue
        elif skey.count("Char"): continue
        elif skey.count("Plus") or skey.count("Minus"): continue
        elif skey.split(tag)[0].endswith("0") or skey.count("XY"): continue
        elif skey.count("Pio") or skey.count("Kao"): continue

        # # FOR DEBUGGING
        # elif not skey.count("EkinMu"): continue

        doLeft = 0
        if skey.count("Phi"): doLeft = 1
        cv = TCanvas(skey+ 'cv',skey+ 'cv', 1400, 900)
        # right corner
        x1, y1, x2, y2 = 0.7, 0.75, 0.9, 0.88
        if doLeft:
            x1, y1, x2, y2 = 0.2, 0.75, 0.5, 0.88
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

        print twoDhist_flat, skey
        hist_flat = twoDhist_flat.ProjectionX(skey + "makeit1d_flat")
        hist_reweighted = twoDhist_reweighted.ProjectionX(skey + "makeit1d_reweighted")
        nbins = hist_reweighted.GetNbinsX()

        XurMin,XurMax = -1,-1.
        YurMin,YurMax = -1,-1.
        doLogx, doLogy = 0, 0
        if skey.count("Ekin"):
            hist_flat = doEkin(hist_flat,nbins)
            hist_reweighted = doEkin(hist_reweighted,nbins)
            doLogx, doLogy = 1,1
            YurMin,YurMax = 1e-5,8e-1
        elif skey.count("Phi"):
            hist_flat = doPhi(hist_flat,nbins)
            hist_reweighted = doPhi(hist_reweighted,nbins)
            doLogx, doLogy = 0,1
            YurMin,YurMax = 1e-3,2e-1
        elif skey.count("Rad"):
            hist_flat = doRad(hist_flat,nbins)
            hist_reweighted = doRad(hist_reweighted,nbins)
            hist_flat = helpers.doRebin(hist_flat,3)
            hist_reweighted = helpers.doRebin(hist_reweighted,3)
            doLogx, doLogy = 0,1
            YurMin,YurMax = 1e-12,1.2
            #XurMin,XurMax = 0, 600.
            
        hname = skey
        xtitle = sDict[hname][9]
        ytitle = sDict[hname][10] + ' a.u.'

        hist_flat.Scale(1./hist_flat.Integral())
        hist_reweighted.Scale(1./hist_reweighted.Integral())
        
        hist_flat.GetXaxis().SetTitle(xtitle)
        hist_reweighted.GetXaxis().SetTitle(xtitle)

        hist_flat.GetYaxis().SetRangeUser(YurMin,YurMax)
        hist_reweighted.GetYaxis().SetRangeUser(YurMin,YurMax)

        if XurMin != -1:
            hist_flat.GetXaxis().SetRangeUser(XurMin, XurMax)

        lg, lm = "flat", 'l'
        mlegend.AddEntry(hist_flat, lg, lm)
        #        hist_flat.SetLineStyle(2)

        hist_reweighted.SetLineColor(bgcl)
        hist_reweighted.SetMarkerColor(bgcl)
        hist_reweighted.SetMarkerStyle(20)

        hist_reweighted.GetYaxis().SetTitle(ytitle)
        hist_reweighted.Draw("hp")
        hist_flat.Draw("histsame")
        lg, lm = "reweighted", 'lp'
        mlegend.AddEntry(hist_reweighted, lg, lm)

        cv.SetLogx(doLogx)
        cv.SetLogy(doLogy)
        gPad.RedrawAxis()

        lab = mylabel(42)
        lab.DrawLatex(0.41, 0.955, energy+' beam-gas' )
        lab.DrawLatex(0.5, 0.82, sDict[hname][6] )

        mlegend.Draw()

        pname = wwwpath + 'TCT/6.5TeV/beamgas/fluka/bs/reweighted/'+skey+'.pdf'
        pname = '/Users/rkwee/Documents/RHUL/work/HL-LHC/LHC-Collimation/Documentation/ATS/HLHaloBackgroundNote/figures/6500GeV/reweighted/cv81_' + skey + '.pdf'
        if energy.count("4 TeV"):
            pname = '/Users/rkwee/Documents/RHUL/work/HL-LHC/LHC-Collimation/Documentation/ATS/HLHaloBackgroundNote/figures/4TeV/reweighted/cv81_' + skey + '.pdf'
        print('Saving file as ' + pname) 
        cv.Print(pname)

