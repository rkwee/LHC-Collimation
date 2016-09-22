#!/usr/bin/python
#
# check beamsize along s from fluka file
# Sept 16
#
# R Kwee, 2016
# 
# ---------------------------------------------------------------------------------
import ROOT, sys, glob, os, math, helpers
from ROOT import *
from array import array
from helpers import *
import createTTree 
import os
# --------------------------------------------------------------------------------

def cv73():
    
    pathtofiles = projectpath + 'valBG4TeV/'
    otherparking= projectpath + 'HaloRun2/valBG4TeV2/'

    for job in range(14,72):

        index = str(job)
    
        if len(index) < 3:
            index = '0'*(3-len(str(job)))+str(job)
        datafile = '/afs/cern.ch/project/lhc_mib/HL1.0/valBG4TeV3/traj_fort.89.' + index 

        print "Want to use ", datafile
        #
        TTreeFileName = createTTree.ctree(datafile)

        cmd = "mv " + datafile + ".root " + otherparking + datafile.split("alBG4TeV3/")[-1] + ".root"
        print cmd
        os.system(cmd)
        #if not os.path.exists( datafile ): break


