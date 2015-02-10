#!/usr/bin/python
#
# plots from LPI file
#
# R Kwee-Hinzmann, Feb 2015
# ---------------------------------------------------------------------------------
import ROOT, sys, glob, os, math, helpers
from ROOT import *
from helpers import *
from array import array
# ---------------------------------------------------------------------------------
def cv26():
    # histname+entrie
    #gStyle.SetOptStat(0111)
    # name, entries, mean, rms
    # gStyle.SetOptStat(1111)

    # name, mean, rms, underflow, overflow
    # gStyle.SetOptStat(111111)
    # only entries!
    gStyle.SetOptStat(10)
    gStyle.SetPalette(1)
    #gStyle.SetStatX(0.90)
    #gStyle.SetStatY(0.95)
    #gStyle.SetTitleX(0.1)
    #gStyle.SetTitleY(.955)

    showInfo = 1
    debug = 1

    tag_hdf5  = 'twin_H5_NewScatt_TCT_4TeV_B1hHalo_trajectories'
    tag_ascii = 'twin_NewScatt_TCT_4TeV_B1hHalo_trajectories'

    f_hdf5  = workpath + 'runs/' + tag_hdf5 + '/LPI_BLP_out_' + tag_hdf5 + '.s'
    f_ascii = workpath + 'runs/' + tag_ascii + '/LPI_BLP_out_' + tag_ascii + '.s'

    # h5 with fix

    hDict = {
        # #0 nbin, #1 xmin, #2 xmax, #3 xtitle #4 ytitle #5 vPos #6 YurMin #7 YurMax #8 doLogy
        # 'name':[ 11, -0.5, 10.5,'difference', 'entries', 1],
         'turn':[ 200, 0.5, 200.5,'turn number', 'entries', 2, 1, 400, 1],
        's':[ 200, 0, 27100,'s [m]', 'entries', 3, 1, 3000., 0],
        # 'x':[ 100, -0.1, 0.1,'difference', 'entries', 4],
        # 'xp':[ 100, -0.1, 0.1,'difference', 'entries', 5],
        # 'y':[ 100, -0.1, 0.1,'difference', 'entries', 6],
        # 'yp':[ 100, -0.1, 0.1,'difference', 'entries', 7],
        # 'dEoverE':[ 100, -0.1, 0.1,'difference', 'entries', 8],
        # 'type':[ 100, -0.1, 0.1,'difference', 'entries', 9],
        }

    hKeys = hDict.keys()
    for var in hKeys: 

        vPos  = hDict[var][5]-1 # this starts at 0
        hname = var + "_hdf5"
        doLogy = hDict[var][8]
        nbins, xmin, xmax = hDict[var][0], hDict[var][1], hDict[var][2]
        YurMin, YurMax = hDict[var][7], hDict[var][8]
        hist_hdf5  = TH1F(hname, hname, nbins, xmin, xmax)
        hist_hdf5.SetLineColor(kOrange-1)
        hist_hdf5.SetFillStyle(8)
        hist_hdf5.SetFillColor(kOrange-1)
        hist_hdf5.GetYaxis().SetTitle(hDict[var][4])
        hist_hdf5.GetXaxis().SetTitle(hDict[var][3])
        if YurMax > 0.: hist_hdf5.GetYaxis().SetRangeUser(YurMin,YurMax)

        hname = var + "_ascii"
        nbins, xmin, xmax = hDict[var][0], hDict[var][1], hDict[var][2]
        hist_ascii  = TH1F(hname, hname, nbins, xmin, xmax)
        hist_ascii.SetLineColor(kBlack)

        vA, vH = [], []

        with open(f_ascii) as fA:
            for line in fA:
                try:                    
                    vA += [ float(line.split()[vPos]) ]
                    hist_ascii.Fill(vA[-1])
                except ValueError:
                    print "ignoring", line
                except IndexError:
                    print "ignoring as well", line

        with open(f_hdf5) as fH:
            for line in fH:
                try:                    
                    vH += [ float(line.split()[vPos]) ]
                    hist_hdf5.Fill(vH[-1])
                except ValueError:
                    print "ignoring", line
                except IndexError:
                    print "ignoring as well", line

        

        cv = TCanvas( 'cv'+var, 'cv'+var, 10, 10, 900, 600) 
        gPad.SetLogy(doLogy)

        x1, y1, x2, y2 = 0.2, 0.98, 0.8, 0.9
        hist_hdf5.Draw('hist')
        hist_ascii.Draw('histsame')
        lab = mylabel(60)
        lab.DrawLatex(x1, y1-0.1, '' + var)

        x1, y1, x2, y2 = 0.8, 0.55, 0.88, 0.7
        thelegend = TLegend( x1, y1, x2, y2)
        thelegend.SetFillColor(0)
        thelegend.SetLineColor(0)
        thelegend.SetTextSize(0.035)
        thelegend.SetShadowColor(10)
        thelegend.AddEntry(hist_ascii, 'ascii', 'LF')
        thelegend.AddEntry(hist_hdf5, 'hdf5', 'LF')
        thelegend.Draw()

        pname = wwwpath
        pname += 'TCT/4TeV/hdf5/twin/' + var  +'.png'
        cv.SaveAs(pname)
                
