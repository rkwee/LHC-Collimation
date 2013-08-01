#!/usr/bin/python
#
# May 2013, rkwee
## -----------------------------------------------------------------------------------
import helpers
from helpers import *
## -----------------------------------------------------------------------------------
import ROOT, sys, glob, os
from ROOT import *
from array import array
## -------------------------------------------------------------------------------
def cv00():
    print 'run cv00 : aperture plots'
    debug = False

    path  = '/afs/cern.ch/work/r/rkwee/HL-LHC/runs/sourcedirs/NewColl7TeVB1/'
    f1    = path + 'allapert.b1'
    pname  = wwwpath + 'scan/debugB2/'

    text   = f1.split('.')[-1]
    # aper_1 = half width rectangle
    # aper_2 = half height rectangle
    # aper_3 = half horizontal axis ellipse (or radius if circle)
    # aper_4 = half vertical axis ellipse

    XurMin, XurMax = 13000., 13700.
    #    XurMin, XurMax = 0., length_LHC

    # around Q8
    XurMin, XurMax = 19500., 20500.
    cv_x, cv_y = 2000, 400 

    #XurMin, XurMax = -1, -1
    YurMin, YurMax = -1, -1
    rel = '_02_' + text


    xarrayH, xarrayV, yarrayH, yarrayV = [], [], [], []

    with open(f1) as myfile:

        for line in myfile:

            if line.startswith('@'):
                continue
            elif line.startswith('*') or line.startswith('$'):                
                continue

            line  = line.rstrip()

            scoor = float(line.split()[3])
            aper1 = float(line.split()[4])
            aper2 = float(line.split()[5])
            aper3 = float(line.split()[6])
            aper4 = float(line.split()[7])

            aper_v = min(aper2,aper4)
            aper_h = min(aper1,aper3)

            if aper_v:
                yarrayV += [aper_v]
                xarrayV += [scoor]

            if aper_h:
                yarrayH += [aper_h]
                xarrayH += [scoor]

    # plot
    cv = TCanvas( 'cv_ap', 'cv_ap',cv_x, cv_y)

    gr, grH = TGraph(),TGraph()
    gr.Set(len(xarrayV))
    grH.Set(len(xarrayH))

    xtitle = 's [m]'
    #ytitle = 'horizontal aperture '
    ytitle = 'aperture '
    gr.SetMarkerStyle(7)
    gr.SetLineWidth(1)
    gr.SetLineColor(kRed)
    gr.SetMarkerColor(kRed)


    grH.SetMarkerStyle(7)
    grH.SetLineWidth(1)
    grH.SetLineColor(kBlack)
    grH.SetMarkerColor(kBlack)

    for i in range(len(yarrayV)):
        gr.SetPoint(i+1, xarrayV[i], yarrayV[i])
    for i in range(len(yarrayH)):
        grH.SetPoint(i+1, xarrayH[i], yarrayH[i])
        
    gr.GetXaxis().SetTitleOffset(.9)
    gr.GetYaxis().SetTitleOffset(1.2)
    gr.GetXaxis().SetTitle(xtitle)
    gr.GetYaxis().SetTitle(ytitle)

    if XurMin is not -1:
        gr.GetXaxis().SetRangeUser(XurMin, XurMax)
    if YurMin is not -1:
        gr.GetYaxis().SetRangeUser(YurMin, YurMax) 

    gr.Draw('al')
    grH.Draw('lsame')

    x1, y1, x2, y2 = 0.7, 0.7, 0.8, 0.8
    thelegend = TLegend(x1, y1, x2, y2)
    thelegend.SetFillColor(0)
    thelegend.SetLineColor(0)
    thelegend.SetTextSize(0.035)
    thelegend.SetShadowColor(10)
    thelegend.AddEntry(gr,'vertical aperture', "PL")
    thelegend.AddEntry(grH,'horizontal aperture', "PL")
    thelegend.Draw()

    lab = mylabel(70)
    lab.DrawLatex(x1, y1-0.1, text)

    pname += 'aperture'+rel+'.png'
    print("printing " + pname)
    cv.Print(pname)
