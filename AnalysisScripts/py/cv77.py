#!/usr/bin/python
#
# check initial conditions file
## -------------------------------------------------------------------------------
import ROOT, sys, glob, os
from ROOT import *
from helpers import *
## -------------------------------------------------------------------------------
def rms(vec):
    rms = 0.
    for val in vec:
        # convert back to m
        val *= 0.01

        rms += val**2

    return math.sqrt(rms/len(vec))
def cv77():

    
    # this is in fluka units

    foutname = '/afs/cern.ch/project/lhc_mib/bgChecks3/INIC4TeV_fout.dat'
    foutname = gitpath + 'FlukaRoutines/4TeV/beamgas/inicon1/INIC4TeV.dat'
    foutname = '/afs/cern.ch/project/lhc_mib/bgChecks3/INIC6500GeV.dat'
    foutname = projectpath + 'beamsize/6500GeV_beamsize/checkTrajectory6500GeV/orbitDump/INIC6p5.dat'

    # XIN(NIN), YIN(NIN), ZIN(NIN), UIN(NIN), VIN(NIN),tIn(NIN)
    cnames = ['XIN', 'YIN', 'ZIN', 'UIN', 'VIN', 'tIn']


    energy = "6.5TeV"
    gamma_rel = 6.5e3/0.938
    betaStar = 0.8
    # energy = "4TeV"
    # gamma_rel = 4e3/0.938
    # betaStar = 0.6

    XINs, YINs = [],[]

    print "opening", foutname
    with open(foutname) as cf:
        for line in cf:
            line.rstrip()
            lineList = line.split()
            
            XINs += [float(lineList[0])]
            YINs += [float(lineList[1])]


    # sigmaX = stddev(XINs)
    # sigmaY = stddev(YINs)
    sigmaX = rms(XINs)
    sigmaY = rms(YINs)

    emittanceX = sigmaX*sigmaX /betaStar 
    emittanceY = sigmaY*sigmaY /betaStar 

    print sigmaX, sigmaY
    print "this corresponds to an geometric emittance of ", emittanceX, '  ',emittanceY
    emittance_norm = 3.5e-6

    emittance_nX = emittanceX*gamma_rel
    emittance_nY = emittanceY*gamma_rel
    print "this corresponds to an norm emittance of ", emittance_nX, '  ',emittance_nY
    print "compared to nominal emittance of ", emittance_nX/emittance_norm, '  ',emittance_nY/emittance_norm

    emittance_geo = emittance_norm/gamma_rel
    sigma_calc = math.sqrt(betaStar * emittance_geo)

    print sigma_calc
