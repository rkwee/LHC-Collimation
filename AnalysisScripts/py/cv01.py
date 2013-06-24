
#!/usr/bin/python
#
# May 2013, rkwee
## -----------------------------------------------------------------------------------
print 'run cv01 : phase-space of input distribution'
## -----------------------------------------------------------------------------------
import ROOT, sys, glob, os
from ROOT import *
import helpers
from helpers import *
## -------------------------------------------------------------------------------
def cv01():

    debug = False

    path  = '/afs/cern.ch/work/r/rkwee/public/sixtrack_example/clean_input/'
    path = "/afs/cern.ch/work/r/rkwee/HL-LHC/SixTrack/SixTrack_4446_coll_gfortran_O4/run_d5/"
    genpath = "/afs/cern.ch/work/r/rkwee/HL-LHC/roderik/inputdistributions/"

    distTypes = ['d1', 'd2', 'd3', 'd5']

    for distType in distTypes:

        path = genpath + distType + '/'
        # has 6 colums: X[m]   Xp[rad]   Y [m]   Yp[rad]   s in bucket [m]  E[MeV]
        f1    = path + 'dist0.dat'


        xarrayX, yarrayX = [], []
        xarrayY, yarrayY = [], []
        sigma_x = 0.4716E-03
        sigma_y = 0.0755

        print("opening " + f1)

        with open(f1) as myfile:

            for line in myfile:

                line  = line.rstrip()

                xcoor  = float(line.split()[0])
                xpcoor = float(line.split()[1])
                ycoor  = float(line.split()[2])
                ypcoor = float(line.split()[3])

                xarrayX += [xcoor ]
                yarrayX += [xpcoor]
                xarrayY += [ycoor ]
                yarrayY += [ypcoor]

        # plot
        cv = TCanvas( 'cv_ap' + distType, 'cv_ap', 900, 900)
        cv.SetRightMargin(0.12)

        grX = TGraph()
        grX.Set(len(xarrayX))

        grY = TGraph()
        grY.Set(len(xarrayY))

        xtitle = 'x, y [m]'
        ytitle = "x', y' [rad]"

        grX.SetMarkerStyle(7)
        grY.SetMarkerStyle(7)
        grX.SetLineWidth(2)
        grY.SetLineWidth(2)
        grX.SetMarkerColor(kMagenta+2)
        grY.SetMarkerColor(kMagenta)
        grX.SetFillColor(kMagenta+2)
        grY.SetFillColor(kMagenta)
        grX.SetLineColor(kMagenta+2)
        grY.SetLineColor(kMagenta)

        for i in range(len(xarrayX)):
            grX.SetPoint(i+1, xarrayX[i], yarrayX[i])

        for i in range(len(xarrayY)):
            grY.SetPoint(i+1, xarrayY[i], yarrayY[i])

        grX.GetXaxis().SetTitleOffset(.9)
        grX.GetYaxis().SetTitleOffset(1.6)
        grX.GetXaxis().SetTitle(xtitle)
        grX.GetYaxis().SetTitle(ytitle)
        grX.Draw('ap')
        grY.Draw('samep')
        # x1, y1, x2, y2a
        thelegend = TLegend(0.75, 0.8, 0.84, 0.9) 
        thelegend.SetFillColor(0)
        thelegend.SetLineColor(0)
        thelegend.SetTextSize(0.035)
        thelegend.SetShadowColor(10)
        thelegend.AddEntry(grX,"x'", "PLEF")
        thelegend.AddEntry(grY,"y'", "PLEF")
        thelegend.Draw()

        clab = mylabel(60)
        clab.DrawLatex(0.2, 0.9, 'distribution type ' + distType.split("d")[-1])

        pname  = wwwpath
        pname += 'phasespace_'+distType+'.pdf'
        cv.Print(pname)

        pname  = wwwpath
        pname += 'phasespace_'+distType+'.png'
        cv.Print(pname)

