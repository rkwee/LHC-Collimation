#!/usr/bin/python
#
# June 2015, rkwee
## -------------------------------------------------------------------------------
# selects randomly 10 out of 1000 values per s-location : use to preprare input for beamgas with size
## -------------------------------------------------------------------------------
import random, helpers, gzip
from helpers import workpath
# -----------------------------------------------------------------------------------
def createSelectionList(nSPos,nTraj):

    # select between 0 and 999
    selList = []
    for s in range(nSPos):

        tList = []
        for t in range(nTraj):
            rndm = random.randint(0,999)
            tList += [rndm]
        selList += [ tList ] 
        #print "added ", selList[-1], 'to list'
    return selList

def cv48():


    # -- out file name as input for fluka
    # foutname = workpath + 'runs/runs/checkTrajectory6500GeV/4TeV/BEAMGAS.dat'
    # fout = open(foutname, 'w')
                  
    # format: #0 CXTRCK, #1 CYTRCK, #2 CZTRCK, #3 XTRACK(0), #4 YTRACK(0), #5 ZTRACK(0), #6JTRACK, #7 NCASE, #8 ATRACK
    pathtofiles = '/afs/cern.ch/project/lhc_mib/beamgas/4TeV_beamsize/createTrajectories/'
    files = [ pathtofiles + '13evts/ir1_4TeV_settings_from_TWISS_20MeV_b1_orbitDumpICON001_fort.89.gz' ]

    nsteps, Nsel = 547589,2
    

    stepsize = 0.0998809
    selList = createSelectionList(nsteps,Nsel)

    for mfile in files:
        print 'opening....', mfile
        mf = gzip.open(mfile)

        for line in mf:

            
