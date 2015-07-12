#!/usr/bin/python
#
# June 2015, rkwee
## -------------------------------------------------------------------------------
import pymadx
## -------------------------------------------------------------------------------
import ROOT, sys, os, time, math
from ROOT import *
import lossmap, helpers, array, random
from helpers import wwwpath, length_LHC, mylabel, gitpath, length_LHC
from array import array
# -----------------------------------------------------------------------------------
def cv42():

    # twiss file
    tf = pymadx.Tfs('/afs/cern.ch/work/r/rkwee/HL-LHC/LHC-Collimation/SixTrackConfig/6.5TeV/MED800/B1/1cm/MYM.tfs')

    # use all locations for sampling the beam-size


    # number of randomly produced values per s location
    N = 1

    # out file name as input for fluka
    foutname = 'bgpos.dat'
    fout = open(foutname, 'w')

    emittance_norm = 3.75e-6
    gamma_rel = 6.5e3/0.938
    emittance_geo = emittance_norm/gamma_rel
    gauss1 = TF1('gauss1', 'exp(-0.5*(x**2))', -5.,5.)
    gauss2 = TF1('gauss2', 'exp(-0.5*(x**2))', -5.,5.)
    gauss3 = TF1('gauss3', 'exp(-0.5*(x**2))', -5.,5.)
    gauss4 = TF1('gauss4', 'exp(-0.5*(x**2))', -5.,5.)
    gauss5 = TF1('gauss5', 'exp(-0.5*(x**2))', -5.,5.)
    gauss6 = TF1('gauss6', 'exp(-0.5*(x**2))', -5.,5.)

    nsteps = 545850
    for i in range(nsteps):

        name = 'MYM.' + str(i+1)

        row = tf.GetRowDict(name)
        betx = row['BETX']
        alfx = row['ALFX']
        bety = row['BETY']
        alfy = row['ALFY']
        s    = row['S'] * 100

        sigx = math.sqrt(emittance_geo * betx)
        sigy = math.sqrt(emittance_geo * bety)
        ts = str(0.0)

        for i in range(N):
            # convert x and y from m to cm
            big_x  = gauss1.GetRandom()
            big_xp = gauss2.GetRandom()
            small_xp = math.sqrt(emittance_geo/betx) * (big_xp - alfx*big_x)
            small_x  = big_x*sigx * 100

            big_y  = gauss3.GetRandom()
            big_yp = gauss4.GetRandom()
            small_yp = math.sqrt(emittance_geo/bety) * (big_yp - alfy*big_y)
            small_y  = math.sqrt(bety*emittance_geo) * big_y * 100

            line ='{0:15}  {1:15}  {2:10}  {3:15}  {4:15}  {5:5}'.format(small_x, small_y, s, small_xp, small_yp, ts)
            fout.write(line + '\n')

    fout.close()
        
# ----------------------------------------------------------------------------





