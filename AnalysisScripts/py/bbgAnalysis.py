
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
    # TTreeFileName = 'data/4TeV/ir1_BH_4TeV_settings_from_TWISS_20MeV_b1_nprim7964000_66.root'

    # TTreeFileName = workpath + 'runs/4TeV_Halo/ir1_BH_4TeV_settings_from_TWISS_20MeV_b1_nprim7964000_66.root'
    #TTreeFileName = workpath + 'runs/FL_TCT5IN_roundthin/hilumi_ir1_hybrid_b1_20MeV_exp_nprim1635000_30.root'
    # TTreeFileName = workpath + 'runs/FL_TCT5IN_roundthinB1_2nd/hilumi_ir1_hybrid_b1_exp_20MeV_nprim5319000_30.root'
    # TTreeFileName = workpath + 'runs/FL_TCT5LOUT_roundthinB1_2nd/hilumi_ir1_hybrid_b1_exp_20MeV_nprim5350000_30.root'    
    
    # TTreeFileName = workpath + 'runs/FL_TCT5IN_roundthin_B2/hilumi_ir1_hybrid_b2_exp_20MeV_nprim5315000_30.root'
    # TTreeFileName = workpath + 'runs/FL_TCT5LOUT_roundthin_B2/hilumi_ir1_hybrid_b2_exp_20MeV_nprim5001000_30.root'

    #TTreeFileName = workpath + 'runs/FL_6500GeV_HaloB1_20MeV/ir1_6500GeV_b1_20MeV_nprim4752000_30.root'
    #TTreeFileName = '/afs/cern.ch/project/lhc_mib/tct_simulations/FlukaRuns/runs/hilumi_ir1b1_exp_20MeV_nominalCollSett_nprim1291000_30.root'
    #TTreeFileName = workpath + 'runs/FL_6500GeV_HaloB2_20MeV/ir1_6500GeV_b2_20MeV_nprim3646000_30.root'
    #TTreeFileName = 'runBG_UVcorr/ir1_BG_4TeV_settings_from_TWISS_20MeV_b1_nprim4414500_67.root'
    #TTreeFileName = "/afs/cern.ch/project/lhc_mib/bbgen/4TeV/beamgas/withoutBeamSize/beam-gas_4TeV-IR1_to_arc_20MeV_cutoff_nprim28788000_66.root"
    #TTreeFileName = "/afs/cern.ch/project/lhc_mib/beamgas/6500GeV_beamsize/runs400/ir1_BG_bs_6500GeV_b1_20MeV_nprim2314800_67.root"
    #TTreeFileName = "/afs/cern.ch/project/lhc_mib/beamgas/6500GeV_beamsize/runs10k_20GeV/ir1_BG_bs_6500GeV_b1_20GeV_nprim127560000_67.root"
    TTreeFileName = "/afs/cern.ch/project/lhc_mib/tct_simulations/FlukaRuns/runs_modTAN/hilumi_ir1b1_exp_20MeV_nominalCollSett_modTAN_nprim1390500_30.root"
    # for comparisons plot change in plotSpectra
    # ---------------------
    # define tag in helpers!
    tag = tag_BG_4TeV
    tag = '_crabcfb1_modTAN'
    #tag = tag_BG_6p5TeV
    # tag = tag_BH_7TeV
    doComp = 0
    fillTTree.fillHistos(TTreeFileName, tag, doComp)
    plotSpectra.plotSpectra(TTreeFileName, tag, doComp)
