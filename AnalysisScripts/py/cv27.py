#!/usr/bin/python
#
# R Kwee-Hinzmann, Nov 2014
# ---------------------------------------------------------------------------------
import ROOT, sys, glob, os, math, helpers
from ROOT import *
from helpers import *
from array import array
# ---------------------------------------------------------------------------------
def cv27():
    # histname+entrie
    #gStyle.SetOptStat(0111)
    # name, entries
    gStyle.SetOptStat(1111)
    # only entries!
    #gStyle.SetOptStat(10)
    gStyle.SetPalette(1)
    gStyle.SetStatX(0.90)
    gStyle.SetStatY(0.95)
    gStyle.SetTitleX(0.1)
    gStyle.SetTitleY(.955)

    showInfo = 1
    debug = 1


    # h5 with fix
    pathtofile = '/afs/cern.ch/work/r/rkwee/HL-LHC/runs/testHDF5_1Pack/run_test_3/'
    rootfile_hdf5  = pathtofile + 'incr10k_dbg/tracks2.h5-to-dat.rawlist.root'
    rootfile_ascii = pathtofile + 'ascii/tracks2.dat.root'        

    rf_ascii = TFile.Open(rootfile_ascii)
    rf_hdf5  = TFile.Open(rootfile_hdf5)
    mt_ascii = rf_ascii.Get('particle')
    mt_hdf5 = rf_hdf5.Get('particle')

    # plot all columns
    mt_hdf5.Scan(0)
    # use root directly
   #tree->SetScanField(0);
   #tree->Scan("*"); >tree.log
   #  will create a file tree.log
# see https://root.cern.ch/root/html/TTreePlayer.html#TTreePlayer:Scan
