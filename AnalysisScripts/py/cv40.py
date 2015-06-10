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
def cv40():

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

    XurMin, XurMax = length_LHC-300, length_LHC
    rel = '_IR1Left'
    XurMin, XurMax = 0,300
    rel = '_IR1Right'
    XurMin, XurMax = IP5-300, IP5+300
    rel = '_IP5'
    XurMin, XurMax = IP8-300, IP8+300
    rel = '_IP8'

    XurMin, XurMax = -1, -1
    rel = '_phasespace'

    cv = TCanvas( 'cv', 'cv', 900, 900)

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
    lm = 'p'


    xList, yList, color, mStyle, lg = X, PX, kGreen+1, 21, "x,x'"
    g1 = makeTGraph(xList, yList, color, mStyle)
    mlegend.AddEntry(g1, lg, lm) 
    mg.Add(g1)

    xList, yList, color, mStyle, lg = Y, PY, kBlue+1, 27, "y,y'"
    g3 = makeTGraph(xList, yList, color, mStyle)
    mlegend.AddEntry(g3, lg, lm) 
    mg.Add(g3)

    mg.Draw("a"+lm)
    mg.GetXaxis().SetTitle('x,y')
    if XurMin != -1:
        mg.GetXaxis().SetRangeUser(XurMin,XurMax)

    mlegend.Draw()

    pname  = wwwpath
    subfolder = 'TCT/6.5TeV/beamgas/'
    pname += subfolder + 'twiss_b1'+rel+'.png'

    print('Saving file as ' + pname ) 
    cv.Print(pname)

# ----------------------------------------------------------------------------





