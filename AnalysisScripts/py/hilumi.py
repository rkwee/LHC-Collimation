#!/usr/bin/python
#
# May, 2013. rkwee
# -----------------------------------------------------------------------------------
from optparse import OptionParser

parser = OptionParser()
# parser.add_option("-r", dest="release", type="string",
#                   help="put any string name")
parser.add_option("-c", dest="cvNumber", type="string",
                  help="put number to run cv function")

(options, args) = parser.parse_args()

cvNumber = options.cvNumber
print "collimation "
## -----------------------------------------------------------------------------------
import ROOT, sys, glob, os
from ROOT import *
from helpers import *
## -----------------------------------------------------------------------------------
moduleName = __import__(cvNumber)
## -----------------------------------------------------------------------------------

if __name__ == "__main__":
    gROOT.SetBatch()
    gROOT.Reset()
    gROOT.SetStyle("Plain")
    gROOT.LoadMacro(gitpath + "C/AtlasStyle.C")
    gROOT.LoadMacro(gitpath + "C/AtlasUtils.C")
    SetAtlasStyle()

    #gStyle.SetOptStat(1000100110)
    gStyle.SetPalette(1)
    gStyle.SetStatX(0.95)
    gStyle.SetStatY(0.95)
    gStyle.SetTitleX(0.1)
    gStyle.SetTitleY(.955)

    gStyle.SetOptStat(0)
    #gStyle.SetCanvasColor(10)
    # gStyle.SetPalette(100,prepPalette())
 
    exec "moduleName.%s()" %cvNumber
  
    print '--- fin ---'
# # ---------------------

