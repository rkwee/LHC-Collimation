#!/usr/bin/python
#
# plots difference of tracks2.dat and tracks2.h5
# use Scan output of ttree
#
# R Kwee-Hinzmann, Feb 2015
# ---------------------------------------------------------------------------------
import ROOT, sys, glob, os, math, helpers
from ROOT import *
from helpers import *
from array import array
# ---------------------------------------------------------------------------------
def cv28():
    # histname+entrie
    #gStyle.SetOptStat(0111)
    # name, entries, mean, rms
    # gStyle.SetOptStat(1111)
    gStyle.SetOptStat(111111)
    # only entries!
    #gStyle.SetOptStat(10)
    gStyle.SetPalette(1)
    gStyle.SetStatX(0.90)
    gStyle.SetStatY(0.95)
    gStyle.SetTitleX(0.1)
    gStyle.SetTitleY(.955)

    showInfo = 1
    debug = 1

    pathtofile = '/afs/cern.ch/work/r/rkwee/HL-LHC/runs/testHDF5_1Pack/run_test_3/'

    # h5 with fix ## not directly used
    rootfile_hdf5  = pathtofile + 'incr10k_dbg/tracks2.h5-to-dat.rawlist.root'
    rootfile_ascii = pathtofile + 'ascii/tracks2.dat.root'        

    # TTree:Scan output ## for precision
    f_ascii = pathtofile + 'tree_ascii.log'
    f_hdf5  = pathtofile + 'tree_hdf5.log'

    # trajectories
    pathtofile = '/tmp/rkwee/'
    f_ascii = pathtofile + "tracks2_extract.dat"
    f_hdf5  = pathtofile + "tracks2.h5.dat.extract" 

    # LPI file
    pathtofile = ''
    f_ascii = pathtofile + 'H5testFix_HL_TCT5IN_relaxColl_vHaloB1_roundthin/run_05538/LPI_BLP_out.s'
    f_hdf5  = pathtofile + 'H5_HL_TCT5IN_relaxColl_vHaloB1_roundthin/run_05538/LPI_BLP_out.s'

    hDict = {
        # #0 nbin, #1 xmin, #2 xmax, #3 xtitle #4 ytitle #5 vPos #6 YurMin #7 YurMax #8 doLogy
        # 'name':[ 11, -0.5, 10.5,'difference', 'entries', 1],
        'turn':[ 201, -0.5, 200.5,'difference', 'entries', 2],
        's':[ 100, -0.001, 0.02,'difference', 'entries', 3],
        'x':[ 100, -0.001, 0.05,'difference', 'entries', 4],
        'xp':[ 100, -0.001, 0.05,'difference', 'entries', 5],
        'y':[ 100, -0.001, 0.05,'difference', 'entries', 6],
        'yp':[ 100, -0.001, 0.1,'difference', 'entries', 7],
        'dEoverE':[ 100, -0.001, 0.001,'difference', 'entries', 8],
        'type':[ 100, -0.001, 0.1,'difference', 'entries', 9],
        }

    def cleanline(listeof, pattern):
        while pattern in listeof:
            listeof.remove(pattern)
        return listeof

    hKeys = hDict.keys()
    for var in hKeys: 

        vPos  = hDict[var][5]
        hname = var + '_difference'
        nbins, xmin, xmax = hDict[var][0], hDict[var][1], hDict[var][2]
        hist  = TH1F(hname, hname, nbins, xmin, xmax)
        vA, vH = [], []

        with open(f_ascii) as fA:
            for line in fA:
                if line.count("*"):
                    try:                    
                        cline = cleanline(line.split(), "*")
                        vA += [ float(cline[vPos]) ]
                    except ValueError:
                        print "ignoring", line
                    except IndexError:
                        print "ignoring as well", line
                else:
                    try:
                        vA += [ float( line.split()[vPos-1]) ]
                    except:
                        print line.split(), vPos-1
                        print line.split()[vPos-1]

                        print "Couldn't read", line
                        sys.exit()

        with open(f_hdf5) as fH:
            for line in fH:
                if line.count("*"):
                    try:                    
                        cline = cleanline(line.split(), "*")
                        vH += [ float(cline[vPos]) ]
                    except ValueError:
                        print "ignoring", line
                    except IndexError:
                        print "ignoring as well", line
                else:
                    try:
                        vH += [ float(line.split()[vPos-1]) ]
                    except:
                        print "Couldn't read", line
                        sys.exit()

        
        for i,v in enumerate(vH):
            hist.Fill(fabs(fabs(vA[i]) - fabs(vH[i])))

        cv = TCanvas( 'cv'+hname, 'cv'+hname, 10, 10, 900, 600) 
        gPad.SetLogy(1)

        x1, y1, x2, y2 = 0.2, 0.98, 0.84, 0.9
        hist.Draw('hist')
        lab = mylabel(60)
        lab.DrawLatex(x1, y1-0.1, 'difference in ' + var)

        pname = wwwpath
        # pname += 'TCT/4TeV/hdf5/checkPrecision/' + hname  +'.png'
        pname += 'TCT/4TeV/hdf5/trajectories/LPI_' + hname  +'.png'
        cv.SaveAs(pname)
                
