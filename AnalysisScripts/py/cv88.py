#!/usr/bin/python
#
# 
# rebin XYN plots

# Oct 16
#
# R Kwee, 2016
# 
# ---------------------------------------------------------------------------------
import ROOT, sys, glob, os, math, helpers
from ROOT import *
from array import array
#from fillTTree import *
#from fillTTree_dict import generate_sDict
from helpers import makeTGraph, mylabel, wwwpath, thispath
# --------------------------------------------------------------------------------
def cv88():


    # BH b2 4 TeV
    bbgFile = thispath + "results_ir1_BH_4TeV_settings_from_TWISS_20MeV_b2_nprim6914000_30.root"
    hname = "XYNMuons_BH_4TeV_B2_20MeV"
    lText = '4 TeV Halo B2'
    lcase  = " #mu^{#pm}"# E_{kin} > 10 GeV"
    yrel = "/TCT hit"

    # HL B1 TeV original binning is bad
    bbgFile = thispath + "results_hilumi_ir1_hybrid_b1_exp_20MeV_nprim5319000_30.root" # TCT5s in, retracted, use old file as new one doesnt have this kind of info anymore    
    hname = "OrigXZMuon_BH_HL_tct5inrdB1_20MeV"
    lText = 'HL TCT5s in, rd B1, 2#sigma-retract.'
    lcase  = " #mu^{#pm} E_{kin} > 100 GeV"
    yrel = "/TCT int."

    # BH b1 4 TeV
    bbgFile = thispath + "results_ir1_BH_4TeV_settings_from_TWISS_20MeV_b1_nprim6904000_30.root"
    hname = "XYNMuons_BH_4TeV_B1_20MeV"
    lText = '4 TeV Halo B1'
    lcase  = " #mu^{#pm}"# E_{kin} > 10 GeV"
    yrel = "/TCT hit"

    # BG 4 TeV
    bbgFile = thispath + "results_ir1_BG_bs_4TeV_20MeV_b1_nprim5925000_67.root"
    hname = "XYNMuons_BG_4TeV_20MeV_bs" # note the tag is GeV but it is MeV
    lText = '4 TeV BG with beamsize'
    lcase  = " #mu^{#pm}"# E_{kin} > 10 GeV"
    yrel = "/BG int."

    # BH b1 6.5 TeV
    bbgFile = thispath + "results_ir1_BH_6500GeV_b1_20MeV_nprim4752000_30.root"
    hname = "XYNMuons_BH_6500GeV_haloB1_20MeV"
    lText = '6.5 TeV Halo B1'
    lcase  = " #mu^{#pm}"# E_{kin} > 10 GeV"
    yrel = "/TCT hit"

    # BG 6.5 TeV
    bbgFile = thispath + "results_ir1_BG_bs_6500GeV_b1_20MeV_nprim3198000_67.root"
    hname = "XYNMuons_BG_6500GeV_flat_20GeV_bs" # note the tag is GeV but it is MeV
    lText = '6.5 TeV BG with beamsize'
    lcase  = " #mu^{#pm}"# E_{kin} > 10 GeV"
    yrel = "/BG int."

    # HL
    bbgFile = thispath + "results_hilumi_ir1_hybrid_b2_exp_20MeV_nprim5924500_30.root"
    hname = "XYNMuons_BH_HL_tct5inrdB2_20MeV"
    lText = "HL TCT5s in, retract. sett., B2"
    lcase =  " #mu^{#pm}"# E_{kin} > 100 GeV"
    yrel = "/TCT int."
    
    bbgFile = thispath + "results_hilumi_ir1_hybrid_b2_exp_20MeV_nprim5001000_30.root"
    hname = "XYNMuons_BH_HL_tct5otrdB2_20MeV"
    lText = "HL TCT4s only, retract. sett., B2"

    bbgFile = thispath + "results_hilumi_ir1_hybrid_b1_exp_20MeV_nprim5550000_30.root"
    hname = "XYNMuons_BH_HL_tct5inrdB1_20MeV"
    lText = "HL TCT5s in, retract. sett., B1"
    lcase =  " #mu^{#pm}"# E_{kin} > 100 GeV"
    yrel = "/TCT int."

    
    xtitle ="x [cm]"
    ytitle ="y [cm]"

#    xtitle ="s [cm]"
#    ytitle ="x [cm]"


    print "Opening", bbgFile
    nprim = float(bbgFile.split('nprim')[-1].split('_')[0])
    rf = TFile.Open(bbgFile, "READ")
    
    rbf = 5
    hist = rf.Get(hname)
    print hist
    nbinsX =    hist.GetXaxis().GetNbins()
    nbinsY =    hist.GetYaxis().GetNbins()

    print("nbinsX=", nbinsX)
    print("nbinsY=", nbinsY)
    print("rebinning histogram in X and Y by factor", rbf)
    rebinnedX = hist.RebinX(rbf)
    rebinnedXY = rebinnedX.RebinY(rbf)

    nbinsX = rebinnedX.GetNbinsX()
    nbinsY = rebinnedXY.GetNbinsY()

    for xbin in range(1,nbinsX+1):
        xwidth = rebinnedXY.GetXaxis().GetBinWidth(xbin)
        for ybin in range(1,nbinsY+1):
            content = rebinnedXY.GetBinContent(xbin, ybin)
            ywidth = rebinnedXY.GetYaxis().GetBinWidth(ybin)
            rebinnedXY.SetBinContent(xbin,ybin,content/xwidth/ywidth)

            
    cv = TCanvas("cv", "cv", 1100, 1000)
    gStyle.SetPalette(1)
    
    cv.SetRightMargin(0.2)
    cv.SetTopMargin(0.12)
    #cv.SetLeftMargin(-0.1)
    rebinnedXY.GetXaxis().SetTitle(xtitle)
    rebinnedXY.GetYaxis().SetTitle(ytitle)
    rebinnedXY.GetZaxis().SetTitleOffset(1.4)
    rebinnedXY.GetZaxis().SetTitle( "particles/cm^{2}" + yrel) 
                 
    XurMin, XurMax = -1, -1
    YurMin, YurMax = -1, -1

    #XurMin, XurMax = -15, 15
    #YurMin, YurMax = -15, 15
    rebinnedXY.Draw("COLZ")

    if XurMin != -1:
        pass
    rebinnedXY.GetXaxis().SetRangeUser(XurMin,XurMax)

    if YurMin != -1:
        pass
    rebinnedXY.GetYaxis().SetRangeUser(YurMin,YurMax)

    gPad.SetLogz(1)
    gPad.RedrawAxis()
    cv.RedrawAxis()

    lx, ly = 0.5,0.8
    lab = mylabel(62)
    lab.DrawLatex(lx,ly,lcase)

    lx, ly = 0.18,0.9
    lab.DrawLatex(lx,ly,lText)
    pname = "/Users/rkwee/Documents/RHUL/work/HL-LHC/LHC-Collimation/Documentation/ATS/HLHaloBackgroundNote/figures/" + hname + ".pdf"
    cv.SaveAs(pname)
