#!/usr/bin/python
#
# Mar 2017, rkwee
## -------------------------------------------------------------------------------
import pymadx
## -------------------------------------------------------------------------------
import ROOT, sys, os, time, math
from ROOT import *
import lossmap, helpers, array
from helpers import wwwpath, length_LHC, mylabel, gitpath, makeTGraph
from array import array
# -----------------------------------------------------------------------------------
def cv90():

    # twiss file

    tf = pymadx.Tfs("/afs/cern.ch/work/r/rkwee/HL-LHC/LHC-Collimation/SixTrackConfig/7TeV/hilumiLHC/TCThaloStudies_relaxedCollSettings/b1/twiss.hllhcv1.b1.tfs")

    BETX = tf.GetColumn('BETX')
    BETY = tf.GetColumn('BETY')
    ALFX = tf.GetColumn('ALFX')
    ALFY = tf.GetColumn('ALFY')
    X    = tf.GetColumn('X')
    Y    = tf.GetColumn('Y')
    PX   = tf.GetColumn('PX')
    PY   = tf.GetColumn('PY')
    S    = tf.GetColumn('S')

    colls = ['TCTH.5L1.B1', 'TCTH.4L1.B1',#'TCTVA.5L1.B1', 'TCTVA.4L1.B1',
             'TCTH.5L5.B1', 'TCTH.4L5.B1',#'TCTVA.5L5.B1', 'TCTVA.4L5.B1',
             ]

    for collName in colls:
        mux  = tf.GetColumnDict('MUX')[collName]
        muy  = tf.GetColumnDict('MUY')[collName]

        print "mux",mux, "muy", muy, collName




