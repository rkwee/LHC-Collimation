#!/usr/bin/python
#
# Oct 2015, rkwee
## -------------------------------------------------------------------------------
# re-use this to dump -8 particles 
## -------------------------------------------------------------------------------
import ROOT, helpers
from ROOT import *

# -----------------------------------------------------------------------------------

def cv49():

    bbgFile = helpers.projectpath + "BG/FL_4TeV_BG_20GeV_10k/ir1_BG_bs_4TeV_settings_from_TWISS_20GeV_b1_nprim167850000_67.root"

    bbgFile = helpers.projectpath + "bbgen/4TeV/beam-gas_4TeV-IR1_to_arc_20MeV_cutoff_nprim28788000.root"

    bbgFile = helpers.projectpath + "bbgen/4TeV/beamgas/ir1_BG_bs_4TeV_settings_from_TWISS_20MeV_b1_nprim5925000_67.root"

    print "reading.....", bbgFile

    rf = TFile.Open(bbgFile)
    mt = rf.Get("particle")

    hname = "minusAcht"
    nbins, xmin, xmax = 10, -9.5, 0.5
    hist  = TH1F(hname, hname, nbins, xmin, xmax )

    var = "particle"
    cut = " particle == -8"
    mt.Project(hname, var, cut)
    print hname, "has", hist.GetEntries(), " entries."

