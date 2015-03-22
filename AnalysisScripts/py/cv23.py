#!/usr/bin/python
#
# R Kwee-Hinzmann, Nov 2014
# ---------------------------------------------------------------------------------
import ROOT, sys, glob, os, math, helpers
from ROOT import *
from helpers import *
from array import array
# ---------------------------------------------------------------------------------
def cv23():
    # histname+entrie
    #gStyle.SetOptStat(0111)
    # name, entries
    # gStyle.SetOptStat(11)
    # only entries!
    gStyle.SetOptStat(10)
    gStyle.SetPalette(1)
    gStyle.SetStatX(0.90)
    gStyle.SetStatY(0.95)
    gStyle.SetTitleX(0.1)
    gStyle.SetTitleY(.955)

    showInfo = 1
    # plot x,xp; y,yp, x:s, y:s
    # for TCTH ad TCTV at IR1: icoll = 55 TCTH.4L1.B1,56 TCTVA.4L1.B1//71 TCTH.4R1.B2, 71 TCTH.4R1.B2
    # https://github.com/rkwee/LHC-Collimation/blob/master/SixTrackConfig/4TeV/TCThaloStudies/b1/collgaps.dat

    tags = [

        'NewScatt_TCT_4TeV_B1hHalo',
        'NewScatt_TCT_4TeV_B1vHalo',
        'NewScatt_TCT_4TeV_B2hHalo',
        'NewScatt_TCT_4TeV_B2vHalo',

        'TCT_4TeV_B1hHalo',
        'TCT_4TeV_B1vHalo',
        'TCT_4TeV_B2hHalo',
        'TCT_4TeV_B2vHalo',

        ]

    hDict = {
        ## x,y in [m] #0 var #1 xnbins, xmin, xmax, ynbins, ymin, ymax, #2 xtitle, #3 ytitle
        # 'xxpHist':['xp:x', [100,-30.,30., 100,-0.6,0.6],'x', 'x\'[mrad]'],
        # 'yypHist':['yp:y', [100,-30.,30., 100,-0.6,0.6],'y', 'y\'[mrad]'],
        # 'xsHist' :['x:s',  [100,0,1, 100,-30,30],'s[m]', 'x[m]'],
        # 'ysHist' :['y:s',  [100,0,1,100,-20,20],'s[m]', 'y[m]'],
        'xyHist':['y:x', [100,-30.,30., 100,-20.,20.],'x [mm]', 'y [mm]'],
        }

    icollsB1 = [
        (55,'TCTH.4L1.B1'),
        (56,'TCTVA.4L1.B1'),
        ]
    icollsB2 = [
        (71,'TCTH.4R1.B2'), 
        (72,'TCTVA.4R1.B2'),
        ]

    for tag in tags:

        rfname = workpath + 'runs/'+tag+'/impacts_real_'+tag+'.dat.root'
        icolls= icollsB2
        if rfname.count('B1'): icolls = icollsB1

        print "Opening","."*33, rfname
        rf = TFile.Open(rfname)
        mt = rf.Get('particle')

        for collid,collName in icolls:

            for hname in hDict.keys():


                xnbins, xmin, xmax = hDict[hname][1][0],hDict[hname][1][1],hDict[hname][1][2]
                ynbins, ymin, ymax = hDict[hname][1][3],hDict[hname][1][4],hDict[hname][1][5]

                hist = TH2F(hname, hname, xnbins, xmin, xmax, ynbins, ymin, ymax)

                xtitle, ytitle = hDict[hname][2],hDict[hname][3]
                hist.GetXaxis().SetTitle(xtitle)
                hist.GetYaxis().SetTitle(ytitle)

                # store sum of squares of weights 
                hist.Sumw2()

                var = hDict[hname][0]
                if showInfo: print 'INFO: will fill these variables ', var, 'into', hname

                cut = 'icoll == ' + str(collid)

                if showInfo: print 'INFO: will apply a cut of ', cut, 'to', hname
                mt.Project(hname, var, cut)
                if showInfo: print 'INFO: Have ', hist.GetEntries(), ' entries in', hname, ' for ', collName

                cv = TCanvas( 'cv'+hname, 'cv'+hname, 10, 10, 900, 600) 

                hist.Draw('colz')

                x1, y1, x2, y2 = 0.2, 0.98, 0.84, 0.9
                lab = mylabel(60)
                lab.DrawLatex(x1, y1-0.1, tag)
                lab = mylabel(60)
                lab.DrawLatex(x1, y1-0.15, collName)

                pname = wwwpath
                pname += 'TCT/4TeV/compNewSixTrackScattering/' + hname + '_' + tag + '_' + collName + '.png'

                cv.SaveAs(pname)

