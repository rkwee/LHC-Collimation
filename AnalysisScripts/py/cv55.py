#!/usr/bin/python
#
# June 2015, rkwee
## -------------------------------------------------------------------------------
import ROOT
from ROOT import *
import helpers
from helpers import wwwpath, length_LHC, mylabel
from createTTree import treeName
# from cv47->54
# -----------------------------------------------------------------------------------

def cv55():

    showInfo = 1

    # format is: XIN(NIN), YIN(NIN), ZIN(NIN), UIN(NIN), VIN(NIN),TIN(NIN)
    #    bgInput = '/afs/cern.ch/project/lhc_mib/beamsize/4TeV_beamsize/BGAS10.dat.root'
    bgInput = ' /afs/cern.ch/work/r/rkwee/HL-LHC/LHC-Collimation/FlukaRoutines/6.5TeV/beamgas/BGASB.dat.root'
    #bgInput = ' /afs/cern.ch/project/lhc_mib/beamgas/6500GeV_beamsize/downselected_fort.89.10.cv53.root'
    #    bgInput = ' /afs/cern.ch/project/lhc_mib/merge/awked_fort.89.29m.txt.root'
    #bgInput = ' /afs/cern.ch/project/lhc_mib/merge/awked_fort.89.44050.txt.root' # gives seg fault
    #bgInput = ' /afs/cern.ch/project/lhc_mib/merge/awked_fort.89_44.txt.root'
    rf = TFile.Open(bgInput)
    mt = rf.Get(treeName)

    xVar, yVar, zVar, dircosX, dircosY = "XIN", "YIN", "ZIN", "UIN", "VIN"
    if bgInput.count("89"): xVar, yVar, zVar, dircosX, dircosY = "XTRACK", "YTRACK", "ZTRACK","CXTRCK", "CYTRCK"
    # "CXTRCK/F:CYTRCK/F:CZTRCK/F:XTRACK/F:YTRACK/F:ZTRACK/F:JTRACK/F:NCASE/I:ATRACK/F"

    hDict = {
        ##key: hname : #0var #1 xnbins, #2 xmin, #3xmax, #4 cutstring #5 xtitle, #6 ytitle, #7 lab spos,

        # 'x_MQXA.1R1':[xVar, 100,-1.,1., zVar + " > 29.3345e2 && "+ zVar +" < 29.3355e2",'x [cm]', 'entries', "s = 29.335 m,#sigma_{x} = 0.08522 cm"],
        # 'y_MQXA.1R1':[yVar, 100,-.5,1.5, zVar + " > 29.3345e2 && "+ zVar +" < 29.3355e2",'y [cm]', 'entries', "s = 29.335 m,#sigma_{y} = 0.06288 cm"],
        # 'xp_MQXA.1R1':[dircosX, 100,-3.e-4,3.e-4, zVar + " > 29.3345e2 && "+ zVar +" < 29.3355e2",'xp [rad]', 'entries', "s = 29.335 m,xp = -9.1e-10 rad,#sigma_{xp} = 5.9e-07 rad"],
        # 'yp_MQXA.1R1':[dircosY, 100,0.1e-3,1.e-4, zVar + " > 29.3345e2 && "+ zVar +" < 29.3355e2",'yp [rad]', 'entries', "s = 29.335 m,yp = -5.4374e-05 rad,#sigma_{yp} = 8.0e-07 rad"],

#         'x_MQXB.B2R1':[xVar, 100,-1.,1., zVar + " > 44.04999e2 && "+ zVar +" < 44.05001e2",'x [cm]', 'entries', "s = 44.05 m,#sigma_{x} = 0.11212 cm"],
# #        'y_MQXB.B2R1':[yVar, 100,-.5,1.5, zVar + " > 44.04999e2 && "+ zVar +" < 44.05001e2",'y [cm]', 'entries', "s = 44.05 m,#sigma_{y} = 0.0850 cm"],
#         # 'xp_MQXB.B2R1':[dircosX, 100,-3.e-4,3.e-4, zVar + " > 44.04999e2 && "+ zVar +" < 44.05001e2",'xp [rad]', 'entries', "s = 44.05 m,xp = 6.99e-10 rad,#sigma_{xp} = 4.5e-07 rad"],
# #        'yp_MQXB.B2R1':[dircosY, 100,0.1e-3,1.e-4, zVar + " > 44.04999e2 && "+ zVar +" < 44.05001e2",'yp [rad]', 'entries', "s = 44.05 m,yp = 0.292e-3 rad,#sigma_{yp} = 5.9e-07 rad"],

        # 'x_MQXA.3R1':[xVar, 20,-0.6, 0.6, zVar + " > 53.3e2  && "+ zVar +" < 53.4e2",'x [cm]', 'entries', "s = 53.335 m,#sigma_{x} = 0.08211 cm"],
        # 'y_MQXA.3R1':[yVar, 20,0.,1.4, zVar + " > 53.3e2  && "+ zVar +" < 53.4e2",'y [cm]', 'entries', "s = 53.335 m,#sigma_{y} = 0.1165 cm"],
#        'xp_MQXA.3R1':[dircosX, 100,-1e-5,1.e-5, zVar + " > 53.3e2  && "+ zVar +" < 53.4e2",'xp [rad]', 'entries', "s = 53.335 m,xp = 5e-12 rad"],
        'yp_MQXA.3R1':[dircosY, 20,1e-6,-1.e-4 , zVar + " > 53.3e2  && "+ zVar +" < 53.4e2",'yp [rad]', 'entries', "s = 53.335 m,yp = 4.969e-05 rad"],

        }

    lab = mylabel(42)
    x1, y1, x2, y2 = 0.2, 0.98, 0.84, 0.9
    for hname in hDict.keys():

        xnbins, xmin, xmax     = hDict[hname][1],hDict[hname][2],hDict[hname][3]
        print   xnbins, xmin, xmax
        hist = TH1F(hname, hname, xnbins, xmin, xmax)

        xtitle, ytitle = hDict[hname][5],hDict[hname][6]
        hist.GetXaxis().SetTitle(xtitle)
        hist.GetYaxis().SetTitle(ytitle)

        #fit1 = hist.GetFunction("gaus")

        #fit1.Draw()

        # store sum of squares of weights 
        hist.Sumw2()

        var = hDict[hname][0]
        if showInfo: print 'INFO: will fill these variables ', var, 'into', hname

        cut = hDict[hname][4]

        if showInfo: print 'INFO: will apply a cut of ', cut, 'to', hname
        mt.Project(hname, var, cut)
        dataEntries = hist.GetEntries()

        if showInfo: print 'INFO: Have ', dataEntries, ' entries in', hname

        f1 = TF1("f1","gaus",xmin, xmax)
        r = hist.Fit('gaus', 'S')
        hist.GetFunction("gaus").SetLineColor(kRed)
        cov = r.GetCovarianceMatrix() # to access the covariance matrix

        chi2 = r.Chi2()
        constant = r.Value(0)
        mean = r.Value(1)
        meanerr = r.ParError(1)
        sigma = r.Value(1)
        sigmaerr = r.ParError(1)
        ndf = r.Ndf()
        print "Chi2 of fit", chi2, "/ ndf", ndf
        print "-"*100

        cv = TCanvas( 'cv'+hname, 'cv'+hname, 10, 10, 900, 600) 
        gStyle.SetOptFit(01011)
        gStyle.SetOptStat(10)
        hist.Draw("hsame")

        lab.DrawLatex(x1, y1-0.1, hname.split("_")[-1])
        lab.DrawLatex(x1, y1-0.15, hDict[hname][7].split(",")[0])
        if len(hDict[hname][7].split(",")) > 1:
            lab.DrawLatex(x1, y1-0.2, hDict[hname][7].split(",")[1])
            if len(hDict[hname][7].split(",")) > 2:
                lab.DrawLatex(x1, y1-0.25, hDict[hname][7].split(",")[2])

        if bgInput.count("6.5TeV"):
            pname  = wwwpath + "TCT/6.5TeV/beamgas/"
        else:
            pname  = wwwpath + "TCT/4TeV/beamgas/"
        pname += hname.replace('.', '_') + ".pdf"

        cv.SaveAs(pname)





# ----------------------------------------------------------------------------





