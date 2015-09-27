#!/usr/bin/python
#
# June 2015, rkwee
## -------------------------------------------------------------------------------
import ROOT
from ROOT import TH1F, TCanvas
import helpers
from helpers import wwwpath, length_LHC, mylabel
# from cv47
# -----------------------------------------------------------------------------------
def cv56():


    # number of randomly produced values per s location
    myfile = '/afs/cern.ch/project/lhc_mib/beamgas/4TeV_beamsize/BGAS10.dat'
    outfilename = '/afs/cern.ch/project/lhc_mib/beamgas/4TeV_beamsize/BGAS.dat'

    myfile = '/afs/cern.ch/work/r/rkwee/HL-LHC/LHC-Collimation/FlukaRoutines/6.5TeV/beamgas/BGASB.dat'
    outfilename = '/afs/cern.ch/work/r/rkwee/HL-LHC/LHC-Collimation/FlukaRoutines/6.5TeV/beamgas/BB.dat'

    outfile = open(outfilename, 'w')
    print "Writing ..... ", outfilename

    with open(myfile) as mf:

        for line in mf:

            # format is: XIN(NIN), YIN(NIN), ZIN(NIN), UIN(NIN), VIN(NIN),tIn(NIN)
            [XIN, YIN, ZIN, UIN, VIN,tIn] = line.split()

            newUIN = str(-float(UIN))
            newVIN = str(-float(VIN))

            newline = XIN + ' '+ YIN + ' '+ ZIN + ' '+ newUIN + ' '+ newVIN + ' '+ tIn + '\n'

            outfile.write(newline)


    outfile.close()




