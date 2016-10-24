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
from helpers import makeTGraph, mylabel, wwwpath, thispath
from fillTTree_dict import generate_sDict
import cv70
# --------------------------------------------------------------------------------
def doEkin(hist,nbins):
    for bin in range(1,nbins+1):
        content = hist.GetBinContent(bin)
        width   = hist.GetBinWidth(bin)
        bcenter = hist.GetXaxis().GetBinCenterLog(bin)
        hist.SetBinContent(bin,bcenter*content/width)
    return hist

def doNormalBinw(hist,nbins):
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
def cv81():

    do4TeV = 1 # 
    do6p5  = 0 #
    
    if do4TeV:
        year = "2012"
        energy = "4 TeV"
        pressFile = '/afs/cern.ch/work/r/rkwee/HL-LHC/beam-gas-sixtrack/pressure_profiles_2012/LSS1_B1_Fill2736_Final.csv'
        pressFile = '/Users/rkwee/Documents/RHUL/work/data/4TeV/LSS1_B1_Fill2736_Final.csv'

        bbgFile = '/afs/cern.ch/project/lhc_mib/valBG4TeV/ir1_BG_bs_4TeV_20MeV_b1_nprim5925000_67.root'
        bbgFile = thispath + 'ir1_BG_bs_4TeV_20MeV_b1_nprim5925000_67.root'
        beamintensity = 2e14    
        tag = '_BG_4TeV_20MeV_bs'
        bgcl = kPink-3
    elif do6p5:
        year = "2015"
        energy = "6.5 TeV"
        bbgFile = '/Users/rkwee/Documents/RHUL/work/HL-LHC/runs/TCT/ir1_BG_bs_6500GeV_b1_20MeV_nprim3198000_67.root'
        pressFile = "/Users/rkwee/Downloads/Density_Fill4536_2041b_26158.8832-500_B1_withECLOUD.txt"
        beamintensity = 2.29e14 ## https://acc-stats.web.cern.ch/acc-stats/#lhc/fill-details 4536, ring 1.
        tag = '_BG_6500GeV_flat_20MeV_bs' #!! MMMeV
        bgcl = kYellow+2
    else:
        year = "2011"
        energy = " 3.5 TeV "
        pressFile = "/Users/rkwee/Documents/RHUL/work/HL-LHC/runs/TCT/LSS1_B1_fill_2028-sync_rad_and_ecloud.csv"
        bbgFile = "/Users/rkwee/Documents/RHUL/work/HL-LHC/runs/TCT/beam_gas_3.5TeV_IR1_to_arc_20MeV_100M_nprim7660649_66.root"
        beamintensity = 1.66e14    
        tag = "_BG_3p5TeV_20MeV"
        bgcl = kTeal

    
    print "Opening", bbgFile
    nprim = float(bbgFile.split('nprim')[-1].split('_')[0])
    rfile = TFile.Open(bbgFile, "READ")
    tBBG = rfile.Get("particle")
    yrel = ''
    sDict = generate_sDict(tag, nprim, tBBG, yrel)

    # -- small version of plotSpectra    
    Trev  = 1./11245
    kT = 1.38e-23*300

    # rootfile with results
    rfoutname = cv70.resultFileBG(bbgFile,year)
    print "Opening", "."*30,rfoutname
    rf = TFile.Open(rfoutname, "READ")

    for i,skey in enumerate(sDict.keys()):

        if skey.count("Sel"): continue
        elif skey.count("Neg"): continue
        elif skey.count("Pos"): continue
        elif skey.count("Z") and not skey.startswith("OrigZ"): continue
        elif skey.count("Neu_"): continue
        elif skey.count("Char"): continue
        elif skey.count("Plus") or skey.count("Minus"): continue
        elif skey.split(tag)[0].endswith("0") or skey.count("XY"): continue
        elif skey.count("Pio") or skey.count("Kao"): continue

        # # FOR DEBUGGING
        #        elif not skey.count("OrigZAl"): continue

        doLeft = 0
        if skey.count("Phi"): doLeft = 1
        cv = TCanvas(skey+ 'cv',skey+ 'cv', 1400, 900)
        # right corner
        x1, y1, x2, y2 = 0.5, 0.75, 0.9, 0.88
        xpos = 0.3
        if doLeft:
            x1, y1, x2, y2 = 0.2, 0.75, 0.5, 0.88
            xpos = 0.59
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
        print hist_flat.GetEntries()

        hname = skey
        xtitle = sDict[hname][9]
        ytitle = sDict[hname][10] 
        ytitle = ytitle.split("/")[0]+ '/a.u.'
        
        XurMin,XurMax = -1,-1.
        YurMin,YurMax = -1,-1.
        doLogx, doLogy = 0, 0

        # devide by binwidth
        if skey.count("Ekin"):
            hist_flat = doEkin(hist_flat,nbins)
            hist_reweighted = doEkin(hist_reweighted,nbins)
            doLogx, doLogy = 1,1
            YurMin,YurMax = 5e2,8e8
        elif skey.count("Phi"):
            hist_flat = doNormalBinw(hist_flat,nbins)
            hist_reweighted = doNormalBinw(hist_reweighted,nbins)
            doLogx, doLogy = 0,1
            legendunit = sDict[hname][10]
            if skey.count("En") and not skey.count("Mu"):YurMin,YurMax = 3e7,8e9
            elif skey.count("Mu") and not skey.count("En"):YurMin,YurMax = 3e4,5e5
            else: YurMin,YurMax = 1e5,6e8
        elif skey.count("Rad"):
            hist_flat = doRad(hist_flat,nbins)
            hist_reweighted = doRad(hist_reweighted,nbins)
            hist_flat = helpers.doRebin(hist_flat,3)
            hist_reweighted = helpers.doRebin(hist_reweighted,3)
            doLogx, doLogy = 0,1
            legendunit = sDict[hname][10]
            #XurMin,XurMax = 0, 600.
        elif skey.count("OrigZ"):
            rbf = 4
            hist_flat = doNormalBinw(hist_flat,nbins)
            hist_reweighted = doNormalBinw(hist_reweighted,nbins)
            hist_flat.Rebin(rbf)
            hist_flat.Scale(1./rbf)
            hist_reweighted.Rebin(rbf)
            hist_reweighted.Scale(1./rbf)
            YurMin,YurMax = 1e-1,6e7
            legendunit = "/m"
            doLogx, doLogy = 0,1
            xtitle = "s [m]"
            
        hist_flat.Scale(1e7/nprim)
        hist_flat.GetXaxis().SetTitle(xtitle)
        hist_reweighted.GetXaxis().SetTitle(xtitle)

        if XurMin != -1:
            hist_flat.GetXaxis().SetRangeUser(XurMin, XurMax)
            hist_reweighted.GetXaxis().SetRangeUser(XurMin, XurMax)

        if YurMin != -1:
            hist_flat.GetYaxis().SetRangeUser(YurMin, YurMax)
            hist_reweighted.GetYaxis().SetRangeUser(YurMin,YurMax)
            
        lg, lm = "flat [10^{7}"+legendunit+"/BG int.]", 'l'
        mlegend.AddEntry(hist_flat, lg, lm)
        #        hist_flat.SetLineStyle(2)

        hist_reweighted.SetLineColor(bgcl)
        hist_reweighted.SetMarkerColor(bgcl)
        hist_reweighted.SetMarkerSize(0.2)
        hist_reweighted.SetMarkerStyle(20)

        hist_reweighted.GetYaxis().SetTitle(ytitle)
        hist_reweighted.Draw("hp")
        hist_flat.Draw("histsame")
        lg, lm = "reweighted ["+legendunit+"/s]", 'lp'
        mlegend.AddEntry(hist_reweighted, lg, lm)

        cv.SetLogx(doLogx)
        cv.SetLogy(doLogy)
        gPad.RedrawAxis()

        lab = mylabel(42)
        lab.DrawLatex(0.41, 0.955, energy+' beam-gas' )
        lab.DrawLatex(xpos, 0.82, sDict[hname][6] )

        mlegend.Draw()

        pname = wwwpath + 'TCT/6.5TeV/beamgas/fluka/bs/reweighted/'+skey+'.pdf'
        pname = '/Users/rkwee/Documents/RHUL/work/HL-LHC/LHC-Collimation/Documentation/ATS/HLHaloBackgroundNote/figures/6500GeV/reweighted/cv81_' + skey + '.pdf'
        if energy.count("4 TeV"):
            pname = '/Users/rkwee/Documents/RHUL/work/HL-LHC/LHC-Collimation/Documentation/ATS/HLHaloBackgroundNote/figures/4TeV/reweighted/cv81_' + skey + '.pdf'
        elif energy.count("3.5 TeV"):
            pname = '/Users/rkwee/Documents/RHUL/work/HL-LHC/LHC-Collimation/Documentation/ATS/HLHaloBackgroundNote/figures/4TeV/reweighted/xcheck2011/cv81_' + skey + '.pdf'
        print('Saving file as ' + pname) 
        cv.Print(pname)

