#!/usr/bin/python
#
# Mar 2015, rkwee
## -------------------------------------------------------------------------------
import pymadx
## -------------------------------------------------------------------------------
import ROOT, sys, os, time, math
from ROOT import *
import lossmap, helpers, array
from helpers import *
from array import array
# -----------------------------------------------------------------------------------
def cv43():

    showInfo = 1

    # for each file serveral plots

    tags = [

        'H5_HL_TCT5IN_relaxColl_hHaloB1_roundthin'
        ]


    subfolder = 'TCT/HL/relaxedColl/newScatt/'

    nbins, xmin, xmax = 200,0., 2.
    hx = []

    # collimators
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
    # for each collimator fix a color
    bCol = [
         kBlue,
         kCyan,
         kCyan-2,
         kMagenta+1,
         kMagenta+2,
         kViolet,
         kGreen+2,
         kOrange-2,
         kRed+2,
        ]

    hx = []
    for tag in tags:

        collsummary = workpath + "runs/" + tag + "/coll_summary_" + tag + ".dat"
        cDict = collDict(collsummary)
        rfname = workpath + 'runs/sourcedirs/HL_TCT_7TeV/fluka/hybrid/b1/tct5inrd.dat.root'
        print "Opening","."*33, rfname
        rf = TFile.Open(rfname)
        mt = rf.Get('particle')
        rel = rfname.split('/')[-1].split('.dat')[0]

        collgaps = workpath + "LHC-Collimation/SixTrackConfig/7TeV/hilumiLHC/TCThaloStudies_relaxedCollSettings/b1/collgaps.dat.TCT5LIN"
        cgDict = collgapsDict(collgaps)
        print "and using","."*33, collgaps

        for collName in colls:

            try:
                collid = cDict[collName][0]
            except KeyError:
                print(collName, 'key not found')
                continue

            cut = 'icoll == ' + collid

            # get halfgap in mm as x and y are in mm.
            print collName, cgDict[collName][5]
            halfgap = float(cgDict[collName][5]) * 1000.
            var = ''
            if collName.count('TCTV'): var = 'TMath::Abs(y)'
            elif collName.count('TCTH'): var = 'TMath::Abs(x)'
            if var: var+= ' - ' + str(halfgap)

            va = 'x'
            print 'INFO: histgramming var', var

            # define histograms
            hname = 'hist_' + rel + '_' + collName.replace('.', '_')
            hx += [ TH1F(hname,hname,nbins, xmin, xmax) ]

            if showInfo: print 'INFO: will apply a cut of ', cut, 'to', hname
            mt.Project(hname, var, cut)
            if showInfo: print 'INFO: Have ', hx[-1].GetEntries(), ' entries in', hname, ' for ', collName

            xtitle, ytitle = 'b [mm]', "entries"
            hx[-1].GetXaxis().SetLabelSize(0.02)
            hx[-1].GetYaxis().SetLabelSize(0.03)
            hx[-1].GetXaxis().SetTitle(xtitle)
            hx[-1].GetYaxis().SetTitle(ytitle)


    # canvas
    a,b = 1,len(hx) + 1
    cv = TCanvas( 'cv', 'cv', a*900, b*700)
    cv.Divide(a,b)
    cv.SetRightMargin(0.3)
    cv.SetLeftMargin(0.2)
    cv.SetTopMargin(0.15)


    x1, y1, x2, y2 = 0.2, 0.98, 0.84, 0.9
    lab = mylabel(60)
    hy = []
    for i,hist in enumerate(hx):

        hy += [hist.Clone('cloon' +  hist.GetName())]
        cv.cd(i+1)
        if not i: dOpt = 'hist'
        else: dOpt = 'histsame'
        hist.SetFillColor(kBlue)
        hist.Draw(dOpt)

        hname = hist.GetName().split(rel + '_')[-1].replace('_', '.')
        if showInfo: print 'INFO: Plotting', hname

        lab.DrawLatex(x1, y1-0.1, hname)


    x1, y1, x2, y2 = 0.63,0.7,0.9,0.93
    thelegend = TLegend( x1, y1, x2, y2)
    thelegend.SetFillColor(0)
    thelegend.SetFillStyle(0)
    thelegend.SetLineColor(0)
    thelegend.SetTextSize(0.03)
    thelegend.SetShadowColor(0)
    thelegend.SetBorderSize(0)
    thelegend.SetTextSize(0.04)

    nentries = mt.GetEntries()
    print 'have', nentries, ' in tree'
    for i,hist in enumerate(hy):

        cv.cd(len(hx)+1)
        pad = cv.GetPad(len(hx)+1)
        pad.SetLogy(1)
        if not i: dOpt = 'hist'
        else: dOpt = 'histsame'

        hist.Scale(1./nentries)
        hist.SetLineColor(bCol[i])
        hist.SetFillColor(bCol[i])
        hist.SetLineStyle(i+1)
        hist.SetFillStyle(3001+i)
        hist.GetYaxis().SetTitle('normalised entries')
        hist.GetYaxis().SetRangeUser(0.001,0.05)
        hist.Draw(dOpt)

        hname = hist.GetName().split(rel + '_')[-1].replace('_', '.')
        if showInfo: print 'INFO: Plotting', hname

        thelegend.AddEntry(hist, hname, "fl")

    thelegend.Draw()
    lab.DrawLatex(0.45, y2+0.03, rel)
    pname  = wwwpath
    pname += subfolder + 'impactparameter_'+rel+'.png'

    print('Saving file as ' + pname ) 
    cv.SaveAs(pname)
        
# ----------------------------------------------------------------------------





