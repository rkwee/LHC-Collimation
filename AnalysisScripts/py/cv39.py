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
def cv39():

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
    IP5  = tf.GetColumnDict('S')['IP5']
    IP8  = tf.GetColumnDict('S')['IP8']

    # no shift if val is length
    shiftVal = length_LHC

    cnt = 0

    S_shifted, X_shifted = [], []
    for s in S:
        s_shifted = s + shiftVal
        #print "s_shifted", s_shifted

        if s_shifted >= length_LHC:
            cnt += 1 
            s_shifted -= length_LHC
            #print "s_shifted after subtraction", s_shifted

        S_shifted += [s_shifted]
        #print "using", s_shifted

    S_shifted.sort()
    XurMin, XurMax = length_LHC-300, length_LHC
    rel = '_IR1Left'
    XurMin, XurMax = 0,300
    rel = '_IR1Right'
    XurMin, XurMax = IP5-300, IP5+300
    rel = '_IP5'
    XurMin, XurMax = IP8-300, IP8+300
    rel = '_IP8'

    cv = TCanvas( 'cv', 'cv', 2100, 900)

    x1, y1, x2, y2 = 0.8, 0.65, 0.9, 0.9
    mlegend = TLegend( x1, y1, x2, y2)
    mlegend.SetFillColor(0)
    mlegend.SetFillStyle(0)
    mlegend.SetLineColor(0)
    mlegend.SetTextSize(0.035)
    mlegend.SetShadowColor(0)
    mlegend.SetBorderSize(0)

    mg = TMultiGraph()
    # marker in legend
    lm = 'lp'

    xList, yList, color, mStyle, lg = S_shifted, X, kGreen-1, 22, 'x'
    g0 = makeTGraph(xList, yList, color, mStyle)

    mlegend.AddEntry(g0, lg, lm)    
    mg.Add(g0)

    xList, yList, color, mStyle, lg = S_shifted, PX, kGreen+1, 21, "x'"
    g1 = makeTGraph(xList, yList, color, mStyle)
    mlegend.AddEntry(g1, lg, lm) 
    mg.Add(g1)

    xList, yList, color, mStyle, lg = S_shifted, Y, kBlue-1, 20, "y"
    g2 = makeTGraph(xList, yList, color, mStyle)
    mlegend.AddEntry(g2, lg, lm) 
    mg.Add(g2)

    xList, yList, color, mStyle, lg = S_shifted, PY, kBlue+1, 27, "y'"
    g3 = makeTGraph(xList, yList, color, mStyle)
    mlegend.AddEntry(g3, lg, lm) 
    mg.Add(g3)

    mg.Draw("a"+lm)
    mg.GetXaxis().SetTitle('s [m]')
    if XurMin != -1:
        mg.GetXaxis().SetRangeUser(XurMin,XurMax)

    mlegend.Draw()

    pname  = wwwpath
    subfolder = 'TCT/6.5TeV/beamgas/'
    pname += subfolder + 'twiss_b1'+rel+'.png'

    print('Saving file as ' + pname ) 
    cv.Print(pname)

# ----------------------------------------------------------------------------





