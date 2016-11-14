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

    gamma_rel = 4.e3/0.938
    energy = '4TeV'

    # twiss file
    # tf = pymadx.Tfs('/afs/cern.ch/work/r/rkwee/HL-LHC/LHC-Collimation/SixTrackConfig/6.5TeV/MED800/B1/twiss_lhcb1_med_new_thin_800.tfs')
    # tf = pymadx.Tfs('/afs/cern.ch/work/r/rkwee/HL-LHC/LHC-Collimation/SixTrackConfig/6.5TeV/MED800/B1/1cm/twiss_lhcb1_med_new_thin_800_1cm.tfs')
    # tf = pymadx.Tfs("/afs/cern.ch/work/r/rkwee/HL-LHC/LHC-Collimation/SixTrackConfig/4TeV/beamgas/twiss_4tev_b1.data")
    tf = pymadx.Tfs("/afs/cern.ch/work/r/rkwee/HL-LHC/LHC-Collimation/SixTrackConfig/6.5TeV/background_2015_80cm/MADX_2015/twiss_b2.tfs")
    gamma_rel = 6.5e3/0.938
    energy = "6.5TeV"

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
    shiftVal = length_LHC#-500

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
    lShift = 0.5

    XurMin, XurMax = 0,548.
    XurMin, XurMax = -1,-1
    XurMin, XurMax = length_LHC-500, length_LHC
    # rel = '_sigma_IR1Right_1cm'
    # rel = '_sigma_IR1Left_'+energy
    rel = 'from_twiss_orbit_IR1'
    # lShift = 0.0

    # XurMin, XurMax = IP5-300, IP5+300
    # rel = '_IP5'
    # XurMin, XurMax = IP8-300, IP8+300
    # rel = '_IP8'

    cv = TCanvas( 'cv', 'cv', 2100, 900)

    x1, y1, x2, y2 = 0.8-lShift, 0.65, 0.9-lShift, 0.9
    mlegend = TLegend( x1, y1, x2, y2)
    mlegend.SetFillColor(0)
    mlegend.SetFillStyle(0)
    mlegend.SetLineColor(0)
    mlegend.SetTextSize(0.05)
    mlegend.SetShadowColor(0)
    mlegend.SetBorderSize(0)

    mg = TMultiGraph()
    # marker in legend
    lm = 'l'

    emittance_norm = 3.5e-6
    emittance_geo = emittance_norm/gamma_rel

    SIGX = [math.sqrt(betax * emittance_geo) for betax in BETX]
    SIGY = [math.sqrt(betay * emittance_geo) for betay in BETY]

    # xList, yList, color, mStyle, lg = S_shifted, SIGX, kGreen-1, 22, '#sigma_{x}'
    # g0 = makeTGraph(xList, yList, color, mStyle)
    # mlegend.AddEntry(g0, lg, lm)    
    # mg.Add(g0)
    # xList, yList, color, mStyle, lg = S_shifted, SIGY, kGreen-2, 20, '#sigma_{y}'
    # g1 = makeTGraph(xList, yList, color, mStyle)
    # mlegend.AddEntry(g1, lg, lm)    
    # mg.Add(g1)
    ytitle = 'beam size [m]'

    xList, yList, color, mStyle, lg = S_shifted, X, kGreen+1, 21, "x [m]"
    g1 = makeTGraph(xList, yList, color, mStyle)
    mlegend.AddEntry(g1, lg, lm) 
    mg.Add(g1)

    xList, yList, color, mStyle, lg = S_shifted, Y, kBlue-1, 20, "y [m]"
    g2 = makeTGraph(xList, yList, color, mStyle)
    mlegend.AddEntry(g2, lg, lm) 
    mg.Add(g2)
    ytitle = 'orbit'

    # xList, yList, color, mStyle, lg = S_shifted, PY, kBlue+1, 27, "y'"
    # g3 = makeTGraph(xList, yList, color, mStyle)
    # mlegend.AddEntry(g3, lg, lm) 
    # mg.Add(g3)

    mg.Draw("a"+lm)

    l = TLine()
    l.SetLineStyle(1)
    YurMin, YurMax = 0, 0.0019
    l.SetLineColor(kRed)

    # s = 22.6
    # l.DrawLine(s,YurMin,s,YurMax)

    # s = 59.
    # l.DrawLine(s,YurMin,s,YurMax)

    # s = 153.
    # l.DrawLine(s,YurMin,s,YurMax)

    # s = 269.
    # l.DrawLine(s,YurMin,s,YurMax)

    mg.GetYaxis().SetTitle(ytitle)
    mg.GetXaxis().SetTitle('s [m]')
    if XurMin != -1:
        mg.GetXaxis().SetRangeUser(XurMin,XurMax)

    mlegend.Draw()

    pname  = wwwpath
    subfolder = 'TCT/'+energy+'/beamgas/'
    pname += subfolder + ytitle +'_'+rel.replace(".", "p")+'.pdf'

    print('Saving file as ' + pname ) 
    cv.Print(pname)

    pname  = wwwpath
    subfolder = 'TCT/'+energy+'/beamgas/'
    pname += subfolder + 'from_twiss_'+rel.replace(".", "p")+'.png'


    print('Saving file as ' + pname ) 
    cv.Print(pname)

# ----------------------------------------------------------------------------





