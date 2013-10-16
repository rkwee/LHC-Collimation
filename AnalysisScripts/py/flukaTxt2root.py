#!/usr/bin/python
#
# R Kwee-Hinzmann, 2013
# -----------------------------------------------------------------------------------------------------------------------

import optparse
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-f", "--file", dest="filename", type="string",
                  help="put the path of the merged fort.66 file from fluka runs")

(options, args) = parser.parse_args()

fname = options.filename
# ---------------------------------------------------------------------------------
import ROOT, sys, glob, os, math
from ROOT import *
from array import array
# ---------------------------------------------------------------------------------
#######################################################################################
    # http://bbgen.web.cern.ch/bbgen/bruce/fluka_beam_gas_arc_4TeV/flukaIR15.html
    # 1  FLUKA run number (between 1 and 3000)
    # 2  ID of primary particle (between 1 and 60 000 in each run)
    # 3  FLUKA particle type (an explanation of the numbers can be found here)
    # 4  kinetic energy (GeV)
    # 5  statistical weight (should be 1 for all particles)
    # 6  X (cm)
    # 7  Y (cm)
    # 8  directional cosine w.r.t X-axis
    # 9  directional cosine w.r.t Y-axis
    # 10 time (s) since start of primary particle
    # 11 total energy (GeV)
    # 12 X_start (cm) : starting position of primary particle
    # 13 Y_start (cm)
    # 14 Z_start (cm)
    # 15 t_start (s) : starting time of primary particle where t=0 is at the entrance of the TCTH
#######################################################################################
def getColContent(colNumber):

    print 'processing........................', fname

    col = []
    with open(fname) as myfile:

        for line in myfile:       

            col += [float(line.split()[colNumber])]


    return array('d', col)
# ---------------------------------------------------------------------------------
def do1DHisto(hname, colNumber, xaxis):

    col  = getColContent(colNumber) 

    hist1 = TH1F(hname, hname, len(xaxis)-1, array('d', xaxis) )

    for colVal in col: 
        hist1.Fill(colVal)

    return hist1
# ---------------------------------------------------------------------------------
def saveRootFile():

    rfoutname = 'test.root'

    print 'writing ', rfoutname
    rfile = TFile.Open(rfoutname, "RECREATE")

    hname, colNumber, nbins, xmin, xmax = "Ekin", 3, 100, 1e-3, 1e6

    # exponent width
    width = 1./nbins*(math.log10(xmax) - math.log10(xmin))

    # axis with exponents only 
    xtmp  = [math.log10(xmin) + i * width for i in range(nbins+1)]

    # real axis in power of 10
    xaxis = [math.pow(10, xExp) for xExp in xtmp]

    hist  = do1DHisto(hname, colNumber, xaxis) 

    hist.Write()

    rfile.Close()
# ---------------------------------------------------------------------------------
if __name__ == "__main__":

    saveRootFile()
