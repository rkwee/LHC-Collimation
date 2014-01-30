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


    rfAfile = '/afs/cern.ch/work/r/rkwee/HL-LHC/runs/TCT/rotate/4TeV/B2/f15R1tEx.root'
    rfXfile = '/afs/cern.ch/work/r/rkwee/HL-LHC/runs/TCT/rotate/4TeV/B2/new05/oldFormat_final_hits_and_angles_new05.root'

    rfAfile = '/afs/cern.ch/work/r/rkwee/HL-LHC/runs/TCT/rotate/4TeV/B1/f15L1tEx.root'
    rfXfile = '/afs/cern.ch/work/r/rkwee/HL-LHC/runs/TCT/rotate/4TeV/B1/HALO_B1.root'

    rel = '_rb_v2'

    rfA = TFile.Open(rfAfile)
    rfX = TFile.Open(rfXfile)
    ntA = rfA.Get('particle')
    ntX = rfX.Get('particle')
    
    vars = ['yp','xp','x','y','z']

    for var in vars:
        
        hAname = 'hA'+var
        hXname = 'hX'+var

        # for yp
        if var.count('yp'): nbins, xmin, xmax = 100, -3e-4, 3e-4
        # for xp
        if var.count('xp'): nbins, xmin, xmax = 100, -2e-3, 2e-3
        # for y
        if var == 'y': nbins, xmin, xmax = 100, -2, 2
        # for x
        if var == 'x': nbins, xmin, xmax = 100, -13, 0
        # for z
        if var == 'z': nbins, xmin, xmax = 100, 14230,14950.

        histA = TH1F(hAname, hAname, nbins, xmin, xmax)
        histX = TH1F(hXname, hXname, nbins, xmin, xmax)

        ntA.Project(hAname, var)
        ntX.Project(hXname, var)
        cv = TCanvas( 'cv'+var, 'cv'+var, 10, 10, 800, 600 )
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

        pname = wwwpath + 'TCT/4TeV/debug/' + var + rel + '.png'
        cv.SaveAs(pname)
