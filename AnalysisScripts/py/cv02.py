#!/usr/bin/python
#
# May 2013, rkwee
## -------------------------------------------------------------------------------
import ROOT, sys, glob, os
from ROOT import *
import helpers
from helpers import *
## -------------------------------------------------------------------------------
def cv02():
    print 'run cv02 : plotting betafunctions'

    debug = False

    path  = '/afs/cern.ch/work/r/rkwee/public/sixtrack_example/clean_input/'

    # 1=ielem 2=name 3=s 4=TBETAX 5=TBETAY
    f1    = path + 'betafunctions.dat'

    XurMin, XurMax = 9000., 19000.
    #XurMin, XurMax = -1, -1
    YurMin, YurMax = -1, -1

    rel = '_01'

    xarray, bxarray, byarray = [],[],[]

    with open(f1) as myfile:

        for line in myfile:

            line  = line.rstrip()
            if line.count("TBETAY"):
                continue

            if debug:
                print line

            scoor = float(line.split()[-3])
            betaX = float(line.split()[-2])
            betaY = float(line.split()[-1])

            xarray  += [scoor]
            bxarray += [betaX]
            byarray += [betaY]


    # plot
    cv = TCanvas( 'cv_ap', 'cv_ap', 2200, 600)
    cv.SetRightMargin(0.12)

    grx, gry = TGraph(), TGraph()
    grx.Set(len(xarray))
    gry.Set(len(xarray))

    xtitle = 's [m]'
    ytitle = "#beta-function [m]"
    
    grx.SetMarkerStyle(7)
    grx.SetLineWidth(1)
    grx.SetLineColor(kRed)
    grx.SetMarkerColor(kRed)

    gry.SetMarkerStyle(7)
    gry.SetLineWidth(1)
    gry.SetLineColor(kBlue)
    gry.SetMarkerColor(kBlue)

    for i in range(len(byarray)):
        grx.SetPoint(i+1, xarray[i], bxarray[i])
        gry.SetPoint(i+1, xarray[i], byarray[i])

    if XurMin is not -1:
        grx.GetXaxis().SetRangeUser(XurMin, XurMax)
        gry.GetXaxis().SetRangeUser(XurMin, XurMax)
    if YurMin is not -1:
        grx.GetYaxis().SetRangeUser(YurMin, YurMax) 
        gry.GetYaxis().SetRangeUser(YurMin, YurMax) 

    grx.GetXaxis().SetTitleOffset(.9)
    grx.GetYaxis().SetTitleOffset(1.6)
    grx.GetXaxis().SetTitle(xtitle)
    grx.GetYaxis().SetTitle(ytitle)
    grx.Draw('al')
    gry.Draw('lsame')

    # x1, y1, x2, y2
    thelegend = TLegend(0.7, 0.7, 0.8, 0.8) 
    thelegend.SetFillColor(0)
    thelegend.SetLineColor(0)
    thelegend.SetTextSize(0.035)
    thelegend.SetShadowColor(10)
    thelegend.AddEntry(grx,'#beta_{x}', "PL")
    thelegend.AddEntry(gry,'#beta_{y}', "PL")
    thelegend.Draw()

    pname  = wwwpath
    pname += 'betafunction'+rel+'.png'
    print("printing " + pname)
    cv.Print(pname)
