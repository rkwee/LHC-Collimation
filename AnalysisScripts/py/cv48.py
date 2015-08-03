#!/usr/bin/python
#
# June 2015, rkwee
## -------------------------------------------------------------------------------
# selects randomly 10 out of 1000 values per s-location : use to preprare input for beamgas with size
## -------------------------------------------------------------------------------
import random, helpers, gzip, math
from helpers import workpath
# -----------------------------------------------------------------------------------
debug = 0

def createSelectionList(nSPos,nTraj,von,bis):

    # select between von to bis
    selList = []
    for s in range(nSPos):

        tList = []
        while len(tList) != nTraj:
            rndm = random.randint(von,bis)
            if rndm not in tList:
                tList += [rndm]

        # sorting to avoid retrieving data from a lower block and then going back to retrieve data from an upper block 
        tList.sort()

        selList += [ tList ]
        if debug: print "added ", selList[-1], 'to list'

    return selList


def cv48():

    # -- out file name as input for fluka
    foutname = workpath + 'runs/checkTrajectory6500GeV/4TeV/massaged_fort.89'
    print 'writing ... ', foutname
    fout = open(foutname, 'w')
                  
    # format: #0 CXTRCK, #1 CYTRCK, #2 CZTRCK, #3 XTRACK(0), #4 YTRACK(0), #5 ZTRACK(0), #6JTRACK, #7 NCASE, #8 ATRACK
    pathtofiles = '/afs/cern.ch/project/lhc_mib/beamgas/4TeV_beamsize/createTrajectories/'
    files = [ pathtofiles + '13evts/ir1_4TeV_settings_from_TWISS_20MeV_b1_orbitDump001_fort.89.gz' ]
    files = [ pathtofiles + '13evts/test.txt.gz' ]

    # Nsel can be at max the total available number of trajectories
    nsteps, Nsel = 547589,10
    nsteps, Nsel = 10,2
    
    stepsize = 0.0998809
    selList = createSelectionList(nsteps,Nsel,1,4)
    
    print "using this selection list of length", len(selList), selList 

    for mfile in files:
        print 'opening....', mfile
        mf = gzip.open(mfile)

        for cnt,line in enumerate(mf):
            i = cnt+1
            print "at line", i

            # loop over entire list
            for s,sList in enumerate(selList):

                for traj in sList:

                    # line of interest
                    lineOfInt = (traj-1) * nsteps + s+1
                    if debug: print "line of interest is", lineOfInt, "which corresponds to traj", traj, "in block", s+1

                    if i < lineOfInt: 

                        print "want line", lineOfInt, '. Am at line', i
                        break

                    elif i > lineOfInt: continue

                    line = line.rstrip()

                    ncase  = int(line.split()[7])
                    ztrack = float(line.split()[5])
                    strack = s*stepsize
                    print "selected traj", ncase, 'at position', ztrack, "(original), ", strack, '(calculated). diff ', math.fabs(ztrack-strack)
                    fout.write(line + "\n")














    fout.close()
