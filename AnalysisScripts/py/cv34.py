#!/usr/bin/python
#
# from cv23->31
# plot fluka input/sixtrack output distributions on 1 cv
# R Kwee-Hinzmann, Nov 2014
# ---------------------------------------------------------------------------------
import ROOT, sys, glob, os, math, helpers
from ROOT import *
from helpers import *
from array import array
# ---------------------------------------------------------------------------------
def cv34():

    showInfo = 1

    # histname+entrie
    #gStyle.SetOptStat(0111)
    # under and over flow
    gStyle.SetOptStat(111111)
    # name, entries
    # gStyle.SetOptStat(11)
    # only entries!
    # gStyle.SetOptStat(10)
    gStyle.SetPalette(1)
    gStyle.SetStatX(0.90)
    gStyle.SetStatY(0.95)
    gStyle.SetTitleX(0.1)
    gStyle.SetTitleY(.955)

    # OK for H5_HL_TCT5IN runs 
    icollsIR1 = [
       # ('54', 'TCTH.5L1.B1'),
       # ('55', 'TCTVA.5L1.B1'),
        # ('52', 'TCTH.4L1.B1'), 
       ('53', 'TCTVA.4L1.B1'),
        ]
    #0 var #1 xnbins #2 xmin #3 xmax #4 ynbins #5 ymin F #6 ymax F #7 xtitle F #8 ytitle F 
    #9 xnbins S #10 xminS #11 xmax S #12 ynbins #13 ymin #14 ymax #15 xtitle S #16 ytitle S #17 labelSize
    hDict_relaxed = {
        'xy': ['y:x', 100, -12., -2., 400, -4., 4., "x [cm]", "y [cm]", 100, -50., 50., 400, -40., 40., "x [mm]", "y [mm]", -1,],
        'xz': ['x:s', 100, 1.33093E+04 - 50., 1.33093E+04 + 50., 120, -11., -5., "z [cm]", "x [cm]", 100, 0., 1., 120, -25., 35.,"s [m]", "x [mm]", 0.03],
        'yz': ['y:s', 100, 1.33093E+04 - 50., 1.33093E+04 + 50., 120, -3., 3., "z [cm]", "y [cm]", 100, 0., 1., 120, -25., 35., "s [m]", "y [mm]", 0.03],
        'yp': ['yp',  100, -0.002, 0.002, -1, -1, -1,"yp (direction cosine)", "entries", 100, -2., 2., -1, -1, -1, "yp [mrad]", "entries", -1],
        'xp': ['xp',  100, 0.001, 0.002, -1, -1, -1, "xp (direction sine)", "entries",  100, -0.5, 0.5, -1, -1, -1, "xp [mrad]", "entries", 0.03],

        }
    # # ---------------------
    # TCTIMPAC
    hDict_nominal = {
        'xy': ['y:x', 100, -5., 5., 400, -4., 4., "x [cm]", "y [cm]", 100, -50., 50., 400, -40., 40., "x [mm]", "y [mm]", -1,],
        'xz': ['x:s', 100, - 50., 50., 120, -2.5, 3.5, "z [cm]", "x [cm]", 100, 0., 1., 120, -25., 35.,"s [m]", "x [mm]", 0.03],
        'yz': ['y:s', 100, -50., 50., 120, -3., 3., "z [cm]", "y [cm]", 100, 0., 1., 120, -25., 35., "s [m]", "y [mm]", 0.03],
        'yp': ['yp',  100, -0.002, 0.002, -1, -1, -1,"yp (direction cosine)", "entries", 100, -2., 2., -1, -1, -1, "yp [mrad]", "entries", 0.03],
        'xp': ['xp',  100, -0.0003, 0.0003, -1, -1, -1, "xp (direction sine)", "entries",  100, -0.23, 0.23, -1, -1, -1, "xp [mrad]", "entries", -1],
        # TCTH
        #'xp': ['xp',  100, -0.00023, 0.00023, -1, -1, -1, "xp (direction sine)", "entries",  100, -0.23, 0.23, -1, -1, -1, "xp [mrad]", "entries", -1],

        }

    # fluka, sixtrack files
    rfFname = "/afs/cern.ch/work/r/rkwee/HL-LHC/runs/sourcedirs/HL_TCT_7TeV/fluka/hybrid/anton.FL_TCT5IN_roundthin_anton.run_00000.dat.root"
    rfSname = "/afs/cern.ch/work/r/rkwee/HL-LHC/runs/sourcedirs/HL_TCT_7TeV/fluka/hybrid/tct5inrd.root"
    subfolder = 'relaxedColl/newScatt/fluka/geo/'
    hDict = hDict_relaxed

    # rfFname = "/afs/cern.ch/work/r/rkwee/HL-LHC/runs/sourcedirs/HL_TCT_7TeV/fluka/anton.FL_ats-HL_LHC_nominal.run_00000.hllhc_ir1_tightsett_b2001_fort.83.root"
    # rfSname = "/afs/cern.ch/work/r/rkwee/HL-LHC/runs/sourcedirs/HL_TCT_7TeV/fluka/TCTIMPAC.root"
    # subfolder = 'nominalColl/'
    # hDict = hDict_nominal

    rfF = TFile.Open(rfFname)
    rfS = TFile.Open(rfSname)
    
    mtF = rfF.Get('particle')
    mtS = rfS.Get('particle')

    cut = 'icoll == 53' 
    collName = "TCTV4"

    # # ---------------------

    for pV in hDict.keys():
        prettyVar = pV

        var = hDict[pV][0]

        if not var.count(':'):
            hnameF = prettyVar +  "_"+collName+"_fluka"
            xtitle, ytitle = hDict[pV][7], hDict[pV][8]
            xnbins, xmin, xmax = hDict[pV][1], hDict[pV][2], hDict[pV][3]

            histF = TH1F(hnameF, hnameF, xnbins, xmin, xmax)
            histF.SetMarkerStyle(6)
            if hDict[pV][17] > 0.0: histF.GetXaxis().SetLabelSize(0.03)
            histF.GetXaxis().SetTitle(xtitle)    
            histF.GetYaxis().SetTitle(ytitle)    
            histF.Sumw2()
            mtF.Project(hnameF, var, cut)
    
            hnameS = prettyVar + "_"+collName+"_sixtrack"
            xtitle, ytitle = hDict[pV][15], hDict[pV][16]
            xnbins, xmin, xmax = hDict[pV][9], hDict[pV][10], hDict[pV][11]
            histS = TH1F(hnameS, hnameS, xnbins, xmin, xmax)
            histS.SetMarkerStyle(6)
            histS.GetXaxis().SetTitle(xtitle)
            histS.GetYaxis().SetTitle(ytitle)    
            histS.Sumw2()
            mtS.Project(hnameS, var, cut)

            drawOpt = 'hist'
        else:

            hnameF = prettyVar +  "_"+collName+"_fluka"
            xtitle, ytitle = hDict[pV][7], hDict[pV][8]
            xnbins, xmin, xmax = hDict[pV][1], hDict[pV][2], hDict[pV][3]
            ynbins, ymin, ymax = hDict[pV][4], hDict[pV][5], hDict[pV][6]
            histF = TH2F(hnameF, hnameF, xnbins, xmin, xmax, ynbins, ymin, ymax)
            histF.SetMarkerStyle(6)
            if hDict[pV][17] > 0.0: histF.GetXaxis().SetLabelSize(0.03)
            histF.GetXaxis().SetTitle(xtitle)
            histF.GetYaxis().SetTitle(ytitle)    
            histF.Sumw2()
            mtF.Project(hnameF, var, cut)
    
            hnameS = prettyVar + "_"+collName+"_sixtrack"
            xtitle, ytitle = hDict[pV][15], hDict[pV][16]
            xnbins, xmin, xmax = hDict[pV][9], hDict[pV][10], hDict[pV][11]
            ynbins, ymin, ymax = hDict[pV][12], hDict[pV][13], hDict[pV][14]
            histS = TH2F(hnameS, hnameS, xnbins, xmin, xmax, ynbins, ymin, ymax)
            histS.SetMarkerStyle(6)
            histS.GetXaxis().SetTitle(xtitle)
            histS.GetYaxis().SetTitle(ytitle)    
            histS.Sumw2()
            mtS.Project(hnameS, var, cut)
            drawOpt = 'p'

        hname = hnameS.split('_s')[0]
        a,b = 1,2
        cv = TCanvas( 'cv'+hname, 'cv'+hname, 10, 10, a*900, b*600) 
        cv.Divide(a,b)
        cv.SetGridy(1)
        cv.cd(1)
        histF.Draw(drawOpt)
        x1, y1, x2, y2 = 0.2, 0.98, 0.84, 0.9
        lab = mylabel(60)
        lab.DrawLatex(x1, y1-0.15, hnameF.split('_')[-1])

        cv.cd(2)
        histS.Draw(drawOpt)
        lab = mylabel(60)
        lab.DrawLatex(x1, y1-0.15, hnameS.split('_')[-1])

        pname = wwwpath
        pname += 'TCT/HL/'+subfolder+'compFlukaSixTrack_' + hname + '.png'

        cv.SaveAs(pname)

