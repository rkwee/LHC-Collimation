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

    colls = [
         'TCTH.5L1.B1',
         'TCTVA.5L1.B1',
         'TCTH.4L1.B1', 
         'TCTVA.4L1.B1',
         'TCTH.5R1.B2',
         'TCTVA.5R1.B2',
         'TCTH.4R1.B2', 
         'TCTVA.4R1.B2',
        ]

    for tag in tags:
        collsummary = workpath + "runs/" + tag + "/coll_summary_" + tag + ".dat"
        cDict = collDict(collsummary)
        rfname = workpath + 'runs/'+tag+'/impacts_real_'+tag+'.dat.root'
        rfname = workpath + "runs/sourcedirs/HL_TCT_7TeV/fluka/hybrid/tct5otrd.dat.root"       
        rfname = workpath + "runs/sourcedirs/HL_TCT_7TeV/fluka/TCTIMPAC.dat.root"

        rel = rfname.split('/')[-1].split('.')[0]

        print "Opening","."*33, rfname
        rf = TFile.Open(rfname)
        mt = rf.Get('particle')

        for collName in colls:

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

                collid = cDict[collName][0]
                cut = 'icoll == ' + collid

                if showInfo: print 'INFO: will apply a cut of ', cut, 'to', hname
                mt.Project(hname, var, cut)
                if showInfo: print 'INFO: Have ', hist.GetEntries(), ' entries in', hname, ' for ', collName

                cv = TCanvas( 'cv'+hname, 'cv'+hname, 10, 10, 900, 600) 
                cv.SetRightMargin(0.15)

                hist.Draw('colz')

                x1, y1, x2, y2 = 0.2, 0.98, 0.84, 0.9
                lab = mylabel(60)
                lab.DrawLatex(x1, y1-0.1, rel)
                lab = mylabel(60)
                lab.DrawLatex(x1, y1-0.15, collName)

                pname = wwwpath
                # pname += 'TCT/HL/relaxedColl/newScatt/' + hname + '_' + rel + '_' + collName + '.png'
                pname += 'TCT/HL/nominalColl/beamhalo/' + hname + '_' + rel + '_' + collName + '.png'

                cv.SaveAs(pname)

