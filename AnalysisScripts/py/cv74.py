#!/usr/bin/python
#
# check beamsize along s from fluka file
# Sept 16
#
# R Kwee, 2016
# 
# ---------------------------------------------------------------------------------
import ROOT, sys, glob, os, math, helpers
from ROOT import *
from array import array
from helpers import *
import createTTree 
import os
# --------------------------------------------------------------------------------


def cv74():

    filename = projectpath + 'HaloRun2/valBG4TeV2/oneFileAllTraj.dat.89.root'
    filename = projectpath + 'HaloRun2/valBG4TeV2/traj_fort.89.10.root'

    print "Opening", filename
    rf = TFile.Open(filename)

    
    # make 1 bin 1cm
    xnbins, xmin, xmax = 54693,0.,54693.

    ynbins, ymin, ymax = 300, 0., 2.

    # G option for gaussian errors
    # -- getting the mean value
    # 1.
    hnameProf = 'YvSProf'
    YvSProf = TProfile(hnameProf, hnameProf, xnbins, xmin, xmax, ymin, ymax)
    YvSProfG = TProfile(hnameProf+'G', hnameProf+'G', xnbins, xmin, xmax, ymin, ymax, "G")
    YvSProfS = TProfile(hnameProf+'S', hnameProf+'S', xnbins, xmin, xmax, ymin, ymax, "S")
    # 2.
    hnameHist = "YvSHist"
    YvSHist = TH2F(hnameHist, hnameHist, xnbins, xmin, xmax, ynbins, ymin, ymax)

    mt = rf.Get("particle")

    var='YTRACK:ZTRACK'
    cuts = ''
    # mt.Project(hnameHist, var, cuts)
    # mt.Project(hnameProf, var, cuts)
    # mt.Project(hnameProf+'G', var, cuts)
    mt.Project(hnameProf+'S', var, cuts)

    # 3.
    hnameTraj = 'histTraj'
    histTraj = TH1F(hnameTraj, hnameTraj, xnbins, xmin, xmax)
    histTraj = YvSHist.ProjectionX()

    xtitle, ytitle = '#sigma_{y} [cm]', 'entries'

    # srange = [1.*s for s in range(xnbins+1)]
    # zpos = 5333.5
    # # zpos = 5.3335
    # # xnbins = 10

    # for i in range(xnbins):
    #     if zpos < srange[i+1] and zpos >= srange[i]:
    #         zbin = srange.index(i+1)
        
    # print "srange[zbin]", srange[zbin]
    # # 4. 
    # hnameYSlice = 'histYSlice'
    # histYSlice = TH1F(hnameYSlice, hnameYSlice, ynbins, ymin, ymax)
    # var = 'YTRACK'
    # cuts = "("+str( srange[zbin] )+' <= ZTRACK)&&(ZTRACK < '+str(srange[zbin+1])+")" 
    # print "Applying", cuts, "to", var, "in", hnameYSlice
    # mt.Project(hnameYSlice, var, cuts)
    # print "histYSlice.GetEntries()", histYSlice.GetEntries()

    # print zbin, "(YvSProf.GetBinEntries(zbin)", YvSProf.GetBinEntries(zbin)
    # print zbin, "(YvSProf.GetBinError(zbin)", YvSProf.GetBinError(zbin)
    # print zbin, "(YvSProfG.GetBinEntries(zbin)", YvSProfG.GetBinEntries(zbin)
    # print zbin, "(YvSProfG.GetBinError(zbin)", YvSProfG.GetBinError(zbin)
    print zbin, "(YvSProfS.GetBinError(zbin)", YvSProfS.GetBinError(zbin)
    
    # for i in range(1,int(xmax+1)):
    #     #NperBin = YversusS.GetBinEntries(i)
    #     spread  = YversusS.GetBinError(i)
    #     sigmayVSs.SetBinContent(i, spread)

#    sigmayVSs.GetXaxis().SetTitle(xtitle)
#    sigmayVSs.GetYaxis().SetTitle(ytitle)
    a,b = 2,2
    cv = TCanvas('cv', 'cv', a*2000, b*800)
    cv.Divide(a,b)

    x1, y1, x2, y2 = 0.7, 0.75, 0.9, 0.88
    mlegend = TLegend( x1, y1, x2, y2)
    mlegend.SetFillColor(0)
    mlegend.SetFillStyle(0)
    mlegend.SetLineColor(0)
    mlegend.SetTextSize(0.035)
    mlegend.SetShadowColor(0)
    mlegend.SetBorderSize(0)
    #ZurMin, ZurMax = 
    #twodhist.GetZaxis().SetRangeUser(ZurMin, ZurMax)
    cv.cd(1)
    YvSHist.Draw("colz")
    YvSProf.SetLineColor(kBlack)
    YvSProf.Draw("samele")
    YvSProfS.SetLineColor(kBlue)
    YvSProfS.Draw("samele")
    YvSProfG.SetLineColor(kRed)
    YvSProfG.Draw("samele")

    cv.cd(2)
    histYSlice.Draw()
    cv.cd(3)
    histTraj.Draw()
    cv.cd(4)
    YvSProf.Draw()

    pname = wwwpath + 'TCT/4TeV/beamgas/cv74_' + hnameTraj + '.png'
    cv.SaveAs(pname)

