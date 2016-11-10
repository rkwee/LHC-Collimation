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

    # BG
    bbgFile = thispath + "results_ir1_BG_bs_6500GeV_b1_20MeV_nprim3198000_67.root"
    hname = "XYNMuons_BG_6500GeV_flat_20GeV_bs" # note the tag is GeV but it is MeV
    lText = '6.5 TeV BG with beamsize'
    lcase  = " #mu^{#pm}"# E_{kin} > 10 GeV"
    yrel = "/BG int."
    # BH b1 6.5 TeV

    if 1:
        bbgFile = thispath + "results_ir1_BH_6500GeV_b1_20MeV_nprim4752000_30.root"
        hname = "XYNMuons_BH_6500GeV_haloB1_20MeV"
        lText = '6.5 TeV Halo B1'
        lcase  = " #mu^{#pm}"# E_{kin} > 10 GeV"
        yrel = "/TCT hit"
    
    print "Opening", bbgFile
    nprim = float(bbgFile.split('nprim')[-1].split('_')[0])
    rf = TFile.Open(bbgFile, "READ")
    
    rbf = 5
    hist = rf.Get(hname)
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

            
    cv = TCanvas("cv", "cv", 1200, 900)
    gStyle.SetPalette(1)
    
    cv.SetRightMargin(0.2)
    cv.SetTopMargin(0.12)
    #cv.SetLeftMargin(-0.1)
    rebinnedXY.GetXaxis().SetTitle("x [cm]")
    rebinnedXY.GetYaxis().SetTitle("y [cm]")
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
