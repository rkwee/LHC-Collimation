#!/usr/bin/python
#
# Mar 2016, rkwee
## -------------------------------------------------------------------------------
#  checking event numbers in 6.5 TeV file BH B2 file
## -------------------------------------------------------------------------------
import ROOT, sys, os, time, math
from ROOT import *
import helpers, array
from helpers import *
from array import array
# -----------------------------------------------------------------------------------
def cv63():
    
    # name, mean, rms, underflow, overflow                                                                                                                
    gStyle.SetOptStat(111111)

    fname = projectpath + 'bbgen/6.5TeV/ir1_BH_6500GeV_b2_20MeV_nprim3646000_30.root'
    rf = TFile.Open(fname)

    hname, xbin, xmin, xmax = 'particleID', 50, -0.5, 49.5
    hist = TH1F(hname, hname, xbin, xmin, xmax)

    # tree name
    mt = rf.Get('particle')

    # variable name
    var = 'particle'

    cut = 'event >9 && event <21'
    mt.Project(hname, var, cut)

    a,b =1,1
    cv = TCanvas( 'cv', 'cv', a*1500, b*900)
    cv.Divide(a,b)
    cv.SetRightMargin(0.3)
    cv.SetLeftMargin(0.2)
    cv.SetTopMargin(0.15)
    x1, y1, x2, y2 = 0.8, 0.65, 0.9, 0.9
    mlegend = TLegend( x1, y1, x2, y2)
    mlegend.SetFillColor(0)
    mlegend.SetFillStyle(0)
    mlegend.SetLineColor(0)
    mlegend.SetShadowColor(0)
    mlegend.SetBorderSize(0)


    hist.Draw('hist')


    pname = wwwpath + 'TCT/debug/eventnumbers/particles_with_event10and20.png'
    print 'saving ', pname
    cv.SaveAs(pname)
