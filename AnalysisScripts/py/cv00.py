#!/usr/bin/python
#
# May 2013, rkwee
## -----------------------------------------------------------------------------------
import helpers
from helpers import *
## -----------------------------------------------------------------------------------
import ROOT, sys, glob, os
from ROOT import *
## -------------------------------------------------------------------------------
def cv00():
    #print 'run cv00 : horizontal aperture'
    print 'run cv00 : vertical aperture'
    debug = False

    path  = '/afs/cern.ch/work/r/rkwee/public/sixtrack_example/clean_input/'
    f1    = path + 'allapert.b1'

    # aper_1 = half width rectangle
    # aper_2 = half height rectangle
    # aper_3 = half horizontal axis ellipse (or radius if circle)
    # aper_4 = half vertical axis ellipse


    xarray, yarray = [], []

    with open(f1) as myfile:

        for line in myfile:

            if line.startswith('@'):

                continue

            elif line.startswith('*') or line.startswith('$'):
                print line

                continue

            line  = line.rstrip()

            scoor = float(line.split()[3])
            aper1 = float(line.split()[4])
            aper2 = float(line.split()[5])
            aper3 = float(line.split()[6])
            aper4 = float(line.split()[7])

            xarray += [scoor]

            # aperture
            yarray += [min(aper2,aper4)]


    # plot
    cv = TCanvas( 'cv_ap', 'cv_ap', 1200, 600 )    

    gr = TGraph()
    gr.Set(len(xarray))

    xtitle = 's [m]'
    #ytitle = 'horizontal aperture '
    ytitle = 'vertical aperture '
    gr.SetMarkerStyle(7)
    gr.SetLineWidth(2)
    gr.SetMarkerColor(kRed)

    for i in range(len(yarray)):
        gr.SetPoint(i+1, xarray[i], yarray[i])

    gr.GetXaxis().SetTitleOffset(.9)
    gr.GetYaxis().SetTitleOffset(1.2)
    gr.GetXaxis().SetTitle(xtitle)
    gr.GetYaxis().SetTitle(ytitle)
    gr.Draw('ap')
    pname  = wwwpath
    pname += 'verticalApert.png'
    cv.Print(pname)
