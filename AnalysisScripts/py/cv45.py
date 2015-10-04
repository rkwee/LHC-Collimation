#!/usr/bin/python
#
# Mar 2015, rkwee
## -------------------------------------------------------------------------------
# replacement for gnuplot script to plot simply colums from a text against each other 
## -------------------------------------------------------------------------------
import ROOT, sys, os, time, math
from ROOT import *
import helpers, array
from helpers import wwwpath, length_LHC, mylabel, gitpath, makeTGraph, workpath
from array import array
# -----------------------------------------------------------------------------------
def cv45():

    # current path
    cpath = workpath + 'runs/checkTrajectory6500GeV/4TeV/'
    cpath = '/afs/cern.ch/project/lhc_mib/beamgas/6500GeV_beamsize/'
    trakfiles = [
        # filen name, Xindex, Yindex, markerstyle, 
        # ['/afs/cern.ch/work/r/rkwee/HL-LHC/runs/checkTrajectory6500GeV/madSY_b2.dat', 0,1, kGreen+1, 21, ],
        # [cpath + 'ir1b2_exp001_TRAKFILE.luigi', 2,1, kBlue+1, 27, ],
        # [cpath + 'ir1b2_exp001_TRAKFILE.145', 2,1, kBlue+1, 23, ],
        # [cpath + 'madSYX_b2_thin.dat', 0,1, kGreen-1, 21, 'madx thin seq'], #plots x:s 2,0,  1,0 plots y:s
        # [cpath + 'madSYX_b2_thick.dat', 0,1, kBlue-1, 22, 'madx thick seq'],
        # [cpath + 'ir1_4TeV_settings_from_TWISS_20MeV_b1001_TRAKFILE', 2,1, kRed, 20, 'fluka incoming proton'], # 2,0 plots x:s  1,0 plots y:s]
        # [cpath + 'ir1_4TeV_settings_from_TWISS_20MeV_b1_MYM001_TRAKFILE', 2,1, kMagenta, 23, 'fluka outgoing aproton'], # 2,0 plots x:s  1,0 plots y:s
        # [cpath + 'ir1_4TeV_settings_from_TWISS_20MeV_b1001_TRAKFILE', 2,0, kRed, 20, 'fluka incoming proton'], # 2,0 plots x:s  1,0 plots y:s]
        # [cpath + 'ir1_4TeV_settings_from_TWISS_20MeV_b1_MYM001_TRAKFILE', 2,0, kMagenta, 23, 'fluka outgoing aproton'], # 2,0 plots x:s  1,0 plots y:s
        # [cpath + 'ir1_4TeV_settings_from_TWISS_20MeV_b1_MYM001_fort.89', 5,4, kBlack, 6, 'test size'], # 0cx 1cy 2cz 3x 4y 5z 6J 7A 
        # [cpath + 'ir1_4TeV_settings_from_TWISS_20MeV_b1_orbitDump001_fort.89', 5,4, kBlack, 6, 'test size'], # 0cx 1cy 2cz 3x 4y 5z 6J 7A 
        # [cpath + 'ir1_4TeV_settings_from_TWISS_20MeV_b1_orbitDump001_fort.89', 5,3, kBlack, 6, 'test size'], # 0cx 1cy 2cz 3x 4y 5z 6J 7A 
        # [cpath + 'BEAMGAS.dat', 2,1, kBlack, 6, 'input final BEAMGAS', '_yBEAMGAS', 'y cm'], # 0x 1y 2z 3u 4v 
        # [cpath + 'BEAMGAS.dat', 2,0, kBlack, 6, 'input final BEAMGAS', '_xBEAMGAS', 'x cm'], # 0x 1y 2z 3u 4v 
        # [cpath + 'startBG.dat', 2,1, kBlack, 6, 'input fluka startBG'], # 0x 1y 2z 3u 4v 
        # [cpath + 'startBG.dat', 2,0, kBlack, 6, 'input fluka startBG'], # 0x 1y 2z 3u 4v 
        # [cpath + 'THISISIT.dat', 5,4, kBlack, 6, 'input THISISIT', '_yTHISISIT', 'y cm'], # 0x 1y 2z 3u 4v 
        # [cpath + 'THISISIT.dat', 2,0, kBlack, 6, 'input THISISIT', '_xTHISISIT', 'x cm'], # 0x 1y 2z 3u 4v 
        # [cpath + 'BGAS10.dat', 2,1, kBlack, 6, 'input final BEAMGAS', '_yBGAS10', 'y cm'], # 0x 1y 2z 3u 4v 
        # [cpath + 'BGAS10.dat', 2,0, kBlack, 6, 'input final BEAMGAS', '_xBGAS10', 'x cm'], # 0x 1y 2z 3u 4v 
        # [cpath + 'BGAS.dat', 2,1, kBlack, 6, 'input final BEAMGAS', '_yBGAS', 'y cm'], # 0x 1y 2z 3u 4v repls
        [cpath + 'awked_downselected_fort.89.10.cv53', 2,1, kBlack, 6, 'input final BEAMGAS 6.5 TeV', '_yBGAS', 'y cm'], # 0x 1y 2z 3u 4v repls
        # [cpath + 'awked_downselected_fort.89.10.cv53', 2,0, kBlack, 6, 'input final BEAMGAS 6.5 TeV', '_xBGAS', 'x cm'], # 0x 1y 2z 3u 4v repls

       ]

    rel = ''
    ytitle = ''

    XurMin, XurMax = 5,57000
    XurMin, XurMax = -1, -1

    YurMin, YurMax = -0.02,0.03
    YurMin, YurMax = -0.02, 0.7
    YurMin, YurMax = -1,-1

    cv = TCanvas( 'cv', 'cv', 1000, 600)

    x1, y1, x2, y2 = 0.34, 0.65, 0.9, 0.9
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

    gr = []

    for fn,Xindex,Yindex,color,mStyle,lg,rel,ytitle in trakfiles:
        print 'opening', fn
        [S,Y] = helpers.getListFromColumn([Xindex,Yindex], fn)
        xList, yList = S,Y 
        gr += [ makeTGraph(xList, yList, color, mStyle) ]
        mlegend.AddEntry(gr[-1], lg, lm) 
        mg.Add(gr[-1])

    mg.Draw("a"+lm)
    mg.GetYaxis().SetTitle(ytitle)
    mg.GetXaxis().SetTitle('s [cm]')
    if XurMin != -1:
        mg.GetXaxis().SetRangeUser(XurMin,XurMax)

    if YurMin != -1:
        mg.GetYaxis().SetRangeUser(YurMin,YurMax)
        rel += 'Zoom'

    mlegend.Draw()

    pname = cpath + 'inputFluka6500GeV'+rel+'.root'

    print('Saving file as ' + pname ) 
    cv.Print(pname)

# ----------------------------------------------------------------------------





