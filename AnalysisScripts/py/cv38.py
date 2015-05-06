#!/usr/bin/python
#
# from cv23->31->34->35->36->38
# R Kwee-Hinzmann, Apr 2015
# ---------------------------------------------------------------------------------
import ROOT, sys, glob, os, math, helpers, subprocess
from ROOT import *
from helpers import *
# ---------------------------------------------------------------------------------
def cv38():

    gStyle.SetOptStat(0)
    gStyle.SetPalette(1)
    gStyle.SetStatX(0.90)
    gStyle.SetStatY(0.95)
    gStyle.SetTitleX(0.1)
    gStyle.SetTitleY(.955)


    tctLabels = [
        'TCTH.5',
        'TCTV.5',
        'TCTH.4', 
        'TCTV.4',
        ]

    collsIR1 = [
        'TCTH.5L1.B1',
        'TCTVA.5L1.B1',
        'TCTH.4L1.B1', 
        'TCTVA.4L1.B1',
        ]

    thisIR = 'IR1/IR5'

    collsIR5 = [
        'TCTH.5L5.B1',
        'TCTVA.5L5.B1',
        'TCTH.4L5.B1', 
        'TCTVA.4L5.B1',
        ]


    fTCT5IN_hB1_round = workpath + 'runs/H5_HL_TCT5IN_relaxColl_hHaloB1_roundthin/coll_summary_H5_HL_TCT5IN_relaxColl_hHaloB1_roundthin.dat'
    cDict_hB1round = collDict(fTCT5IN_hB1_round)
    fTCT5IN_vB1_round = workpath + 'runs/H5_HL_TCT5IN_relaxColl_vHaloB1_roundthin/coll_summary_H5_HL_TCT5IN_relaxColl_vHaloB1_roundthin.dat'
    cDict_vB1round = collDict(fTCT5IN_vB1_round)
    fTCT5IN_hB1_flat = workpath + 'runs/H5_HL_TCT5IN_relaxColl_hHaloB1_flatthin/coll_summary_H5_HL_TCT5IN_relaxColl_hHaloB1_flatthin.dat'
    cDict_hB1flat = collDict(fTCT5IN_hB1_flat)
    fTCT5IN_vB1_flat = workpath + 'runs/H5_HL_TCT5IN_relaxColl_vHaloB1_flatthin/coll_summary_H5_HL_TCT5IN_relaxColl_vHaloB1_flatthin.dat'
    cDict_vB1flat = collDict(fTCT5IN_vB1_flat)


    # -- get nprim per simulation
    fnames = [fTCT5IN_hB1_round, fTCT5IN_vB1_round, 
              fTCT5IN_hB1_flat, fTCT5IN_vB1_flat,
              ]

    nprimfiles = [fn.split('coll_s')[0] + 'nprim.txt' for fn in fnames]
    nprims = []
    for np in nprimfiles:
        cmd = 'grep "for targetfile LPI" ' + np
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        myStdOut = process.stdout.read()
        nprim = float(myStdOut.split()[0]) * 6400.        
        print "nprim =", nprim, 'in', np
        # -->
        nprims += [ nprim ]

    # -- get N hits on TCT as sum of hor. and ver. B1 
    nhitsIR1 = []
    for tct in collsIR1:
        try:
            nhitsIR1 += [ [tct,[float(cDict_hB1round[tct][3]) , float(cDict_vB1round[tct][3]), float(cDict_hB1flat[tct][3]), float(cDict_vB1flat[tct][3])] ] ]

        except KeyError:
            print "TCT5 should be present!!!"

    nhitsIR5 = []
    for tct in collsIR5:
        try:
            nhitsIR5 += [ [tct,[float(cDict_hB1round[tct][3]) , float(cDict_vB1round[tct][3]), float(cDict_hB1flat[tct][3]), float(cDict_vB1flat[tct][3])] ] ]

        except KeyError:
            print "TCT5 should be present!!!"

    nhitsDictIR1 = dict(nhitsIR1)
    normhitsIR1 = []
    for tct in collsIR1:
        normhitsIR1 += [[tct,[nhitsDictIR1[tct][i]/nprims[i] for i in range(len(nprims))]] ]
    normhitsDictIR1 = dict(normhitsIR1)

    nhitsDictIR5 = dict(nhitsIR5)
    normhitsIR5 = []
    for tct in collsIR5:
        normhitsIR5 += [[tct,[nhitsDictIR5[tct][i]/nprims[i] for i in range(len(nprims))]] ]

    normhitsDictIR5 = dict(normhitsIR5)


    # define histo
    hname, nbins, xmin, xmax = "compTCT5IN_ir1_round", 4, -0.5, 3.5
    hist_ir1_round = TH1F(hname, hname, nbins, xmin, xmax)

    hname = "compTCT5IN_ir1_flat"
    hist_ir1_flat = hist_ir1_round.Clone(hname)

    hname, nbins, xmin, xmax = "compTCT5IN_ir5_round", 4, -0.5, 3.5
    hist_ir5_round = TH1F(hname, hname, nbins, xmin, xmax)

    hname = "compTCT5IN_ir5_flat"
    hist_ir5_flat = hist_ir5_round.Clone(hname)


    hist_ir1_round.GetXaxis().SetLabelSize(0.08)
    hist_ir1_flat.GetXaxis().SetLabelSize(0.08)
    hist_ir5_round.GetXaxis().SetLabelSize(0.08)
    hist_ir5_flat.GetXaxis().SetLabelSize(0.08)


    hist_ir1_round.SetMarkerSize(2.)
    hist_ir1_flat.SetMarkerSize(2.)
    hist_ir5_round.SetMarkerSize(2.)
    hist_ir5_flat.SetMarkerSize(2.)

    hist_ir1_round.SetMarkerStyle(20)
    hist_ir1_round.SetMarkerColor(kBlue-3)
    hist_ir1_flat.SetMarkerStyle(32)
    hist_ir1_flat.SetMarkerColor(kBlue-3)
    hist_ir5_round.SetMarkerStyle(21)
    hist_ir5_round.SetMarkerColor(kRed-1)
    hist_ir5_flat.SetMarkerStyle(28)
    hist_ir5_flat.SetMarkerColor(kRed-1)

    sTCT4val_ir1_rd, sTCT5val_ir1_rd = 0., 0.
    sTCT4val_ir1_ft, sTCT5val_ir1_ft = 0., 0.

    sTCT4val_ir5_rd, sTCT5val_ir5_rd = 0., 0.
    sTCT4val_ir5_ft, sTCT5val_ir5_ft = 0., 0.
    
    for bin,coll in enumerate(tctLabels):
        tct = coll 
        if tct.count('TCTV'): 
            tct = tct.replace('V', 'VA')

        tct += 'L1.B1'

        hist_ir1_round.GetXaxis().SetBinLabel(bin+1,coll)    
        val_ir1_rd = normhitsDictIR1[tct][0] + normhitsDictIR1[tct][1]
        hist_ir1_round.SetBinContent(bin+1,val_ir1_rd)

        val_ir1_ft = normhitsDictIR1[tct][2] + normhitsDictIR1[tct][3]
        hist_ir1_flat.SetBinContent(bin+1,val_ir1_ft)

        # summed values IR1
        if tct.count('4L'):
            sTCT4val_ir1_rd += val_ir1_rd
            sTCT4val_ir1_ft += val_ir1_ft
        elif tct.count('5L'):
            sTCT5val_ir1_rd += val_ir1_rd
            sTCT5val_ir1_ft += val_ir1_ft

        tct = coll 
        if tct.count('TCTV'): 
            tct = tct.replace('V', 'VA')

        tct += 'L5.B1'

        hist_ir5_round.GetXaxis().SetBinLabel(bin+1,coll)    
        val_ir5_rd = normhitsDictIR5[tct][0] + normhitsDictIR5[tct][1]
        hist_ir5_round.SetBinContent(bin+1,val_ir5_rd)

        val_ir5_ft = normhitsDictIR5[tct][2] + normhitsDictIR5[tct][3]
        hist_ir5_flat.SetBinContent(bin+1,val_ir5_ft)

        # summed values IR5
        if tct.count('4L'):
            sTCT4val_ir5_rd += val_ir5_rd
            sTCT4val_ir5_ft += val_ir5_ft
        elif tct.count('5L'):
            sTCT5val_ir5_rd += val_ir5_rd
            sTCT5val_ir5_ft += val_ir5_ft
        

    YurMin, YurMax = 1e-8, 1e-2

    print "sTCT4val_ir1_rd",sTCT4val_ir1_rd
    print "sTCT5val_ir1_rd",sTCT5val_ir1_rd
    print "sTCT4val_ir1_ft",sTCT4val_ir1_ft
    print "sTCT5val_ir1_ft",sTCT5val_ir1_ft

    print '.'*30
    print 'sum rd', sTCT4val_ir1_rd+sTCT5val_ir1_rd
    print 'sum ft', sTCT4val_ir1_ft+sTCT5val_ir1_ft

    print '-'*30
    print "sTCT4val_ir5_rd",sTCT4val_ir5_rd
    print "sTCT5val_ir5_rd",sTCT5val_ir5_rd
    print "sTCT4val_ir5_ft",sTCT4val_ir5_ft
    print "sTCT5val_ir5_ft",sTCT5val_ir5_ft

    print '.'*30
    print 'sum rd', sTCT4val_ir5_rd+sTCT5val_ir5_rd
    print 'sum ft', sTCT4val_ir5_ft+sTCT5val_ir5_ft


    a,b = 1,1
    cv = TCanvas( 'cv'+hname, 'cv'+hname, 10, 10, a*900, b*600) 
    cv.Divide(a,b)
    cv.SetGridx(1)
    cv.SetGridy(1)
    cv.SetLogy(1)
    hist_ir1_round.GetYaxis().SetTitle('h+v loss per primary')
    hist_ir1_round.GetYaxis().SetRangeUser(YurMin, YurMax)
    hist_ir1_round.Draw('p')

    hist_ir1_flat.GetYaxis().SetTitle('h+v loss per primary')
    hist_ir1_flat.GetYaxis().SetRangeUser(YurMin, YurMax)
    hist_ir1_flat.Draw('psame')

    hist_ir5_round.GetYaxis().SetTitle('h+v loss per primary')
    hist_ir5_round.GetYaxis().SetRangeUser(YurMin, YurMax)
    hist_ir5_round.Draw('psame')

    hist_ir5_flat.GetYaxis().SetTitle('h+v loss per primary')
    hist_ir5_flat.GetYaxis().SetRangeUser(YurMin, YurMax)
    hist_ir5_flat.Draw('psame')


    x1, y1, x2, y2 = 0.63,0.7,0.9,0.93
    thelegend = TLegend( x1, y1, x2, y2)
    thelegend.SetFillColor(0)
    thelegend.SetFillStyle(0)
    thelegend.SetLineColor(0)
    thelegend.SetTextSize(0.03)
    thelegend.SetShadowColor(0)
    thelegend.SetBorderSize(0)
    thelegend.SetTextSize(0.04)
    thelegend.AddEntry(hist_ir1_round, 'round beam IR1', "p")
    thelegend.AddEntry(hist_ir1_flat, 'flat beam IR1', "p")
    thelegend.AddEntry(hist_ir5_round, 'round beam IR5', "p")
    thelegend.AddEntry(hist_ir5_flat, 'flat beam IR5', "p")
    thelegend.Draw()

    lab = mylabel(60)
    lab.DrawLatex(x1-0.44, y1+0.1, thisIR)

    lab = mylabel(42)
    lab.DrawLatex(x1-0.44, y1+0.16, 'incoming B1    TCT4 + TCT5')

    pname = wwwpath
    pname += 'TCT/HL/relaxedColl/newScatt/fluka/compOptics_IR1IR5.pdf'


    cv.SaveAs(pname)

