#!/usr/bin/python
#
# R Kwee-Hinzmann, 2013
# ---------------------------------------------------------------------------------
import ROOT, sys, glob, os, math, helpers
from ROOT import *
from helpers import *
from array import array
# ---------------------------------------------------------------------------------
import optparse
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-f", "--file", dest="filename", type="string",
                  help="put the path of the merged fort.66 file from fluka runs")

parser.add_option("-c", dest="doCreate", type="int",
                  help="0 or 1 for creating a rootfile or not.")

(options, args) = parser.parse_args()

fname  = options.filename
doCreate = options.doCreate
#######################################################################################
    # FORMAT RODERIK (input to fluka)
    # 1 X_start (cm) : starting position of primary particle
    # 2 Y_start (cm)
    # 3 Z_start (cm)
    # 4 XP (mrad)
    # 5 XP (mrad)
    # 6 t_start (s) : starting time of primary particle where t=0 is at the entrance of the TCTH
#######################################################################################
    # FORMAT impacts_real (for new routine)
    # 1 icoll
    # 2 c_rot
    # 3 s
    # 4 x
    # 5 xp [mrad]
    # 6 y
    # 7 yp [mrad]
    # 8 nabs
    # 9 np
    # 10 ntu
#######################################################################################
# setting variables

debug        = 1
treeName     = "particle"
sourceformatR = "x/F:y/F:z/F:xp/F:yp/F:t/F"
sourceformatA = "icoll/I:c_rot/F:s/F:x/F:xp/F:y/F:yp/F:nabs/F:np/F:ntu/F"

sourceformat  = sourceformatA
# ---------------------------------------------------------------------------------
rfoutName = fname.split('.')[0] + ".root"
subfolder = 'TCT/HL/'
# ---------------------------------------------------------------------------------
def createTTree(fname):
  print "writing ", rfoutName

  mytree = TTree(treeName,treeName)
  mytree.ReadFile(fname,sourceformat)
  mytree.SaveAs(rfoutName)
# ---------------------------------------------------------------------------------
def plotSpectra(fname):

    rf = TFile(fname + '.root')
    mt = rf.Get(treeName)

    hname = 'yp'

    cv = TCanvas( 'cv'+hname, 'cv'+hname, 1200, 900)

    nbins, xmin, xmax = 200, -0.5, 0.5

    hist = TH1F(hname, hname, nbins, xmin, xmax)

    var = hname 
    cut = ''

    mt.Project(hname,var,cut)

    pname = wwwpath + subfolder + hname + '_HL_TCT'

    print('Saving file as' + pname ) 
    cv.Print(pname + '.pdf')
    # cv.Print(pname + '.png')
      
# ---------------------------------------------------------------------------------
if __name__ == "__main__":

    gROOT.SetBatch()
    gROOT.SetStyle("Plain")
    gROOT.LoadMacro("/afs/cern.ch/user/r/rkwee/scratch0/miScripts/py/AtlasStyle.C")
    gROOT.LoadMacro("/afs/cern.ch/user/r/rkwee/scratch0/miScripts/py/AtlasUtils.C")
    SetAtlasStyle()

    if doCreate:  createTTree(fname)
    plotSpectra(fname)
