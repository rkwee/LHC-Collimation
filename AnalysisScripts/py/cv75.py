#!/usr/bin/python
#
# Mar 2015, rkwee
## -------------------------------------------------------------------------------
#
#
# mix of cv39, cv74 to plot twiss beamsize with fluka beamsize
# 
import pymadx
## -------------------------------------------------------------------------------
import ROOT, sys, os, time, math
from ROOT import *
import lossmap, helpers, array
from helpers import wwwpath, length_LHC, mylabel, gitpath, makeTGraph, projectpath
from array import array
# -----------------------------------------------------------------------------------
def getStatErrFromTProf(mt, varComp):

    # make 1 bin 1cm
    xnbins, xmin, xmax = 54693,0.,54693.

    # cut out shitty trajectory
    ynbins, ymin, ymax = 300, -0.15, 2.

    # -- getting the mean value
    # 1.
    hnameProfS = varComp + 'vSProf'
    CvSProfS = TProfile(hnameProfS, hnameProfS, xnbins, xmin, xmax, ymin, ymax, "S")

    var  = varComp+':ZTRACK'
    cuts = ''

    mt.Project(hnameProfS, var, cuts)
    print "Found", CvSProfS.GetEntries(), "entries in", hnameProfS
    print "binerror",CvSProfS.GetBinError(5334)
    statErrors = [ CvSProfS.GetBinError(bin) for bin in range(1,xnbins+1) ]

    print "returning a list of length ", len(statErrors)
    return statErrors

# -----------------------------------------------

def cv75():

    # twiss file
    # tf = pymadx.Tfs('/afs/cern.ch/work/r/rkwee/HL-LHC/LHC-Collimation/SixTrackConfig/6.5TeV/MED800/B1/twiss_lhcb1_med_new_thin_800.tfs')
    energy = "4TeV"
    gamma_rel = 4e3/0.938
    betaStar = 0.6
    # tf = pymadx.Tfs('/afs/cern.ch/work/r/rkwee/HL-LHC/LHC-Collimation/SixTrackConfig/6.5TeV/MED800/B1/1cm/twiss_lhcb1_med_new_thin_800_1cm.tfs')
    tf = pymadx.Tfs("/afs/cern.ch/work/r/rkwee/HL-LHC/LHC-Collimation/SixTrackConfig/4TeV/beamgas/twiss_4tev_b1.data")
    gamma_rel = 6.5e3/0.938
    gamma_rel = 4.e3/0.938
    energy = '4TeV'

    BETX = tf.GetColumn('BETX')
    BETY = tf.GetColumn('BETY')
    S    = tf.GetColumn('S')

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
    # XurMin, XurMax = length_LHC-550, length_LHC
    # rel = '_orbit_IR1Left_4TeV'
    # lShift = 0.5

    XurMin, XurMax = 0,548.
    rel = '_compsigma_IR1Right_4TeV'
    # rel = '_sigma_IR1Right_4TeV'
    # rel = '_orbit_IR1_4TeV'
    lShift = 0.0

    # XurMin, XurMax = IP5-300, IP5+300
    # rel = '_IP5'
    # XurMin, XurMax = IP8-300, IP8+300
    # rel = '_IP8'
    # -----------------------------------------------
    # fluka part from cv74

    filename = projectpath + 'HaloRun2/valBG4TeV2/oneFileAllTraj.dat.89.root'
    filename = projectpath + 'HaloRun2/valBG4TeV2/traj_fort.89.10.root'

    print "Opening", filename
    rf = TFile.Open(filename)
    mt = rf.Get("particle")
    SIGYflu = getStatErrFromTProf(mt, "YTRACK")
    srange_meter = [0.01*s for s in range(1,54694)]

    a,b = 1,1
    cv = TCanvas( 'cv', 'cv', a*2100, b*900)
    cv.Divide(a,b)
    cv.cd(1)

    x1, y1, x2, y2 = 0.5-lShift, 0.65, 0.9-lShift, 0.9
    mlegend = TLegend( x1, y1, x2, y2)
    mlegend.SetFillColor(0)
    mlegend.SetFillStyle(0)
    mlegend.SetLineColor(0)
    mlegend.SetTextSize(0.05)
    mlegend.SetShadowColor(0)
    mlegend.SetBorderSize(0)

    mg = TMultiGraph()
    # marker in legend
    lm = 'lp'

    emittance_norm = 3.5e-6
    emittance_geo = emittance_norm/gamma_rel

    SIGX = [math.sqrt(betax * emittance_geo)*100 for betax in BETX]
    SIGY = [math.sqrt(betay * emittance_geo)*100 for betay in BETY]

    xList, yList, color, mStyle, lg = S_shifted, SIGX, kGreen-1, 22, '#sigma_{x} from Twiss'
    g0 = makeTGraph(xList, yList, color, mStyle)
    mlegend.AddEntry(g0, lg, lm)    
    mg.Add(g0)

    xList, yList, color, mStyle, lg = S_shifted, SIGY, kGreen-2, 20, '#sigma_{y} from Twiss'
    g1 = makeTGraph(xList, yList, color, mStyle)
    mlegend.AddEntry(g1, lg, lm)    
    mg.Add(g1)
    ytitle = 'beam size [cm]'

    print len(S_shifted)
    
    xList, yList, color, mStyle, lg = srange_meter, SIGYflu, kGreen+1, 21, '#sigma_{y} from fluka'
    g1 = makeTGraph(xList, yList, color, mStyle)
    mlegend.AddEntry(g1, lg, lm) 
    mg.Add(g1)

    # xList, yList, color, mStyle, lg = S_shifted, PY, kBlue+1, 27, "y'"
    # g3 = makeTGraph(xList, yList, color, mStyle)
    # mlegend.AddEntry(g3, lg, lm) 
    # mg.Add(g3)


    mg.Draw("a"+lm)

    l = TLine()
    l.SetLineStyle(1)
    YurMin, YurMax = 0, 0.0019
    l.SetLineColor(kRed)

    s = 22.6
    l.DrawLine(s,YurMin,s,YurMax)

    s = 59.
    l.DrawLine(s,YurMin,s,YurMax)

    s = 153.
    l.DrawLine(s,YurMin,s,YurMax)

    s = 269.
    l.DrawLine(s,YurMin,s,YurMax)

    mg.GetYaxis().SetTitle(ytitle)
    mg.GetXaxis().SetTitle('s [m]')
    if XurMin != -1:
        mg.GetXaxis().SetRangeUser(XurMin,XurMax)

    mlegend.Draw()
    pname  = wwwpath
    subfolder = 'TCT/'+energy+'/beamgas/'
    pname += subfolder + 'twiss_b1'+rel+'.png'

    print('Saving file as ' + pname ) 
    cv.Print(pname)

# ----------------------------------------------------------------------------




