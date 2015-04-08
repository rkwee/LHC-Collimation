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
def cv35():

    gStyle.SetOptStat(0)
    gStyle.SetPalette(1)
    gStyle.SetStatX(0.90)
    gStyle.SetStatY(0.95)
    gStyle.SetTitleX(0.1)
    gStyle.SetTitleY(.955)


    collsIR1 = [
        'TCTH.5L1.B1',
        'TCTVA.5L1.B1',
        'TCTH.4L1.B1', 
        'TCTVA.4L1.B1',
        ]
    YurMin, YurMax = 1e-8, 1.e-2
    thisIR = 'IR1'
    colls = collsIR1

    collsIR5 = [
        'TCTH.5L5.B1',
        'TCTVA.5L5.B1',
        'TCTH.4L5.B1', 
        'TCTVA.4L5.B1',
        ]
    YurMin, YurMax = 1e-8, 1e-2
    thisIR = 'IR5'
    colls = collsIR5

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

    # -- get nprim per simulation
    fnames = [fTCT5IN_hB1_rd, fTCT5IN_vB1_rd, fTCT5LOUT_hB1_rd, fTCT5LOUT_vB1_rd]
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
    nhits = []
    for tct in colls:
        try:
            nhits += [ [tct,[float(cDict_tct5in_hB1rd[tct][3]) , float(cDict_tct5in_vB1rd[tct][3]), \
                                 float(cDict_tct5lout_hB1rd[tct][3]), float(cDict_tct5lout_vB1rd[tct][3])]] ]
        except KeyError:
            nhits += [ [tct,[float(cDict_tct5in_hB1rd[tct][3]) , float(cDict_tct5in_vB1rd[tct][3]), \
                                 0., 0.]]] 
            
    print nhits
    nhitsDict = dict(nhits)
    normhits = []
    for tct in colls:
        normhits += [[tct,[nhitsDict[tct][i]/nprims[i] for i in range(len(nprims))]] ]

    normhitsDict = dict(normhits)
    print normhits

    # define histo
    hname, nbins, xmin, xmax = "compTCT5IN", 4, -0.5, 3.5
    hist_ir1_tct5in = TH1F(hname, hname, nbins, xmin, xmax)
    hname, nbins, xmin, xmax = "compTCT5LOUT", 4, -0.5, 3.5
    hist_ir1_tct5lout = TH1F(hname, hname, nbins, xmin, xmax)

    hist_ir1_tct5in.SetMarkerStyle(21)
    hist_ir1_tct5lout.SetMarkerStyle(20)

    for bin,tct in enumerate(colls):
        hist_ir1_tct5in.GetXaxis().SetBinLabel(bin+1,tct)    
        val = normhitsDict[tct][0] + normhitsDict[tct][1]
        print val, tct
        hist_ir1_tct5in.SetBinContent(bin+1,val)
        #hist_ir1_tct5in.SetBinError(bin+1,1./(nprims[0]+nprims[1]))

        val = normhitsDict[tct][2] + normhitsDict[tct][3]
        hist_ir1_tct5lout.SetBinContent(bin+1,val)
        #hist_ir1_tct5lout.SetBinError(bin+1,1./(nprims[2]+nprims[3]))

    a,b = 1,1
    cv = TCanvas( 'cv'+hname, 'cv'+hname, 10, 10, a*900, b*600) 
    cv.Divide(a,b)
    cv.SetGridx(1)
    cv.SetGridy(1)
    cv.SetLogy(1)
    hist_ir1_tct5in.GetYaxis().SetTitle('h+v loss per primary')
    hist_ir1_tct5in.GetYaxis().SetRangeUser(YurMin, YurMax)
    hist_ir1_tct5in.Draw('p')
    hist_ir1_tct5lout.Draw('psame')

    x1, y1, x2, y2 = 0.63,0.8,0.95,0.93
    thelegend = TLegend( x1, y1, x2, y2)
    thelegend.SetFillColor(0)
    thelegend.SetFillStyle(0)
    thelegend.SetLineColor(0)
    thelegend.SetTextSize(0.035)
    thelegend.SetShadowColor(0)
    thelegend.SetBorderSize(0)
    thelegend.AddEntry(hist_ir1_tct5in, 'TCT4 + TCT5', "p")
    thelegend.AddEntry(hist_ir1_tct5lout, 'TCT4 only', "p")
    thelegend.Draw()

    lab = mylabel(60)
    lab.DrawLatex(x1-0.44, y1+0.015, thisIR)

    lab = mylabel(60)
    lab.DrawLatex(x1-0.26, y1+0.015, '')

    lab = mylabel(42)
    lab.DrawLatex(x1-0.44, y1+0.08, 'incoming B1    round beam optics')

    pname = wwwpath
    pname += 'TCT/HL/relaxedColl/newScatt/fluka/compTCT5LINOUT_'+thisIR+'.png'


    cv.SaveAs(pname)

