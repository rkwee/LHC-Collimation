#!/usr/bin/python
#
# if doWriteRFile == 1
#    writes out root file : histograms for lossmaps and 1 ttree with normalisation factor
#    
# use cv25 to plot lossmaps comparing different files
#
#
# Oct 2014, rkwee
## -------------------------------------------------------------------------------
import ROOT, sys, glob, os, time, math
from ROOT import *
import lossmap, helpers, array
from helpers import wwwpath, file_len, length_LHC, mylabel, addCol, gitpath, workpath
from array import array
## -------------------------------------------------------------------------------

def cv24():

    debug        = 1
    doWriteRFile = 1

    colls = [

        ('NewScatt_TCT_4TeV_B1hHalo'),
        ('NewScatt_TCT_4TeV_B2hHalo'),

        ]

    for coll in colls:

        if not coll.startswith('_'): 
            tag  = coll
            coll = '_'+coll


        beam   = 'b2'            
        beamn  = '2'        
        if coll.count('B1'):
            beam  = 'b1'
            beamn = '1'

        # my results 
        thispath  = workpath + 'runs/' + tag +'/'
        thispath = tag + '/'

        rfname = thispath + 'lossmap'+ coll +'.root'
        trname = 'normtree' + coll
        colNumber = 4
            
        f3 = gitpath + 'SixTrackConfig/4TeV/TCThaloStudies/'+beam+'/CollPositions.'+beam+'.dat'

        # use for normalisation the sum of nabs (col 4)
        f4 = thispath + 'coll_summary' + coll + '.dat'

        # ------------------------------------------------

        if doWriteRFile:

            print 'Writing ' + '.'* 25 +' ' + rfname        

            # create a root file
            rf = TFile(rfname, 'recreate')
    
            nt  = TTree(trname,'norm for each coll') 

            if not os.path.exists(f4): 
                print f4,' does not exist?!'
                continue

            t0 = time.time()
            h_tot_loss, h_cold, h_warm = lossmap.lossmap(beam,thispath,coll, f3, length_LHC) 
            t1 = time.time()
            print(str(t1-t0)+' for returning lossmap histograms of ' + coll )

            if debug:
                if h_cold.GetEntries() < 1.:
                    print 'Empty histogram! Binary characters in LPI file?'
                    sys.exit()

            h_tot_loss.Write()
            h_cold.Write()
            h_warm.Write()            

            # -- write the for each norm value a branch into ttree
            t0 = time.time()

            # setting branch name 
            branchname = coll.replace('.','QQQ')

            if debug and 0: print globals()

            # use globals dict to convert strings to variable names
            globals()[branchname] = array('i',[0])

            # create branch
            nt.Branch(branchname, globals()[branchname], branchname+'/i')

            # get value
            maxval = int(addCol(f4, colNumber-1))

            # assigning value
            globals()[branchname][0] = maxval

            # write to tree
            nt.Fill()

            t1 = time.time()

            nt.Write()
            rf.Close()

