#!/usr/bin/python
#
# from cv23->31->34->35
# R Kwee-Hinzmann, Apr 2015
# ---------------------------------------------------------------------------------
import ROOT, sys, glob, os, math, helpers, subprocess
from ROOT import *
from helpers import *
from array import array
# ---------------------------------------------------------------------------------
def cv37():

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
    YurMin, YurMax = 1e-8, 1.e-2
    thisIR = 'IR1/IR5'


    collsIR5 = [
        'TCTH.5L5.B1',
        'TCTVA.5L5.B1',
        'TCTH.4L5.B1', 
        'TCTVA.4L5.B1',
        ]
    YurMin, YurMax = 1e-8, 1e-2

    colls = collsIR1 + collsIR5

    fTCT5IN_hB1_rd = workpath + 'runs/H5_HL_TCT5IN_relaxColl_hHaloB1_roundthin/coll_summary_H5_HL_TCT5IN_relaxColl_hHaloB1_roundthin.dat'
    cDict_tct5in_hB1rd = collDict(fTCT5IN_hB1_rd)
    fTCT5IN_vB1_rd = workpath + 'runs/H5_HL_TCT5IN_relaxColl_vHaloB1_roundthin/coll_summary_H5_HL_TCT5IN_relaxColl_vHaloB1_roundthin.dat'
    cDict_tct5in_vB1rd = collDict(fTCT5IN_vB1_rd)

    fTCT5LOUT_hB1_rd = workpath + 'runs/H5_HL_TCT5LOUT_relaxColl_hHaloB1_roundthin/coll_summary_H5_HL_TCT5LOUT_relaxColl_hHaloB1_roundthin.dat'
    cDict_tct5lout_hB1rd = collDict(fTCT5LOUT_hB1_rd)
    fTCT5LOUT_vB1_rd = workpath + 'runs/H5_HL_TCT5LOUT_relaxColl_vHaloB1_roundthin/coll_summary_H5_HL_TCT5LOUT_relaxColl_vHaloB1_roundthin.dat'
    cDict_tct5lout_vB1rd = collDict(fTCT5LOUT_vB1_rd)

    # -- get sum of impacting protons on TCPs at IR7
    tcpL7 = ['TCP.D6L7.B1', 'TCP.C6L7.B1', 'TCP.B6L7.B1']
    ntcp_tct5in_hB1rd, ntcp_tct5in_vB1rd, ntcp_tct5lout_hB1rd, ntcp_tct5lout_vB1rd = 0, 0, 0, 0

    for tcp in tcpL7:
        ntcp_tct5in_hB1rd += float(cDict_tct5in_hB1rd[tcp][2])
        ntcp_tct5in_vB1rd += float(cDict_tct5in_vB1rd[tcp][2])
        ntcp_tct5lout_hB1rd += float(cDict_tct5lout_hB1rd[tcp][2])
        ntcp_tct5lout_vB1rd += float(cDict_tct5lout_vB1rd[tcp][2])
    # -->
    ntcp = [ntcp_tct5in_hB1rd, ntcp_tct5in_vB1rd, ntcp_tct5lout_hB1rd, ntcp_tct5lout_vB1rd]

    # -- get nprim per simulation -- collimator independent
    fnames = [fTCT5IN_hB1_rd, fTCT5IN_vB1_rd, fTCT5LOUT_hB1_rd, fTCT5LOUT_vB1_rd]
    nprimfiles = [fn.split('coll_s')[0] + 'nprim.txt' for fn in fnames]
    nprims = []
    for np in nprimfiles:
        cmd = 'grep "for targetfile LPI" ' + np
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        myStdOut = process.stdout.read()
        nprim = float(myStdOut.split()[0]) * 6400.        
        #print "nprim =", nprim, 'in', np
        # -->
        nprims += [ nprim ]

    # -- get N hits on TCT as sum of hor. and ver. B1 
    nhitsIR1 = []
    for tct in collsIR1:
        try:
            nhitsIR1 += [ [tct,[float(cDict_tct5in_hB1rd[tct][3]) , float(cDict_tct5in_vB1rd[tct][3]), \
                                 float(cDict_tct5lout_hB1rd[tct][3]), float(cDict_tct5lout_vB1rd[tct][3])]] ]
        except KeyError:
            nhitsIR1 += [ [tct,[float(cDict_tct5in_hB1rd[tct][3]) , float(cDict_tct5in_vB1rd[tct][3]), \
                                 0., 0.]]] 

    nhitsIR5 = []
    for tct in collsIR5:
        try:
            nhitsIR5 += [ [tct,[float(cDict_tct5in_hB1rd[tct][3]) , float(cDict_tct5in_vB1rd[tct][3]), \
                                 float(cDict_tct5lout_hB1rd[tct][3]), float(cDict_tct5lout_vB1rd[tct][3])]] ]
        except KeyError:
            nhitsIR5 += [ [tct,[float(cDict_tct5in_hB1rd[tct][3]) , float(cDict_tct5in_vB1rd[tct][3]), \
                                 0., 0.]]] 
            
    nhitsDictIR1 = dict(nhitsIR1)
    nhitsDictIR5 = dict(nhitsIR5)
    normhitsIR1 = []
    for tct in collsIR1:
        normhitsIR1 += [[tct,[nhitsDictIR1[tct][i]/nprims[i] for i in range(len(nprims))]] ]

    normhitsIR5 = []
    for tct in collsIR5:
        normhitsIR5 += [[tct,[nhitsDictIR5[tct][i]/nprims[i] for i in range(len(nprims))]] ]

    normhitsDictIR1 = dict(normhitsIR1)
    normhitsDictIR5 = dict(normhitsIR5)

    print normhitsDictIR1
    print normhitsDictIR5

    # define histo
    hname, nbins, xmin, xmax = "compTCT5IN_ir1", 4, -0.5, 3.5
    hist_ir1_tct5in = TH1F(hname, hname, nbins, xmin, xmax)
    hname, nbins, xmin, xmax = "compTCT5IN_ir5", 4, -0.5, 3.5
    hist_ir5_tct5in = TH1F(hname, hname, nbins, xmin, xmax)


    hname, nbins, xmin, xmax = "compTCT5LOUT_ir1", 4, -0.5, 3.5
    hist_ir1_tct5lout = TH1F(hname, hname, nbins, xmin, xmax)
    hname, nbins, xmin, xmax = "compTCT5LOUT_ir5", 4, -0.5, 3.5
    hist_ir5_tct5lout = TH1F(hname, hname, nbins, xmin, xmax)

    hist_ir1_tct5in.GetXaxis().SetLabelSize(0.07)
    hist_ir5_tct5in.GetXaxis().SetLabelSize(0.06)
    hist_ir1_tct5lout.GetXaxis().SetLabelSize(0.05)
    hist_ir5_tct5lout.GetXaxis().SetLabelSize(0.04)

    hist_ir1_tct5in.SetMarkerSize(2.)
    hist_ir5_tct5in.SetMarkerSize(2.)
    hist_ir1_tct5lout.SetMarkerSize(2.)
    hist_ir5_tct5lout.SetMarkerSize(2.)

    hist_ir1_tct5in.SetMarkerStyle(21)
    hist_ir1_tct5in.SetMarkerColor(kBlack)
    hist_ir5_tct5in.SetMarkerStyle(20)
    hist_ir5_tct5in.SetMarkerColor(kGray+1)

    hist_ir1_tct5lout.SetMarkerColor(kBlack)
    hist_ir1_tct5lout.SetMarkerStyle(23)
    hist_ir5_tct5lout.SetMarkerColor(kGray+1)
    hist_ir5_tct5lout.SetMarkerStyle(30)

    sval_ir1OUT, sTCT4val_ir1IN, sTCT5val_ir1IN = 0., 0., 0.
    sval_ir5OUT, sTCT4val_ir5IN, sTCT5val_ir5IN = 0., 0., 0.

    for bin,coll in enumerate(tctLabels):

        tct = coll 
        if tct.count('TCTV'): 
            tct = tct.replace('V', 'VA')

        tct += 'L1.B1'

        hist_ir1_tct5in.GetXaxis().SetBinLabel(bin+1,coll)    
        valIR1IN = normhitsDictIR1[tct][0] + normhitsDictIR1[tct][1]

        hist_ir1_tct5in.SetBinContent(bin+1,valIR1IN)
        valIR1OUT = normhitsDictIR1[tct][2] + normhitsDictIR1[tct][3]
        ratioIR1 = valIR1OUT/valIR1IN
        print tct, 'IR1 TCT5LIN, TCT5LOUT, ratio OUT/IN', valIR1IN, valIR1OUT, ratioIR1
        hist_ir1_tct5lout.SetBinContent(bin+1,valIR1OUT)

        # summed values IR1
        sval_ir1OUT += valIR1OUT
        if tct.count('4L'):
            sTCT4val_ir1IN += valIR1IN
        elif tct.count('5L'):
            sTCT5val_ir1IN += valIR1IN

        tct = coll 
        if tct.count('TCTV'): 
            tct = tct.replace('V', 'VA')

        tct += 'L5.B1'

        hist_ir5_tct5in.GetXaxis().SetBinLabel(bin+1,coll)    
        valIR5IN = normhitsDictIR5[tct][0] + normhitsDictIR5[tct][1]
        hist_ir5_tct5in.SetBinContent(bin+1,valIR5IN)
        valIR5OUT = normhitsDictIR5[tct][2] + normhitsDictIR5[tct][3]
        hist_ir5_tct5lout.SetBinContent(bin+1,valIR5OUT)
        ratioIR5 = valIR5OUT/valIR5IN
        print tct, 'IR5 TCT5LIN, TCT5LOUT, ratio OUT/IN', valIR5IN, valIR5OUT, ratioIR5

        # summed values IR5
        sval_ir5OUT += valIR5OUT
        if tct.count('4L'):
            sTCT4val_ir5IN += valIR5IN
        elif tct.count('5L'):
            sTCT5val_ir5IN += valIR5IN

    print "sval_ir1OUT", sval_ir1OUT
    print "sTCT4val_ir1IN", sTCT4val_ir1IN
    print "sTCT5val_ir1IN", sTCT5val_ir1IN
    print "sval_ir1IN/OUT", sTCT4val_ir1IN/sval_ir1OUT
    print "sval_ir1OUT/IN", sval_ir1OUT/sTCT4val_ir1IN

    print '.'*20

    print "sval_ir5OUT", sval_ir5OUT
    print "sTCT4val_ir5IN", sTCT4val_ir5IN
    print "sTCT5val_ir5IN", sTCT5val_ir5IN
    print "sval_ir5OUT/IN", sval_ir5OUT/sTCT4val_ir5IN
    print "sval_ir5OUT/IN", sTCT4val_ir5IN/sval_ir5OUT

    a,b = 1,1
    cv = TCanvas( 'cv'+hname, 'cv'+hname, 10, 10, a*900, b*600) 
    cv.Divide(a,b)
    cv.SetGridx(1)
    cv.SetGridy(1)
    cv.SetLogy(1)
    hist_ir1_tct5in.GetYaxis().SetTitle('h+v loss per primary')
    hist_ir1_tct5in.GetYaxis().SetRangeUser(YurMin, YurMax)
    hist_ir1_tct5in.Draw('p')
    hist_ir5_tct5in.Draw('psame')
    hist_ir1_tct5lout.Draw('psame')
    hist_ir5_tct5lout.Draw('psame')


    x1, y1, x2, y2 = 0.63,0.74,0.88,0.93
    thelegend = TLegend( x1, y1, x2, y2)
    thelegend.SetFillColor(0)
    thelegend.SetFillStyle(0)
    thelegend.SetLineColor(0)
    thelegend.SetTextSize(0.03)
    thelegend.SetShadowColor(0)
    thelegend.SetBorderSize(0)
    thelegend.SetTextSize(0.04)
    thelegend.AddEntry(hist_ir1_tct5in, 'TCT4 + TCT5 IR1', "p")
    thelegend.AddEntry(hist_ir1_tct5lout, 'TCT4 only IR1', "p")
    thelegend.AddEntry(hist_ir5_tct5in, 'TCT4 + TCT5 IR5', "p")
    thelegend.AddEntry(hist_ir5_tct5lout, 'TCT4 only IR5', "p")
    thelegend.Draw()

    lab = mylabel(60)
    lab.DrawLatex(x1-0.44, y1+0.1, thisIR)

    lab = mylabel(42)
    lab.DrawLatex(x1-0.44, y1+0.16, 'incoming B1  round beam optics')

    pname = wwwpath
    pname += 'TCT/HL/relaxedColl/newScatt/fluka/compTCT5LINOUT_roundthin_B1_IR1IR5.pdf'


    cv.SaveAs(pname)

