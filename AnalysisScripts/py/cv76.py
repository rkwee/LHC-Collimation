#!/usr/bin/python
#
# Mar 2015, rkwee
## -------------------------------------------------------------------------------
#
#
# check neutrons in RadN dist
# 
import pymadx
## -------------------------------------------------------------------------------
import ROOT, sys, os, time, math
from ROOT import *
from helpers import wwwpath, length_LHC, mylabel, gitpath, makeTGraph, projectpath
from array import array
# ----------------------------------------------------------------------------------
def cv76():
    fname = projectpath +  "bbgen/4TeV/beamgas/ir1_BG_bs_4TeV_settings_from_TWISS_20MeV_b1_nprim5925000_67.root"
    fname = projectpath +  "beamsize/4TeV_beamsize/runBG_UVcorr/ir1_BG_bs_4TeV_settings_from_TWISS_20MeV_b1_nprim5925000_67.root" #this is the old one
    fname = projectpath +  "HaloRun2/valBG4TeV2/ir1_BG_bs_4TeV_settings_from_TWISS_20MeV_b1_nprim5925000_67.root"
    rf = TFile.Open(fname)
    print rf
    nprim = float(fname.split("nprim")[-1].split("_")[0])
    tBBG = rf.Get("particle")
    print tBBG
    sDict = {
        'RadNNeutronsTEST':[ ['8'], 1., 1200, 0, 1200, tBBG, 'neutrons',kRed, '-9999','r [cm]', 'particles/cm^{2}', -9999, -9999, -9999, ],
        }

    for skey in sDict.keys():
        print skey
        particleTypes = sDict[skey][0]
        hname         = skey
        nbins         = sDict[skey][2]
        xmin          = sDict[skey][3]
        xmax          = sDict[skey][4]
        ynbins        = sDict[skey][11]
        ymin          = sDict[skey][12]
        ymax          = sDict[skey][13]

        binwidth = xmax/nbins
        xaxis = [i*binwidth for i in range(nbins+1)]
        nbins   = len(xaxis)-1
        hist    = TH1F(hname, hname, nbins, array('d', xaxis))

        hNeut = 'histoNeut'
        histNeut = hist.Clone(hNeut)

        hMuon = 'histoMuon'
        histMuon = hist.Clone(hMuon)

        var = 'TMath::Sqrt(x*x + y*y)'
        cut =  'energy_ke >= 0.02'
        cut = 'particle==8'
        print 'INFO: will apply a cut of ', cut, 'to', hname
        tBBG.Project(hname, var, cut)
        print 'INFO: Have ', hist.GetEntries(), ' entries in', hname

        var = 'TMath::Sqrt(x*x + y*y)'
        cut =  'energy_ke >= 0.02 && (particle==8)'
        print 'INFO: will apply a cut of ', cut, 'to', hNeut
        tBBG.Project(hNeut, var, cut)
        print 'INFO: Have ', histNeut.GetEntries(), ' entries in', hNeut

        var = 'TMath::Sqrt(x*x + y*y)'
        cut =  'energy_ke >= 0.02 && (particle==10 || particle==11)'
        print 'INFO: will apply a cut of ', cut, 'to', hMuon
        tBBG.Project(hMuon, var, cut)
        print 'INFO: Have ', histMuon.GetEntries(), ' entries in', hMuon

        testbin = hist.FindBin(300.)
        binarea = math.pi*(hist.GetBinLowEdge(testbin+1)**2 - hist.GetBinLowEdge(testbin)**2)
        lowedge = hist.GetBinLowEdge(testbin)
        highedge = hist.GetBinLowEdge(testbin+1)

        contNeut = hist.GetBinContent(testbin)

        print "contNeut", contNeut, "from ", lowedge, "to", highedge
        print "contNeut/nprim", contNeut/nprim
        print "contNeut/nprim/binarea ", contNeut/nprim/binarea
# ----------------------------------------------------------------------------





