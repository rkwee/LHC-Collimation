#!/usr/bin/python
#
#
# Nov  2013, rkwee
## -------------------------------------------------------------------------------
import ROOT, sys, glob, os
from ROOT import *
from helpers import wwwpath, mylabel
from array import array
## -------------------------------------------------------------------------------
def cv14():


#    rfA = TFile.Open('/afs/cern.ch/work/r/rkwee/HL-LHC/runs/sourcedirs/TCT_4TeV_60cm/fluka/HALO_new02.root')

    rfAfile = '/afs/cern.ch/work/r/rkwee/HL-LHC/runs/sourcedirs/TCT_4TeV_60cm/fluka/HALO_rb.root'
    rfXfile = '/afs/cern.ch/work/r/rkwee/HL-LHC/runs/TCT/rotate/4TeV/debug/noXangle/oldFormat_final_hits_and_angles_debug_noXangle.root'
    rfXfile = '/afs/cern.ch/work/r/rkwee/HL-LHC/runs/TCT/rotate/4TeV/debug/new04/oldFormat_final_hits_and_angles_new04.root'
    rfA = TFile.Open(rfAfile)
    rfX = TFile.Open(rfXfile)
    ntA = rfA.Get('particle')
    ntX = rfX.Get('particle')
    hAname = 'hA'
    hXname = 'hX'
    
    var = 'z'

    # for yp
    nbins, xmin, xmax = 100, -3e-4, 3e-4
    # for xp
    # nbins, xmin, xmax = 100, -2e-3, 2e-3
    # for y
    nbins, xmin, xmax = 100, -2, 2
    # for x
    nbins, xmin, xmax = 100, -13, 0
    # z
    nbins, xmin, xmax = 100, 14230,14950.

    histA = TH1F(hAname, hAname, nbins, xmin, xmax)
    histX = TH1F(hXname, hXname, nbins, xmin, xmax)
    
    ntA.Project(hAname, var)
    ntX.Project(hXname, var)
    cv = TCanvas( 'cv', 'cv', 10, 10, 800, 600 )
    gPad.SetLogy(1)

    histA.SetLineColor(kRed)
    histA.SetFillColor(kRed)
    histA.Draw('hist')
    histX.Draw('histsame')

    x1, y1, x2, y2 = 0.2,0.78,0.5,0.92
    mlegend = TLegend( x1, y1, x2, y2)
    mlegend.SetFillColor(0)
    mlegend.SetFillStyle(0)
    mlegend.SetLineColor(0)
    mlegend.SetTextSize(0.035)
    mlegend.SetShadowColor(0)
    mlegend.SetBorderSize(0)
    mlegend.AddEntry(histA, rfAfile.split('/')[-1].split('.root')[0], "l")
    mlegend.AddEntry(histX, rfXfile.split('/')[-1].split('.root')[0], "l")
    mlegend.Draw()

    pname = wwwpath + 'TCT/4TeV/debug/' + var + '.png'
    cv.SaveAs(pname)
