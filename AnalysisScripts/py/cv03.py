#!/usr/bin/python
#
# May 2013, rkwee
## -------------------------------------------------------------------------------
import ROOT, sys, glob, os
from ROOT import *
import lossmap
import helpers
from helpers import wwwpath
## -------------------------------------------------------------------------------

TCS = [
    'nominal',
    'TCSG.A6L7.B1',     
    'TCSG.B5L7.B1',     
    'TCSG.A5L7.B1',     
    'TCSG.D4L7.B1',     
    'TCSG.B4L7.B1',
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
        q8, q10 = 0., 0.
        Q8_losses, Q10_losses = [],[]

        maxval = -1.;
        minval = 10.;

        for tcs in TCS:

            tag = '_'+ tcs
            cold_loss = rf.Get('cold_loss' + tag)
            print "-"*20, tag, "-"*20
            #p1_cold_loss
            p1_bin_start = cold_loss.FindBin(p1_cold_loss_start)
            p1_bin_end   = cold_loss.FindBin(p1_cold_loss_end)
            p1_cold_loss = cold_loss.Integral(p1_bin_start,p1_bin_end)/(p1_bin_end - p1_bin_start)

            for i in range(p1_bin_start, p1_bin_end+1):
                q8 += cold_loss.GetBinContent(i)

            p2_bin_start = cold_loss.FindBin(p2_cold_loss_start)
            p2_bin_end   = cold_loss.FindBin(p2_cold_loss_end)
            p2_cold_loss = cold_loss.Integral(p2_bin_start,p2_bin_end)/(p2_bin_end - p2_bin_start)

            for i in range(p2_bin_start, p2_bin_end+1):
               q10 += cold_loss.GetBinContent(i)

            #print "cold loss at Q8:", p1_cold_loss, q8/(p1_bin_end - p1_bin_start)
            #print "cold loss at Q10:", p2_cold_loss, q10/(p2_bin_end - p2_bin_start)

            q8, q10 = 0., 0.

            Q8_losses  += [(tcs, p1_cold_loss)]
            Q10_losses += [(tcs, p2_cold_loss)]

            if p1_cold_loss > maxval:
                maxval = p1_cold_loss

            if p2_cold_loss > maxval:
                maxval = p2_cold_loss

            if p1_cold_loss < minval:
                minval = p1_cold_loss 

            if p2_cold_loss < minval:
                minval = p2_cold_loss 

        # plot the benchmark plots
        bmPlot(Q8_losses,Q10_losses,'comp',maxval,minval)

def bmPlot(Q8_losses,Q10_losses,rel,maxval,minval):

    nbins = len(Q8_losses)
    hname = rel

    cv = TCanvas( 'cv' + hname, 'cv' + hname, 800, 600)
    cv.SetLeftMargin(0.15)
    cv.SetRightMargin(0.15)
    cv.SetTopMargin(0.15)

    hist1 = TH1F(hname, hname, nbins, 1, nbins+1)
    hist1.GetYaxis().SetRangeUser(minval*.95, maxval*1.13)
    hist1.SetMarkerStyle(22)
    hist1.SetMarkerColor(kMagenta-3)
    hist1.GetYaxis().SetTitle('Cleaning Inefficiency #eta')
    hist2 = TH1F(hname+'d', hname+'d', nbins, 1, nbins+1)
    hist2.SetMarkerStyle(23)
    hist2.SetMarkerColor(kGreen-3)

    cnt = 0

    for tcs,val in Q8_losses:
        cnt +=1 
        hist1.GetXaxis().SetBinLabel(cnt, tcs)
        hist1.SetBinContent(cnt, val)

    cnt = 0

    for tcs,val in Q10_losses:
        cnt +=1 
        hist2.SetBinContent(cnt, val)

    hist1.Draw('P')
    hist2.Draw('PSAME')

    # x1, y1, x2, y2a
    thelegend = TLegend(0.18, 0.6, 0.42, 0.7) 
    thelegend.SetFillColor(0)
    thelegend.SetLineColor(0)
    thelegend.SetTextSize(0.035)
    thelegend.SetShadowColor(10)
    thelegend.AddEntry(hist1,'at Q8', "P")
    thelegend.AddEntry(hist2,'at Q10', "P")
    thelegend.Draw()

    pname  = wwwpath
    pname += 'scan/'+hname+'losses.png'

    cv.SaveAs(pname)
