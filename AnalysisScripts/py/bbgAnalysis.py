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
    gROOT.LoadMacro(gitpath + "AnalysisScripts/C/AtlasStyle.C")
    gROOT.LoadMacro(gitpath + "AnalysisScripts/C/AtlasUtils.C")
    SetAtlasStyle()

    # ---------------------
    #TTreeFileName = createTTree.ctree(datafile)

    #TTreeFileName = 'data/4TeV/ir1_4TeV_settings_from_TWISS_b2_nprim7825000_66.root'        
    # TTreeFileName = 'data/4TeV/ir1_4TeV_settings_from_TWISS_20MeV_b2_nprim5356000_66.root'
    # TTreeFileName = 'data/4TeV/ir1_4TeV_settings_from_TWISS_20GeV_b2_nprim158890000_66.root'
    #TTreeFileName = 'data/4TeV/ir1_4TeV_settings_from_TWISS_20MeV_b1_nprim7964000_66.root'
    #TTreeFileName = workpath + 'runs/FL_TCT5IN_roundthin/hilumi_ir1_hybrid_b1_20MeV_exp_nprim1635000_30.root'
    TTreeFileName = workpath + 'runs/FL_TCT5IN_roundthinB1_2nd/hilumi_ir1_hybrid_b1_exp_20MeV_nprim3000_30.root'
    TTreeFileName = workpath + 'runs/FL_TCT5LOUT_roundthinB1_2nd/hilumi_ir1_hybrid_b1_exp_20MeV_nprim10000_30.root'

    # ---------------------
    # define tag in helpers!
    # tag = tag_BH_4TeV
    #fillTTree.fillHistos(TTreeFileName, tag)
    tag = tag_BH_7TeV
    #fillTTree.fillHistos(TTreeFileName, tag)

    plotSpectra.plotSpectra(TTreeFileName, tag)
