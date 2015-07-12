#!/usr/bin/python
#
# Mar 2015, rkwee
## -------------------------------------------------------------------------------
# replacement for gnuplot script to plot simply colums from a text against each other 
## -------------------------------------------------------------------------------
import ROOT, sys, os, time, math
from ROOT import *
import lossmap, helpers, array
from helpers import wwwpath, length_LHC, mylabel, gitpath, makeTGraph, workpath
from array import array
# -----------------------------------------------------------------------------------
def cv45():

    # current path
    cpath = workpath + 'runs/checkTrajectory6500GeV/'

    fn1 = '/afs/cern.ch/work/r/rkwee/HL-LHC/runs/checkTrajectory6500GeV/madSY_b2.dat'
    #fn1 = cpath + 'ir1b2_exp_noScoringRegion001_TRAKFILE.1425'
    fn2 = cpath + 'ir1b2_exp001_TRAKFILE.luigi'
    fn3 = cpath + 'ir1b2_exp001_TRAKFILE.145'
    #fn3 = cpath + '4TeV/ir1_4TeV_settings_from_TWISS_20MeV_b1001_TRAKFILE'
#plot '/afs/cern.ch/work/r/rkwee/HL-LHC/runs/checkTrajectory6500GeV/ir1b2_exp001_TRAKFILE.1425' us 3:2,\
#     
#plot '/afs/cern.ch/work/r/rkwee/HL-LHC/runs/ir1b2_exp001_TRAKFILE.luigi' us 3:2,\
#plot     '/afs/cern.ch/work/r/rkwee/HL-LHC/runs/checkTrajectory6500GeV/' us 3:2
#     '/afs/cern.ch/work/r/rkwee/HL-LHC/runs/checkTrajectory6500GeV/madSY_b1.dat' us 1:2,\
#     '/afs/cern.ch/work/r/rkwee/HL-LHC/runs/checkTrajectory6500GeV/madSY_b2.dat' us 1:2


    XurMin, XurMax = 5,57000
    #XurMin, XurMax = -1, -1

    YurMin, YurMax = -0.02,0.03
    
    #YurMin, YurMax = -1,-1

    cv = TCanvas( 'cv', 'cv', 1000, 600)

    x1, y1, x2, y2 = 0.4, 0.65, 0.9, 0.9
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

    print 'opening', fn1
    [S,Y] = helpers.getListFromColumn([0,1], fn1)
    xList, yList, color, mStyle, lg = S,Y, kGreen+1, 21, fn1.split(cpath)[-1]
    g1 = makeTGraph(xList, yList, color, mStyle)
    mlegend.AddEntry(g1, lg, lm) 
    mg.Add(g1)

    print 'opening', fn2
    [S,Y] = helpers.getListFromColumn([2,1], fn2)
    xList, yList, color, mStyle, lg = S, Y, kBlue+1, 27, fn2.split(cpath)[-1]
    g2 = makeTGraph(xList, yList, color, mStyle)
    mlegend.AddEntry(g2, lg, lm) 
    mg.Add(g2)

    print 'opening', fn3
    [S,Y] = helpers.getListFromColumn([2,1], fn3)
    xList, yList, color, mStyle, lg = S, Y, kBlue+1, 23, fn3.split(cpath)[-1]
    g3 = makeTGraph(xList, yList, color, mStyle)
    mlegend.AddEntry(g3, lg, lm) 
    mg.Add(g3)

    mg.Draw("a"+lm)
    mg.GetYaxis().SetTitle('y [cm]')
    mg.GetXaxis().SetTitle('s [cm]')
    if XurMin != -1:
        mg.GetXaxis().SetRangeUser(XurMin,XurMax)

    rel = ''
    if YurMin != -1:
        mg.GetYaxis().SetRangeUser(YurMin,YurMax)
        rel = 'Zoom'

    mlegend.Draw()

    pname = cpath + 'compTRAKFILE'+rel+'.root'

    print('Saving file as ' + pname ) 
    cv.Print(pname)

# ----------------------------------------------------------------------------





