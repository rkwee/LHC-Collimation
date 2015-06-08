#!/usr/bin/python
#
# Mar 2015, rkwee
## -------------------------------------------------------------------------------
import pymadx
## -------------------------------------------------------------------------------
import ROOT, sys, os, time, math
from ROOT import *
import lossmap, helpers, array
from helpers import wwwpath, length_LHC, mylabel, gitpath, makeTGraph
from array import array
# -----------------------------------------------------------------------------------
def cv41():

    # twiss file
    tf = pymadx.Tfs('/afs/cern.ch/work/r/rkwee/HL-LHC/LHC-Collimation/SixTrackConfig/6.5TeV/MED800/B1/twiss_lhcb1_med_new_thin_800.tfs')

    BETX = tf.GetColumn('BETX')
    BETY = tf.GetColumn('BETY')
    ALFX = tf.GetColumn('ALFX')
    ALFY = tf.GetColumn('ALFY')
    X    = tf.GetColumn('X')
    Y    = tf.GetColumn('Y')
    PX   = tf.GetColumn('PX')
    PY   = tf.GetColumn('PY')
    S    = tf.GetColumn('S')

    emittance_norm = 3.75e-6
    gamma_rel = 6.5e3/0.938
    emittance_geo = emittance_norm/gamma_rel
    gauss1 = TF1('gauss1', 'exp(-0.5*(x**2))', -5.,5.)
    gauss2 = TF1('gauss2', 'exp(-0.5*(x**2))', -5.,5.)
    gauss3 = TF1('gauss3', 'exp(-0.5*(x**2))', -5.,5.)
    gauss4 = TF1('gauss4', 'exp(-0.5*(x**2))', -5.,5.)
    gauss5 = TF1('gauss5', 'exp(-0.5*(x**2))', -5.,5.)
    gauss6 = TF1('gauss6', 'exp(-0.5*(x**2))', -5.,5.)

    h1 = TH2F("f1","f1",100,-1e-2,1e-2,100,-1e-3,1e-3)
    h2 = TH2F("f2","f2",100,-1e-2,1e-2,100,-1e-3,1e-3)
    h3 = TH2F("f3","f3",100,-1e-2,1e-2,100,-1e-2,1e-2)

    for i in range(len(X)):
        big_x  = gauss1.GetRandom()
        big_xp = gauss2.GetRandom()
        small_xp = math.sqrt(emittance_geo/BETX[i]) * (big_xp - ALFX[i]*big_x)
        small_x  = math.sqrt(BETX[i]*emittance_geo) * big_xp - emittance_geo * ALFX[i] * big_x
        h1.Fill(small_x,small_xp)

        big_y  = gauss3.GetRandom()
        big_yp = gauss4.GetRandom()
        small_yp = math.sqrt(emittance_geo/BETY[i]) * (big_yp - ALFY[i]*big_y)
        small_y  = math.sqrt(BETY[i]*emittance_geo) * big_yp - emittance_geo * ALFY[i] * big_y
        h2.Fill(small_y,small_yp)

        sigmaX = math.sqrt(emittance_geo * BETX[i])
        sigmaY = math.sqrt(emittance_geo * BETY[i])
        h3.Fill(sigmaX, sigmaY)

    a,b = 3,1
    cv = TCanvas( 'cv', 'cv', a*600, b*600)
    cv.Divide(a,b)
    cv.SetRightMargin(0.3)
    cv.SetLeftMargin(0.2)
    cv.SetTopMargin(0.15)
    xtitle, ytitle = 'x [m]', "x' [rad]"
    h1.GetXaxis().SetLabelSize(0.02)
    h1.GetYaxis().SetLabelSize(0.03)
    h1.GetZaxis().SetLabelSize(0.03)
    h1.GetXaxis().SetTitle(xtitle)
    h1.GetYaxis().SetTitle(ytitle)
    xtitle, ytitle = 'y [m]', "y' [rad]"
    h2.GetXaxis().SetLabelSize(0.02)
    h2.GetYaxis().SetLabelSize(0.03)
    h2.GetZaxis().SetLabelSize(0.03)
    h2.GetXaxis().SetTitle(xtitle)
    h2.GetYaxis().SetTitle(ytitle)
    xtitle, ytitle = '#sigma_{x}', "#sigma_{y}"
    h3.GetXaxis().SetLabelSize(0.02)
    h3.GetYaxis().SetLabelSize(0.03)
    h3.GetZaxis().SetLabelSize(0.03)
    h3.GetXaxis().SetTitle(xtitle)
    h3.GetYaxis().SetTitle(ytitle)


    cv.cd(1)
    h1.Draw('colz')
    cv.cd(2)
    h2.Draw('colz')
    cv.cd(3)
    h3.Draw('colz')

    rel = 'gauss'
    pname  = wwwpath
    subfolder = 'TCT/6.5TeV/beamgas/'
    pname += subfolder + 'twiss_b1'+rel+'.png'

    print('Saving file as ' + pname ) 
    cv.SaveAs(pname)

# ----------------------------------------------------------------------------





