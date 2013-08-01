
#!/usr/bin/python
#
# June 2013, rkwee
## -----------------------------------------------------------------------------------
print 'run cv05 : phase-space of input distribution'
## -----------------------------------------------------------------------------------
import ROOT, sys, glob, os
from ROOT import *
import helpers
from helpers import *
## -------------------------------------------------------------------------------
def cv05():

    debug = False

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
                yarrayY += [ypcoor]

        # plot
        cv = TCanvas( 'cv_ap' + distType, 'cv_ap', 900, 900)
        cv.SetRightMargin(0.12)

        grX = TGraph()
        grX.Set(len(xarrayX))

        xtitle = 'x [m]'
        ytitle = "y [m]"

        grX.SetMarkerStyle(7)
        grX.SetLineWidth(2)
        grX.SetMarkerColor(kCyan+2)
        grX.SetFillColor(kCyan+2)
        grX.SetLineColor(kCyan+2)


        for i in range(len(xarrayX)):
            grX.SetPoint(i+1, xarrayX[i], yarrayY[i])

        grX.GetXaxis().SetTitleOffset(.9)
        grX.GetYaxis().SetTitleOffset(1.6)
        grX.GetXaxis().SetTitle(xtitle)
        grX.GetYaxis().SetTitle(ytitle)
        grX.Draw('ap')

        clab = mylabel(60)
        clab.DrawLatex(0.45, 0.88, 'distribution type ' + distType.split("d")[-1])

        pname  = wwwpath
        pname += 'realspace_'+distType+'.pdf'
        cv.Print(pname)

        pname  = wwwpath
        pname += 'realspace_'+distType+'.png'
        cv.Print(pname)

