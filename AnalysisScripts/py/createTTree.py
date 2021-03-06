#!/usr/bin/python
#
# R Kwee-Hinzmann, 2013
# ---------------------------------------------------------------------------------
import ROOT, sys, glob, os, math, helpers
from ROOT import *
from helpers import *
# ---------------------------------------------------------------------------------
# plotting from several rootfiles of the same format!!:
treeName     = "particle"
fortformat66 = "event/I:generation/I:particle/I:energy_ke/F:weight/F:x/F:y/F:xp/F:yp/F:age/F:energy_tot/F:x_interact/F:y_interact/F:z_interact/F:t_interact/F"
# for 4 TeV BG w/bs, 6.5 TeV BG bs too.
fortformat67 = "event/I:generation/I:particle/I:energy_ke/F:weight/F:x/F:y/F:xp/F:yp/F:age/F:energy_tot/F:x_interact/F:y_interact/F:z_interact/F:t_interact/F:x_track/F:y_track/F:z_track/F:x_origmu/F:y_origmu/F:z_origmu/F"
#fortformat67 = "event/I:generation/I:particle/I:energy_ke/F:weight/F:x/F:y/F:xp/F:yp/F:age/F:energy_tot/F:x_interact/F:y_interact/F:z_interact/F:t_interact/F:x_origmu/F:y_origmu/F:z_origmu/F"
fortformat30 = "event/I:particle/I:generation/I:weight/F:x/F:y/F:xp/F:yp/F:energy_tot/F:energy_ke/F:age/F:x_interact/F:y_interact/F:z_interact/F"
fortformat31 = "event/I:generation/I:particle/I:weight/F:x/F:y/F:xp/F:yp/F:energy_tot/F:energy_ke/F:age/F:x_interact/F:y_interact/F:z_interact/F"
# only for new Halo at 4 TeV and offmom 4 TeV and maybe 6.5 TeV halo
#fortformat30 = "event/I:particle/I:generation/I:weight/F:x/F:y/F:xp/F:yp/F:energy_tot/F:energy_ke/F:age/F:x_origmu/F:y_origmu/F:z_origmu/F"
fortformat84 = "NIN/F:ICOLIN/F:XHELP/F:YHELP/F:ZHELP/F:XPHELP/F:YPHELP/F:ZPHELP/F"
fortformat89 = "CXTRCK/F:CYTRCK/F:CZTRCK/F:XTRACK/F:YTRACK/F:ZTRACK/F:JTRACK/F:NCASE/I:ATRACK/F" ## sometimes JTRACK is missing in 4 TeV files..
#fortformat89 = "CXTRCK/F:CYTRCK/F:CZTRCK/F:XTRACK/F:YTRACK/F:ZTRACK/F:NCASE/I:ATRACK/F"
impactsformat= "icoll/I:c_rotation/F:s/F:x/F:xp/F:y/F:yp/F:nabs/I:np/I:ntu/I"
tracks2format= "name/I:turn/I:s/F:x/F:xp/F:y/F:yp/F:dEoverE/F:type"
antInpformat = "ipart/I:icoll/I:x/F:y/F:s/F:xp/F:yp/F:zp"
flukaBGformat= "XIN/F:YIN/F:ZIN/F:UIN/F:VIN/F:TIN" # also old 4 TeV input format of source-forced-interactions-TCT.f
fortformat91= "randomID/F"
# ---------------------------------------------------------------------------------
# fname (=input) are the merged fort.66 or fort.30 file from fluka runs"
def ctree(fname):

    debug = 1

    if fname.endswith("30"): 
        fortformat = fortformat30

    elif fname.endswith("31"): 
        fortformat = fortformat31

    elif fname.endswith("66"): 
        fortformat = fortformat66

    elif fname.endswith("67"): 
        fortformat = fortformat67

    elif fname.endswith("84"): 
        fortformat = fortformat84

    elif fname.count("fort.89") or fname.endswith("89"):
        fortformat = fortformat89

    elif fname.endswith("91"): 
        fortformat = fortformat91

    elif fname.count('impacts_real'):
        fortformat = impactsformat

    elif fname.count("tracks2"):
        fortformat = tracks2format

    elif fname.count("anton"):
        fortformat = antInpformat

    elif fname.count("BGAS") or fname.count("startBG") or fname.count("tIR1"):
        fortformat = flukaBGformat

    else:
        print "no format defined. "
        #fortformat = flukaBGformat
  
        return

    print("Reading file", fname, "/n Using format", fortformat)
    # -----------------------------------------------------------------------------
    
    #rfoutName = projectpath + 'HaloRun2/valBG4TeV2/' + fname.split("/")[-1] +".root"
    rfoutName =  rfoutName = fname +".root"
    print "writing ", rfoutName
    
    myfile = TFile(rfoutName, 'recreate')
    mytree = TTree(treeName,treeName)
    mytree.ReadFile(fname,fortformat)

    #st*d root
    #for i in range(100): myfile.Delete(treeName + ";" + str(i))

    mytree.Write()
    myfile.Close()
    print 'done'
    return rfoutName
# ---------------------------------------------------------------------------------
