#!/usr/bin/python
#
# from cv23->31->34->35
# R Kwee-Hinzmann, Apr 2015
# ---------------------------------------------------------------------------------
import ROOT, sys, glob, os, math, helpers, subprocess
from ROOT import *
from helpers import *
# ---------------------------------------------------------------------------------
def cv36():

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
    YurMin, YurMax = 1e-6, 1.e-3
    thisIR = 'IR1'
    colls = collsIR1

    collsIR5 = [
        'TCTH.5L5.B1',
        'TCTVA.5L5.B1',
        'TCTH.4L5.B1', 
        'TCTVA.4L5.B1',
        ]
    YurMin, YurMax = 1e-8, 1e-3
    thisIR = 'IR5'
    colls = collsIR5

    fTCT5IN_hB1_round = workpath + 'runs/H5_HL_TCT5IN_relaxColl_hHaloB1_roundthin/coll_summary_H5_HL_TCT5IN_relaxColl_hHaloB1_roundthin.dat'
    cDict_hB1round = collDict(fTCT5IN_hB1_round)
    fTCT5IN_vB1_round = workpath + 'runs/H5_HL_TCT5IN_relaxColl_vHaloB1_roundthin/coll_summary_H5_HL_TCT5IN_relaxColl_vHaloB1_roundthin.dat'
    cDict_vB1round = collDict(fTCT5IN_vB1_round)
    fTCT5IN_hB1_flat = workpath + 'runs/H5_HL_TCT5IN_relaxColl_hHaloB1_flatthin/coll_summary_H5_HL_TCT5IN_relaxColl_hHaloB1_flatthin.dat'
    cDict_hB1flat = collDict(fTCT5IN_hB1_flat)
    fTCT5IN_vB1_flat = workpath + 'runs/H5_HL_TCT5IN_relaxColl_vHaloB1_flatthin/coll_summary_H5_HL_TCT5IN_relaxColl_vHaloB1_flatthin.dat'
    cDict_vB1flat = collDict(fTCT5IN_vB1_flat)


    fTCT5IN_hB1_sround = workpath + 'runs/H5_HL_TCT5IN_relaxColl_hHaloB1_sroundthin/coll_summary_H5_HL_TCT5IN_relaxColl_hHaloB1_sroundthin.dat'
    cDict_hB1sround = collDict(fTCT5IN_hB1_sround)
    fTCT5IN_vB1_sround = workpath + 'runs/H5_HL_TCT5IN_relaxColl_vHaloB1_sroundthin/coll_summary_H5_HL_TCT5IN_relaxColl_vHaloB1_sroundthin.dat'
    cDict_vB1sround = collDict(fTCT5IN_vB1_sround)
    fTCT5IN_hB1_sflat = workpath + 'runs/H5_HL_TCT5IN_relaxColl_hHaloB1_sflatthin/coll_summary_H5_HL_TCT5IN_relaxColl_hHaloB1_sflatthin.dat'
    cDict_hB1sflat = collDict(fTCT5IN_hB1_sflat)
    fTCT5IN_vB1_sflat = workpath + 'runs/H5_HL_TCT5IN_relaxColl_vHaloB1_sflatthin/coll_summary_H5_HL_TCT5IN_relaxColl_vHaloB1_sflatthin.dat'
    cDict_vB1sflat = collDict(fTCT5IN_vB1_sflat)

    # -- get nprim per simulation
    fnames = [fTCT5IN_hB1_round, fTCT5IN_vB1_round, 
              fTCT5IN_hB1_flat, fTCT5IN_vB1_flat,
              fTCT5IN_hB1_sround, fTCT5IN_vB1_sround, 
              fTCT5IN_hB1_sflat, fTCT5IN_vB1_sflat,
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
    nhits = []
    for tct in colls:
        try:
            nhits += [ [tct,[float(cDict_hB1round[tct][3]) , float(cDict_vB1round[tct][3]), float(cDict_hB1flat[tct][3]), float(cDict_vB1flat[tct][3]), \
                             float(cDict_hB1sround[tct][3]) , float(cDict_vB1sround[tct][3]), float(cDict_hB1sflat[tct][3]), float(cDict_vB1sflat[tct][3])]] ]
                                 
        except KeyError:
            print "TCT5 should be present!!!"

    print nhits
    nhitsDict = dict(nhits)
    normhits = []
    for tct in colls:
        normhits += [[tct,[nhitsDict[tct][i]/nprims[i] for i in range(len(nprims))]] ]

    normhitsDict = dict(normhits)
    print normhits

    # define histo
    hname, nbins, xmin, xmax = "compTCT5IN_round", 4, -0.5, 3.5
    hist_round = TH1F(hname, hname, nbins, xmin, xmax)
    hname = "compTCT5IN_hB1_round"
    hist_round_hB1 = hist_round.Clone(hname)
    hname = "compTCT5IN_vB1_round"
    hist_round_vB1 = hist_round.Clone(hname)

    hname = "compTCT5IN_flat"
    hist_flat = hist_round.Clone(hname)
    hname = "compTCT5IN_hB1_flat"
    hist_flat_hB1 = hist_round.Clone(hname)
    hname = "compTCT5IN_vB1_flat"
    hist_flat_vB1 = hist_round.Clone(hname)

    hname = "compTCT5IN_sround"
    hist_sround = hist_round.Clone(hname)
    hname = "compTCT5IN_hB1_sround"
    hist_sround_hB1 = hist_round.Clone(hname)
    hname = "compTCT5IN_vB1_sround"
    hist_sround_vB1 = hist_round.Clone(hname)

    hname = "compTCT5IN_sflat"
    hist_sflat = hist_round.Clone(hname)
    hname = "compTCT5IN_hB1_sflat"
    hist_sflat_hB1 = hist_round.Clone(hname)
    hname = "compTCT5IN_vB1_sflat"
    hist_sflat_vB1 = hist_round.Clone(hname)

    hist_round_hB1.SetMarkerSize(.9)
    hist_round_hB1.SetMarkerStyle(23)
    hist_round_vB1.SetMarkerStyle(22)
    hist_round_hB1.SetMarkerColor(kGray+1)
    hist_round_vB1.SetMarkerColor(kGray+1)
    hist_round.SetMarkerStyle(22)
    hist_round.SetMarkerColor(kBlue-3)

    hist_flat_hB1.SetMarkerStyle(32)
    hist_flat_vB1.SetMarkerStyle(26)
    hist_flat_hB1.SetMarkerColor(kGray+1)
    hist_flat_vB1.SetMarkerColor(kGray+1)
    hist_flat.SetMarkerStyle(29)
    hist_flat.SetMarkerColor(kGreen-1)

    hist_sround_hB1.SetMarkerStyle(5)
    hist_sround_vB1.SetMarkerStyle(3)
    hist_sround_hB1.SetMarkerColor(kGray+1)
    hist_sround_vB1.SetMarkerColor(kGray+1)
    hist_sround.SetMarkerStyle(34)
    hist_sround.SetMarkerColor(kMagenta)

    hist_sflat_hB1.SetMarkerStyle(27)
    hist_sflat_vB1.SetMarkerStyle(28)
    hist_sflat_hB1.SetMarkerColor(kGray+1)
    hist_sflat_vB1.SetMarkerColor(kGray+1)
    hist_sflat.SetMarkerStyle(33)
    hist_sflat.SetMarkerColor(kCyan+1)

    for bin,tct in enumerate(colls):

        hist_round.GetXaxis().SetBinLabel(bin+1,tct)    
        val = normhitsDict[tct][0] + normhitsDict[tct][1]
        hist_round.SetBinContent(bin+1,val)
        hist_round_hB1.SetBinContent(bin+1, normhitsDict[tct][0])
        hist_round_vB1.SetBinContent(bin+1, normhitsDict[tct][1])
        # hist_round.SetBinError(bin+1,1./(nprims[0]+nprims[1]))

        val = normhitsDict[tct][2] + normhitsDict[tct][3]
        hist_flat.SetBinContent(bin+1,val)
        hist_flat_hB1.SetBinContent(bin+1, normhitsDict[tct][2])
        hist_flat_vB1.SetBinContent(bin+1, normhitsDict[tct][3])
        # hist_flat.SetBinError(bin+1,1./(nprims[2]+nprims[3]))

        hist_sround.GetXaxis().SetBinLabel(bin+1,tct)    
        val = normhitsDict[tct][4] + normhitsDict[tct][5]
        hist_sround.SetBinContent(bin+1,val)
        hist_sround_hB1.SetBinContent(bin+1, normhitsDict[tct][4])
        hist_sround_vB1.SetBinContent(bin+1, normhitsDict[tct][5])
        # hist_sround.SetBinError(bin+1,1./(nprims[4]+nprims[5]))
        print val, tct

        val = normhitsDict[tct][6] + normhitsDict[tct][7]
        hist_sflat.SetBinContent(bin+1,val)
        hist_sflat_hB1.SetBinContent(bin+1, normhitsDict[tct][6])
        hist_sflat_vB1.SetBinContent(bin+1, normhitsDict[tct][7])
        # hist_sflat.SetBinError(bin+1,1./(nprims[6]+nprims[7]))


    a,b = 1,1
    cv = TCanvas( 'cv'+hname, 'cv'+hname, 10, 10, a*900, b*600) 
    cv.Divide(a,b)
    cv.SetGridx(1)
    cv.SetGridy(1)
    cv.SetLogy(1)
    hist_round.GetYaxis().SetTitle('loss per primary')
    hist_round.GetYaxis().SetRangeUser(YurMin, YurMax)
    hist_round.Draw('p')
    # hist_round_hB1.Draw('psame')
    # hist_round_vB1.Draw('psame')

    hist_flat.GetYaxis().SetTitle('loss per primary')
    hist_flat.GetYaxis().SetRangeUser(YurMin, YurMax)
    hist_flat.Draw('psame')
    # hist_flat_hB1.Draw('psame')
    # hist_flat_vB1.Draw('psame')
    hist_sround.GetYaxis().SetTitle('loss per primary')
    hist_sround.GetYaxis().SetRangeUser(YurMin, YurMax)
    hist_sround.Draw('p')
    # hist_sround_hB1.Draw('psame')
    # hist_sround_vB1.Draw('psame')
    hist_sflat.Draw('psame')
    # hist_sflat_hB1.Draw('psame')
    # hist_sflat_vB1.Draw('psame')
    hist_round.Draw('psame')
    hist_flat.Draw('psame')
    hist_sround.Draw('psame')
    x1, y1, x2, y2 = 0.63,0.7,0.95,0.93
    thelegend = TLegend( x1, y1, x2, y2)
    thelegend.SetFillColor(0)
    thelegend.SetFillStyle(0)
    thelegend.SetLineColor(0)
    thelegend.SetTextSize(0.03)
    thelegend.SetShadowColor(0)
    thelegend.SetBorderSize(0)
    thelegend.AddEntry(hist_round, 'h+v round beam', "p")
    # thelegend.AddEntry(hist_round_hB1, 'h round beam', "p")
    # thelegend.AddEntry(hist_round_vB1, 'v round beam', "p")
    thelegend.AddEntry(hist_flat, 'h+v flat beam', "p")
    # thelegend.AddEntry(hist_flat_hB1, 'h flat beam', "p")
    # thelegend.AddEntry(hist_flat_vB1, 'v flat beam', "p")
    thelegend.AddEntry(hist_sround, 'h+v sround beam', "p")
    # thelegend.AddEntry(hist_sround_hB1, 'h sround beam', "p")
    # thelegend.AddEntry(hist_sround_vB1, 'v sround beam', "p")
    thelegend.AddEntry(hist_sflat, 'h+v sflat beam', "p")
    # thelegend.AddEntry(hist_sflat_hB1, 'h sflat beam', "p")
    # thelegend.AddEntry(hist_sflat_vB1, 'v sflat beam', "p")
    thelegend.Draw()

    lab = mylabel(60)
    lab.DrawLatex(x1-0.44, y1+0.1, thisIR)

    lab = mylabel(42)
    lab.DrawLatex(x1-0.44, y1+0.16, 'incoming B1    TCT4 + TCT5')

    pname = wwwpath
    pname += 'TCT/HL/relaxedColl/newScatt/fluka/compOptics_'+thisIR+'.pdf'


    cv.SaveAs(pname)

