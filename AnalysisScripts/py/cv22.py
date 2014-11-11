#!/usr/bin/python
#
# get average losses
#
# Nov 2014, rkwee
## -------------------------------------------------------------------------------
import ROOT, sys, glob, os, time, math
from ROOT import *
import avLosses
from avLosses import avLosses
from helpers import wwwpath, file_len, length_LHC, mylabel, addCol, gitpath, workpath
from array import array
## -------------------------------------------------------------------------------

def cv22():

    debug        = 1

    # subfolder in wwwpath for result plots
    subfolder = './' 
    
    colls = [

        ('NewScatt_TCT_4TeV_B1hHalo'),
        ('TCT_4TeV_B1hHalo'),

        ('NewScatt_TCT_4TeV_B1vHalo'),
        ('TCT_4TeV_B1vHalo'),

        ('NewScatt_TCT_4TeV_B2hHalo'),
        ('TCT_4TeV_B2hHalo'),

        ('NewScatt_TCT_4TeV_B2vHalo'),
        ('TCT_4TeV_B2vHalo'),

        ]


    lossPointsB1 = [('cold_loss', 20290., 20340., "Q8"),
                    ('cold_loss', 20380., 20430., "Q10"),
                    ]
    lossPointsB2 = [('cold_loss', 6950., 7010., "Q7"),
                    ('cold_loss', 7050., 7110., "Q9")
                    ]

    for coll in colls:

        print '.'*50

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

        rfname = thispath + 'lossmap'+ coll +'.root'
        trname = 'normtree' + coll
            
        if not os.path.exists(rfname): 
            print rfname,' does not exist?!'
            continue

        lossPoints = lossPointsB2
        if coll.count("B1"): lossPoints = lossPointsB1

        # ------------------------------------------------
        for h,loss_start,loss_end,pointName in lossPoints:
            
            losses = avLosses(rfname, coll, 1., h+coll, loss_start, loss_end, pointName)            
            print losses,'\n'
