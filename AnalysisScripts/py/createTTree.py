#!/usr/bin/python
#
# R Kwee-Hinzmann, 2013
# ---------------------------------------------------------------------------------
import ROOT, sys, glob, os, math, helpers, createTTree_dict
from ROOT import *
from helpers import *
from array import array
from createTTree_dict import *
# ---------------------------------------------------------------------------------
import optparse
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-f", "--file", dest="filename", type="string",
                  help="put the path of the merged fort.66 or fort.30 file from fluka runs")

(options, args) = parser.parse_args()

fname  = options.filename
# setting variables for doCreate:
# ---------------------------------------------------------------------------------
debug        = 1
# plotting from several rootfiles of the same format!!:
treeName     = "particle"
fortformat66 = "event/I:generation/I:particle/I:energy_ke/F:weight/F:x/F:y/F:xp/F:yp/F:age/F:energy_tot/F:x_interact/F:y_interact/F:z_interact/F:t_interact/F"
fortformat30 = "event/I:particle/I:generation/I:weight/F:x/F:y/F:xp/F:yp/F:energy_tot/F:energy_ke/F:age/F:x_interact/F:y_interact/F:z_interact/F"

if fname.endswith("30"): 
    fortformat = fortformat30
    varList = varList_HL
    if debug: print "Using HL format", '.'*10
else: 
    fortformat = fortformat66
    varList = varList_4TeV
    if debug: print "Using 4 TeV format", '.'*10
# ---------------------------------------------------------------------------------
zmin, zmax = 2260., 14960.

if not os.path.exists(wwwpath + subfolder):
    print 'making dir', wwwpath + subfolder
    os.mkdir(wwwpath + subfolder)
# ---------------------------------------------------------------------------------
def createTTree(fname):
    rfoutName = fname +".root"
    print "writing ", rfoutName

    mytree = TTree(treeName,treeName)
    mytree.ReadFile(fname,fortformat)
    mytree.SaveAs(rfoutName)
  
# ---------------------------------------------------------------------------------
if __name__ == "__main__":

    gROOT.SetBatch()
    gROOT.SetStyle("Plain")
    gROOT.LoadMacro(gitpath + "C/AtlasStyle.C")
    gROOT.LoadMacro(gitpath + "C/AtlasUtils.C")
    SetAtlasStyle()

    createTTree(fname)
