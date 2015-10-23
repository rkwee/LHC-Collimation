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
from array import array
## -------------------------------------------------------------------------------
def lossmap(beam,path,tag,f3, shiftVal):

    print ' losses on collimator ', beam,path,tag,f3,shiftVal

    debug = 1

    if not path.endswith('/'):
        path += '/'

    tH = time.time()

    f1    = path + 'LPI_BLP_out'+tag+'.s'
    f2    = path + 'coll_summary'+tag+'.dat'

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

    #print "DEBUG: nabs", nabs
    names_pos, coll_pos = [],[]
    
    with open(f3) as myfile:

        for line in myfile:

            line = line.rstrip()

            if line.count("Pos"):
                continue

            try:
                names_pos  += [ line.split()[1] ]
                coll_pos   += [ float(line.split()[2]) ]
            except IndexError:
                print "IndexError. Line is ",line
    
    # -- plot 
    tA = time.time()
    print(str(tA-tH)+" for filling data into lists")

    nbins, xmin, xmax = int(10*length_LHC),shiftVal-length_LHC, shiftVal
    coll_loss = TH1F("coll_loss" + tag,"coll_loss" + tag,nbins, xmin, xmax)
    cold_loss = TH1F("cold_loss" + tag,"cold_loss" + tag,nbins, xmin, xmax)
    warm_loss = TH1F("warm_loss" + tag,"warm_loss" + tag,nbins, xmin, xmax)

    # # -- makes the lines fat

    # myX = [xmin+i*10 for i in range(1,length_LHC+1)]
    # myX = array('f', myX)

    # coll_loss = TH1F("coll_loss" + tag,"coll_loss" + tag,len(myX)-1, myX)
    # cold_loss = TH1F("cold_loss" + tag,"cold_loss" + tag,len(myX)-1, myX)
    # warm_loss = TH1F("warm_loss" + tag,"warm_loss" + tag,len(myX)-1, myX)

    coll_loss.SetLineWidth(1)
    warm_loss.SetLineWidth(1)
    cold_loss.SetLineWidth(1)

    xtitle = 's [m]'
    ytitle = "Cleaning inefficiency #eta [m^{-1}]"
    coll_loss.GetXaxis().SetTitleOffset(.9)
    coll_loss.GetYaxis().SetTitleOffset(1.06)
    coll_loss.GetXaxis().SetTitle(xtitle)
    coll_loss.GetYaxis().SetTitle(ytitle)
    cold_loss.GetXaxis().SetTitleOffset(.9)
    cold_loss.GetYaxis().SetTitleOffset(1.06)
    cold_loss.GetXaxis().SetTitle(xtitle)
    cold_loss.GetYaxis().SetTitle(ytitle)
    warm_loss.GetXaxis().SetTitleOffset(.9)
    warm_loss.GetYaxis().SetTitleOffset(1.06)
    warm_loss.GetXaxis().SetTitle(xtitle)
    warm_loss.GetYaxis().SetTitle(ytitle)
    
    meter  = range(10)
    n_warm = len(warm)
    k_warm = [2*k for k in range(n_warm/2)]

    # -- cold and warm losses for 10th of 1 meter
    for j in range(10):           
        cnt = 0                                                                                                   
        for i in range(len(losses)):

            for k in k_warm:

                shifted_loss = losses[i]
                if shifted_loss >= xmax:
                    shifted_loss -= length_LHC
                
                if losses[i] >= warm[k] and losses[i] <= warm[k+1]:
                    warm_loss.Fill(shifted_loss) 
                elif k<n_warm-1 and losses[i] >= warm[k+1] and losses[i] <= warm[k+2]:
                    cold_loss.Fill(shifted_loss)                     
                else:
                    cnt += 1        

    # -- losses on collimator
    # loop over coll_summary file
    #print "DEBUG: names_sum", names_sum
    #print "DEBUG: names_pos", names_pos
    for i in range(len(names_sum)):

        # loop over CollPositions
        for j in range(len(names_pos)):

            # if we're at the same collimator
            if names_sum[i] == names_pos[j]:

                shifted_losspos = coll_pos[j]

                # shift
                if shifted_losspos >= xmax:
                    shifted_losspos -= length_LHC

                # normalise the weight nabs by collimator length
                coll_loss.Fill(shifted_losspos,nabs[i]/length[i])

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

