#!/usr/bin/python
#
# June 2013, rkwee
## -------------------------------------------------------------------------------
import ROOT, sys, glob, os
from ROOT import *
import helpers
from helpers import *
## -------------------------------------------------------------------------------
def cv04():
    print 'run cv04 : dispersion function ?'

    debug  = False

    doB1   = 1
    doZoom = 0


    if doB1:    
        path = "/tmp/rkwee/7TeVPostLS1_nominal_b1/run_234/"
        text   = 'b1'
        x1, y1, x2, y2 = 0.75, 0.3, 0.84, 0.4
    else:
        path = "/tmp/rkwee/7TeVPostLS1_nominal_b2/run_234/"
        text   = 'b2'
        x1, y1, x2, y2 = 0.75, 0.8, 0.84, 0.9

    f1 = path + 'amplitude.dat'
 
    if doZoom:
        rel = '_02_' + text

        # around Q8
        XurMin, XurMax, YurMin, YurMax, = 19500., 20500., -3.4, 3.4
        XurMin, XurMax, YurMin, YurMax, = 12500., 14500., -3.4, 3.4
    else:
        rel = '_00_' + text
        # entire ring
        XurMin, XurMax,  YurMin, YurMax = 0., length_LHC, -3.4, 3.4

    cmd = "perl -pi -e 's/\\0/ /g' " + f1
    print cmd
    os.system(cmd)             

    pname  = wwwpath + 'scan/debugB2/'

    xarray, dxarray, dyarray = [],[],[]

    with open(f1) as myfile:
        for line in myfile:

            line  = line.rstrip()
            if line.count("orbity"):
                continue

            if debug:
                print line

            scoor = float(line.split()[2])
            dispX = float(line.split()[13])
            dispY = float(line.split()[14])

            if not dispY:
                continue
            
            if not dispX:
                continue

            xarray  += [scoor]
            dxarray += [dispX]
            dyarray += [dispY]
            
        # plot
        cv = TCanvas( 'cv_ap', 'cv_ap', 1000,600)
        cv.SetRightMargin(0.1)

        grX = TGraph()
        grX.Set(len(dxarray))

        grY = TGraph()
        grY.Set(len(dyarray))

        xtitle = 's [m]'
        ytitle = "dispersion function"

        grX.SetMarkerStyle(7)
        grY.SetMarkerStyle(7)
        grX.SetLineWidth(2)
        grY.SetLineWidth(2)
        grX.SetMarkerColor(kAzure+2)
        grY.SetMarkerColor(kAzure-6)
        grX.SetFillColor(kAzure+2)
        grY.SetFillColor(kAzure-6)
        grX.SetLineColor(kAzure+2)
        grY.SetLineColor(kAzure-6)
        grX.SetLineStyle(1)
        grY.SetLineStyle(1)

        for i in range(len(dxarray)):
            grX.SetPoint(i+1, xarray[i],dxarray[i])

        for i in range(len(dyarray)):
            grY.SetPoint(i+1, xarray[i],dyarray[i])

        grX.GetXaxis().SetTitleOffset(.9)
        grX.GetYaxis().SetTitleOffset(1.1)
        grX.GetXaxis().SetTitle(xtitle)
        grX.GetYaxis().SetTitle(ytitle)


        if XurMin is not -1:
            grX.GetXaxis().SetRangeUser(XurMin, XurMax)
        if YurMin is not -1:
            grX.GetYaxis().SetRangeUser(YurMin, YurMax) 


        grX.Draw('al')
        grY.Draw('samel')

        thelegend = TLegend(x1, y1, x2, y2)
        thelegend.SetFillColor(0)
        thelegend.SetLineColor(0)
        thelegend.SetTextSize(0.035)
        thelegend.SetShadowColor(10)
        thelegend.AddEntry(grX,"D_{x}'", "L")
        thelegend.AddEntry(grY,"D_{y}'", "L")
        thelegend.Draw()

        lab = mylabel(70)
        lab.DrawLatex(x1, y1-0.1, text)

        pname = wwwpath + 'scan/debugB2/disp'+rel+'.pdf'
        #v.Print(pname)

        pname = wwwpath + 'scan/debugB2/disp'+rel+'.png'
        cv.Print(pname)

