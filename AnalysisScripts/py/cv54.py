#!/usr/bin/python
#
# June 2015, rkwee
## -------------------------------------------------------------------------------
import ROOT
from ROOT import TH1F, TCanvas
import helpers
from helpers import wwwpath, length_LHC, mylabel
# from cv47
# -----------------------------------------------------------------------------------
def cv54():


    # number of randomly produced values per s location
    myfile = '/afs/cern.ch/project/lhc_mib/beamgas/4TeV_beamsize/BGAS10.dat'

    hname, nbins, xmin, xmax = "spositions", 52800,2200.,55000.,20,0.5,20.5
    histspos2d = TH2F(hname, hname, nbins, xmin, xmax, ynbins, ymin, ymax)
    histspos   = TH1F(hname, hname, nbins, xmin, xmax)
    histspos.GetXaxis().SetTitle('s [cm]')
    histspos.GetYaxis().SetTitle('entries')

    with open(myfile) as mf:

        for line in mf:

            # format is: XIN(NIN), YIN(NIN), ZIN(NIN), UIN(NIN), VIN(NIN),tIn(NIN)
            [XIN, YIN, ZIN, UIN, VIN,tIn] = line.split()
            spos = float(ZIN)
            histspos.Fill(spos)


    for i in range(nbins):

        binContent = histspos.GetBinContent(i)
        
        #if binContent > 11.:
        print "i",i, "binContent =", binContent, histspos.GetBinLowEdge(i), histspos.GetBinLowEdge(i+1)


    a,b = 1,1
    cv = TCanvas( 'cv'+hname, 'cv'+hname, 10, 10, a*900, b*600) 
    cv.Divide(a,b)

    histspos.Draw('p')
    pname = './spos.root'

    cv.SaveAs(pname)



# ----------------------------------------------------------------------------





