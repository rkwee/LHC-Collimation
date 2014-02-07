#!/usr/bin/python
#
# R Kwee-Hinzmann, 2013
# ---------------------------------------------------------------------------------
import ROOT, sys, glob, os, math, helpers, createTTree_dict
from ROOT import *
from helpers import *
# ---------------------------------------------------------------------------------
# plotting from several rootfiles of the same format!!:
treeName     = "particle"
fortformat66 = "event/I:generation/I:particle/I:energy_ke/F:weight/F:x/F:y/F:xp/F:yp/F:age/F:energy_tot/F:x_interact/F:y_interact/F:z_interact/F:t_interact/F"
fortformat30 = "event/I:particle/I:generation/I:weight/F:x/F:y/F:xp/F:yp/F:energy_tot/F:energy_ke/F:age/F:x_interact/F:y_interact/F:z_interact/F"
# ---------------------------------------------------------------------------------
# fname (=input) are the merged fort.66 or fort.30 file from fluka runs"
def ctree(fname):

    debug = 1

    if fname.endswith("30"): 
        fortformat = fortformat30
        if debug: print "Using HL format", '.'*10
    else: 
        fortformat = fortformat66
        if debug: print "Using 4 TeV format", '.'*10

    # -----------------------------------------------------------------------------
    
    rfoutName = fname +".root"
    print "writing ", rfoutName
    
    myfile = TFile(rfoutName, 'recreate')
    mytree = TTree(treeName,treeName)
    mytree.ReadFile(fname,fortformat)

    #st*d root
    for i in range(100): myfile.Delete(treeName + ";" + str(i))

    mytree.Write()
    myfile.Close()
    print 'done'
    return rfoutName
# ---------------------------------------------------------------------------------
