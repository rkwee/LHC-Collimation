#!/usr/bin/python
#
# Feb, 2014, rkwee
# -----------------------------------------------------------------------------------
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-f", dest="datafile", type="string",
                  help="put data file in text format with beam specification and energy in name")

(options, args) = parser.parse_args()

datafile = options.datafile
## -----------------------------------------------------------------------------------
import ROOT, sys, glob, os
from ROOT import *
import helpers
from helpers import *
import createTTree, fillTTree, plotSpectra
## -----------------------------------------------------------------------------------
if __name__ == "__main__":
    gROOT.SetBatch()
    gROOT.Reset()
    gROOT.SetStyle("Plain")
    gROOT.LoadMacro(gitpath + "C/AtlasStyle.C")
    gROOT.LoadMacro(gitpath + "C/AtlasUtils.C")
    SetAtlasStyle()

    # ---------------------
    #TTreeFileName = createTTree.ctree(datafile)

    TTreeFileName = 'data/4TeV/ir1_4TeV_settings_from_TWISS_b2_nprim7825000_66.root'
    #TTreeFileName = 'data/4TeV/ir1_4TeV_settings_from_TWISS_b2_nprim4976000_66.root'
    tag = '_BH_4TeV_B2' 

    TTreeFileName = 'data/4TeV/ir1_4TeV_settings_from_TWISS_20MeV_b1_nprim6971000_66.root'
    tag = '_BH_4TeV_B1' 


    fillTTree.fillHistos(TTreeFileName, tag)
    # ---------------------

    plotSpectra.plotSpectra(TTreeFileName, tag)
