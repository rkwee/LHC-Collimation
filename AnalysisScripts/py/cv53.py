#!/usr/bin/python
#
# June 2015, rkwee
## -------------------------------------------------------------------------------
# selects randomly 10 out of 1000 values per s-location : use to preprare input for beamgas with size
## -------------------------------------------------------------------------------
import random, helpers, gzip, math, time
from helpers import workpath
# -----------------------------------------------------------------------------------
debug = 1
pathtofiles = '/afs/cern.ch/project/lhc_mib/beamgas/4TeV_beamsize/createTrajectories/'
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
        #if debug: print "added ", selList[-1], 'to list'

    return selList

def cv53():
    tbegin = time.time()
    # -- out file name as input for fluka
    foutname = 'downselected_fort.89.cv53'

    print 'writing ... ', foutname
    fout = open(foutname, 'w')

                  
    # format: #0 CXTRCK, #1 CYTRCK, #2 CZTRCK, #3 XTRACK(0), #4 YTRACK(0), #5 ZTRACK(0), #6JTRACK, #7 NCASE, #8 ATRACK

    #files = [pathtofiles + '100evts/run_0000' + str(i) + '/ir1_4TeV_settings_from_TWISS_20MeV_b1_orbitDump001_fort.89.gz' for i in range(1)]
    # Nsel can be at max the total available number of trajectories
    nsteps, Nsel, ntrajMax = 547589,10,1000
    #nsteps, Nsel, ntrajMax = 10,2,8

    files = []
    for job in range(1,ntrajMax+1):
        index = str(job)

        if len(index) < 5:
            index = '0'*(5-len(str(job)))+str(job)

        files += [ pathtofiles + 'inicon1evt/run_'+index+'/ir1_4TeV_settings_from_TWISS_20MeV_b1_orbitDumpICON001_fort.89' ]

    #files = [ pathtofiles + '13evts/test.txt.gz' ]
    
    stepsize = 0.0998809
    selList = createSelectionList(nsteps,Nsel,1,ntrajMax)

    if debug: print "using this selection list of length", len(selList), #selList 
    
    j = 0
    t0 = time.time()
    t1,t2,t3,t4,t5 = 0,0,0,0,0
    for mfile in files:

        print 'opening....', mfile
        t1 = time.time()
     
        with open(mfile) as mf:
	    j += 1
            i = 0
            for line in mf:
                t2 = time.time()
                if j in selList[i]:

                        line = line.rstrip()
                        fout.write(line + ' ' + ' \n')

                        # if debug:
                        #     ncase  = int(line.split()[7])
                        #     ztrack = float(line.split()[5])
                        #     strack = s*stepsize
                        #     print "selected traj", ncase, 'at position', ztrack, "(original), ", strack, '(calculated). diff ', math.fabs(ztrack-strack)

                t3 = time.time()
                i += 1
        t4 = time.time()

    fout.close()
    t5 = time.time()

    print(str(tbegin)+' time when scripts begins')
    print(str(t0-tbegin)+' time until just before first loop.')
    print(str(t1-tbegin)+' time until 1 gzip open call.')
    print(str(t2-tbegin)+' time until looping over lines.')
    print(str(t3-tbegin)+' time after jumping over empty list loop.')
    print(str(t4-tbegin)+' time until out of line loop.')
    print(str(t5-tbegin)+' time until out files loop (1 file only).')


