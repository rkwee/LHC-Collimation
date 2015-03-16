#!/usr/bin/python
#
# from cv23
# R Kwee-Hinzmann, Nov 2014
# ---------------------------------------------------------------------------------
import ROOT, sys, glob, os, math, helpers
from ROOT import *
from helpers import *
from array import array
# ---------------------------------------------------------------------------------
def cv31():
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
    # for TCTs

    tags = [

        'H5_HL_TCT5IN_relaxColl_hHaloB1_roundthin'
        ]

    hDict = {
        ## x,y in [m] #0 var #1 xnbins, xmin, xmax, ynbins, ymin, ymax, #2 xtitle, #3 ytitle
        'xxpHist':['xp:x', [100,-30.,30., 100,-0.6,0.6],'x', 'x\'[mrad]'],
        'yypHist':['yp:y', [100,-30.,30., 100,-0.6,0.6],'y', 'y\'[mrad]'],
        # 'xsHist' :['x:s',  [100,0,1, 100,-30,30],'s[m]', 'x[m]'],
        # 'ysHist' :['y:s',  [100,0,1,100,-20,20],'s[m]', 'y[m]'],
        }

    icollsIR1 = [
       # ('54', 'TCTH.5L1.B1'),
       # ('55', 'TCTVA.5L1.B1'),
        ('52', 'TCTH.4L1.B1'), 
       # ('53', 'TCTVA.4L1.B1'),
    #     ]
    #    icollsIR5 = [
        # ('56', 'TCTH.5L5.B1'),
        # ('57', 'TCTVA.5L5.B1'), 
        # ('19', 'TCTH.4L5.B1'),  
        # ('20', 'TCTVA.4L5.B1'), 
        ]

    for tag in tags:

        rfname = workpath + 'runs/'+tag+'/impacts_real_'+tag+'.dat.root'
        icolls= icollsIR1
        

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

                cut = 'icoll == ' + collid

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
                pname += 'TCT/HL/relaxedColl/newScatt/' + hname + '_' + tag + '_' + collName + '.png'

                cv.SaveAs(pname)

