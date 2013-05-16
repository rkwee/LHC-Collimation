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
    print 'run cv02 : losses on collmator'

    debug = False

    path  = '/afs/cern.ch/work/r/rkwee/public/sixtrack_example/clean_input/'

    # #1=x 2=y 3=xp 4=yp 5=E 6=s 7=t 8=xn 9=yn 10=xpn 11=ypn
    f1    = path + ''

    xarray, yarray = [], []

    with open(f1) as myfile:

        for line in myfile:

            line  = line.rstrip()

            xcoor  = float(line.split()[0])
            xpcoor = float(line.split()[1])
            ycoor  = float(line.split()[2])
            ypcoor = float(line.split()[3])

            xarray += [xcoor ]
            yarray += [xpcoor]


    # plot
    cv = TCanvas( 'cv_ap', 'cv_ap', 900, 900)
    cv.SetRightMargin(0.12)

    gr = TGraph()
    gr.Set(len(xarray))

    xtitle = 'x [m]'
    ytitle = "x' [rad]"
    #xtitle = 'y [m]'
    #ytitle = "y' [rad]"

    gr.SetMarkerStyle(7)
    gr.SetLineWidth(2)
    gr.SetMarkerColor(kRed)

    for i in range(len(yarray)):
        gr.SetPoint(i+1, xarray[i], yarray[i])

    gr.GetXaxis().SetTitleOffset(.9)
    gr.GetYaxis().SetTitleOffset(1.6)
    gr.GetXaxis().SetTitle(xtitle)
    gr.GetYaxis().SetTitle(ytitle)
    gr.Draw('ap')
    pname  = wwwpath
    pname += 'phasespace_x.png'
    cv.Print(pname)
