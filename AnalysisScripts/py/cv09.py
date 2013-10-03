#!/usr/bin/python
#
# September 2013, rkwee
## -------------------------------------------------------------------------------
import ROOT, sys, glob, os
from ROOT import *
import helpers, gzip
from helpers import wwwpath, workpath, mylabel
## -------------------------------------------------------------------------------
def cv09():

    print 'run cv09 raw hits plot '


    tDict = {
         # 0=subdir  # 1=xnbins # 2=xmin  # 3=xmax  # 4=ynbins  # 5=ymin # 6=ymax # 7=xtitle # 8=ytitle # 9=xInd # 10=yInd 
        'xy_52_TCTH.4L1.B1':    ['TCTH/',   100, -4., 3.,  100, -3., 5., 'x [cm]', 'y [cm]', 0, 1],
        'yz_52_TCTH.4L1.B1':    ['TCTH/',   100, 0., 100., 100, -3., 5., 'z [cm]', 'y [cm]', 2, 1],
        'xy_53_TCTVA.4L1.B1':   ['TCTV/',   100, -4., 3.,  100, -3., 5., 'x [cm]', 'y [cm]', 0, 1],
        'yz_53_TCTVA.4L1.B1':   ['TCTV/',   100, 0., 100., 100, -3., 5., 'z [cm]', 'y [cm]', 2, 1],
        'xy_19_TCTH.4L5.B1':    ['TCTH/',   100, -4., 3.,  100, -3., 5., 'x [cm]', 'y [cm]', 0, 1],
        'yz_19_TCTH.4L5.B1':    ['TCTH/',   100, 0., 100., 100, -3., 5., 'z [cm]', 'y [cm]', 2, 1],
        'xy_20_TCTVA.4L5.B1':   ['TCTV/',   100, -4., 3.,  100, -3., 5., 'x [cm]', 'y [cm]', 0, 1],
        'yz_20_TCTVA.4L5.B1':   ['TCTV/',   100, 0., 100., 100, -3., 5., 'z [cm]', 'y [cm]', 2, 1],
        #'55_TCTVA.5L1.B1':  [],
        # '57_TCTVA.5L5.B1': [],
        # '56_TCTH.5L5.B1':  [],
        # '54_TCTH.5L1.B1':  [],

        }


    for tkey in tDict.keys():

        myfile  = workpath + 'runs/TCT/rotate/HL/' + tDict[tkey][0]
        myfile += 'rawhits_influka_units'+ '_' + tkey.lstrip(tkey.split('_')[0] + '_') +'.dat'

        tct     = tkey.split('_')[-1]
        a,b     = 1,1
        cv      = TCanvas( 'cv' + tkey, 'cv' + tkey, 10, 10, a*800, b*600 )
        cv.Divide(a,b)
        gPad.SetRightMargin(0.13) , gPad.SetLeftMargin(0.08)

        hname = 'sixtrack_' + tkey
        xnbins, xmin, xmax = tDict[tkey][1], tDict[tkey][2], tDict[tkey][3]
        ynbins, ymin, ymax = tDict[tkey][4], tDict[tkey][5], tDict[tkey][6]
        hist = TH2F(hname, hname, xnbins, xmin, xmax, ynbins, ymin, ymax )

        xInd, yInd = tDict[tkey][9], tDict[tkey][10]

        with open(myfile) as mf:
            for line in mf:

                x = float(line.split()[xInd])
                y = float(line.split()[yInd])

                hist.Fill(x,y)

        xtitle, ytitle = tDict[tkey][7], tDict[tkey][8]
        hist.GetYaxis().SetTitleOffset(0.82)
        hist.GetXaxis().SetTitle(xtitle)
        hist.GetYaxis().SetTitle(ytitle)
        hist.Draw('colz')

        lab    = mylabel(60)
        x1, y1 = 0.6, 0.95
        lab.DrawLatex(x1, y1-0.1, tct)

        pname  = wwwpath + 'TCT/HL/'
        pname += 'HL_' + hname + '.png'

        print("saving " + pname)

        cv.Print(pname)
