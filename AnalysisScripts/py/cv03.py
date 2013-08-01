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
import math, gzip
## -------------------------------------------------------------------------------

TCS = [

('nominal_B1',  12016858),
('TCSG.4R6.B1',  5979551),
('TCSG.6R7.B1',  6018721),
('TCSG.A4L7.B1',  6800715),
('TCSG.A4R7.B1',  6497420),
('TCSG.A5L7.B1',  6044670),
('TCSG.A6L7.B1',  4488443),
('TCSG.B4L7.B1',  5982305),
('TCSG.B5L7.B1',  6037577),
('TCSG.B5R7.B1',  6052281),
('TCSG.D4L7.B1',  6019343),
('TCSG.D5R7.B1',  6051532),
('TCSG.E5R7.B1',  6010177),
# ('TCSG.4L6.B2',  1657957),
# ('TCSG.6L7.B2',  6273317),
# ('TCSG.A4L7.B2',  6273328),
# ('TCSG.A4R7.B2',  6273353),
# ('TCSG.A5R7.B2',  6240904),
# ('TCSG.A6R7.B2',  5313129),
# ('TCSG.B4R7.B2',  6241294),
# ('TCSG.B5L7.B2',  3367086),
# ('TCSG.B5R7.B2',  6273317),
# ('TCSG.D4R7.B2',  5460328),
# ('TCSG.D5L7.B2',  6260530),
# ('TCSG.E5L7.B2',  6266897),
#('nominal_B2',  6260540),

    ]               

    
def cv03():

    debug        = 0
    doWriteRFile = 1
    doAvLoss     = 1

    rfname = "7TeVPostLS1_scan_B1.root"
#    rfname = "7TeVPostLS1_DEBUG_scan.root"

    if doWriteRFile:
        print "Writing " + rfname

        # create a root file
        rf = TFile(rfname, 'recreate')
        
        for tcs,norm in TCS:
            
            tag      = '_' + tcs
            thispath = '/afs/cern.ch/work/r/rkwee/HL-LHC/runs/7TeVPostLS1' + tag + '/'

            doZoom   = 0
            doPrint  = 1
            h_tot_loss, h_cold, h_warm =  lossmap.lossmap(thispath,tag,doZoom,doPrint) 
            h_tot_loss.Write()
            h_cold.Write()
            h_warm.Write()            

            doZoom   = 1
            doPrint  = 0
            lossmap.lossmap(thispath,tag,doZoom,doPrint) 
            
        rf.Close()

    if doAvLoss:
        print "Calculating losses at Q8 and Q10"

        p1_cold_loss_start, p1_cold_loss_end  = 20290., 20340.
        p2_cold_loss_start, p2_cold_loss_end  = 20380., 20430.

        print "Opening ", rfname
        rf = TFile.Open(rfname)
        max_cold_losses, Q8_losses, Q10_losses = [],[],[]

        # for better visibility 
        scaleFactor = 10.

        for tcs,norm in TCS:

            tag  = '_'+ tcs
            cold_loss = rf.Get('cold_loss' + tag)
            print "-"*20, tcs, "-"*20

            # -- the number of lines in FirstImpact-1 (for header) is the total number of particles hitting a collimator
            # f4   = '/afs/cern.ch/work/r/rkwee/HL-LHC/runs/7TeVPostLS1' + tag + '/FirstImpacts' + tag + '.dat.gz'
            # -- takes ages, do only once for check
            #norm = file_len(f4)-1

            #print '('+tcs+', ' + str(norm) + ')'
            #norm = 1.

            p1_bin_start = cold_loss.FindBin(p1_cold_loss_start)
            p1_bin_end   = cold_loss.FindBin(p1_cold_loss_end)
            p1_cold_loss = cold_loss.Integral(p1_bin_start,p1_bin_end)/(p1_bin_end - p1_bin_start)

            p2_bin_start = cold_loss.FindBin(p2_cold_loss_start)
            p2_bin_end   = cold_loss.FindBin(p2_cold_loss_end)
            p2_cold_loss = cold_loss.Integral(p2_bin_start,p2_bin_end)/(p2_bin_end - p2_bin_start)

            # statistical uncertainty
            p1_stat, p2_stat = 0.,0.

            if debug:
                print('Q8: averaging from bin ' + str(p1_bin_start) + ' to bin ' + str(p1_bin_end))

            for i in range(p1_bin_start, p1_bin_end+1):
                p1_err   = cold_loss.GetBinError(i)
                p1_stat += math.pow(p1_err,2)

                if debug:
                    print tcs, ' Q8: N_'+str(i)+' =',p1_err, ', bin error = ', cold_loss.GetBinError(i), ', norm =', norm

            if debug:
                print tcs, 'val = ', p1_cold_loss, ' +- ', math.sqrt(p1_stat/norm)


            for i in range(p2_bin_start, p2_bin_end+1):
                p2_err   = cold_loss.GetBinError(i)
                p2_stat += math.pow(p2_err,2)


            Q8_losses  += [(tcs, p1_cold_loss, math.sqrt(p1_stat/norm))]
            Q10_losses += [(tcs, p2_cold_loss, math.sqrt(p2_stat/norm))]
            max_cold_losses += [( cold_loss.GetMaximum()/scaleFactor, cold_loss.GetBinError(cold_loss.GetMaximumBin())/scaleFactor )]

            print(tcs + 'bin error max loss =' + str(cold_loss.GetBinError(cold_loss.GetMaximumBin())))


        # plot the benchmark plots
        bmPlot(Q8_losses,Q10_losses,max_cold_losses,'comp')


def bmPlot(Q8_losses,Q10_losses,max_cold_losses,hname):

    nbins = len(Q8_losses)

    cv = TCanvas( 'cv' + hname, 'cv' + hname, 1200, 800)
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

    for val,err in max_cold_losses:
        cnt +=1 
        hist3.SetBinContent(cnt, val)
        #hist3.SetBinError(cnt, err)
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

    cv.Print(pname)
