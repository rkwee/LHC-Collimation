#!/usr/bin/python
#
# R Kwee-Hinzmann, Feb 2015
# ---------------------------------------------------------------------------------
import ROOT, sys, glob, os, math, helpers
from ROOT import *
from helpers import *
from array import array
# ---------------------------------------------------------------------------------
def cv29():
    # histname+entrie
    #gStyle.SetOptStat(0111)
    # name, entries
    # gStyle.SetOptStat(11)
    # only entries!
    # gStyle.SetOptStat(10)

    gStyle.SetOptStat(0)
    gStyle.SetPalette(1)
    gStyle.SetStatX(0.90)
    gStyle.SetStatY(0.95)
    gStyle.SetTitleX(0.1)
    gStyle.SetTitleY(.955)

    showInfo = 1

    pathtofiles = workpath + 'runs/testHDF5_1Pack/run_test_3/'

    rfNames = [
        pathtofiles + 'ascii/tracks2.dat.root',
        pathtofiles + 'incr1000_dbg/realtracks2.dat.root',
        pathtofiles + 'incr10k_dbg/tracks2.h5-to-dat.rawlist.root',
        ]

    # precision 
    pr = ['ascii', 'direct', 'hdf5']
    co = [kBlack, kGreen, kOrange-1]
    dO = ['HIST', "HISTSAME", "HISTSAME"]
    rf = [TFile.Open(rfN) for rfN in rfNames]
    mt = [i.Get('particle') for i in rf]

    hDict = {
        # #0 nbin, #1 xmin, #2 xmax, #3 xtitle #4 ytitle #5 doLogy #6 YurMin #7 YurMax 
        # 'name':[ 11, -0.5, 10.5,'difference', 'entries', 0],
         # 'turn':[ 10, 0.5, 9.5,'turn number', 'entries', 0, 1, 400, 0],
        's':[ 500, 19500, 27500,'s [m]', 'entries', 0, 1, 3000., 0],
        'x':[ 150, -15, 20,'x [mm]', 'entries', 1],
        'xp':[ 300, -1.01, 2.1,'xp', 'entries', 1],
        'y':[ 100, -15, 15,'y [mm]', 'entries', 0],
        'yp':[ 100, -0.5, 0.7,'yp [mrad]', 'entries', 1],
        'dEoverE':[ 100, -2.e-4, 2e-4,'dE/E', 'entries', 1],
        # 'type':[ 100, -0.1, 0.1,'type', 'entries', 0],
        }


    for var in hDict.keys():

        hists = []
        xbins, xmin, xmax = hDict[var][0],hDict[var][1],hDict[var][2]
        hnames = [var+thistype for thistype in pr]

        
        xtitle, ytitle = hDict[var][3],hDict[var][4]
        doLogy = hDict[var][5]
        cv = TCanvas( 'cv'+var, 'cv'+var, 10, 10, 900, 600) 

        x1, y1, x2, y2 = 0.55, 0.72, 0.84, 0.9
        thelegend = TLegend( x1, y1, x2, y2)
        thelegend.SetFillColor(0)
        thelegend.SetLineColor(0)
        thelegend.SetTextSize(0.035)
        thelegend.SetShadowColor(10)

        for h in range(3):
            gPad.SetLogy(doLogy)
            hists += [TH1F(hnames[h], hnames[h], xbins, xmin, xmax)]

            hists[h].GetXaxis().SetTitle(xtitle)
            hists[h].GetYaxis().SetTitle(ytitle)

            hists[h].SetLineColor(co[h])
            #hists[h].SetFillColor(co[h])

            # store sum of squares of weights 
            hists[h].Sumw2()
            mt[h].Project(hnames[h], var)
            hists[h].Draw(dO[h])

            meanval = str(hists[h].GetMean())
            thelegend.AddEntry(hists[h],pr[h] + ': ' + meanval, 'f')


        
        thelegend.Draw()
        hists[-1].Draw(dO[-1])
        pname = wwwpath
        pname += 'TCT/4TeV/hdf5/checkPrecision/' + var + '.png'

        cv.SaveAs(pname)

