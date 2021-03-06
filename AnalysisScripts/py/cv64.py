#!/usr/bin/python
#
# to check beam size along s
# June 2015, rkwee
## -------------------------------------------------------------------------------
import pymadx
## -------------------------------------------------------------------------------
import sys, os, time, math
import helpers
from helpers import wwwpath, length_LHC, mylabel
# -----------------------------------------------------------------------------------
def cv64():

    # twiss file
    # tf = pymadx.Tfs('/afs/cern.ch/work/r/rkwee/HL-LHC/runs/checkTrajectory6500GeV/4TeV/compTrajectories/twiss_b2.data') ## erased

    #tf = pymadx.Tfs('/afs/cern.ch/work/r/rkwee/HL-LHC/LHC-Collimation/SixTrackConfig/6.5TeV/background_2015_80cm/twiss_b2_80cm.tfs')

    # number of randomly produced values per s location
    N = 1

    emittance_norm = 3.5e-6
    gamma_rel = 4e3/0.938
    #gamma_rel = 6.5e3/0.938
    emittance_geo = emittance_norm/gamma_rel


    s = tf.GetColumnDict["S"]
    try:
            row = tf.GetRowDict(name)
        except KeyError:
            print "Couldnt find", name
            continue

        betx = row['BETX']
        xp   = row['PX']
        bety = row['BETY']
        yp   = row['PY']
        s    = row['S'] 

        sigx = math.sqrt(emittance_geo * betx)
        sigy = math.sqrt(emittance_geo * bety)

        sigmaxp = math.sqrt(emittance_geo/betx)
        sigmayp = math.sqrt(emittance_geo/bety)
        line = 'For ' + name + ' at s = ' +str(s)+ ' m: sigma_x =' + str(sigx*100) + ' cm, sigma_y =' + str(sigy*100) + \
            ' cm, xp = '+ str(xp) + ' rad, yp = ' + str(yp) + ' rad' + \
            ' sigma_xp = '+ str(sigmaxp) + ' rad, sigma_yp = ' + str(sigmayp) + ' rad' 

        print line

# ----------------------------------------------------------------------------





