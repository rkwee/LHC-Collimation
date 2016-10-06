#!/usr/bin/python
#
# plot flat and reweighted 2d histo
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
def cv84():

    datafile = '/afs/cern.ch/project/lhc_mib/valBG4TeV/ir1_BG_bs_4TeV_20MeV_b1_nprim5925000_67'
    tag = '_BG_4TeV_20MeV_bs'
    beamintensity = 2e14

    energy = "6.5 TeV"
    datafile = '/Users/rkwee/Documents/RHUL/work/HL-LHC/runs/TCT/ir1_BG_bs_6500GeV_b1_20MeV_nprim3198000_67'
    tag = '_BG_6500GeV_flat_20MeV_bs' #!! MMMeV NOT GeV
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

        # FOR TESTING
        elif not skey.count("Ekin"): continue
        a,b = 1,2
        cv = TCanvas(skey+ 'cv',skey+ 'cv', a*1400, b*900)
        cv.Divide(a,b)
        
        x1, y1, x2, y2 = 0.7, 0.75, 0.9, 0.88
        mlegend = TLegend( x1, y1, x2, y2)
        mlegend.SetFillColor(0)
        mlegend.SetFillStyle(0)
        mlegend.SetLineColor(0)
        mlegend.SetTextSize(0.035)
        mlegend.SetShadowColor(0)
        mlegend.SetBorderSize(0)
        xtitle = sDict[skey][9]



        twoDhname_flat = skey + '_flat'
        twoDhname_reweighted = skey + '_reweighted'
        twoDhist_flat = rf.Get(twoDhname_flat)
        twoDhist_reweighted = rf.Get(twoDhname_reweighted)
        twoDhist_reweighted.GetXaxis().SetTitle(xtitle)
        lg, lm = "reweighted", 'l'
#        mlegend.AddEntry(hist_reweighted, lg, lm)

        doLogx, doLogy = 0, 0
        if skey.count("Ekin"):
             doLogx, doLogy = 1,1
        elif skey.count("Phi"):
             doLogx, doLogy = 0,1
        elif skey.count("Rad"):
             doLogx, doLogy = 0,1

        cv.cd(2)
        twoDhist_reweighted.Draw("colz")
        cv.SetLogx(doLogx)
        cv.SetLogy(doLogy)
        gPad.RedrawAxis()
        cv.cd(1)
        twoDhist_flat.Draw("colz")

        cv.SetLogx(doLogx)
        cv.SetLogy(doLogy)
        gPad.RedrawAxis()

        lab = mylabel(42)
        lab.DrawLatex(0.2, 0.9, 'flat (1)' )
        lab.DrawLatex(0.5, 0.82, 'reweighted (2)' )

        #   mlegend.Draw()

        pname = wwwpath + 'TCT/6.5TeV/beamgas/fluka/bs/reweighted/'+skey+'.pdf'
        pname = '/Users/rkwee/Documents/RHUL/work/HL-LHC/LHC-Collimation/Documentation/ATS/HLHaloBackgroundNote/figures/6500GeV/reweighted/2d_' + skey + '.pdf'
        print('Saving file as ' + pname) 
        cv.Print(pname)

