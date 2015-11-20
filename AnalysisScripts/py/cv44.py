#!/usr/bin/python
#
# Mar 2015, rkwee
## -------------------------------------------------------------------------------
import pymadx
## -------------------------------------------------------------------------------
import ROOT, sys, os, time, math
from ROOT import *
import helpers, array, random
from helpers import wwwpath, length_LHC, gitpath, length_LHC, getListFromColumn, workpath
from array import array
# -----------------------------------------------------------------------------------
treeName     = "step"
fortformat84 = "X/F:Y/F:Z/F:TXX/F:TYY/F:TZZ/F:CTRACK/F:CMTRACK/F:ATRACK/F"
madxformat   = "Z/F:Y/F:X/F"
files = [
    # '/afs/cern.ch/work/r/rkwee/HL-LHC/runs/checkTrajectory6500GeV/ir1b2_exp001_TRAKFILE.1425',
    # '/afs/cern.ch/work/r/rkwee/HL-LHC/runs/checkTrajectory6500GeV/ir1b2_exp001_TRAKFILE.bdx.1425',
    # '/afs/cern.ch/work/r/rkwee/HL-LHC/runs/checkTrajectory6500GeV/ir1b2_exp001_TRAKFILE.p2.1425',
    # '/afs/cern.ch/work/r/rkwee/HL-LHC/runs/checkTrajectory6500GeV/ir1b2_exp001_TRAKFILE.145',
    # '/afs/cern.ch/work/r/rkwee/HL-LHC/runs/checkTrajectory6500GeV/firstTry/madYS.dat', # this file has the correct shape but it's from the wrong side.
    '/afs/cern.ch/project/lhc_mib/beamsize/6500GeV_beamsize/checkBeamSize/madx_SYX.dat'
    # '/afs/cern.ch/work/r/rkwee/HL-LHC/runs/ir1b2_exp001_TRAKFILE.luigi',
    #'/afs/cern.ch/project/lhc_mib/beamgas/6500GeV_beamsize/checkTrajectory6500GeV/orbitDump/ir1_6500GeV_b1_20MeV_orbitDump001_TRAKFILE',
    ]

debug = 1
col = [
    kBlue,
    kCyan,
    kCyan-2,
    kMagenta+1,
    kMagenta+2,
    kViolet,
    kGreen+2,
    kOrange-2,
    kRed+2,
    ]
def cv44a():

    # twiss file
    #tf = pymadx.Tfs('/afs/cern.ch/work/r/rkwee/HL-LHC/runs/checkTrajectory6500GeV/twiss_b1_80cm_10cm.tfs')
    #tf = pymadx.Tfs('/afs/cern.ch/work/r/rkwee/HL-LHC/LHC-Collimation/SixTrackConfig/6.5TeV/MED800/B1/1cm/MYM_10cm.tfs')
    #tf = pymadx.Tfs('/afs/cern.ch/work/r/rkwee/HL-LHC/LHC-Collimation/SixTrackConfig/6.5TeV/MED800/B2/twiss_lhcb2_med_new_thin_800.tfs')
    #tf = pymadx.Tfs('/afs/cern.ch/work/r/rkwee/HL-LHC/LHC-Collimation/SixTrackConfig/6.5TeV/MED800/B1/twiss_lhcb2_med_new_thin_800_1cm_b2.tfs')
    #tf = pymadx.Tfs('/afs/cern.ch/work/r/rkwee/HL-LHC/LHC-Collimation/SixTrackConfig/6.5TeV/MED800/B1/1cm/twiss_lhcb2_med_new_thin_800_10cm.tfs')
    tf = pymadx.Tfs('/afs/cern.ch/work/r/rkwee/HL-LHC/LHC-Collimation/SixTrackConfig/6.5TeV/background_2015_80cm/twiss_b2_80cm.tfs')
    #tf = pymadx.Tfs('/afs/cern.ch/work/r/rkwee/HL-LHC/runs/checkTrajectory6500GeV/4TeV/twiss_b2.data.thin')
    # tf = pymadx.Tfs('/afs/cern.ch/work/r/rkwee/HL-LHC/runs/checkTrajectory6500GeV/4TeV/twiss_b2.data')

    # -- just dump S and Y
    row = tf.GetRowDict
    colS = tf.GetColumn('S')        
    colY = tf.GetColumn('Y')        
    colX = tf.GetColumn('X')        
    

    fileOutName = '/afs/cern.ch/project/lhc_mib/beamsize/6500GeV_beamsize/checkBeamSize/madx_SYX.dat'
    print 'writing..', fileOutName
    mf = open(fileOutName, 'w')

    for i in range(len(colS)):

        line = str(colS[i]*100.) + '  ' + str(colY[i]*100) + ' ' +str(colX[i]*100.) + '\n'
        mf.write(line)

    mf.close()


# -----------------------------------------------------------------------------
def cv44b():

    for fname in files:

        if fname.count("TRAKFILE"): 
            fortformat = fortformat84

        elif fname.count("mad"): 
            fortformat = madxformat

        else:
            print "no format defined. "

        print("Reading file", fname, "/n Using format", fortformat)

    
        rfoutName = fname +".root"
        print "writing ", rfoutName

        myfile = TFile(rfoutName, 'recreate')
        mytree = TTree(treeName,treeName)
        mytree.ReadFile(fname,fortformat)

        #st*d root
        #for i in range(100): myfile.Delete(treeName + ";" + str(i))

        mytree.Write()
        myfile.Close()
        print 'done'

def cv44c():
    a,b = 1,1
    cv = TCanvas( 'cv', 'cv', a*900, b*700)
    cv.Divide(a,b)
    cv.SetRightMargin(0.3)
    cv.SetLeftMargin(0.2)
    cv.SetTopMargin(0.15)
    x1, y1, x2, y2 = 0.8, 0.65, 0.9, 0.9
    mlegend = TLegend( x1, y1, x2, y2)
    mlegend.SetFillColor(0)
    mlegend.SetFillStyle(0)
    mlegend.SetLineColor(0)
    mlegend.SetShadowColor(0)
    mlegend.SetBorderSize(0)


    hists = []
    for i,fname in enumerate(files):

        hname = 'trajectory_' + fname.split('/')[-1].replace('.','_')

        print "creating histogram", hname
        rf   = TFile.Open(fname + '.root')
        ttrk = rf.Get(treeName)

        xbins, xmin, xmax = 1000,0,55000.
        ybins, ymin, ymax = 2000,-1,1

        hists += [ TH2F(hname, hname, xbins, xmin, xmax, ybins, ymin, ymax)]
        hists[-1].SetMarkerStyle(6)
        hists[-1].SetMarkerColor(col[i])

        # store sum of squares of weights 
        hists[-1].Sumw2()

        var = 'Y:Z'
        cut = ''
        ttrk.Project(hname, var, cut)
        if debug: print 'INFO: Have ', hists[-1].GetEntries(), ' entries in', hname

        if len(hists) == 1: drawOpt = ""
        else: drawOpt = ", SAME"
        hists[-1].Draw(var + drawOpt)
        mlegend.AddEntry(hists[-1], hname.split("trajectory_")[-1].split("_")[0] , "pl")    


    #mlegend.Draw()
    cv.SaveAs('~/public/www/HL-LHC/TCT/6.5TeV/beamgas/traj.root')

# ----------------------------------------------------------------------------


def cv44():

    cv44a()
    cv44b()
    cv44c()


