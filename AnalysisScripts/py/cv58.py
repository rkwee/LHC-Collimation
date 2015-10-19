#!/usr/bin/python
#
# June 2015, rkwee
## -------------------------------------------------------------------------------
import ROOT 
import numpy as np
from ROOT import *
import helpers
import array 
from array import array 
from helpers import wwwpath, length_LHC, mylabel, makeTGraph
# from cv54, cv57
# -----------------------------------------------------------------------------------
def cv58():

    formatTRKFILE = [ ("X", np.float), 
                      ("Y", np.float), 
                      ("Z", np.float), 
                      ("TXX", np.float), 
                      ("TYY", np.float), 
                      ("TZZ", np.float), 
                      ("CTRACK", np.float), 
                      ("CMTRACK", np.float), 
                      ("ATRACK", np.float),
                      ]

    formatfort89 = [ ("CXTRCK", np.float),
                     ("CYTRCK", np.float),
                     ("CZTRCK", np.float),
                     ("XTRACK", np.float),
                     ("YTRACK", np.float),
                     ("ZTRACK", np.float),
                     ("JTRACK", np.int),
                     ("NCASE",  np.int),
                     ("ATRACK", np.float),
                     ]

    fname = "ir1_6500GeV_b1_20MeV_orbitDumpINICON001_fort.89"
    fname = "inicon1/createTrajectories/run_00001/ir1_6500GeV_b1_20MeV_orbitDumpINICON001_fort.89"
    #fname = "ir1_6500GeV_b1_20MeV_orbitDump001_TRAKFILE"

    format, xvar, yvar = formatfort89, "ZTRACK", "YTRACK"

    fileDType = np.dtype(format)
    fdata = np.loadtxt(fname,dtype=fileDType)

    # keep order
    xList = fdata[xvar].tolist()
    yList = fdata[yvar].tolist()
    color = kRed
    mStyle = 6
    gr = makeTGraph(xList, yList, color, mStyle)

    hname = "trajectory"
    a,b = 1,1
    cv = TCanvas( 'cv'+hname, 'cv'+hname, 10, 10, a*900, b*600) 
    cv.Divide(a,b)

    gr.Draw('ap')
    pname = "~/public/www/HL-LHC/TCT/6.5TeV/beamgas/plt.png"

    cv.SaveAs(pname)



# ----------------------------------------------------------------------------





