#!/usr/bin/python
#
# May 2013, rkwee
# -----------------------------------------------------------------------------------
# from optparse import OptionParser
# use once to write out rootfile
# initially written by Daniele
## -------------------------------------------------------------------------------
import ROOT, sys, glob, os, commands
from ROOT import *
import helpers, gzip, time
from helpers import *
## -------------------------------------------------------------------------------
def lossmap(beam,path,tag):

    print ' losses on collimator '

    debug = 1

    if not path.endswith('/'):
        path += '/'

    tH = time.time()

    # path  = '/afs/cern.ch/work/r/rkwee/HL-LHC/runs/oldExe/'
    f1    = path + 'LPI_BLP_out'+tag+'.s'
    f2    = path + 'coll_summary'+tag+'.dat'
    f3    = helpers.source_dir + 'NewColl7TeVB'+beam.split('b')[-1]+'/CollPositions.'+beam+'.dat'

    cmd = "perl -pi -e 's/\\0/ /g' " + f1
    print cmd
    os.system(cmd)             

    # loss positions
    losses = []
   
    with open(f1) as myfile:
        
        for line in myfile:
            
            line  = line.rstrip()
            
            losses += [float(line.split()[2])]

    names_sum, nabs, length = [],[],[]
    
    with open(f2) as myfile:
        for line in myfile:
            
            line = line.rstrip()
            
            if line.count("nabs"):
                continue

            names_sum  += [ line.split()[1] ]
            nabs   += [ float(line.split()[3]) ]
            length += [ float(line.split()[6]) ]

    names_pos, coll_pos = [],[]
    
    with open(f3) as myfile:

        for line in myfile:

            line = line.rstrip()

            if line.count("Pos"):
                continue

            names_pos  += [ line.split()[1] ]
            coll_pos   += [ float(line.split()[2]) ]

    
    # -- plot 
    tA = time.time()
    print(str(tA-tH)+" for filling data into lists")
    
    tcs = tag.split('_')[-1]

    nbins, xmin, xmax = 10*length_LHC,0., length_LHC

    coll_loss = TH1F("coll_loss" + tag,"coll_loss" + tag,nbins, xmin, xmax)
    cold_loss = TH1F("cold_loss" + tag,"cold_loss" + tag,nbins, xmin, xmax)
    warm_loss = TH1F("warm_loss" + tag,"warm_loss" + tag,nbins, xmin, xmax)

    xtitle = 's [m]'
    ytitle = "Cleaning inefficiency #eta"
    coll_loss.GetXaxis().SetTitleOffset(.9)
    coll_loss.GetYaxis().SetTitleOffset(1.06)
    coll_loss.GetXaxis().SetTitle(xtitle)
    coll_loss.GetYaxis().SetTitle(ytitle)
    
    meter  = range(10)
    n_warm = len(warm)
    k_warm = [2*k for k in range(n_warm/2)]

    f1_nlines = len(losses)
    f2_nlines = len(names_sum)
    f3_nlines = len(names_pos)

    # -- cold and warm losses for 10th of 1 meter
    for j in range(10):           
        cnt = 0                                                                                                   
        for i in range(f1_nlines):

            for k in k_warm:                
                if losses[i] >= warm[k] and losses[i] <= warm[k+1]:
                    warm_loss.Fill(losses[i])                                                                   
                elif k<n_warm-1 and losses[i] >= warm[k+1] and losses[i] <= warm[k+2]:
                    cold_loss.Fill(losses[i])                                         
                else:
                    cnt += 1        

    print "cnt of neither warm nor cold losses =", cnt, "in file LPI"

    # -- losses on collimator
    # loop over coll_summary file
    for i in range(f2_nlines):

        # loop over CollPositions
        for j in range(f3_nlines):

            # if we're at the same collimator
            if names_sum[i] == names_pos[j]:

                coll_loss.Fill(coll_pos[j],nabs[i])

    tB = time.time()
    print(str(tB -tA)+" for filling histograms")

    return coll_loss, cold_loss, warm_loss

# ------------------------------------------------------------------------------------

def benchmarkEff(rfname,cvName):

    print'opening', rfname

    if not os.path.exists(rfname):
        print 'missing file', rfname
        sys.exit()

    rf    = TFile.Open(rfname)
    pList = rf.Get(cvName).GetListOfPrimitives()

    print 'In', cvName
    for obj in pList:
        if isinstance(obj, TH1):
            print 'found frame histogram', obj.GetName()

# ------------------------------------------------------------------------------------

def check_npart(thispath,appendix):

    index = 1
    
    # l = sum_npart(fname,index)
    #    print("npart of " + fname + " is " + str(l))    

    # ----

    # fname = thispath + "tracks2.dat"
    index = 0
    
    #l = count_npart(fname,index)
    #print("npart of " + fname + " is " + str(l))    

    # ----
    #fname = thispath + "survival"+appendix+".dat"
    #index = 1
    
    #l = count_npart(fname,index)
   
    #print("npart of " + fname + " is " + str(l))    

    # ----
    fname = thispath + "LPI_BLP_out"+appendix+".s"
    index = 1
    
    l = count_npart(fname,index)
   
    print("npart of " + fname + " is " + str(l))    
    # ----

    fname = thispath + "FirstImpacts"+appendix+".dat"
    index = 0
    
    ll = count_npart(fname,index)
    print("npart of " + fname + " is " + str(ll))

# ------------------------------------------------------------------------------------
if __name__ == "__main__":
    gROOT.SetBatch()
    gROOT.Reset()
    gROOT.SetStyle("Plain")
    gROOT.LoadMacro("/afs/cern.ch/user/r/rkwee/scratch0/miScripts/py/AtlasStyle.C")
    gROOT.LoadMacro("/afs/cern.ch/user/r/rkwee/scratch0/miScripts/py/AtlasUtils.C")
    SetAtlasStyle()

    #gStyle.SetOptStat(1000100110)
    gStyle.SetPalette(1)
    gStyle.SetStatX(0.95)
    gStyle.SetStatY(0.95)
    gStyle.SetTitleX(0.1)
    gStyle.SetTitleY(.955)

    gStyle.SetOptStat(0)
    #gStyle.SetCanvasColor(10)
    # gStyle.SetPalette(100,prepPalette())
    tag = '_TCSG.B5L7.B2'
    thispath = '/afs/cern.ch/work/r/rkwee/HL-LHC/runs/7TeVPostLS1' + tag + '/run_0011/'
    beam,path,tag = 'b2', thispath, '',0
    lossmap(beam,path,tag)
  
    print '--- fin ---'
