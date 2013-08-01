#!/usr/bin/python
#
#
# July 2013, rkwee
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

def cv06():


    rfname = "7TeVPostLS1_cold_scan.root"

    if 1:
        p1_cold_loss_start, p1_cold_loss_end  = 20290., 20340.
        p2_cold_loss_start, p2_cold_loss_end  = 20380., 20430.
        
        rf = TFile.Open(rfname)

        for tcs in TCS:

            tag = '_'+ tcs
            cold_loss = rf.Get('cold_loss' + tag)
        
            print "-"*20, tag, "-"*20
 
            p1_bin_start = cold_loss.FindBin(p1_cold_loss_start)
            p1_bin_end   = cold_loss.FindBin(p1_cold_loss_end)
            p1_cold_loss = cold_loss.Integral(p1_bin_start,p1_bin_end)/(p1_bin_end - p1_bin_start)

            print p1_bin_start, p1_bin_end, p1_cold_loss
            cl_rebinned = cold_loss.Clone('rebinnedVersion'+tag)

            rbf = 10
            cl_rebinned.Rebin(rbf)
            cl_rebinned.Scale(1./rbf)

            p1_bin_start = cl_rebinned.FindBin(p1_cold_loss_start)
            p1_bin_end   = cl_rebinned.FindBin(p1_cold_loss_end)
            p1_cold_loss = cl_rebinned.Integral(p1_bin_start,p1_bin_end)/(p1_bin_end - p1_bin_start)

            print p1_bin_start, p1_bin_end, p1_cold_loss

