#!/usr/bin/python
#
#
# Nov  2013, rkwee
## -------------------------------------------------------------------------------
import ROOT, sys, glob, os
from ROOT import *
from helpers import workpath, addCol
## -------------------------------------------------------------------------------
if 1:
    sometext = 'HL hybrid case'
    csfile_H = workpath + 'runs/H5_HL_TCT5LOUT_relaxColl_hHaloB1_roundthin/coll_summary_H5_HL_TCT5LOUT_relaxColl_hHaloB1_roundthin.dat'
    csfile_V = workpath + 'runs/H5_HL_TCT5LOUT_relaxColl_vHaloB1_roundthin/coll_summary_H5_HL_TCT5LOUT_relaxColl_vHaloB1_roundthin.dat'
    Ntct_H   = 8242+1496 # wc -l  H5_HL_TCT5LOUT_relaxColl_*HaloB1_roundthin/i*52*txt
    Ntct_V   = 778+1575 # wc -l  H5_HL_TCT5LOUT_relaxColl_*HaloB1_roundthin/i*53*txt
    NtotBeam = 2.2e11*2808
elif 0:
    sometext = 'HL hybrid case'
    csfile_H = workpath + 'runs/H5_HL_TCT5IN_relaxColl_hHaloB1_roundthin/coll_summary_H5_HL_TCT5IN_relaxColl_hHaloB1_roundthin.dat'
    csfile_V = workpath + 'runs/H5_HL_TCT5IN_relaxColl_vHaloB1_roundthin/coll_summary_H5_HL_TCT5IN_relaxColl_vHaloB1_roundthin.dat'
    Ntct_H   = 8242+1496 # wc -l  H5_HL_TCT5IN_relaxColl_*HaloB1_roundthin/i*52*txt
    Ntct_V   = 778+1575 # wc -l  H5_HL_TCT5IN_relaxColl_*HaloB1_roundthin/i*53*txt
    NtotBeam = 2.2e11*2808
elif 0:
    sometext = 'HL case'
    csfile_H = workpath + 'runs/TCT/ats-HL_LHC_1.0/nominal_settings/hor-B1/coll_summary_hor-B1.dat'
    csfile_V = workpath + 'runs/TCT/ats-HL_LHC_1.0/nominal_settings/ver-B1/coll_summary_ver-B1.dat'
    Ntct_H   = 15793 # ats-HL_LHC_1.0/nominal_settings/impacts_real_on_52_TCTH.4L1.B1.dat
    Ntct_V   = 5817 # ats-HL_LHC_1.0/nominal_settings/impacts_real_on_53_TCTVA.4L1.B1.dat
    NtotBeam = 2.2e11*2808
# ---------------------------------------------------------------------------------
else:
    sometext = '4 TeV case'
    csfile_H = workpath + 'runs/TCT_4TeV_B2hHalo/coll_summary_TCT_4TeV_B2hHalo.dat'
    csfile_V = workpath + 'runs/TCT_4TeV_B2vHalo/coll_summary_TCT_4TeV_B2vHalo.dat'
    Ntct_V   = 3 # wc -l TCT_4TeV_B2vHalo/impacts_real_on_71_TCTH.4R1.B2_B2vHalo.dat
    Ntct_H   = 452 # wc -l TCT_4TeV_B2vHalo/impacts_real_on_72_TCTVA.4R1.B2_B2vHalo.dat
    NtotBeam = 1.5e11*1380
    nprim_4TeV = 1.57e7 # number of simulated primary interactions in fluka
# ---------------------------------------------------------------------------------
def cv07():
    # used to be  doNormR() from flukaText2root:
    # normlise by loss rate

    print sometext

    # lifetime
    tau_1   = 12*60 # loose beam in 12 minutes
    tau_2   = 100*60*60 # in 100 h

    Ntot_H  = addCol(csfile_H, 4-1)
    R1det_H = Ntct_H/Ntot_H * NtotBeam/tau_1
    R2det_H = Ntct_H/Ntot_H * NtotBeam/tau_2

    print "total #p lost in 200 turns _H", Ntot_H

    Ntot_V  = addCol(csfile_V, 4-1)
    R1det_V = Ntct_V/Ntot_V * NtotBeam/tau_1
    R2det_V = Ntct_V/Ntot_V * NtotBeam/tau_2

    print "total #p lost in 200 turns _V", Ntot_V
    print "fraction #p lost in 200 turns  _V", Ntct_V/Ntot_V

    R1det = int(0.5*( R1det_H + R1det_V ))
    R2det = int(0.5*( R2det_H + R2det_V ))

    print  "rate at det if beam is lost in 12 min'",R1det, 'Hz'
    print  "rate at det if beam is lost in 100h",R2det, 'Hz'




