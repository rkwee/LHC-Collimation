#!/usr/bin/python
#
# June 2015, rkwee
## -------------------------------------------------------------------------------
import pymadx
## -------------------------------------------------------------------------------
import sys, os, time, math
import helpers
from helpers import wwwpath, length_LHC, mylabel
# -----------------------------------------------------------------------------------
def cv47():

    # twiss file
    # tf = pymadx.Tfs('/afs/cern.ch/work/r/rkwee/HL-LHC/runs/checkTrajectory6500GeV/4TeV/compTrajectories/twiss_b2.data')
    tf = pymadx.Tfs('/afs/cern.ch/work/r/rkwee/HL-LHC/LHC-Collimation/SixTrackConfig/6.5TeV/background_2015_80cm/twiss_b2_80cm.tfs')

    # number of randomly produced values per s location
    N = 1

    emittance_norm = 3.5e-6
    gamma_rel = 6.5e3/0.938
    emittance_geo = emittance_norm/gamma_rel

    pointsname = ['TCTH.4R1.B2', 'MQXA.1R1', 'MQXA.3R1',
                  'MCBXV.2R1', 'MQXB.B2R1',

                  ]

    for name in pointsname:

        row = tf.GetRowDict(name)
        betx = row['BETX']
        alfx = row['ALFX']
        bety = row['BETY']
        alfy = row['ALFY']
        s    = row['S'] 

        sigx = math.sqrt(emittance_geo * betx)
        sigy = math.sqrt(emittance_geo * bety)

        line = 'For ' + name + ' at s = ' + str(s) + ' m: sigma_x =' + str(sigx*100) + ' cm, sigma_y =' + str(sigy*100) + ' cm'
        print line

# ----------------------------------------------------------------------------





