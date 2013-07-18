#!/usr/bin/python
#
# if doWriteRFile = 1
#    writes out root file 
#    plots lossmap for every tcs
# if doAvLoss = 1
#    uses rootfile 
#    plots losses at Q8 and Q10 
# 
#
# May 2013, rkwee
## -------------------------------------------------------------------------------
import ROOT, sys, glob, os
from ROOT import *
import lossmap
import helpers
from helpers import wwwpath, file_len
import math
## -------------------------------------------------------------------------------

TCS = [
    'nominal',
    'TCSG.A6L7.B1',     
    'TCSG.B5L7.B1',     
    'TCSG.A5L7.B1',     
    'TCSG.D4L7.B1',     
    'TCSG.B4L7.B1',
    ]

# same order as TCS, not used as it is negligable, use once for check
NORM = [
    6009748,    
    4488443,    
    6006612,    
    5958153,
    5796669,    
    5828267,
    ]

    
def cv03():

    doWriteRFile = 0
    doAvLoss     = 1

    rfname = "7TeVPostLS1_scan.root"

    if doWriteRFile:
        print "Writing " + rfname

        # create a root file
        rf = TFile(rfname, 'recreate')
        
        for tcs in TCS:
            
            tag      = '_' + tcs
            thispath = '/afs/cern.ch/work/r/rkwee/HL-LHC/runs/7TeVPostLS1' + tag + '/'
            doZoom   = 0
            
            h_tot_loss, h_cold, h_warm =  lossmap.lossmap(thispath,tag,doZoom) 
            h_tot_loss.Write()
            h_cold.Write()
            h_warm.Write()            

            doZoom   = 1
            lossmap.lossmap(thispath,tag,doZoom) 
            
        rf.Close()

    if doAvLoss:
        print "Calculating losses at Q8 and Q10"

        p1_cold_loss_start, p1_cold_loss_end  = 20290., 20340.
        p2_cold_loss_start, p2_cold_loss_end  = 20380., 20430.

        rf = TFile.Open(rfname)
        max_cold_losses, Q8_losses, Q10_losses = [],[],[]

        # for better visibility 
        scaleFactor = 10.

        for tcs in TCS:

            tag  = '_'+ tcs
            cold_loss = rf.Get('cold_loss' + tag)
            print "-"*20, tcs, "-"*20

            # -- the number of lines in FirstImpact-1 (for header) is the total number of particles hitting a collimator
            f4   = '/afs/cern.ch/work/r/rkwee/HL-LHC/runs/7TeVPostLS1' + tag + '/FirstImpacts' + tag + '.dat'           
            # -- takes ages, do only once for check
            # norm = file_len(f4)-1

            # print 'norm =', norm
            norm = 1.

            p1_bin_start = cold_loss.FindBin(p1_cold_loss_start)
            p1_bin_end   = cold_loss.FindBin(p1_cold_loss_end)
            p1_cold_loss = cold_loss.Integral(p1_bin_start,p1_bin_end)/(p1_bin_end - p1_bin_start)

            p2_bin_start = cold_loss.FindBin(p2_cold_loss_start)
            p2_bin_end   = cold_loss.FindBin(p2_cold_loss_end)
            p2_cold_loss = cold_loss.Integral(p2_bin_start,p2_bin_end)/(p2_bin_end - p2_bin_start)


            # statistical uncertainty
            p1_stat, p2_stat = 0.,0.

            for i in range(p1_bin_start, p1_bin_end+1):
                p1_err   = cold_loss.GetBinError(i)/norm
                p1_stat += math.pow(p1_err,2)

            for i in range(p2_bin_start, p2_bin_end+1):
                p2_err   = cold_loss.GetBinError(i)/norm                
                p2_stat += math.pow(p2_err,2)

            Q8_losses  += [(tcs, p1_cold_loss, math.sqrt(p1_stat))]
            Q10_losses += [(tcs, p2_cold_loss, math.sqrt(p2_stat))]
            max_cold_losses += [cold_loss.GetMaximum()/scaleFactor]

        # plot the benchmark plots
        bmPlot(Q8_losses,Q10_losses,max_cold_losses,'comp')


def bmPlot(Q8_losses,Q10_losses,max_cold_losses,rel):

    nbins = len(Q8_losses)
    hname = rel

    cv = TCanvas( 'cv' + hname, 'cv' + hname, 800, 600)
    cv.SetLeftMargin(0.15)
    cv.SetRightMargin(0.15)
    cv.SetTopMargin(0.15)

    hist1 = TH1F(hname, hname, nbins, 1, nbins+1)
    hist1.SetMarkerStyle(22)
    hist1.SetMarkerColor(kMagenta-3)
    hist1.SetLineColor(kMagenta-3)
    hist1.GetYaxis().SetTitle('Cleaning Inefficiency #eta')

    hist2 = TH1F(hname+'d', hname+'d', nbins, 1, nbins+1)
    hist2.SetMarkerStyle(23)
    hist2.SetMarkerColor(kGreen-3)
    hist2.SetLineColor(kGreen-3)

    hist3 = TH1F(hname+'m', hname+'m', nbins, 1, nbins+1)
    hist3.SetMarkerStyle(20)
    hist3.SetMarkerColor(kAzure-3)
    hist3.SetLineColor(kAzure-3)

    vals = []

    cnt = 0

    for tcs,val,err in Q8_losses:
        cnt +=1 
        hist1.GetXaxis().SetBinLabel(cnt, tcs)
        hist1.SetBinContent(cnt, val)
        #hist1.SetBinError(cnt, err)
        vals += [val]

    cnt = 0

    for tcs,val,err in Q10_losses:
        cnt +=1 
        hist2.SetBinContent(cnt, val)
        #hist2.SetBinError(cnt, err)
        vals += [val]

    cnt = 0

    for val in max_cold_losses:
        cnt +=1 
        hist3.SetBinContent(cnt, val)
        vals += [val]

    minval = min(vals)
    maxval = max(vals)

    hist1.GetYaxis().SetRangeUser(minval*.95, maxval*1.13)
    hist1.Draw('P')
    hist2.Draw('PSAME')
    hist3.Draw('PSAME')

    # x1, y1, x2, y2a
    thelegend = TLegend(0.16, 0.7, 0.42, 0.82) 
    thelegend.SetFillColor(0)
    thelegend.SetLineColor(0)
    thelegend.SetTextSize(0.035)
    thelegend.SetShadowColor(10)
    thelegend.AddEntry(hist1,'at Q8', "P")
    thelegend.AddEntry(hist2,'at Q10', "P")
    thelegend.AddEntry(hist3,'10% of maximum cold loss', "P")
    thelegend.Draw()

    pname  = wwwpath
    pname += 'scan/'+hname+'losses.png'

    cv.SaveAs(pname)
